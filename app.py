import praw
import random
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.environ.get('client_id')
client_secret = os.environ.get('client_secret')
password = os.environ.get('reddit_pass')
username = os.environ.get('reddit_user')

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    password=password,
    username=username,
    user_agent="<Nami Wants Money 0.1>"
)
subreddit = reddit.subreddit('MemePiece+test')

triggers = ['money', 'gold', 'treasure', 'berries', 'orange', 'tangerine']
replies = ["Give me your {}!!!", "I love {}!!!", "Did you say {}?!! Can I have it?", "{} sounds good, let me have it!"]

for comment in subreddit.stream.comments(skip_existing=True):
    if comment.author != 'NamiWantsMoney':
        trigger_match = [x.upper() for x in triggers if x in comment.body.lower()]
        if trigger_match:
            i = ' & '.join([', '.join(trigger_match[:-1]), trigger_match[-1]]) if len(trigger_match) > 1 else trigger_match[0]
            reply = random.choice(replies).format(i)
            comment.reply(reply)
            print(f"[{comment.subreddit.display_name}] - {comment.author} said '{comment.body}' -> {reply}")
