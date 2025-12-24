import requests
import random
import time
from collections import deque
import threading
from log import log_catch_remaining, log_process, log_switching, log_token

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

with open('tokens.tk', 'r') as r1:
    GITHUB_TOKEN = [x.strip() for x in r1.readlines()]

token_queue = deque(GITHUB_TOKEN)
lock = threading.Lock()

def get_user_agent():
    return random.sample(user_agent, 1)[0]

def is_remaining(headers):
  url = 'https://api.github.com/rate_limit'
  try:
      response = requests.get(url, headers=headers, params=None, timeout=120)
      response.raise_for_status()
      rate_limit = response.json()
      log_catch_remaining(f'token {headers["Authorization"]} rate limit is {rate_limit["rate"]["remaining"]} and graphql limit is {rate_limit["resources"]["graphql"]["remaining"]}')
      return rate_limit['rate']['remaining'] > 50 and rate_limit['resources']['graphql']['remaining'] > 50
  except requests.exceptions.Timeout as e:
      log_process(f'token {headers["Authorization"]} timeout! {e}')
      return False
  except Exception as e:
      log_process(f'token {headers["Authorization"]} has been broken! {e}')
      return False

def get_github_token():
    global token_queue
    
    with lock:
      if not token_queue:
          token_queue = deque(GITHUB_TOKEN)
          random.shuffle(token_queue)
      
      return token_queue.popleft()


def graphql_query(issue_or_pr, number, owner_name, repo_name):
  query = f"""
  {{
    repository(owner: "{owner_name}", name: "{repo_name}") {{
      {issue_or_pr}(number: {number}) {{
        timelineItems(first: 100, itemTypes: CROSS_REFERENCED_EVENT) {{
          nodes {{
            ... on CrossReferencedEvent {{
              source {{
                __typename
                ... on PullRequest {{
                  repository {{
                    owner {{
                      login
                    }}
                    name
                  }}
                  number
                  title
                  url
                }}
                ... on Issue {{
                  repository {{
                    owner {{
                      login
                    }}
                    name
                  }}
                  number
                  title
                  url
                }}
              }}
            }}
          }}
        }}
      }}
    }}
  }}
  """
  headers = {
     "Authorization": f"Bearer {get_github_token()}",
     "User-Agent": f"{get_user_agent()}",
    }

  try:
    if is_remaining(headers):
      response = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers, timeout=30)
      x = random.randint(1, 3)
      time.sleep(x)
      log_switching(f'Short: token {headers["Authorization"]} sleep for {x} seconds.')
    else:
      log_token(f'token {headers["Authorization"]} is not enough!')
      x = random.randint(20, 40)
      time.sleep(x)
      log_switching(f'Long: token {headers["Authorization"]} sleep for {x} seconds.')
  except:
     log_process(f'timeout for no {number}')

  data = response.json()
  return data['data']['repository'][issue_or_pr]['timelineItems']['nodes']