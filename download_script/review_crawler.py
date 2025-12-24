import os
import requests
import json
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import schedule
import re
from log import log_catch_remaining, log_process, log_switching, log_token
from package import PACKAGE_NAME

user_agent = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.80 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Android 10; Mobile; rv:89.0) Gecko/89.0 Firefox/89.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/33.0 Mobile/15E148 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.864.64 Safari/537.36 Edg/91.0.864.64',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.864.64 Safari/537.36 Edg/91.0.864.64',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.172',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.172',
]

def get_user_agent():
    return random.sample(user_agent, 1)[0]

def change_tokens():
    time.sleep(random.randint(1, 3))
    if os.path.exists(f'data/{PACKAGE_NAME.split("/")[1]}/tokens.tk'):
        os.system(f'cp tokens.tk data/{PACKAGE_NAME.split("/")[1]}/tokens.tk') # ignore_security_alert RCE
    global tokens
    try:
        with open(f'tokens.tk', 'r') as r1:
            read_tokens = [x.strip() for x in r1.readlines()]
        if len(read_tokens) < 3:
            log_token("Do not change, the token number is not enough.")
        else:
            tokens = random.sample(read_tokens, 10)
            log_token(f"Swifting tokens to {tokens}")
    except:
        log_process("open tokens.tk has problem!!! Please quickly solve the token.tk")

tokens = change_tokens()

disabled_tokens = list()

def get_token():
    global disabled_tokens
    global tokens
    pause_duration = random.randint(1, 3)
    log_switching(f"Pausing for {pause_duration} seconds, shortest")
    time.sleep(pause_duration)
    if len(disabled_tokens) == len(tokens):
        log_token(f"The tokens are all disabled! Please consider change the tokens in data/{PACKAGE_NAME.split('/')[1]}/tokens.tk")
        disabled_tokens = list()
        change_tokens()
    else:
        while True:
            select_token = random.sample(tokens, 1)[0]
            if select_token not in disabled_tokens:
                return select_token

def is_remaining(headers):
    global disabled_tokens
    url = 'https://api.github.com/rate_limit'
    try:
        response = requests.get(url, headers=headers, params=None, timeout=30)
        response.raise_for_status()
        rate_limit = response.json()['rate']
        log_catch_remaining(f"Rate limit: {rate_limit['remaining']} Token: {headers['Authorization']}")
        return rate_limit['remaining'] > 500
    except requests.exceptions.Timeout as e:
        log_catch_remaining(f"Token has timeout! {headers['Authorization']} - {e}")
        change_tokens()
        return False
    except Exception as e:
        log_catch_remaining(f"Token has problem! {headers['Authorization']} - {e}")
        disabled_tokens.append(headers['Authorization'])
        return False

def fetch_others(fetch_type, url, headers=None, params=None):
    result = list()
    while url: # ignore_security_alert RCE
        headers = {
            'Authorization': f'token {get_token()}',
            "User-Agent": get_user_agent(),
        }
        if is_remaining(headers):
            response = requests.get(url, headers=headers, params=params, timeout=60)
            response.raise_for_status() 
        else:
            change_tokens()
            headers['Authorization'] = f'token {get_token()}'
            log_switching(f'Switching token to {headers["Authorization"]} for url: {url}')
            pause_duration = random.randint(10, 30)
            log_switching(f"Pausing for {pause_duration} seconds, long")
            time.sleep(pause_duration)
            continue

        if fetch_type == 'comments' or fetch_type == 'events':
            result.extend(response.json())
        elif fetch_type == 'pulls':
            result.append(response.json())
        elif fetch_type == 'patch':
            result.append(response.text)
        elif fetch_type == 'reviews':
            result.extend(response.json())
        elif fetch_type == 'review_comments':
            result.extend(response.json())
        else:
            raise Exception("Wrong fetch type!")
        
        if 'Link' in response.headers:
            links = response.headers['Link']
            next_link = None
            for link in links.split(','):
                if 'rel="next"' in link:
                    next_link = link[link.find('<') + 1:link.find('>')]
                    break
            url = next_link
            pause_duration = random.randint(3, 5)
            log_switching(f"Pausing for {pause_duration} seconds, page short")
            time.sleep(pause_duration)
        else:
            url = None
    return result

def process_issue(issue, headers, params):
    number = issue['number']

    if issue['pull_request']['review_comments'] > 0:
        review_url = f'https://api.github.com/repos/{PACKAGE_NAME}/pulls/{number}/reviews'
        review_comments_url = f'https://api.github.com/repos/{PACKAGE_NAME}/pulls/{number}/comments'
        reviews = fetch_others('reviews', review_url, headers, params)
        review_comments = fetch_others('review_comments', review_comments_url, headers, params)

        issue['review_comments_details'] = list()

        if not (len(review_comments) != 0 and len(reviews) == 0):

            for review_comment in review_comments:
                if 'in_reply_to_id' in review_comment:
                    continue
                
                patch_msg = dict()
                patch_msg['path'] = review_comment['path']
                patch_msg['commit_id'] = review_comment['commit_id']
                patch_msg['original_commit_id'] = review_comment['original_commit_id']
                patch_msg['diff_hunk'] = review_comment['diff_hunk']
                # if review_comment['start_line'] is not None:
                patch_msg['start_line'] = review_comment['start_line']
                # if review_comment['original_start_line'] is not None:
                patch_msg['original_start_line'] = review_comment['original_start_line']
                # if review_comment['start_side'] is not None:
                patch_msg['start_side'] = review_comment['start_side']
                # if review_comment['line'] is not None:
                patch_msg['line'] = review_comment['line']
                # if review_comment['original_line'] is not None:
                patch_msg['original_line'] = review_comment['original_line']
                # if review_comment['side'] is not None:
                patch_msg['side'] = review_comment['side']
                # if review_comment['original_position'] is not None:
                patch_msg['original_position'] = review_comment['original_position']
                # if review_comment['position'] is not None:
                patch_msg['position'] = review_comment['position']
                # if review_comment['subject_type'] is not None:
                patch_msg['subject_type'] = review_comment['subject_type']

                dialogues = list()
                dialogue_root = dict()
                for review in reviews:
                    if review_comment['pull_request_review_id'] == review['id']:
                        dialogue_root['state'] = review['state']
                        if not review['body'].strip() == '':
                            dialogue_root['review_comment'] = review['body']
                        dialogue_root['comment'] = review_comment['body']
                        dialogue_root['user_name'] = review_comment['user']['login']
                        # if review_comment['author_association'].upper() != 'NONE':
                        dialogue_root['author_association'] = review_comment['author_association']
                        dialogue_root['reactions'] = dict()
                        dialogue_root['reactions']['total_count'] = review_comment['reactions']['total_count']
                        if review_comment['reactions']['+1'] > 0:
                            dialogue_root['reactions']['+1'] = review_comment['reactions']['+1']
                        if review_comment['reactions']['-1'] > 0:
                            dialogue_root['reactions']['-1'] = review_comment['reactions']['-1']
                        if review_comment['reactions']['laugh'] > 0:
                            dialogue_root['reactions']['laugh'] = review_comment['reactions']['laugh']
                        if review_comment['reactions']['hooray'] > 0:
                            dialogue_root['reactions']['hooray'] = review_comment['reactions']['hooray']
                        if review_comment['reactions']['confused'] > 0:
                            dialogue_root['reactions']['confused'] = review_comment['reactions']['confused']
                        if review_comment['reactions']['heart'] > 0:
                            dialogue_root['reactions']['heart'] = review_comment['reactions']['heart']
                        if review_comment['reactions']['rocket'] > 0:
                            dialogue_root['reactions']['rocket'] = review_comment['reactions']['rocket']
                        if review_comment['reactions']['eyes'] > 0:
                            dialogue_root['reactions']['eyes'] = review_comment['reactions']['eyes']
                        dialogue_root['created_at'] = review_comment['created_at']
                        dialogue_root['updated_at'] = review_comment['updated_at']
                        break
                if dialogue_root != {}:
                    dialogues.append(dialogue_root)
                        

                id = review_comment['id']
                for r in review_comments:
                    dialogue = dict()
                    if 'in_reply_to_id' not in r:
                        continue
                    if r['in_reply_to_id'] == id:
                        for review in reviews:
                            if r['pull_request_review_id'] == review['id']:
                                dialogue['state'] = review['state']
                                if not review['body'].strip() == '':
                                    dialogue['review_comment'] = review['body']
                                dialogue['comment'] = r['body']
                                dialogue['user_name'] = r['user']['login']
                                # if r['author_association'].upper() != 'NONE':
                                dialogue['author_association'] = r['author_association']
                                dialogue['reactions'] = dict()
                                dialogue['reactions']['total_count'] = r['reactions']['total_count']
                                if r['reactions']['+1'] > 0:
                                    dialogue['reactions']['+1'] = r['reactions']['+1']
                                if r['reactions']['-1'] > 0:
                                    dialogue['reactions']['-1'] = r['reactions']['-1']
                                if r['reactions']['laugh'] > 0:
                                    dialogue['reactions']['laugh'] = r['reactions']['laugh']
                                if r['reactions']['hooray'] > 0:
                                    dialogue['reactions']['hooray'] = r['reactions']['hooray']
                                if r['reactions']['confused'] > 0:
                                    dialogue['reactions']['confused'] = r['reactions']['confused']
                                if r['reactions']['heart'] > 0:
                                    dialogue['reactions']['heart'] = r['reactions']['heart']
                                if r['reactions']['rocket'] > 0:
                                    dialogue['reactions']['rocket'] = r['reactions']['rocket']
                                if r['reactions']['eyes'] > 0:
                                    dialogue['reactions']['eyes'] = r['reactions']['eyes']
                                dialogue['created_at'] = r['created_at']
                                dialogue['updated_at'] = r['updated_at']
                                break
                    if dialogue != {}:
                        dialogues.append(dialogue)
                msg = dict()
                if len(dialogues) > 0:
                    msg['created_at'] = dialogues[0]['created_at']
                msg['patch_message'] = patch_msg
                msg['comments'] = dialogues

                issue['review_comments_details'].append(msg)
# -------------------------------------------------------------------------------------------------------------------------------
        else:
            selected_id = list()
            for i in range(len(review_comments)):
                if i in selected_id:
                    continue
                else:
                    selected_id.append(i)
                review_comment = review_comments[i]
                patch_msg = dict()
                patch_msg['path'] = review_comment['path']
                patch_msg['diff_hunk'] = review_comment['diff_hunk']
                patch_msg['commit_id'] = review_comment['commit_id']
                patch_msg['original_commit_id'] = review_comment['original_commit_id']
                # if review_comment['start_line'] is not None:
                patch_msg['start_line'] = review_comment['start_line']
                # if review_comment['original_start_line'] is not None:
                patch_msg['original_start_line'] = review_comment['original_start_line']
                # if review_comment['start_side'] is not None:
                patch_msg['start_side'] = review_comment['start_side']
                # if review_comment['line'] is not None:
                patch_msg['line'] = review_comment['line']
                # if review_comment['original_line'] is not None:
                patch_msg['original_line'] = review_comment['original_line']
                # if review_comment['side'] is not None:
                patch_msg['side'] = review_comment['side']
                # if review_comment['original_position'] is not None:
                patch_msg['original_position'] = review_comment['original_position']
                # if review_comment['position'] is not None:
                patch_msg['position'] = review_comment['position']
                # if review_comment['subject_type'] is not None:
                patch_msg['subject_type'] = review_comment['subject_type']

                dialogues = list()
                dialogue_root = dict()
                
                dialogue_root['comment'] = review_comment['body']
                dialogue_root['user_name'] = review_comment['user']['login']
                # if review_comment['author_association'].upper() != 'NONE':
                dialogue_root['author_association'] = review_comment['author_association']
                dialogue_root['reactions'] = dict()
                dialogue_root['reactions']['total_count'] = review_comment['reactions']['total_count']
                if review_comment['reactions']['+1'] > 0:
                    dialogue_root['reactions']['+1'] = review_comment['reactions']['+1']
                if review_comment['reactions']['-1'] > 0:
                    dialogue_root['reactions']['-1'] = review_comment['reactions']['-1']
                if review_comment['reactions']['laugh'] > 0:
                    dialogue_root['reactions']['laugh'] = review_comment['reactions']['laugh']
                if review_comment['reactions']['hooray'] > 0:
                    dialogue_root['reactions']['hooray'] = review_comment['reactions']['hooray']
                if review_comment['reactions']['confused'] > 0:
                    dialogue_root['reactions']['confused'] = review_comment['reactions']['confused']
                if review_comment['reactions']['heart'] > 0:
                    dialogue_root['reactions']['heart'] = review_comment['reactions']['heart']
                if review_comment['reactions']['rocket'] > 0:
                    dialogue_root['reactions']['rocket'] = review_comment['reactions']['rocket']
                if review_comment['reactions']['eyes'] > 0:
                    dialogue_root['reactions']['eyes'] = review_comment['reactions']['eyes']
                dialogue_root['created_at'] = review_comment['created_at']
                dialogue_root['updated_at'] = review_comment['updated_at']
                        
                if dialogue_root != {}:
                    dialogues.append(dialogue_root)
                        

                diff_hunk = review_comment['diff_hunk']
                for j in range(len(review_comments)):
                    if j in selected_id:
                        continue
                    else:
                        selected_id.append(j)
                    r = review_comments[j]
                    dialogue = dict()
                    if r['diff_hunk'] == diff_hunk:
                        dialogue['comment'] = r['body']
                        dialogue['user_name'] = r['user']['login']
                        # if r['author_association'].upper() != 'NONE':
                        dialogue['author_association'] = r['author_association']
                        dialogue['reactions'] = dict()
                        dialogue['reactions']['total_count'] = r['reactions']['total_count']
                        if r['reactions']['+1'] > 0:
                            dialogue['reactions']['+1'] = r['reactions']['+1']
                        if r['reactions']['-1'] > 0:
                            dialogue['reactions']['-1'] = r['reactions']['-1']
                        if r['reactions']['laugh'] > 0:
                            dialogue['reactions']['laugh'] = r['reactions']['laugh']
                        if r['reactions']['hooray'] > 0:
                            dialogue['reactions']['hooray'] = r['reactions']['hooray']
                        if r['reactions']['confused'] > 0:
                            dialogue['reactions']['confused'] = r['reactions']['confused']
                        if r['reactions']['heart'] > 0:
                            dialogue['reactions']['heart'] = r['reactions']['heart']
                        if r['reactions']['rocket'] > 0:
                            dialogue['reactions']['rocket'] = r['reactions']['rocket']
                        if r['reactions']['eyes'] > 0:
                            dialogue['reactions']['eyes'] = r['reactions']['eyes']
                        dialogue['created_at'] = r['created_at']
                        dialogue['updated_at'] = r['updated_at']

                    if dialogue != {}:
                        dialogues.append(dialogue)
                msg = dict()
                if len(dialogues) > 0:
                    msg['created_at'] = dialogues[0]['created_at']
                msg['patch_message'] = patch_msg
                msg['comments'] = dialogues

                issue['review_comments_details'].append(msg)
        
    return issue

def fetch_single_issue(issue_number, headers=None, params=None):
    headers = {
        "Authorization": f'token {get_token()}',
        "User-Agent": get_user_agent(),
    }
    with open(f'data/{PACKAGE_NAME.split("/")[1]}/{issue_number}.json', 'r') as r1:
        single_issue = json.load(r1)
    number = single_issue['number']
    issue = process_issue(single_issue, headers, params)
    with open(f'data/{PACKAGE_NAME.split("/")[1]}/{number}.json', 'w') as w1: # ignore_security_alert RCE
        w1.write(json.dumps(issue, indent=4, ensure_ascii=False))

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

def get_missing_number(folder_path):
    res = list()
    all_json = [x for x in os.listdir(folder_path) if x.endswith('.json')]
    for aj in all_json:
        with open(os.path.join(folder_path, aj), 'r') as r1:
            data = json.load(r1)
        if 'pull_request' not in data or 'number' not in data:
            continue
        if 'review_comments_details' in data:
            continue
        res.append(data['number'])
    return res


if __name__ == '__main__':
    schedule.every(2).minutes.do(change_tokens) # ignore_security_alert RCE

    schedule_therad = threading.Thread(target=run_schedule)
    schedule_therad.daemon = True
    schedule_therad.start()

    change_tokens()
    url = f'https://api.github.com/repos/{PACKAGE_NAME}/issues'
    headers = {
        'Authorization': f'token {get_token()}',
        "User-Agent": get_user_agent(),
    }
    params = {
        'per_page': 100,
        'state': 'all',
    }
    issue_numbers = get_missing_number(f'data/{PACKAGE_NAME.split("/")[1]}')
    # issue_numbers = ['26722']
    # print(issue_numbers)
    random.shuffle(issue_numbers)
    with ThreadPoolExecutor(max_workers=70) as executor:
        futures = {executor.submit(fetch_single_issue, issue_number, headers, params): issue_number for issue_number in issue_numbers}

        for future in as_completed(futures):
            issue_number = futures[future]
            try:
                log_process(f"Begin issue {issue_number}")
                future.result(timeout=3*60)
                log_process(f"Finish issue {issue_number}")
            except Exception as e:
                log_process(f"Issue {issue_number} has problem, Exception: {e}")
