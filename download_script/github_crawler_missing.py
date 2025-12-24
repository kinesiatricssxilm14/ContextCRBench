import os
import requests
import json
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import schedule
import re
from package import PACKAGE_NAME

import logging

class FlushFileHandler(logging.FileHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()

def setup_logging(PACKAGE_NAME):
    if not os.path.exists(f'data/{PACKAGE_NAME.split("/")[1]}'):
        os.system(f'mkdir -p data/{PACKAGE_NAME.split("/")[1]}') # ignore_security_alert RCE

    catch_remaining_logger = logging.getLogger('catch_remaining_logger')
    catch_remaining_logger.setLevel(logging.INFO)
    
    process_logger = logging.getLogger('process_logger')
    process_logger.setLevel(logging.INFO)
    
    switching_logger = logging.getLogger('switching_logger')
    switching_logger.setLevel(logging.INFO)

    token_logger = logging.getLogger('token_logger')
    token_logger.setLevel(logging.INFO)
    
    catch_remaining_handler = FlushFileHandler(f'data/{PACKAGE_NAME.split("/")[1]}/catch_remaining_missing.log')
    catch_remaining_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    catch_remaining_handler.setFormatter(catch_remaining_formatter)
    catch_remaining_logger.addHandler(catch_remaining_handler)
    
    process_handler = FlushFileHandler(f'data/{PACKAGE_NAME.split("/")[1]}/process_missing.log')
    process_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    process_handler.setFormatter(process_formatter)
    process_logger.addHandler(process_handler)
    
    switching_handler = FlushFileHandler(f'data/{PACKAGE_NAME.split("/")[1]}/switching_missing.log')
    switching_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    switching_handler.setFormatter(switching_formatter)
    switching_logger.addHandler(switching_handler)

    token_handler = FlushFileHandler(f'data/{PACKAGE_NAME.split("/")[1]}/token_missing.log')
    token_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    token_handler.setFormatter(token_formatter)
    token_logger.addHandler(token_handler)
    
    return catch_remaining_logger, process_logger, switching_logger, token_logger

catch_remaining_logger, process_logger, switching_logger, token_logger = setup_logging(PACKAGE_NAME)

def log_catch_remaining(message):
    catch_remaining_logger.info(f'[CATCH_REMAINING] {message}')

def log_process(message):
    process_logger.info(f'[PROCESS] {message}')

def log_switching(message):
    switching_logger.info(f'[SWITCHING] {message}')

def log_token(message):
    token_logger.info(f'[TOKEN] {message}')

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
    if not os.path.exists(f'data/{PACKAGE_NAME.split("/")[1]}/tokens.tk'):
        os.system(f'cp tokens.tk data/{PACKAGE_NAME.split("/")[1]}/tokens.tk') # ignore_security_alert RCE
    global tokens
    try:
        with open(f'data/{PACKAGE_NAME.split("/")[1]}/tokens.tk', 'r') as r1:
            read_tokens = [x.strip() for x in r1.readlines()]
        if len(read_tokens) < 3:
            log_token("Do not change, the token number is not enough.")
        else:
            tokens = random.sample(read_tokens, 3)
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
        # 清空disabled_tokens
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
    while url:
        headers = {
            'Authorization': f'token {get_token()}',
            "User-Agent": get_user_agent(),
        }
        if is_remaining(headers):
            response = requests.get(url, headers=headers, params=params, timeout=60*2)
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
        elif fetch_type == 'diff':
            result.append(response.text)
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

    if issue['comments'] > 0:
        comments_url = f'https://api.github.com/repos/{PACKAGE_NAME}/issues/{number}/comments'
        comments_headers = headers
        comments_params = params
        comments = fetch_others('comments', comments_url, comments_headers, comments_params)
        if 'comments_details' not in issue:
            issue['comments_details'] = list()
        issue['comments_details'].extend(comments)
    else:
        issue['comments_details'] = list()

    events_url = f'https://api.github.com/repos/{PACKAGE_NAME}/issues/{number}/events'
    events_headers = headers
    events_params = params
    events = fetch_others('events', events_url, events_headers, events_params) # ignore_security_alert RCE
    if 'events' not in issue:
        issue['events'] = list()
    issue['events'].extend(events)

    if 'pull_request' in issue:
        pr_url = f'https://api.github.com/repos/{PACKAGE_NAME}/pulls/{number}'
        pr_headers = headers
        pr_params = params
        pr = fetch_others('pulls', pr_url, pr_headers, pr_params)
        issue['pull_request'] = pr[0]

        pr_patch_url = f'https://patch-diff.githubusercontent.com/raw/{PACKAGE_NAME}/pull/{number}.diff'
        pr_patch = fetch_others('diff', pr_patch_url, pr_headers, pr_params)
        issue['pull_request']['diff'] = pr_patch[0]

    return issue

def fetch_single_issue(issue_number, headers=None, params=None):
    headers = {
        "Authorization": f'token {get_token()}',
        "User-Agent": get_user_agent(),
    }
    url = f'https://api.github.com/repos/{PACKAGE_NAME}/issues/{issue_number}'

    if is_remaining(headers):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=60*2)
            response.raise_for_status()  
        except Exception as e:
            log_process(f"issue {issue_number} has problem! {e}")
    else:
        headers['Authorization'] = f'token {get_token()}'
        log_switching(f'Switching token to {headers["Authorization"]} for url: {url}')
        pause_duration = random.randint(10, 30)
        log_switching(f"Pausing for {pause_duration} seconds, long")
        time.sleep(pause_duration)
    
    simple_issue = response.json()
    issue = process_issue(simple_issue, headers, params)
    if not os.path.exists(f'data/{PACKAGE_NAME.split("/")[1]}'):
        os.system(f'mkdir -p data/{PACKAGE_NAME.split("/")[1]}')  # ignore_security_alert RCE
    number = issue['number']
    with open(f'data/{PACKAGE_NAME.split("/")[1]}/{number}.json', 'w') as w1:
        w1.write(json.dumps(issue, indent=4, ensure_ascii=False))

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

def get_missing_number():
    with open(f'data/{PACKAGE_NAME.split("/")[1]}/process_missing.log', 'r') as r1:
        x = r1.read()
    if len(x.strip()) > 0:
        text = x
    else:
        with open(f'data/{PACKAGE_NAME.split("/")[1]}/process.log', 'r') as r1:
            text = r1.read()
    pattern = r"Issue (\d+)"
    matches = re.findall(pattern, text)
    issue_numbers = [int(match) for match in matches]
    return issue_numbers

if __name__ == '__main__':
    schedule.every(2).minutes.do(change_tokens)

    schedule_therad = threading.Thread(target=run_schedule)
    schedule_therad.daemon = True
    schedule_therad.start()
    os.system(f'cp tokens.tk data/{PACKAGE_NAME.split("/")[1]}')

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
    issue_numbers = get_missing_number()
    with ThreadPoolExecutor(max_workers=30) as executor:
        futures = {executor.submit(fetch_single_issue, issue_number, headers, params): issue_number for issue_number in issue_numbers}

        for future in as_completed(futures):
            issue_number = futures[future]
            try:
                log_process(f"Begin issue {issue_number}")
                future.result(timeout=3*60)
                log_process(f"Finish issue {issue_number}")
            except Exception as e:
                log_process(f"Issue {issue_number} has problem, Exception: {e}")
