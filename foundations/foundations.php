<?php
$jsonPath = __DIR__ . '/foundations-links.json';
$jsonContent = file_get_contents($jsonPath);

if ($jsonContent === false) {
    die('Unable to read foundations-links.json');
}

$foundationProfile = json_decode($jsonContent, true);

if ($foundationProfile === null) {
    die('Invalid JSON in foundations-links.json');
}

function escape($value) {
    return htmlspecialchars((string)$value, ENT_QUOTES, 'UTF-8');
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
            <h1><?php echo escape($foundationProfile["display_name"]); ?></h1>
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
                <?php foreach ($foundationProfile["profiles"] as $label => $url): ?>
                    <a class="button" href="<?php echo escape($url); ?>" target="_blank" rel="noopener noreferrer">
                        Open <?php echo escape(ucfirst($label)); ?>
                    </a>
                <?php endforeach; ?>
                <a class="button" href="<?php echo escape($foundationProfile["repository"]); ?>" target="_blank" rel="noopener noreferrer">
                    Open Repository
                </a>
            </div>
        </section>

        <section class="card">
            <h2>Foundation Records</h2>
            <ul>
                <?php foreach ($foundationProfile["documents"] as $key => $path): ?>
                    <li><strong><?php echo escape($key); ?></strong>: <?php echo escape($path); ?></li>
                <?php endforeach; ?>
            </ul>
        </section>
    </main>
</body>
</html>
