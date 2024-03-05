-- jobs definition

CREATE TABLE "jobs" (
    id INTEGER PRIMARY KEY,
    postTitle TEXT,
    location TEXT,
    salary TEXT,
    compatibilityRating TEXT,
    hasApplied INTEGER DEFAULT (0),
    link TEXT,
    generateLink TEXT,
    -- Include all other columns here in any order
    skills TEXT,
    jobDescription TEXT,
    benefits TEXT,
    Resume BLOB,
    "createdAt" TEXT,
    companyName TEXT,
    jk TEXT,
    homepage TEXT,
    priority INT DEFAULT 0,
    source TEXT,
    resume_html TEXT,
    resume_pdf TEXT
, emails TEXT, websiteUrl TEXT, HREmail TEXT, PhoneNumber TEXT, hasBeenSearched INTEGER, experience INTEGER, HRName TEXT, emailSent INTEGER, easyApply INTEGER, interviewing INTEGER, compatibility_score INTEGER, missingSkills TEXT, thirdParty INTEGER, processed INTEGER, recruiterName TEXT, recruiterOrigin INTEGER);