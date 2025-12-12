# Rethinking Virtual Rooms: Hybrid Room Design

## Problem Statement

The current virtual room implementation is broken:
- Virtual rooms are never used (0 conversations in the database)
- All virtual rooms are auto-assigned to every new course (causing bloat)
- Physical rooms are often misclassified as virtual and vice versa
- No way to have a single queue serving both in-person and virtual students

### Use Case for Hybrid Rooms

Consider a large class with one queue that serves both in-person and virtual office hours. Some students will be there in person, some virtually. A hybrid room allows efficient matching:
- TAs can indicate whether they're available in-person, virtually, or both
- Students can indicate their preference when joining the queue
- The system enables flexible matching while maintaining a single unified queue

---

## Design Overview

### New Room Type

Add `hybrid` as a third room type alongside `physical` and `virtual`.

```sql
ALTER TYPE room_type ADD VALUE 'hybrid';
```

### New Meeting Mode Enum

```sql
CREATE TYPE meeting_mode AS ENUM ('in_person', 'virtual', 'either');
```

- `in_person` - Physical meeting only
- `virtual` - Virtual meeting only (e.g., Zoom)
- `either` - Flexible, can do either

---

## Key Design Decisions

1. **Mode is per-interaction, not per-conversation** - A student might have multiple meetings within one conversation, some in-person, some virtual.

2. **TAs can change mode while on duty** - No need to go off-duty and back on.

3. **TAs manually select students to dequeue** - Not strict FIFO. They can filter the queue by:
   - Meeting mode compatibility (for hybrid rooms)
   - Tags (e.g., "project 3", "midterm review")

4. **Mode only applies to enqueue/dequeue/requeue interactions** - Not to resolve, leave, no_show, etc.

5. **`meeting_mode` always set in database** - Even for non-hybrid rooms, for consistency and analytics.

6. **Mode selection required for hybrid rooms** - Students must explicitly choose when enqueueing.

7. **Use existing `comment_data` for TA messages** - e.g., Zoom links sent on dequeue.

---

## Schema Changes

### 1. Add 'hybrid' to room_type

```sql
ALTER TYPE room_type ADD VALUE 'hybrid';
```

### 2. Create meeting_mode enum

```sql
CREATE TYPE meeting_mode AS ENUM ('in_person', 'virtual', 'either');
```

### 3. Add mode to active_duty

```sql
ALTER TABLE active_duty ADD COLUMN mode meeting_mode NOT NULL DEFAULT 'either';
```

When a TA goes on duty:
- Physical room → `in_person` (enforced)
- Virtual room → `virtual` (enforced)
- Hybrid room → TA chooses (`in_person`, `virtual`, or `either`)

### 4. Add meeting_mode to interactions

```sql
ALTER TABLE interactions ADD COLUMN meeting_mode meeting_mode;
```

Populated for `enqueue`, `dequeue`, and `requeue` interactions only. NULL for other interaction types (`resolve`, `leave`, `no_show`, `open`, `reopen`).

---

## Logic by Room Type

| Room Type | Enqueue `meeting_mode` | Dequeue `meeting_mode` |
|-----------|------------------------|------------------------|
| Physical | `in_person` (auto-set) | `in_person` (auto-set) |
| Virtual | `virtual` (auto-set) | `virtual` (auto-set) |
| Hybrid | Student chooses: `in_person`, `virtual`, or `either` | TA chooses: `in_person` or `virtual` |

**Note:** Dequeue never uses `either` - the TA must resolve to an actual meeting mode.

---

## Flow Details

### TA Goes On Duty (Hybrid Room)

```
SetOnDuty(course, room, mode: 'in_person' | 'virtual' | 'either')
```

- For hybrid rooms, TA specifies their availability
- TA can update mode while on duty without going off-duty first

### Student Enqueues (Hybrid Room)

```
Enqueue(course, room, topic, description, tags, mode: 'in_person' | 'virtual' | 'either')
```

- Student must select a mode for hybrid rooms
- Creates interaction with `typ = 'enqueue'` and `meeting_mode = <student's preference>`

### TA Views Queue

TA can filter the queue by:
- **Mode compatibility** - Based on TA's current mode and student preferences
- **Tags** - e.g., show only "project 3" students

Filtering is a UI/query feature, not hard enforcement.

### TA Dequeues Student

```
Dequeue(course, room, conversation_id, meeting_mode: 'in_person' | 'virtual', comment?)
```

- TA explicitly picks the student (existing behavior, not FIFO)
- TA specifies actual meeting mode for this interaction
- Optional `comment` (e.g., Zoom link) stored in existing `comment_data` field
- Creates interaction with `typ = 'dequeue'`, `meeting_mode = <actual>`, `comment_data = <message>`

### Mode Compatibility (for filtering)

| TA Mode | Can Help Students With |
|---------|------------------------|
| `in_person` | `in_person`, `either` |
| `virtual` | `virtual`, `either` |
| `either` | `in_person`, `virtual`, `either` |

This is used for filtering the queue view, not hard enforcement.

---

## Migration for Existing Data

Backfill `meeting_mode` for existing interactions:

```sql
UPDATE interactions i
SET meeting_mode = CASE
    WHEN r.typ = 'physical' THEN 'in_person'::meeting_mode
    WHEN r.typ = 'virtual' THEN 'virtual'::meeting_mode
    ELSE NULL
END
FROM conversations c
JOIN rooms r ON c.room_id = r.id
WHERE i.conversation_id = c.id
  AND i.typ IN ('enqueue', 'dequeue', 'requeue');
```

---

## API Changes Summary

| Mutation | Change |
|----------|--------|
| `SetOnDuty` | Add optional `mode` param (required for hybrid, auto-set for physical/virtual) |
| `UpdateDutyMode` | New mutation to change mode while on duty |
| `Enqueue` | Add optional `mode` param (required for hybrid, auto-set for physical/virtual) |
| `Dequeue` | Add optional `mode` param (required for hybrid, auto-set for physical/virtual) |
| `Requeue` | Add optional `mode` param (same logic as Enqueue) |

---

## Files Requiring Changes

### Database
- `initdb/00_define_types.sql` - Add `hybrid` to room_type, create `meeting_mode` enum
- `initdb/20_create_user_tables.sql` - Add `mode` column to `active_duty`
- `initdb/30_create_conversational_tables.sql` - Add `meeting_mode` column to `interactions`
- New migration script for existing data

### Go Code
- `data/room/room.go` - Add `HYBRID` constant
- `data/interaction/interaction.go` - Add `MeetingMode` field
- `data/queue/enqueue.go` - Accept and store meeting mode
- `data/queue/dequeue.go` - Accept and store meeting mode
- `data/user/user_service.go` - Update `SetOnDuty` to accept mode
- `resolvers/ta_mutation.go` - Update mutations for mode parameter
- `resolvers/student_mutation.go` - Update enqueue mutation
- GraphQL schema files - Add mode parameters to mutations

### Analytics (Deferred)
- `initdb/30_create_conversational_tables.sql` - Review `avg_wait_time` materialized view
- May need additional views segmented by meeting mode

---

## Future Considerations

1. **Remove auto-assignment of virtual rooms** - The current logic that assigns all virtual rooms to new courses is broken and should be removed or rethought.

2. **Room type validation** - Consider warning or preventing creation of "physical" rooms with virtual-sounding names (Zoom, Virtual, Online).

3. **Analytics by mode** - Once hybrid rooms are in use, add analytics to track wait times and usage patterns by meeting mode.

4. **Default meeting URLs** - Hybrid rooms could have a default Zoom/virtual meeting URL that auto-populates `comment_data` on virtual dequeues.
