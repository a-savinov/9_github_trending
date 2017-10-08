import datetime as dt
import json

import requests


def generate_repo_request_url(count_of_repo=20, days_ago_count=7):
    api_url = 'https://api.github.com'
    days_ago_date = (
        dt.datetime.now() - dt.timedelta(days=days_ago_count)).date()
    request_url = (
        '{}/search/repositories?q=created:>{}&sort=stars?page=1&per_page={}'.
        format(api_url, days_ago_date, count_of_repo))
    return request_url


def generate_issues_request_url(repo_owner, repo_name, issue_state='open'):
    api_url = 'https://api.github.com'
    # issue_state can be: open, closed, or all
    request_url = '{}/repos/{}/{}/issues?state={}'.format(
        api_url, repo_owner, repo_name, issue_state)
    return request_url


def get_trending_repositories():
    response = requests.get(generate_repo_request_url())
    return json.loads(response.content.decode('utf-8'))


def get_open_issues_amount(repo_owner, repo_name):
    response = requests.get(generate_issues_request_url(repo_owner, repo_name))
    raw_json = json.loads(response.content.decode('utf-8'))
    open_issues_amount = len(raw_json)
    return open_issues_amount


if __name__ == '__main__':
    github_projects_response = get_trending_repositories()
    print('Information about most trending repositories:')
    for github_project_json in github_projects_response['items']:
        project_stars = github_project_json['stargazers_count']
        project_owner = github_project_json['owner']['login']
        project_name = github_project_json['name']
        project_url = github_project_json['html_url']
        open_issues = get_open_issues_amount(project_owner, project_name)
        print('Project: stars: {:6} name: {:30} open issues: {:5} URL: {}'.
            format(project_stars, project_name, open_issues, project_url))
