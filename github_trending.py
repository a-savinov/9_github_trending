import datetime as dt

import requests


def get_trending_repositories(count_of_repo=20, days_ago_count=7):
    api_url = 'https://api.github.com'
    days_ago_date = (dt.datetime.now() - dt.timedelta(days=days_ago_count)) \
        .date()
    request_url = '{}/search/repositories?q=created:>{}&sort=stars?page=1' \
        '&per_page={}'.format(api_url, days_ago_date, count_of_repo)
    response = requests.get(request_url).json()['items']
    return response


def generate_normal_issues_list(issues):
    issues_list = [issue for issue in issues if not issue.get('pull_request')]
    return issues_list


def get_open_issues_amount(repo_owner, repo_name):
    api_url = 'https://api.github.com'
    request_url = '{}/repos/{}/{}/issues'.format(api_url, repo_owner, repo_name)
    response = requests.get(request_url).json()
    open_issues_amount = len(generate_normal_issues_list(response))
    return open_issues_amount


if __name__ == '__main__':
    github_projects_response = get_trending_repositories()
    print('Information about most trending repositories:')
    for github_project_json in github_projects_response:
        project_stars = github_project_json['stargazers_count']
        project_owner = github_project_json['owner']['login']
        project_name = github_project_json['name']
        project_url = github_project_json['html_url']
        open_issues = get_open_issues_amount(project_owner, project_name)
        print('Project: stars: {:6} name: {:30} open issues: {:5} URL: {}'.
              format(project_stars, project_name, open_issues, project_url))
