import praw
import random
from dotenv import load_dotenv
import os
import re

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

# For test subreddit
# subreddit = reddit.subreddit('test')

# For MemePiece + test
subreddit = reddit.subreddit('MemePiece+test')

triggers = ['money', 'gold', 'treasure', 'berries', 'tangerine']
replies = ["Give me your {}!!!", "I love {}!!!", "Did you say {}?!! Can I have it?", "{} sounds good, let me have it!"]

special_triggers = {
    r'\bmap\b': ['I will map out the entire world.', "My dream is to make a map of the whole world!"],
    r'na+mi[-|~|\s]s+w+a+n+': ['Ewww hentai! 😒', "That'll be 10,000,000 berries! 😏", "Kyaaaaaa~~hhhh 😨", "You can have a look for some berries 😉", "👊 If you think I'm just another cute girl, you're dead wrong!"],
    r'bellemere': ["Don't touch Bellemere-san's tangerines with your dirty hands."],
    r'navigator': ["I'm the best navigator around here!"],
    r'\boranges?\b': ["Tangerines are tastier!"],
}

for comment in subreddit.stream.comments(skip_existing=True):
    if comment.author != 'NamiWantsMoney' and comment.is_root:
        for k, v in special_triggers.items():
            comment_ = comment.body.lower().replace("\\", '')
            if re.search(k, comment_, re.IGNORECASE):
                reply = random.choice(v)
                comment.reply(reply)
                print(f"[{comment.subreddit.display_name}] - {comment.author} said '{comment.body}' -> {reply}")
                break
        else:
            trigger_match = [x.upper() for x in triggers if x in comment.body.lower()]
            if trigger_match:
                i = ' & '.join([', '.join(trigger_match[:-1]), trigger_match[-1]]) if len(trigger_match) > 1 else trigger_match[0]
                reply = random.choice(replies).format(i)
                comment.reply(reply)
                print(f"[{comment.subreddit.display_name}] - {comment.author} said '{comment.body}' -> {reply}")
