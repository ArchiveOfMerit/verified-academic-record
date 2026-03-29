<?php
$foundationProfile = [
    "name" => "Justin-Ames Gamache",
    "credentials" => "M.Ed., M.S.",
    "role" => "Scholar-Practitioner",
    "summary" => "Justin-Ames Gamache, M.Ed., M.S., is a scholar-practitioner whose work sits at the intersection of educational technology, psychology, leadership, and higher education. With an interdisciplinary foundation in education and psychology, he explores mindfulness, student well-being, identity, equity, and the role of leadership and technology in shaping meaningful, human-centered learning environments. His work integrates research and practice to advance teaching, learning, and student success, with particular attention to data security, privacy-conscious technology use, reflective, inclusive, equity-minded leadership, and The Archive of Merit Project as a public-facing commitment to preserving verified merit and achievement.",
    "project_name" => "The Archive of Merit Project",
    "branch_name" => "foundation/archive-of-merit-project",
    "repository" => "https://github.com/ArchiveOfMerit/verified-academic-record",
    "linkedin" => "https://www.linkedin.com/in/thescholarlypsychologistdoctoraleducationaltechnology/",
    "researchgate" => "https://www.researchgate.net/profile/Justin-Ames-Gamache-3",
    "focus_areas" => [
        "Educational Technology",
        "Psychology",
        "Leadership",
        "Higher Education",
        "Mindfulness",
        "Student Well-Being",
        "Identity",
        "Equity",
        "Data Security",
        "Privacy-Conscious Technology",
        "Human-Centered Learning"
    ]
];

function escape($value) {
    return htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Foundations PHP Record</title>
    <meta
        name="description"
        content="Foundation record page for Justin-Ames Gamache and The Archive of Merit Project."
    />
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #101418;
            color: #f4f7fb;
            line-height: 1.6;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px 20px;
        }

        .card {
            background: #18202a;
            border: 1px solid #2a3440;
            border-radius: 14px;
            padding: 24px;
            margin-bottom: 20px;
        }

        .eyebrow {
            margin: 0 0 10px;
            color: #9fc3ff;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.82rem;
            font-weight: 700;
        }

        h1, h2 {
            margin-top: 0;
        }

        .button-row {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 16px;
        }

        .button {
            display: inline-block;
            padding: 12px 18px;
            border-radius: 10px;
            background: #202b36;
            border: 1px solid #3d4b5b;
            color: #ffffff;
            text-decoration: none;
            font-weight: 700;
        }

        .button:hover {
            background: #2a3744;
        }

        ul {
            margin: 0;
            padding-left: 22px;
        }

        li {
            margin-bottom: 8px;
        }

        code {
            background: #0d1117;
            padding: 2px 6px;
            border-radius: 6px;
        }
    </style>
</head>
<body>
    <main class="container">
        <section class="card">
            <p class="eyebrow"><?php echo escape($foundationProfile["project_name"]); ?></p>
            <h1>
                <?php echo escape($foundationProfile["name"]); ?>,
                <?php echo escape($foundationProfile["credentials"]); ?>
            </h1>
            <p><strong><?php echo escape($foundationProfile["role"]); ?></strong></p>
            <p><?php echo escape($foundationProfile["summary"]); ?></p>
        </section>

        <section class="card">
            <h2>Foundation Branch</h2>
            <p><strong>Branch:</strong> <code><?php echo escape($foundationProfile["branch_name"]); ?></code></p>
            <p>
                <strong>Repository:</strong>
                <a href="<?php echo escape($foundationProfile["repository"]); ?>" target="_blank" rel="noopener noreferrer">
                    <?php echo escape($foundationProfile["repository"]); ?>
                </a>
            </p>
        </section>

        <section class="card">
            <h2>Focus Areas</h2>
            <ul>
                <?php foreach ($foundationProfile["focus_areas"] as $area): ?>
                    <li><?php echo escape($area); ?></li>
                <?php endforeach; ?>
            </ul>
        </section>

        <section class="card">
            <h2>Public Profiles</h2>
            <div class="button-row">
                <a class="button" href="<?php echo escape($foundationProfile["linkedin"]); ?>" target="_blank" rel="noopener noreferrer">
                    Open LinkedIn
                </a>
                <a class="button" href="<?php echo escape($foundationProfile["researchgate"]); ?>" target="_blank" rel="noopener noreferrer">
                    Open ResearchGate
                </a>
                <a class="button" href="<?php echo escape($foundationProfile["repository"]); ?>" target="_blank" rel="noopener noreferrer">
                    Open Repository
                </a>
            </div>
        </section>
    </main>
</body>
</html>
