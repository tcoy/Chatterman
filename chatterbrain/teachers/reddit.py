import requests
import json


class RedditTeacher:
    def __init__(self, brain):
        self.brain = brain

    def teach(self, subreddit):
        self.subreddit = subreddit

        if '/r/' not in subreddit:
            self.subreddit = '/r/' + self.subreddit

        reddit_url = 'http://www.reddit.com'
        subreddit_url = reddit_url + '%s' % subreddit
        hot_url = subreddit_url + '/hot.json'
        print('peeking at %s' % reddit_url)

        hot_req = requests.get(hot_url, headers={
            'User-agent': 'chatterman-bot-1.0'})
        data = json.loads(hot_req.content)

        if 'error' not in data:
            try:
                for child in data['data']['children']:
                    permalink = child['data']['permalink'] + '.json'
                    url = reddit_url + permalink
                    print('reading url %s' % url)
                    comments_req = requests.get(url, headers={
                        'User-agent': 'chatterman-bot-1.0'})
                    data = json.loads(comments_req.content)
                    if 'error' not in data:
                        for comment in data['data']['children']:
                            body = comment['data']['body']
                            print('Learned comment: %s' % body)
                    else:
                        return False
                return True
            except KeyError:
                return False
        else:
            return False
