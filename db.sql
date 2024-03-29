-- jobs definition

CREATE TABLE jobs (
	id INTEGER,
	postTitle TEXT,
	location TEXT,
	salary TEXT,
	compatibilityRating TEXT,
	hasApplied INTEGER DEFAULT (0),
	link TEXT,
	generateLink TEXT,
	skills TEXT,
	jobDescription TEXT,
	benefits TEXT,
	Resume BLOB,
	createdAt TEXT,
	companyName TEXT,
	jk TEXT,
	homepage TEXT,
	"source" TEXT,
	emails TEXT,
	websiteUrl TEXT,
	HREmail TEXT,
	PhoneNumber TEXT,
	hasBeenSearched INTEGER,
	experience INTEGER,
	HRName TEXT,
	emailSent INTEGER,
	easyApply INTEGER,
	interviewing INTEGER,
	compatibility_score INTEGER,
	missingSkills TEXT,
	thirdParty INTEGER,
	recruiterName TEXT,
	locality TEXT,
	country TEXT,
	logo TEXT,
	datePosted TEXT,
	validThrough TEXT,
	employmentType TEXT,
	jobLocationType TEXT,
	applicantLocationRequirements TEXT, salaryMax REAL, salaryMin REAL,
	CONSTRAINT JOBS_PK PRIMARY KEY (id)
);