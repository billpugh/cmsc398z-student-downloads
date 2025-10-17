# Testudo Course Scanner Database Schema (Complete)

This diagram includes all fields, including the temporal tracking fields (first_seen/last_seen) used for historical data tracking.

```mermaid
erDiagram
    snapshots {
        INTEGER id PK
        TEXT term_id
        TEXT department
        DATETIME snapshot_time
        INTEGER courses_found
        INTEGER sections_found
        TEXT status
        TEXT error_message
    }

    current_snapshot {
        TEXT term_id PK
        TEXT department PK
        INTEGER snapshot_id FK
    }

    course_info {
        TEXT term_id PK
        TEXT course_id PK
        TEXT department "GENERATED"
        TEXT title
        INTEGER credits
        TEXT grading_method
        TEXT prerequisites
        TEXT restrictions
        TEXT cross_listed_with
        TEXT credit_restrictions
        TEXT description
        INTEGER description_approved
        INTEGER first_seen_snapshot_id FK
        INTEGER last_seen_snapshot_id FK
    }

    section_info {
        TEXT term_id PK,FK
        TEXT course_id PK,FK
        TEXT section_id PK
        TEXT days
        TEXT start_time
        TEXT end_time
        TEXT building_code
        TEXT room_number
        TEXT location
        TEXT delivery_type
        INTEGER first_seen_snapshot_id FK
        INTEGER last_seen_snapshot_id FK
    }

    section_meetings {
        TEXT term_id PK,FK
        TEXT course_id PK,FK
        TEXT section_id PK,FK
        TEXT meeting_type PK
        TEXT days PK
        TEXT start_time PK
        TEXT end_time
        TEXT building_code
        TEXT room_number
        INTEGER first_seen_snapshot_id FK
        INTEGER last_seen_snapshot_id FK
    }

    instructor_info {
        TEXT term_id PK,FK
        TEXT course_id PK,FK
        TEXT section_id PK,FK
        TEXT instructor_name PK
        INTEGER first_seen_snapshot_id FK
        INTEGER last_seen_snapshot_id FK
    }

    seats_snapshot {
        TEXT term_id PK,FK
        TEXT course_id PK,FK
        TEXT section_id PK,FK
        DATETIME snapshot_time PK
        INTEGER total_seats
        INTEGER open_seats
        INTEGER waitlist_count
        INTEGER taken_seats "GENERATED"
    }

    snapshots ||--o{ current_snapshot : "current"
    snapshots ||--o{ course_info : "first_seen"
    snapshots ||--o{ course_info : "last_seen"
    snapshots ||--o{ section_info : "first_seen"
    snapshots ||--o{ section_info : "last_seen"
    snapshots ||--o{ section_meetings : "first_seen"
    snapshots ||--o{ section_meetings : "last_seen"
    snapshots ||--o{ instructor_info : "first_seen"
    snapshots ||--o{ instructor_info : "last_seen"
    course_info ||--o{ section_info : "has"
    section_info ||--o{ section_meetings : "has"
    section_info ||--o{ instructor_info : "taught_by"
    section_info ||--o{ seats_snapshot : "tracked_in"
```

## Key Relationships

- **snapshots → current_snapshot**: One snapshot can be current for many term/department combinations (1:N)
- **snapshots → course_info, section_info, etc.**: Snapshots track when records were first/last seen
- **course_info → section_info**: One course can have many sections (1:N)
- **section_info → section_meetings**: One section can have many meeting times (1:N)
- **section_info → instructor_info**: One section can have many instructors (1:N)
- **section_info → seats_snapshot**: One section can have many seat snapshots over time (1:N)

## Temporal Tracking

The `first_seen_snapshot_id` and `last_seen_snapshot_id` fields enable historical tracking:

- **first_seen_snapshot_id**: References the snapshot when a record first appeared in scraped data
- **last_seen_snapshot_id**: References the snapshot when a record was last seen in scraped data
- Records are never deleted, allowing tracking of when courses/sections were dropped or changed
- To find current/active records, query where `last_seen_snapshot_id` equals the current snapshot ID
- To find dropped records, query where `last_seen_snapshot_id` is less than the current snapshot ID
- Join with `snapshots` table to get the actual timestamps: `JOIN snapshots ON last_seen_snapshot_id = snapshots.id`

## Benefits of Snapshot IDs vs Timestamps

- **Referential integrity**: Foreign keys ensure first/last seen always reference actual snapshots
- **More compact storage**: INTEGER vs DATETIME
- **Simpler queries**: Direct comparison of IDs instead of timestamps
- **Better performance**: Indexed integer comparisons are faster than datetime comparisons

## Notes

- `snapshots` table tracks metadata about scraping operations
- `current_snapshot` table maintains the most recent snapshot for each term/department combination
- Primary keys (PK) are shown for each table
- Foreign keys (FK) show which fields link to parent tables
- GENERATED fields are automatically computed by the database (department, taken_seats)
- **section_meetings composite key**: The primary key includes `(meeting_type, days, start_time)` to allow sections to have multiple meetings of the same type (e.g., multiple labs at different times)
