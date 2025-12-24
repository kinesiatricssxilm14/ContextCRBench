import json
import os
import re
import sys
from parse_url import extract_references
from package import PACKAGE_NAME

def parse_github_reference(text):
    text = text.lower()
    key_pattern = r'\b(fix(?:es|ed)?|close[sd]?|solve[sd]?)\b'
    pattern = rf'{key_pattern}[:\s]+([^\s\r\n\t]+)'
    matches = re.findall(pattern, text, re.IGNORECASE)
    parsed_references = []
    for match in matches:
        key = match[0]
        content = match[1].strip() 
        parsed_references.append({"key": key, "link": content})
    return parsed_references

root_path = f'data/{PACKAGE_NAME.split("/")[1]}'
all_json = [root_path + '/' + x for x in os.listdir(root_path) if x.endswith('.json')]

import random
random.shuffle(all_json)
pair = list()
for aj in all_json:
    fixed_list = list()
    with open(aj, 'r') as r1:
        data = json.load(r1)
    if 'pull_request' in data:
        continue
    if 'cited_by' not in data:
        continue
    # print(aj)
    for dcb in data['cited_by']:
        # print(dcb['number'])
        # print('*'*100)
        fixed_pr_no = -1
        if not dcb['is_own_repo']:
            continue
        pr_number = dcb['number']
        pr_path = '/'.join(aj.split('/')[:-1]) + '/' + pr_number + '.json'
        if not os.path.exists(pr_path):
            continue
        with open(pr_path, 'r') as r2:
            pr_data = json.load(r2)
        if 'pull_request' not in pr_data:
            continue
        # if not pr_data['pull_request']['merged']:
        #     continue
        text = ''
        title = pr_data.get('title', '')
        if title is None:
            title = ''
        text += title
        body = pr_data.get('body', '')
        if body is None:
            body = ''
        # print(pr_number)
        text += ' '
        text += body
        comments = pr_data.get('comments_details', [])
        for x in comments:
            text += ' '
            text += x['body']
        review_comments = pr_data.get('review_comments_details', [])
        for y in review_comments:
            text += ' '
            text += y.get('review_comment', '')
            text += ' '
            text += y.get('comment', '')
        res = parse_github_reference(text)
        # print(text)
        # print('@'*100)
        # print(res)
        links = ''
        for r in res:
            links += r['link']
            links += ' '
        reference = extract_references(links, dcb['owner'], dcb['repo_name'], pr_number, trust=True)
        if_pair = False
        for r in reference:
            if str(r['number']) == str(data['number']) and r['is_own_repo']:
                if_pair = True
        if if_pair:
            fixed_pr_no = int(pr_number)
        if fixed_pr_no != -1:
            fixed_list.append(fixed_pr_no)
    # if len(fixed_list) > 0:
    data['fixed_by'] = fixed_list
    with open(aj, 'w') as w1:
        w1.write(json.dumps(data, indent=4, ensure_ascii=False))
    if len(fixed_list) > 0:
        pair.append([aj, fixed_list])


print(pair)
print(len(pair))

# print(parse_github_reference('\nFixes: https://github.com/nodejs/node/issues/54327\r\n\r\n<!--\r\nBefore'))