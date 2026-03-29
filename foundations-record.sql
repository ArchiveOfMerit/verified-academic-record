-- Archive of Merit Project
-- Foundation branch SQL record

CREATE TABLE foundation_profile (
    id INTEGER PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    credentials VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    summary TEXT NOT NULL,
    focus_areas TEXT NOT NULL,
    project_name VARCHAR(255) NOT NULL,
    branch_name VARCHAR(255) NOT NULL
);

INSERT INTO foundation_profile (
    id,
    full_name,
    credentials,
    title,
    summary,
    focus_areas,
    project_name,
    branch_name
) VALUES (
    1,
    'Justin-Ames Gamache',
    'M.Ed., M.S.',
    'Scholar-Practitioner',
    'Justin-Ames Gamache, M.Ed., M.S., is a scholar-practitioner whose work sits at the intersection of educational technology, psychology, leadership, and higher education. With an interdisciplinary foundation in education and psychology, he explores mindfulness, student well-being, identity, equity, and the role of leadership and technology in shaping meaningful, human-centered learning environments. His work integrates research and practice to advance teaching, learning, and student success, with particular attention to data security, privacy-conscious technology use, reflective, inclusive, equity-minded leadership, and The Archive of Merit Project as a public-facing commitment to preserving verified merit and achievement.',
    'Educational Technology; Psychology; Leadership; Higher Education; Mindfulness; Student Well-Being; Identity; Equity; Data Security; Privacy-Conscious Technology; Human-Centered Learning',
    'The Archive of Merit Project',
    'foundation/archive-of-merit-project'
);

SELECT * FROM foundation_profile;
