import argparse
import requests
import json
import pandas as pd
import datetime as dt
from dateutil import tz

from_zone = tz.gettz('UTC')
to_zone = tz.gettz('America/New_York')
utc = dt.datetime.utcnow().replace(tzinfo=from_zone)
est = utc.astimezone(to_zone)

today = est.date()

API_ROOT = 'https://nyt-games-prd.appspot.com/svc/crosswords'
LEADERBOARD_INFO = API_ROOT + '/v6/leaderboard/mini.json'

parser = argparse.ArgumentParser(description='Fetch NYT Crossword stats')
parser.add_argument(
    '-u', '--username', help='NYT Account Email Address', required=True)
parser.add_argument(
    '-p', '--password', help='NYT Account Password', required=True)
parser.add_argument(
    '-w', '--working-directory',
    help='Where to save the file',
    default='/path/path/path` # change to the working directory you want the data to land in
)

def login(username, password):
    """ Return the NYT-S cookie after logging in """
    login_resp = requests.post(
        'https://myaccount.nytimes.com/svc/ios/v2/login',
        data={
            'login': username,
            'password': password,
        },
        headers={
            'User-Agent': 'Crossword/20210331164208 CFNetwork/1220.1 Darwin/20.3.0',
            'client_id': 'ios.crosswords',
        }
    )
    login_resp.raise_for_status()
    for cookie in login_resp.json()['data']['cookies']:
        if cookie['name'] == 'NYT-S':
            return cookie['cipheredValue']
    raise ValueError('NYT-S cookie not found')

def get_leaderboard_stats(cookie):
    leaderboard_resp = requests.get(
        LEADERBOARD_INFO,
        cookies={
            'NYT-S': cookie,
        },
    )
    leaderboard_resp.raise_for_status()
    leaderboard_info = leaderboard_resp.json().get('data')

    df = pd.json_normalize(leaderboard_info)
    df = pd.DataFrame(df)
    friends_list = [userid1, userid2] # only needed if you want to cut out users from the points rankings
    df = df[df['userID'].isin(friends_list)]
    # remove NAs; if all NAs, return error
    try:
        df = df[df['score.secondsSpentSolving'].notna()]
    except KeyError:
        print("There have been no crossword completions today.")
        input()    # posts error message
        import sys
        sys.exit(1)     # exit program
    df = df[['name', 'score.secondsSpentSolving']]
    df['date'] = today
    df['rank'] = df['score.secondsSpentSolving'].rank(method='min').astype(int)
    df['points'] = df['score.secondsSpentSolving'].rank(method='min', ascending = False).astype(int)
    return df

if __name__ == '__main__':
    args = parser.parse_args()
    cookie = login(args.username, args.password)
    df = get_leaderboard_stats(cookie)
    df.to_csv('{}/crossword_stats_{}.csv'.format(args.working_directory, today))
