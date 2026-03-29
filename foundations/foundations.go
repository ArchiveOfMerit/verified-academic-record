package main

import (
	"encoding/json"
	"html/template"
	"log"
	"net/http"
	"os"
)

type FoundationData struct {
	ProjectName string            `json:"project_name"`
	BranchName  string            `json:"branch_name"`
	FolderName  string            `json:"folder_name"`
	FullName    string            `json:"full_name"`
	Credentials string            `json:"credentials"`
	DisplayName string            `json:"display_name"`
	Role        string            `json:"role"`
	Repository  string            `json:"repository"`
	Profiles    map[string]string `json:"profiles"`
	Documents   map[string]string `json:"documents"`
	FocusAreas  []string          `json:"focus_areas"`
	Summary     string            `json:"summary"`
}

var foundationData FoundationData

func loadFoundationData() error {
	file, err := os.Open("foundations-links.json")
	if err != nil {
		return err
	}
	defer file.Close()

	decoder := json.NewDecoder(file)
	return decoder.Decode(&foundationData)
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
			<h1>{{.DisplayName}}</h1>
			<p><strong>{{.Role}}</strong></p>
			<p>{{.Summary}}</p>
		</div>

		<div class="card">
			<h2>Foundation Branch</h2>
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
				{{range $label, $url := .Profiles}}
				<a class="button" href="{{$url}}" target="_blank" rel="noopener noreferrer">Open {{$label}}</a>
				{{end}}
				<a class="button" href="{{.Repository}}" target="_blank" rel="noopener noreferrer">Open Repository</a>
				<a class="button" href="/api/foundation" target="_blank" rel="noopener noreferrer">View JSON API</a>
			</div>
		</div>

		<div class="card">
			<h2>Foundation Records</h2>
			<ul>
				{{range $key, $path := .Documents}}
				<li><strong>{{$key}}</strong>: {{$path}}</li>
				{{end}}
			</ul>
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

	if err := tmpl.Execute(w, foundationData); err != nil {
		http.Error(w, "render error", http.StatusInternalServerError)
		return
	}
}

func foundationAPIHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	encoder := json.NewEncoder(w)
	encoder.SetIndent("", "  ")

	if err := encoder.Encode(foundationData); err != nil {
		http.Error(w, "json error", http.StatusInternalServerError)
		return
	}
}

func main() {
	if err := loadFoundationData(); err != nil {
		log.Fatal("failed to load foundations-links.json: ", err)
	}

	http.HandleFunc("/", foundationPageHandler)
	http.HandleFunc("/api/foundation", foundationAPIHandler)

	log.Println("Foundation server running at http://localhost:8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal(err)
	}
}
