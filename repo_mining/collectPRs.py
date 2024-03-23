import requests
import matplotlib.pyplot as plt
import numpy as np

# GitHub Authentication function
def github_auth(url, token):
    headers = {'Authorization': 'Bearer {}'.format(token)}
    response = requests.get(url, headers=headers)
    return response.json()

# Function to get the data for a specific repository
def get_repo_data(username, repo_name, token):
    base_url = 'https://api.github.com/repos/'
    repo_data = {}

    prs = github_auth(base_url + username + '/' + repo_name + '/pulls?state=all', token)
    issues = github_auth(base_url + username + '/' + repo_name + '/issues?state=all', token)
    issue_comments = github_auth(base_url + username + '/' + repo_name + '/issues/comments', token)

    pr_comments = []
    for pr in prs:
        pr_comments.extend(github_auth(pr['comments_url'], token))

    users = {}

    for pr in prs:
        user_login = pr['user']['login']
        if user_login not in users:
            user_data = github_auth('https://api.github.com/users/' + user_login, token)
            users[user_login] = user_data['name'] if user_data['name'] else user_login

    for issue in issues:
        user_login = issue['user']['login']
        if user_login not in users:
            user_data = github_auth('https://api.github.com/users/' + user_login, token)
            users[user_login] = user_data['name'] if user_data['name'] else user_login

    for comment in issue_comments:
        user_login = comment['user']['login']
        if user_login not in users:
            user_data = github_auth('https://api.github.com/users/' + user_login, token)
            users[user_login] = user_data['name'] if user_data['name'] else user_login

    for comment in pr_comments:
        user_login = comment['user']['login']
        if user_login not in users:
            user_data = github_auth('https://api.github.com/users/' + user_login, token)
            users[user_login] = user_data['name'] if user_data['name'] else user_login

    repo_data = {users[user]: {
        'prs': len([pr for pr in prs if pr['user']['login'] == user]),
        'pr_comments': len([comment for comment in pr_comments if comment['user']['login'] == user]),
        'issues': len([issue for issue in issues if issue['user']['login'] == user]),
        'issue_comments': len([comment for comment in issue_comments if comment['user']['login'] == user])
    } for user in users}

    return repo_data

def create_graph(repo_data):
    users = list(repo_data.keys())
    prs = [repo_data[user]['prs'] for user in users]
    pr_comments = [repo_data[user]['pr_comments'] for user in users]
    issues = [repo_data[user]['issues'] for user in users]
    issue_comments = [repo_data[user]['issue_comments'] for user in users]

    x = np.arange(len(users))  # the label locations
    width = 0.2  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, prs, width, label='PRs')
    rects2 = ax.bar(x + width/2, pr_comments, width, label='PR Comments')
    rects3 = ax.bar(x + 3*width/2, issues, width, label='Issues')
    rects4 = ax.bar(x + 5*width/2, issue_comments, width, label='Issue Comments')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Count')
    ax.set_title('PRs, PR Comments, Issues, and Issue Comments by User')
    ax.set_xticks(x)
    ax.set_xticklabels(users)
    ax.legend()

    fig.tight_layout()

    plt.show()
    plt.savefig('scatterplotPRs.png', bbox_inches='tight')

# Main part of the script
username = 'UNLV-CS472-672'
repo_name = '2024-S-GROUP2-2DRove'
token = 'temp'
repo_data = get_repo_data(username, repo_name, token)
create_graph(repo_data)