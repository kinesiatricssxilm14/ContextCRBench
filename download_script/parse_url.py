import re
import json
from graphql_query import graphql_query
def extract_references(text, owner, repo_name, issue_or_pr_no, trust=False):
    issue_pr_url_pattern = re.compile(r'https://github\.com/([^/]+)/([^/]+)/issues/(\d+)')
    pr_url_pattern = re.compile(r'https://github\.com/([^/]+)/([^/]+)/pull/(\d+)')
    hash_reference_pattern = re.compile(r'#(\d+)')
    
    gh_pattern = re.compile(r'gh-(\d+)')
    GH_pattern = re.compile(r'GH-(\d+)')
    pull_slash_pattern = re.compile(r'pull/(\d+)')
    pull_dash_pattern = re.compile(r'pull-(\d+)')
    issue_dash_pattern = re.compile(r'issue-(\d+)')
    issue_slash_pattern = re.compile(r'issue/(\d+)')
    
    references = []
    
    for match in issue_pr_url_pattern.finditer(text):
        ref_owner, ref_repo, number = match.groups()
        is_own_repo = (ref_owner == owner and ref_repo == repo_name)
        references.append({
            'owner': ref_owner,
            'repo_name': ref_repo,
            'number': number,
            'is_own_repo': is_own_repo
        })
    
    for match in pr_url_pattern.finditer(text):
        ref_owner, ref_repo, number = match.groups()
        is_own_repo = (ref_owner == owner and ref_repo == repo_name)
        references.append({
            'owner': ref_owner,
            'repo_name': ref_repo,
            'number': number,
            'is_own_repo': is_own_repo
        })
    
    for match in hash_reference_pattern.finditer(text):
        number = match.group(1)
        references.append({
            'owner': owner,
            'repo_name': repo_name,
            'number': number,
            'is_own_repo': True
        })
    
    for pattern in [gh_pattern, GH_pattern, pull_slash_pattern, pull_dash_pattern, issue_dash_pattern, issue_slash_pattern]:
        for match in pattern.finditer(text):
            number = match.group(1)
            references.append({
                'owner': owner,
                'repo_name': repo_name,
                'number': number,
                'is_own_repo': True
            })

    if trust:
        return references
        
    final_res = list()
    for reference in references:
        try:
            res = graphql_query('issue', reference['number'], reference['owner'], reference['repo_name'])
        except:
            res = graphql_query('pullRequest', reference['number'], reference['owner'], reference['repo_name'])
        for r in res:
            if r['source']['number'] == issue_or_pr_no:
                final_res.append(reference)
                break
    return final_res




# print(extract_references('\nFixes: https://github.com/nodejs/node/issues/54327\r\n\r\n<!--\r\nBefore', 'nodejs', 'node', 54327, True))