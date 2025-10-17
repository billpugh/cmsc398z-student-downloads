-- ============================================================================
-- Testudo Course Scanner Database Schema
-- ============================================================================
-- SQLite database for tracking University of Maryland course and section
-- information over time, scraped from Testudo (app.testudo.umd.edu)
--
-- Key Concepts:
-- - TERM_ID: Semester identifier in format YYYYMM (e.g., 202508 = Fall 2025)
-- - COURSE_ID: Course identifier (e.g., CMSC132)
-- - SECTION_ID: Section identifier (e.g., 0101, 0201)
-- - DEPARTMENT: 4-letter department code extracted from course_id (e.g., CMSC, MATH)
--
-- Historical Tracking:
-- - first_seen: Timestamp when record first appeared in scraped data
-- - last_seen: Timestamp when record was last seen in scraped data
-- - Records are NOT deleted, allowing tracking of when courses/sections were dropped
--
-- ============================================================================

-- Snapshots table to track when scans were performed
CREATE TABLE IF NOT EXISTS snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    term_id TEXT NOT NULL,
    department TEXT NOT NULL,
    snapshot_time DATETIME NOT NULL,
    courses_found INTEGER,
    sections_found INTEGER,
    status TEXT,  -- 'success', 'partial', 'failed'
    error_message TEXT,
    UNIQUE(term_id, department, snapshot_time)
);

-- Current snapshot table to track the most recent snapshot for each term/department
CREATE TABLE IF NOT EXISTS current_snapshot (
    term_id TEXT NOT NULL,
    department TEXT NOT NULL,
    snapshot_id INTEGER NOT NULL,
    PRIMARY KEY (term_id, department),
    FOREIGN KEY (snapshot_id) REFERENCES snapshots(id)
);

-- Course information table
CREATE TABLE IF NOT EXISTS course_info (
    term_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    department TEXT GENERATED ALWAYS AS (SUBSTR(course_id, 1, 4)) STORED,
    title TEXT NOT NULL,
    credits INTEGER,
    grading_method TEXT,
    prerequisites TEXT,
    restrictions TEXT,
    cross_listed_with TEXT,
    credit_restrictions TEXT,
    description TEXT,
    description_approved INTEGER NOT NULL DEFAULT 1,  -- 1 if from approved-course-text, 0 if from course-text
    first_seen_snapshot_id INTEGER NOT NULL,
    last_seen_snapshot_id INTEGER NOT NULL,
    PRIMARY KEY (term_id, course_id),
    FOREIGN KEY (first_seen_snapshot_id) REFERENCES snapshots(id),
    FOREIGN KEY (last_seen_snapshot_id) REFERENCES snapshots(id)
);

-- ============================================================================
-- Section information table
-- ============================================================================
-- Stores basic section information including instructors and seat counts.
-- For sections with multiple meeting times (lecture + discussion), the schedule
-- fields contain the LECTURE time (or first meeting if no lecture).
--
-- IMPORTANT: Use section_meetings table for complete meeting information!
--
-- Field Formats:
-- - days: Meeting days using abbreviations without spaces
--   Examples: "MWF" (Mon/Wed/Fri), "TuTh" (Tue/Thu), "MW" (Mon/Wed)
--   Format: M=Monday, Tu=Tuesday, W=Wednesday, Th=Thursday, F=Friday
-- - start_time, end_time: 12-hour format with am/pm (e.g., "1:00pm", "11:30am")
-- - building_code: Building abbreviation (e.g., "CSI", "IRB", "ESJ")
-- - room_number: Room number as string (e.g., "1115", "0324")
-- - location: Computed field combining building_code and room_number
-- - delivery_type: "f2f" (face-to-face), "online", or "blended"
--
-- Relationship to section_meetings:
-- - section_info contains legacy schedule fields for backward compatibility
-- - section_meetings contains ALL meeting times (lectures, discussions, labs)
-- - For sections with multiple meetings, consult section_meetings for complete info
-- ============================================================================
CREATE TABLE IF NOT EXISTS section_info (
    term_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    section_id TEXT NOT NULL,
    days TEXT,                   -- Legacy: lecture days (use section_meetings for all meetings)
    start_time TEXT,             -- Legacy: lecture start time
    end_time TEXT,               -- Legacy: lecture end time
    building_code TEXT,          -- Legacy: lecture building
    room_number TEXT,            -- Legacy: lecture room
    location TEXT,               -- Legacy: computed lecture location
    delivery_type TEXT,          -- How course is delivered: f2f, online, blended
    first_seen_snapshot_id INTEGER NOT NULL,
    last_seen_snapshot_id INTEGER NOT NULL,
    PRIMARY KEY (term_id, course_id, section_id),
    FOREIGN KEY (term_id, course_id) REFERENCES course_info(term_id, course_id),
    FOREIGN KEY (first_seen_snapshot_id) REFERENCES snapshots(id),
    FOREIGN KEY (last_seen_snapshot_id) REFERENCES snapshots(id)
);

-- ============================================================================
-- Section meetings table
-- ============================================================================
-- Stores individual meeting times for each section. Many sections have multiple
-- meeting types (e.g., lecture + discussion, lecture + lab).
--
-- Example: CMSC132 Section 0101 has TWO meetings:
--   - Lecture:    MWF 1:00pm-1:50pm in CSI 1115
--   - Discussion: MW  2:00pm-2:50pm in CSI 2107
--
-- Field Formats:
-- - meeting_type: Type of meeting, extracted from HTML or defaulted to "Lecture"
--   Common values: "Lecture", "Discussion", "Lab"
--   Note: First meeting without explicit type is assumed to be "Lecture"
--   Sections may have multiple meetings of the same type (e.g., multiple labs)
-- - days: Meeting days using abbreviations WITHOUT spaces
--   Day abbreviations: M=Monday, Tu=Tuesday, W=Wednesday, Th=Thursday, F=Friday
--   Examples:
--     "MWF"  = Monday, Wednesday, Friday
--     "TuTh" = Tuesday, Thursday
--     "MW"   = Monday, Wednesday
--     "F"    = Friday only
-- - start_time, end_time: Time in 12-hour format with am/pm
--   Examples: "1:00pm", "2:50pm", "11:30am", "9:00am"
-- - building_code: Building abbreviation
--   Examples: "CSI" (Iribe Center), "IRB" (A.V. Williams), "ESJ" (Engineering)
-- - room_number: Room number as string (may have leading zeros)
--   Examples: "1115", "0324", "2107"
--
-- Usage Notes:
-- - Sections may have multiple meetings of the same type (e.g., multiple labs)
-- - Seat counts (in seats_snapshot) are per SECTION, not per meeting
-- - Enrollment is at the section level; students attend all meetings for a section
-- - Use last_seen to identify when a meeting time changed or was removed
-- ============================================================================
CREATE TABLE IF NOT EXISTS section_meetings (
    term_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    section_id TEXT NOT NULL,
    meeting_type TEXT NOT NULL,  -- 'Lecture', 'Discussion', 'Lab', etc.
    days TEXT,                    -- Meeting days: MWF, TuTh, MW, etc.
    start_time TEXT,              -- Start time: 1:00pm, 11:30am, etc.
    end_time TEXT,                -- End time: 1:50pm, 12:20pm, etc.
    building_code TEXT,           -- Building: CSI, IRB, ESJ, etc.
    room_number TEXT,             -- Room: 1115, 0324, etc.
    first_seen_snapshot_id INTEGER NOT NULL,
    last_seen_snapshot_id INTEGER NOT NULL,
    PRIMARY KEY (term_id, course_id, section_id, meeting_type, days, start_time),
    FOREIGN KEY (term_id, course_id, section_id) REFERENCES section_info(term_id, course_id, section_id),
    FOREIGN KEY (first_seen_snapshot_id) REFERENCES snapshots(id),
    FOREIGN KEY (last_seen_snapshot_id) REFERENCES snapshots(id)
);

-- Instructor information table
CREATE TABLE IF NOT EXISTS instructor_info (
    term_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    section_id TEXT NOT NULL,
    instructor_name TEXT NOT NULL,
    first_seen_snapshot_id INTEGER NOT NULL,
    last_seen_snapshot_id INTEGER NOT NULL,
    PRIMARY KEY (term_id, course_id, section_id, instructor_name),
    FOREIGN KEY (term_id, course_id, section_id) REFERENCES section_info(term_id, course_id, section_id),
    FOREIGN KEY (first_seen_snapshot_id) REFERENCES snapshots(id),
    FOREIGN KEY (last_seen_snapshot_id) REFERENCES snapshots(id)
);

-- Seats snapshot table
CREATE TABLE IF NOT EXISTS seats_snapshot (
    term_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    section_id TEXT NOT NULL,
    snapshot_time DATETIME NOT NULL,
    total_seats INTEGER,
    open_seats INTEGER,
    waitlist_count INTEGER,
    taken_seats INTEGER GENERATED ALWAYS AS (total_seats - open_seats) STORED,
    PRIMARY KEY (term_id, course_id, section_id, snapshot_time),
    FOREIGN KEY (term_id, course_id, section_id) REFERENCES section_info(term_id, course_id, section_id)
);


-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_snapshots_term_dept ON snapshots(term_id, department);
CREATE INDEX IF NOT EXISTS idx_snapshots_time ON snapshots(snapshot_time);
CREATE INDEX IF NOT EXISTS idx_current_snapshot_snapshot_id ON current_snapshot(snapshot_id);
CREATE INDEX IF NOT EXISTS idx_course_info_term ON course_info(term_id);
CREATE INDEX IF NOT EXISTS idx_course_info_department ON course_info(department);
CREATE INDEX IF NOT EXISTS idx_course_info_last_seen_snapshot ON course_info(last_seen_snapshot_id);
CREATE INDEX IF NOT EXISTS idx_course_info_description_approved ON course_info(description_approved);
CREATE INDEX IF NOT EXISTS idx_section_info_term ON section_info(term_id);
CREATE INDEX IF NOT EXISTS idx_section_info_course ON section_info(term_id, course_id);
CREATE INDEX IF NOT EXISTS idx_section_info_last_seen_snapshot ON section_info(last_seen_snapshot_id);
CREATE INDEX IF NOT EXISTS idx_section_meetings_section ON section_meetings(term_id, course_id, section_id);
CREATE INDEX IF NOT EXISTS idx_section_meetings_type ON section_meetings(meeting_type);
CREATE INDEX IF NOT EXISTS idx_section_meetings_last_seen_snapshot ON section_meetings(last_seen_snapshot_id);
CREATE INDEX IF NOT EXISTS idx_instructor_info_section ON instructor_info(term_id, course_id, section_id);
CREATE INDEX IF NOT EXISTS idx_instructor_info_name ON instructor_info(instructor_name);
CREATE INDEX IF NOT EXISTS idx_instructor_info_last_seen_snapshot ON instructor_info(last_seen_snapshot_id);
CREATE INDEX IF NOT EXISTS idx_seats_snapshot_section ON seats_snapshot(term_id, course_id, section_id);
CREATE INDEX IF NOT EXISTS idx_seats_snapshot_time ON seats_snapshot(snapshot_time);

-- Composite indexes for optimal query performance
CREATE INDEX IF NOT EXISTS idx_course_info_term_dept_last_seen ON course_info(term_id, department, last_seen_snapshot_id);
CREATE INDEX IF NOT EXISTS idx_course_info_term_last_seen ON course_info(term_id, last_seen_snapshot_id);
CREATE INDEX IF NOT EXISTS idx_section_info_term_last_seen ON section_info(term_id, last_seen_snapshot_id);
CREATE INDEX IF NOT EXISTS idx_seats_snapshot_section_time ON seats_snapshot(term_id, course_id, section_id, snapshot_time);

-- ============================================================================
-- Example queries for common operations
-- ============================================================================

-- Query 1: Get all meeting times for a specific section
-- Example: Show lecture and discussion times for CMSC132-0101
-- SELECT meeting_type, days, start_time, end_time, building_code, room_number
-- FROM section_meetings
-- WHERE term_id = '202508' AND course_id = 'CMSC132' AND section_id = '0101'
-- ORDER BY meeting_type;
--
-- Result:
--   Discussion | MW  | 2:00pm | 2:50pm | CSI | 2107
--   Lecture    | MWF | 1:00pm | 1:50pm | CSI | 1115

-- Query 2: Find all sections that meet on specific days
-- Example: Find all sections meeting on Monday, Wednesday, Friday
-- SELECT DISTINCT course_id, section_id, meeting_type, start_time, end_time
-- FROM section_meetings
-- WHERE term_id = '202508' AND days = 'MWF'
-- ORDER BY course_id, section_id;

-- Query 3: Find sections with both lecture and discussion
-- SELECT sm1.course_id, sm1.section_id,
--        sm1.days as lecture_days, sm1.start_time as lecture_start,
--        sm2.days as discussion_days, sm2.start_time as discussion_start
-- FROM section_meetings sm1
-- JOIN section_meetings sm2 ON sm1.term_id = sm2.term_id
--                           AND sm1.course_id = sm2.course_id
--                           AND sm1.section_id = sm2.section_id
-- WHERE sm1.term_id = '202508'
--   AND sm1.meeting_type = 'Lecture'
--   AND sm2.meeting_type = 'Discussion'
-- ORDER BY sm1.course_id, sm1.section_id;

-- Query 4: Get current courses and total taken seats for a specific department in a term
-- SELECT
--     ci.course_id,
--     ci.title,
--     COALESCE(SUM(ss.taken_seats), 0) as total_taken_seats
-- FROM course_info ci
-- JOIN current_snapshot cs ON ci.term_id = cs.term_id AND ci.department = cs.department
-- LEFT JOIN section_info si ON ci.term_id = si.term_id AND ci.course_id = si.course_id
-- LEFT JOIN seats_snapshot ss ON si.term_id = ss.term_id
--                            AND si.course_id = ss.course_id
--                            AND si.section_id = ss.section_id
--                            AND ss.snapshot_time = (SELECT snapshot_time FROM snapshots WHERE id = cs.snapshot_id)
-- WHERE ci.term_id = ?
--   AND ci.department = ?
--   AND ci.last_seen_snapshot_id = cs.snapshot_id
-- GROUP BY ci.course_id, ci.title
-- ORDER BY ci.course_id;

-- Query 5: Get current courses and total taken seats for all departments in a term
-- SELECT
--     ci.course_id,
--     ci.title,
--     COALESCE(SUM(ss.taken_seats), 0) as total_taken_seats
-- FROM course_info ci
-- JOIN current_snapshot cs ON ci.term_id = cs.term_id AND ci.department = cs.department
-- LEFT JOIN section_info si ON ci.term_id = si.term_id AND ci.course_id = si.course_id
-- LEFT JOIN seats_snapshot ss ON si.term_id = ss.term_id
--                            AND si.course_id = ss.course_id
--                            AND si.section_id = ss.section_id
--                            AND ss.snapshot_time = (SELECT snapshot_time FROM snapshots WHERE id = cs.snapshot_id)
-- WHERE ci.term_id = ?
--   AND ci.last_seen_snapshot_id = cs.snapshot_id
-- GROUP BY ci.course_id, ci.title
-- ORDER BY ci.course_id;

-- Query 6: Find dropped courses for a specific department
-- SELECT
--     ci.course_id,
--     ci.title,
--     s.snapshot_time as last_seen_time
-- FROM course_info ci
-- JOIN current_snapshot cs ON ci.term_id = cs.term_id AND ci.department = cs.department
-- JOIN snapshots s ON ci.last_seen_snapshot_id = s.id
-- WHERE ci.term_id = ?
--   AND ci.department = ?
--   AND ci.last_seen_snapshot_id < cs.snapshot_id;

-- Query 7: Find dropped sections for a specific department
-- SELECT
--     si.course_id,
--     si.section_id,
--     s.snapshot_time as last_seen_time
-- FROM section_info si
-- JOIN course_info ci ON si.term_id = ci.term_id AND si.course_id = ci.course_id
-- JOIN current_snapshot cs ON ci.term_id = cs.term_id AND ci.department = cs.department
-- JOIN snapshots s ON si.last_seen_snapshot_id = s.id
-- WHERE si.term_id = ?
--   AND ci.department = ?
--   AND si.last_seen_snapshot_id < cs.snapshot_id;

-- Query 8: Get current snapshot ID and time for a specific department in a term
-- SELECT cs.snapshot_id, s.snapshot_time
-- FROM current_snapshot cs
-- JOIN snapshots s ON cs.snapshot_id = s.id
-- WHERE cs.term_id = ? AND cs.department = ?;

-- Query 9: Get all departments and their current snapshot times for a term
-- SELECT
--     cs.department,
--     cs.snapshot_id,
--     s.snapshot_time as current_snapshot_time
-- FROM current_snapshot cs
-- JOIN snapshots s ON cs.snapshot_id = s.id
-- WHERE cs.term_id = ?
-- ORDER BY cs.department;

-- ============================================================================
-- Notes on Data Relationships
-- ============================================================================
--
-- Hierarchy:
--   course_info (1) -> (many) section_info (1) -> (many) section_meetings
--   section_info (1) -> (many) instructor_info
--   section_info (1) -> (many) seats_snapshot
--
-- Key Points:
-- - Seat counts are per SECTION, not per meeting
-- - Students enroll in a SECTION and attend ALL its meetings
-- - A section may have 0+ meetings (online courses may have no physical meetings)
-- - Most face-to-face sections have 1 meeting (lecture only)
-- - Upper-level courses often have 2+ meetings (lecture + discussion/lab)
-- - Meeting times can change; check first_seen/last_seen to track changes
-- ============================================================================
