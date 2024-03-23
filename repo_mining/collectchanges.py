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

    users = {}

    for pr in prs:
        user_login = pr['user']['login']
        if user_login not in users:
            user_data = github_auth('https://api.github.com/users/' + user_login, token)
            users[user_login] = user_data['name'] if user_data['name'] else user_login

        pr_detail = github_auth(pr['url'], token)
        if users[user_login] not in repo_data:
            repo_data[users[user_login]] = pr_detail['changed_files']
        else:
            repo_data[users[user_login]] += pr_detail['changed_files']

    return repo_data

# Function to create a graph from the repository data
def create_graph(repo_data):
    users = list(repo_data.keys())
    changed_files = [repo_data[user] for user in users]

    x = np.arange(len(users))  # the label locations
    width = 0.5  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x, changed_files, width, label='Changed Files')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Count')
    ax.set_title('Changed Files by User')
    ax.set_xticks(x)
    ax.set_xticklabels(users)
    ax.legend()

    fig.tight_layout()

    plt.show()
    plt.savefig('bargraph.png', bbox_inches='tight')

# Main part of the script
username = 'UNLV-CS472-672'
repo_name = '2024-S-GROUP2-2DRove'
token = 'temp'
repo_data = get_repo_data(username, repo_name, token)
create_graph(repo_data)