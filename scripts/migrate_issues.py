import os
import requests

# Setze die API URLs
GITHUB_API_URL = "https://api.github.com"
AZURE_DEVOPS_API_URL = "https://dev.azure.com/QMIB/Test_Git/_apis/wit/workitems/$Issue?api-version=6.0"

# Lese die Tokens aus den Umgebungsvariablen aus
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
AZURE_DEVOPS_TOKEN = os.getenv('AZURE_DEVOPS_TOKEN')

# Setze die Headers für die API-Aufrufe
HEADERS_GITHUB = {
    "Authorization": f"token {GITHUB_TOKEN}"
}
HEADERS_AZURE = {
    "Authorization": f"Basic {AZURE_DEVOPS_TOKEN}",
    "Content-Type": "application/json-patch+json"
}

# Funktion zum Abrufen der Issues von GitHub
def get_github_issues(repo):
    url = f"{GITHUB_API_URL}/repos/{repo}/issues"
    response = requests.get(url, headers=HEADERS_GITHUB)
    
    # Debug-Ausgabe: Zeige den Inhalt der API-Antwort
    print("GitHub API Response:", response.text)
    
    # Überprüfe, ob die Antwort im JSON-Format ist
    try:
        issues = response.json()
    except ValueError:
        print("Error: Die API-Antwort ist kein gültiges JSON.")
        return []

    return issues

# Funktion zum Erstellen von Issues in Azure DevOps
def create_azure_devops_issue(title, body):
    data = [
        {
            "op": "add",
            "path": "/fields/System.Title",
            "value": title
        },
        {
            "op": "add",
            "path": "/fields/System.Description",
            "value": body
        }
    ]
    response = requests.post(AZURE_DEVOPS_API_URL, json=data, headers=HEADERS_AZURE)
    return response.json()

# Hauptfunktion zur Migration der Issues
def migrate_issues(repo):
    issues = get_github_issues(repo)
    for issue in issues:
        # Überprüfe, ob 'issue' ein dict ist, bevor du versuchst, auf seine Felder zuzugreifen
        if isinstance(issue, dict):
            title = issue['title']
            body = issue.get('body', '')
            create_azure_devops_issue(title, body)
        else:
            print("Warning: Ein Issue ist kein Dictionary und wird übersprungen:", issue)

if __name__ == "__main__":
    # Hier den Namen deines Repositories und dein Azure DevOps Projekt anpassen
    migrate_issues("vexufx/Test_Git")
