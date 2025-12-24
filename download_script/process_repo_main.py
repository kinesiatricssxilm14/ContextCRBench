from parse_url import extract_references
import os
import json
from graphql_query import graphql_query
from concurrent.futures import ThreadPoolExecutor
from log import log_process
from package import PACKAGE_NAME

def process_json_file(json_file, owner_name, repo_name):
    with open(f'data/{repo_name}/{json_file}', 'r') as f:
        data = json.load(f)
    if 'cite' in data:
        return
    cite = list()
    tmp = extract_references(data.get('body', ''), owner_name, repo_name, data.get('number', 0))
    cite.extend(tmp)
    tmp = extract_references(data.get('title', ''), owner_name, repo_name, data.get('number', 0))
    cite.extend(tmp)
    for comment in data.get('comments_details', []):
        tmp = extract_references(comment['body'], owner_name, repo_name, data.get('number', 0))
        cite.extend(tmp)

    for review_comment in data.get('review_comments_details', []):
        for com in review_comment['comments']:
            tmp = extract_references(com.get('review_comment', ''), owner_name, repo_name, data.get('number', 0))
            cite.extend(tmp)
            tmp = extract_references(com.get('comment', ''), owner_name, repo_name, data.get('number', 0))
            cite.extend(tmp)

    cite = list({frozenset(item.items()): item for item in cite}.values())  # Remove duplicates
    data['cite'] = cite

    log_process(f'begin query no {data["number"]}')
    if 'pull_request' in data:
        issue_or_pr = 'pullRequest'
    else:
        issue_or_pr = 'issue'
    cited_by_json = graphql_query(issue_or_pr, data['number'], owner_name, repo_name)
    cited_by = []

    for cbj in cited_by_json:
        tmp = extract_references(cbj['source']['url'], owner_name, repo_name, data.get('number', 0), trust=True)
        cited_by.extend(tmp)

    cited_by = list({frozenset(item.items()): item for item in cited_by}.values())  # Remove duplicates
    data['cited_by'] = cited_by

    with open(f'data/{repo_name}/{json_file}', 'w') as f:
        json.dump(data, f, indent=4)

    log_process(f'Finish valid {data["number"]}')

if __name__  == '__main__':
    owner_name = f'{PACKAGE_NAME.split("/")[0]}'
    repo_name = f'{PACKAGE_NAME.split("/")[1]}'
    all_json = [x for x in os.listdir('data/' + repo_name) if x.endswith('.json')]
    with ThreadPoolExecutor(max_workers=30) as executor:
        for json_file in all_json:
            executor.submit(process_json_file, json_file, owner_name, repo_name)