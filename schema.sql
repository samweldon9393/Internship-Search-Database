CREATE TABLE companies(
    company_name text primary key,
    industry text, headquarters text,
    size text, website text,
    careers_page text,
    contact_email text,
    contact_person text,
    notes text,
    is_target boolean,
    last_updated date
);
CREATE TABLE applications(
    application_id integer primary key autoincrement,
    company_name text references companies(company_name),
    position_title text not null,
    department_or_team text,
    location text,
    application_date date not null default current_date,
    salary numeric(6,2),
    status text,
    status_date date,
    job_posting_url text,
    where_applied text not null,
    resume_version text,
    referral_name text,
    interview_date date,
    follow_up_date date,
    offer_details text,
    notes text,
    last_updated date default current_date,
    start_date date,
    end_date date,
    job_board text
);
CREATE TABLE contacts(
    contact_name text primary key,
    company_name text references companies(company_name),
    linkedin text,
    email text,
    phone_number bigint,
    last_contacted date,
    where_met text
);
CREATE TABLE events (
    event_id INTEGER PRIMARY KEY,
    Event_name TEXT NOT NULL,
    event_date DATE,
    notes TEXT,
    contact_person TEXT,
    event_website TEXT
);
CREATE TABLE event_companies(
    event_id INTEGER NOT NULL,
    company_name TEXT NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events(event_id),
    FOREIGN KEY (company_name) REFERENCES companies(company_name),
    PRIMARY KEY (event_id, company_name)
);
