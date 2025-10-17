CREATE TABLE snapshots (
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
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE current_snapshot (
    term_id TEXT NOT NULL,
    department TEXT NOT NULL,
    snapshot_id INTEGER NOT NULL,
    PRIMARY KEY (term_id, department),
    FOREIGN KEY (snapshot_id) REFERENCES snapshots(id)
);
CREATE TABLE course_info (
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
CREATE TABLE section_info (
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
CREATE TABLE instructor_info (
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
CREATE TABLE seats_snapshot (
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
CREATE INDEX idx_snapshots_term_dept ON snapshots(term_id, department);
CREATE INDEX idx_snapshots_time ON snapshots(snapshot_time);
CREATE INDEX idx_current_snapshot_snapshot_id ON current_snapshot(snapshot_id);
CREATE INDEX idx_course_info_term ON course_info(term_id);
CREATE INDEX idx_course_info_department ON course_info(department);
CREATE INDEX idx_course_info_last_seen_snapshot ON course_info(last_seen_snapshot_id);
CREATE INDEX idx_course_info_description_approved ON course_info(description_approved);
CREATE INDEX idx_section_info_term ON section_info(term_id);
CREATE INDEX idx_section_info_course ON section_info(term_id, course_id);
CREATE INDEX idx_section_info_last_seen_snapshot ON section_info(last_seen_snapshot_id);
CREATE INDEX idx_instructor_info_section ON instructor_info(term_id, course_id, section_id);
CREATE INDEX idx_instructor_info_name ON instructor_info(instructor_name);
CREATE INDEX idx_instructor_info_last_seen_snapshot ON instructor_info(last_seen_snapshot_id);
CREATE INDEX idx_seats_snapshot_section ON seats_snapshot(term_id, course_id, section_id);
CREATE INDEX idx_seats_snapshot_time ON seats_snapshot(snapshot_time);
CREATE INDEX idx_course_info_term_dept_last_seen ON course_info(term_id, department, last_seen_snapshot_id);
CREATE INDEX idx_course_info_term_last_seen ON course_info(term_id, last_seen_snapshot_id);
CREATE INDEX idx_section_info_term_last_seen ON section_info(term_id, last_seen_snapshot_id);
CREATE INDEX idx_seats_snapshot_section_time ON seats_snapshot(term_id, course_id, section_id, snapshot_time);
CREATE TABLE "section_meetings" (
            term_id TEXT NOT NULL,
            course_id TEXT NOT NULL,
            section_id TEXT NOT NULL,
            meeting_type TEXT NOT NULL,
            days TEXT,
            start_time TEXT,
            end_time TEXT,
            building_code TEXT,
            room_number TEXT,
            first_seen_snapshot_id INTEGER NOT NULL,
            last_seen_snapshot_id INTEGER NOT NULL,
            PRIMARY KEY (term_id, course_id, section_id, meeting_type, days, start_time),
            FOREIGN KEY (term_id, course_id, section_id) REFERENCES section_info(term_id, course_id, section_id),
            FOREIGN KEY (first_seen_snapshot_id) REFERENCES snapshots(id),
            FOREIGN KEY (last_seen_snapshot_id) REFERENCES snapshots(id)
        );
CREATE INDEX idx_section_meetings_section ON section_meetings(term_id, course_id, section_id);
CREATE INDEX idx_section_meetings_type ON section_meetings(meeting_type);
CREATE INDEX idx_section_meetings_last_seen_snapshot ON section_meetings(last_seen_snapshot_id);
