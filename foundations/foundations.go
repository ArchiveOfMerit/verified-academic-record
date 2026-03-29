package main

import (
	"encoding/json"
	"html/template"
	"log"
	"net/http"
)

type Profile struct {
	Name        string   `json:"name"`
	Credentials string   `json:"credentials"`
	Role        string   `json:"role"`
	Summary     string   `json:"summary"`
	FocusAreas  []string `json:"focus_areas"`
	ProjectName string   `json:"project_name"`
	BranchName  string   `json:"branch_name"`
	Repository  string   `json:"repository"`
	LinkedIn    string   `json:"linkedin"`
	ResearchGate string  `json:"researchgate"`
}

var foundationProfile = Profile{
	Name:        "Justin-Ames Gamache",
	Credentials: "M.Ed., M.S.",
	Role:        "Scholar-Practitioner",
	Summary:     "Justin-Ames Gamache, M.Ed., M.S., is a scholar-practitioner whose work sits at the intersection of educational technology, psychology, leadership, and higher education. With an interdisciplinary foundation in education and psychology, he explores mindfulness, student well-being, identity, equity, and the role of leadership and technology in shaping meaningful, human-centered learning environments. His work integrates research and practice to advance teaching, learning, and student success, with particular attention to data security, privacy-conscious technology use, reflective, inclusive, equity-minded leadership, and The Archive of Merit Project as a public-facing commitment to preserving verified merit and achievement.",
	FocusAreas: []string{
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
		"Human-Centered Learning",
	},
	ProjectName:  "The Archive of Merit Project",
	BranchName:   "foundation/archive-of-merit-project",
	Repository:   "https://github.com/ArchiveOfMerit/verified-academic-record",
	LinkedIn:     "https://www.linkedin.com/in/thescholarlypsychologistdoctoraleducationaltechnology/",
	ResearchGate: "https://www.researchgate.net/profile/Justin-Ames-Gamache-3",
}

const pageTemplate = `
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Foundation Record</title>
	<style>
		body {
			margin: 0;
			font-family: Arial, sans-serif;
			background: #0f141a;
			color: #f5f7fa;
			line-height: 1.6;
		}
		.container {
			max-width: 1000px;
			margin: 0 auto;
			padding: 40px 20px;
		}
		.card {
			background: #17202a;
			border: 1px solid #2c3947;
			border-radius: 14px;
			padding: 24px;
			margin-bottom: 20px;
		}
		h1, h2 {
			margin-top: 0;
		}
		.eyebrow {
			font-size: 0.82rem;
			text-transform: uppercase;
			letter-spacing: 0.08em;
			color: #9cc4ff;
			font-weight: bold;
			margin-bottom: 10px;
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
			background: #22303d;
			border: 1px solid #3b4a5a;
			color: #ffffff;
			text-decoration: none;
			font-weight: bold;
		}
		.button:hover {
			background: #2b3a49;
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
	<div class="container">
		<div class="card">
			<div class="eyebrow">{{.ProjectName}}</div>
			<h1>{{.Name}}, {{.Credentials}}</h1>
			<p><strong>{{.Role}}</strong></p>
			<p>{{.Summary}}</p>
		</div>

		<div class="card">
			<h2>Foundation Branch</h2>
			<p>This record is tied to the repository and branch structure below.</p>
			<p><strong>Repository:</strong> <a href="{{.Repository}}" target="_blank" rel="noopener noreferrer">{{.Repository}}</a></p>
			<p><strong>Branch:</strong> <code>{{.BranchName}}</code></p>
		</div>

		<div class="card">
			<h2>Focus Areas</h2>
			<ul>
				{{range .FocusAreas}}
				<li>{{.}}</li>
				{{end}}
			</ul>
		</div>

		<div class="card">
			<h2>Public Profiles</h2>
			<div class="button-row">
				<a class="button" href="{{.LinkedIn}}" target="_blank" rel="noopener noreferrer">Open LinkedIn</a>
				<a class="button" href="{{.ResearchGate}}" target="_blank" rel="noopener noreferrer">Open ResearchGate</a>
				<a class="button" href="{{.Repository}}" target="_blank" rel="noopener noreferrer">Open Repository</a>
				<a class="button" href="/api/foundation" target="_blank" rel="noopener noreferrer">View JSON API</a>
			</div>
		</div>
	</div>
</body>
</html>
`

func foundationPageHandler(w http.ResponseWriter, r *http.Request) {
	tmpl, err := template.New("foundation").Parse(pageTemplate)
	if err != nil {
		http.Error(w, "template error", http.StatusInternalServerError)
		return
	}

	if err := tmpl.Execute(w, foundationProfile); err != nil {
		http.Error(w, "render error", http.StatusInternalServerError)
		return
	}
}

func foundationAPIHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	encoder := json.NewEncoder(w)
	encoder.SetIndent("", "  ")

	if err := encoder.Encode(foundationProfile); err != nil {
		http.Error(w, "json error", http.StatusInternalServerError)
		return
	}
}

func main() {
	http.HandleFunc("/", foundationPageHandler)
	http.HandleFunc("/api/foundation", foundationAPIHandler)

	log.Println("Foundation server running at http://localhost:8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal(err)
	}
}
