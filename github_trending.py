import datetime as dt
import json

import requests

API_URL = 'https://api.github.com'


def get_n_trending_repositories_json(top_size, days_ago):
    days_ago = (dt.datetime.now() - dt.timedelta(days=days_ago)).date()
    response = requests.get(
        API_URL + '/search/repositories?q=created:>' + str(days_ago) +
        '&sort=stars?page=1&per_page=' + str(top_size))
    return json.loads(response.content)


if __name__ == '__main__':
    days_period = 7
    repositories_count = 20
    github_projects_response = get_n_trending_repositories_json(
        repositories_count, days_period)
    print('Information about {} most trending repositories:'.format(
        repositories_count))
    for github_project_json in github_projects_response['items']:
        project_stars = github_project_json['stargazers_count']
        project_name = github_project_json['name']
        project_url = github_project_json['html_url']
        open_issues = github_project_json['open_issues_count']
        print('Project: stars: {:6} name: {:30} open issues: {:5} URL: {}'.
              format(project_stars, project_name, open_issues, project_url))
