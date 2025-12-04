# Week 1 Goal: Understanding Dual-State Consistency in Quuly

## Learning Objectives

By the end of this session, students will be able to:

1. Run Quuly locally using GitHub Codespaces
2. Explain what a Conversation represents and its lifecycle states
3. Trace a dequeue action through both database and Redis changes
4. Identify the specific code responsible for each state change
5. Explain how Redis state would be rebuilt from the database
6. Apply code review thinking to distributed state consistency problems

**Core Focus**: Understand how Quuly maintains consistency between PostgreSQL (source of truth) and Redis (real-time queue state) during conversation state transitions, using the "dequeue" action as a case study.

---

## Session Overview

### Setup (Required First)
1. Get Quuly running on GitHub Codespaces
2. Load the `cmsc398z-test` dataset
3. Verify dev-login works (login as instructor, TA, and student)

### Understanding Conversations
Students will learn what a "Conversation" represents in Quuly - the complete lifecycle of a help request from when a student joins the queue through resolution. They'll observe this from both TA/instructor and student perspectives simultaneously, including:
- Student joins queue
- TA dequeues student to help them
- TA marks as resolved, OR returns to student (who may rejoin queue)
- The various state transitions possible

**Tip: Use two browsers (or a private/incognito window) to be logged in as both a student and a TA at the same time.** This lets you see real-time updates from both perspectives - for example, the notification a student receives when a TA dequeues them. You could use Safari for one role and Chrome for another, or use a private window in the same browser.

### Architecture Overview
High-level understanding of Quuly's three-tier backend:
- **Go backend** (zion): GraphQL API, business logic
- **PostgreSQL database**: Source of truth, persistent state
- **Redis**: Real-time queue state, pub/sub notifications

**Key architectural insight**: When you have dual state (database + Redis), keeping them in sync is critical. One important scenario requiring careful review is rebuilding Redis state from the database after a restart.

### Conceptual Topics (Self-Study)
The lesson plan includes four conceptual topics (GraphQL, Go, Redis, Docker) that students can explore at their leisure. The in-class focus is understanding how a conversation evolves through state transitions and how that's tracked in both the database and Redis.

---

## Core Learning Activity: Tracing the Dequeue Operation

Students will trace what happens when a TA dequeues a student from the queue. This is a focused case study in dual-state consistency.

### Questions to Answer (with code exploration)

**Database Side:**
1. How does the database represent a student waiting to be helped?
   - What table? What column values indicate "in queue"?
2. How is the database changed when the student is dequeued?
   - What state change occurs? What record is created?
3. What is the SQL statement that makes this change?

**Redis Side:**
4. How does Redis represent a student waiting to be helped?
   - What data structure? What key pattern?
5. How does Redis change when a student is dequeued?
   - What command removes them from the queue?
6. What notifications are generated?

**Coordination:**
7. What is the backend method that performs both the database and Redis updates?
8. How is this change coordinated? Is it truly atomic?
   - What happens if the system crashes between the Redis update and database commit?
9. If the system crashed and Redis state had to be rebuilt, what code does that?
   - Does `LoadQueues()` correctly reconstruct the queue from the database?

### Code Locations to Examine

| Component | File | Key Functions/Sections |
|-----------|------|----------------------|
| Database schema | `zion-db/initdb/30_create_conversational_tables.sql` | `conversations` table, `interactions` table, state enum |
| Dequeue entry point | `zion/data/queue/dequeue.go` | `Dequeue()` function |
| Queue service | `zion/data/queue/queue_service.go` | `DequeueConversation()`, `LoadQueues()` |
| Redis queue operations | `zion/redis/queues.go` | `Dequeue()`, `BulkInsert()` |

---

## Code Review Mindset

**Treat this like a real code review.** The code may have bugs or edge cases. Be skeptical.

- Look for any inconsistencies between database and Redis state
- Identify places where the consistency logic is particularly tricky
- Consider: what happens in various failure scenarios?
- **Prizes may be awarded** for identifying actual bugs or problematic code that should be changed

---

## Deliverable: LEARNINGS-WEEK1.md

After tracing through the code and understanding how dequeue works, write an explanation addressing:

1. **How consistency is maintained**: Explain the sequence of operations when a TA dequeues a student. What updates the database? What updates Redis? In what order?

2. **Rebuild scenario**: If Redis crashed and `LoadQueues()` ran to rebuild the queue state from the database, explain why the reconstructed state would (or would not) match what was there before the crash. Be specific about:
   - What database query `LoadQueues()` uses
   - What database state a dequeued conversation has
   - Why a conversation that was dequeued before the crash would (or would not) incorrectly appear in the rebuilt queue

3. **Edge cases or concerns**: Document any edge cases, potential bugs, or areas where the code is particularly fragile. This is your code review.

**Format**: Write this as if you were doing a code review for a colleague who added this feature and asked you to verify the consistency guarantees are correct.

---

## By End of Session, Students Can:

1. Run Quuly locally using GitHub Codespaces
2. Explain what a Conversation represents and its lifecycle states
3. Trace a dequeue action through both database and Redis changes
4. Identify the specific code responsible for each state change
5. Explain how Redis state would be rebuilt from the database
6. Apply code review thinking to distributed state consistency problems

---

## Connection to Week 2

Next week, students will make changes to conversation state transition code. Understanding the consistency requirements from Week 1 prepares them to:
- Modify transition logic without breaking consistency
- Know what to verify when changing dual-state code
- Apply the same code review rigor to their own changes
