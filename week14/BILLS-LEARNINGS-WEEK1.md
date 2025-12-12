# Week 1 Learnings: Dequeue Operation Analysis

## How Consistency is Maintained

When a TA dequeues a student, the following sequence of operations occurs:

1. **Lock acquisition** (`zion/data/queue/dequeue.go`): A Redis lock is acquired for the course/room to serialize dequeue operations
2. **Active conversation check**: Verify the TA doesn't already have an active conversation
3. **Redis update** (`zion/redis/queues.go`): `ZPopMin` removes the conversation ID from the Redis sorted set queue
4. **Database transaction** (`zion/data/queue/queue_service.go`):
   - Begin transaction
   - Update conversation state from `'in_queue'` to `'being_helped'`
   - Insert a new interaction record with `typ = 'dequeue'`
   - Commit transaction
5. **Lock release**: The Redis lock is released via `defer`

The key design decision is that **PostgreSQL is the source of truth**. Redis provides fast queue access and real-time notifications, but if Redis state is lost, it can be rebuilt from the database.

## Rebuild Scenario: LoadQueues Analysis

If Redis crashes and `LoadQueues()` runs to rebuild the queue state:

**The query used:**
```sql
SELECT c.course_id, c.room_id, array_agg(c.id ORDER BY i.created) as conversations
FROM conversations c
JOIN (SELECT conversation_id, typ, created,
      ROW_NUMBER() OVER (PARTITION BY conversation_id ORDER BY created DESC) as rn
      FROM interactions) as i
ON i.conversation_id = c.id
WHERE state = 'in_queue'
  AND i.rn = 1
  AND i.typ IN ('enqueue', 'requeue')
GROUP BY c.course_id, c.room_id;
```

**Why a dequeued conversation won't incorrectly appear:**
- After a successful dequeue, the conversation's state is `'being_helped'`, not `'in_queue'`
- The `WHERE state = 'in_queue'` clause excludes it
- Additionally, the most recent interaction would be `'dequeue'`, which isn't in the `('enqueue', 'requeue')` list

**Why the interaction join is needed:**
- The join provides the `ORDER BY i.created` for the `array_agg`, ensuring the queue is rebuilt in correct FIFO order
- The `conversations.created` timestamp is when the conversation was first created, not when it was most recently enqueued (a student can rejoin the queue multiple times)
- The interaction check also serves as defensive programming—if a bug sets `state = 'in_queue'` without creating the proper interaction, this query would catch the inconsistency

## Edge Cases and Concerns

### 1. Unnecessary ZCard Check and Possibly Unnecessary Lock

In `zion/redis/queues.go`, the `Dequeue` function checks the queue length before popping:

```go
res := p.client.ZCard(getQueueKey(courseID, roomID))
count, err := res.Result()
if count == 0 {
    return nil, nil
}
convo := p.client.ZPopMin(getQueueKey(courseID, roomID), 1)
```

**The `ZCard` check is unnecessary:** `ZPopMin` is atomic and returns nothing if the queue is empty. The result is the same whether you check first or just call `ZPopMin` directly. The code would be simpler and equally correct without the `ZCard` call.

**The Redis lock may also be unnecessary:** The dequeue functions in `zion/data/queue/dequeue.go` acquire a per-room lock (`DequeueLock(course, room)`) before doing anything. But what does this lock actually protect?

- The `ZPopMin` operation is atomic—two concurrent calls will each get a different conversation (or one gets nothing).
- The `StaffHasActiveConversation` check is per-TA, but the lock is per-room. A per-room lock doesn't prevent the same TA from making concurrent requests anyway.

If the only Redis queue operation performed while holding the lock is the atomic `ZPopMin`, and the lock scope (per-room) doesn't match what it might be trying to protect (per-TA check), then the lock may be legacy code that could be removed.

**Recommendation:** Investigate whether the lock serves any purpose. If not, removing both the `ZCard` check and the lock would simplify the code.

### 2. Redis-Database Consistency Window

Redis is updated **before** the database transaction commits. If the server crashes after `ZPopMin` but before `tx.Commit()`:
- The conversation is removed from the Redis queue
- The database still has `state = 'in_queue'`

**Mitigation:** On restart, `LoadQueues()` rebuilds Redis from the database, so the conversation would be restored to the queue. The student might experience a brief inconsistency, but the system self-corrects.

**Potential improvement:** Start the database transaction before performing the Redis update. This would catch database connection failures early, before modifying Redis state.

### 3. Student Leaves While TA Dequeues (Race Condition) — POTENTIAL DATABASE CORRUPTION

When a student clicks "Leave Queue", the code path is:
1. `FindByID` — fetch conversation state from database
2. `GetNextState` — validate transition is legal (pure function, no side effects)
3. `Remove` — call `ZRem` to remove from Redis queue
4. Database transaction — update state to `'ongoing'`, insert `'leave'` interaction

**There are two race windows:**

**Window 1: TA dequeues before student's `FindByID`**
- Student reads state = `'being_helped'` (TA already changed it)
- `GetNextState('being_helped', LEAVE)` returns `ok = false`
- Student gets `INVALID_TRANSITION_ERROR`
- **Database is consistent**, but error message is confusing

**Window 2: TA dequeues after student's `FindByID` but before student's `tx.Commit()`**
- Student reads state = `'in_queue'`
- `GetNextState('in_queue', LEAVE)` returns `'ongoing'`, `ok = true`
- TA dequeues (Redis `ZPopMin` + DB update to `'being_helped'`)
- Student's `Remove` calls `ZRem`, which returns 0 items removed but **no error**
- Student's DB transaction overwrites state to `'ongoing'`
- **DATABASE IS CORRUPTED** — TA thinks they're helping, but state says `'ongoing'`

**Root cause:** The `Remove` function in `zion/redis/queues.go` doesn't check if `ZRem` actually removed anything:

```go
func (p *PushClient) Remove(courseID, roomID, conversationID string) error {
    res := p.client.ZRem(getQueueKey(courseID, roomID), conversationID)
    return res.Err()  // Only checks for errors, not whether anything was removed
}
```

**Fix:** `Remove` should check `res.Val()` and return an error (or `false`) if nothing was removed. The caller should then abort before the database transaction. This would close Window 2.

**UX improvement for Window 1:** Detect when a student tries to leave but the conversation is already `'being_helped'` and show a friendly message:
> "Good news! A TA has already started helping you. Please proceed to meet with them, or if you no longer need help, use 'Resolve' to let them know."

### 4. Ownership Model Recommendation

A useful mental model for reasoning about correctness: **successfully performing a Redis operation grants "ownership" of that conversation for the subsequent database update.**

For example:
- `ZPopMin` grants ownership to update the conversation to `'being_helped'`
- `ZRem` (for leave) grants ownership to update the conversation to `'ongoing'`

Documenting which Redis action grants permission for each database update would make the consistency guarantees more explicit and easier to verify during code review.

### 5. Invariant Checking Recommendation

To increase confidence in the system's consistency, consider implementing runtime invariant checks:

1. All conversations with `state = 'in_queue'` should be in the corresponding Redis queue
2. All Redis queue entries should have a matching conversation with `state = 'in_queue'`
3. For each `'in_queue'` conversation, the most recent interaction should be `'enqueue'` or `'requeue'`

These checks could be:
- Run as part of end-to-end tests in CI
- Run periodically in production (e.g., every few minutes)
- Logged/alerted if violations are detected

This wouldn't prevent errors, but would help catch drift before it causes user-visible problems.


### More bugs found:

When a student requeues a conversation, they don't have an option to switch rooms

When a student requests help, their view of space and rooms doesn't update. 