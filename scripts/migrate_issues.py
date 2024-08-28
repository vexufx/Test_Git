import requests

GITHUB_API_URL = "https://api.github.com"
AZURE_DEVOPS_API_URL = "https://dev.azure.com/QMIB/_apis/wit/workitems/$Issue?api-version=6.0"

GITHUB_TOKEN = "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"
AZURE_DEVOPS_TOKEN = "pndibg4ad4gkxkhxa2mv6dtr4qzhkf3mnc75uinmtqh3kost22oa"

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
    migrate_issues("vexufx/Test_Git")
