# Testudo Course Scanner Database Schema

```mermaid
erDiagram
    snapshots {
        INTEGER id PK
        TEXT term_id
        TEXT department
        DATETIME snapshot_time
    }

    current_snapshot {
        TEXT term_id PK
        TEXT department PK
        INTEGER snapshot_id FK
    }

    course_info {
        TEXT term_id PK
        TEXT course_id PK
        TEXT title
        INTEGER credits
    }

    section_info {
        TEXT term_id PK,FK
        TEXT course_id PK,FK
        TEXT section_id PK
        TEXT delivery_type
    }

    section_meetings {
        TEXT term_id PK,FK
        TEXT course_id PK,FK
        TEXT section_id PK,FK
        TEXT meeting_type PK
        TEXT days PK
        TEXT start_time PK
    }

    instructor_info {
        TEXT term_id PK,FK
        TEXT course_id PK,FK
        TEXT section_id PK,FK
        TEXT instructor_name PK
    }

    seats_snapshot {
        TEXT term_id PK,FK
        TEXT course_id PK,FK
        TEXT section_id PK,FK
        DATETIME snapshot_time PK
        INTEGER total_seats
        INTEGER open_seats
    }

    snapshots ||--o{ current_snapshot : "tracks"
    snapshots ||--|| course_info : "temporal"
    snapshots ||--|| section_info : "temporal"
    course_info ||--o{ section_info : "has"
    section_info ||--o{ section_meetings : "meetings"
    section_info ||--o{ instructor_info : "instructors"
    section_info ||--o{ seats_snapshot : "seats"
```

## Key Relationships

- **snapshots → current_snapshot**: Tracks most recent snapshot per term/department (1:N)
- **snapshots → course_info, section_info**: Temporal tracking via first_seen/last_seen snapshot IDs
- **course_info → section_info**: One course has many sections (1:N)
- **section_info → section_meetings**: One section has multiple meeting times (1:N)
- **section_info → instructor_info**: One section has multiple instructors (1:N)
- **section_info → seats_snapshot**: One section tracked over time (1:N)

## Notes

- **Simplified View**: Only key fields shown. See `schema_diagram_complete.md` for all fields
- **Primary keys (PK)**: Uniquely identify each record
- **Foreign keys (FK)**: Link to parent tables
- **Temporal tracking**: All tables use `first_seen_snapshot_id` and `last_seen_snapshot_id` (not shown)
- **Generated fields**: `department` in course_info, `taken_seats` in seats_snapshot computed automatically
