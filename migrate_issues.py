import requests

GITHUB_API_URL = "https://api.github.com"
AZURE_DEVOPS_API_URL = "https://dev.azure.com/{organization}/_apis/wit/workitems/$Issue?api-version=6.0"

GITHUB_TOKEN = "your_github_pat"
AZURE_DEVOPS_TOKEN = "your_azure_devops_pat"

HEADERS_GITHUB = {
    "Authorization": f"token {GITHUB_TOKEN}"
}
HEADERS_AZURE = {
    "Authorization": f"Basic {AZURE_DEVOPS_TOKEN}",
    "Content-Type": "application/json-patch+json"
}

def get_github_issues(repo):
    url = f"{GITHUB_API_URL}/repos/{repo}/issues"
    response = requests.get(url, headers=HEADERS_GITHUB)
    return response.json()

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

def migrate_issues(repo):
    issues = get_github_issues(repo)
    for issue in issues:
        title = issue['title']
        body = issue.get('body', '')
        create_azure_devops_issue(title, body)

if __name__ == "__main__":
    migrate_issues("username/repositoryname")
