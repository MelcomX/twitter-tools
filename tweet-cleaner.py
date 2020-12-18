# Based on: https://pushpullfork.com/i-deleted-tweets/
# Based on: https://github.com/FJSF/TwitterCleaner/blob/master/purge_twitter.py
import config

import tweepy
import csv
import sys
import time
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_key, config.access_secret)
global api
api = tweepy.API(auth)
# Code from: https://stackoverflow.com/a/3041990/6704070
def query_yes_no(question, default="false"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
def delete_all_likes():
    delete_some_likes(False)

def delete_some_likes(some=True):
    print("\nDeleting choosen likes\n")

    # Get user detail
    me = api.me()

    print('Likes Count: ', me.favourites_count)

    # counter
    unliked = 0
    seen = 0
    index =0
    start = int(input("Please enter a starting number"))
    likes = tweepy.Cursor(api.favorites).items()
    # Start unliking
    try:
        for like in likes:
             if index < start:
                 print("start" + str(start) + " index: " + str(index))
                 index += 1
                 continue
             seen += 1
             index += 1
             if (query_yes_no("Delete the folowing like of the tweet: " + like.text, "no")) or (not some):
                 print("now deleting the like")
                 api.destroy_favorite(like.id)
                 unliked += 1


    finally:
        print("ups")
    print(unliked, "/", me.favourites_count, " tweets unliked")
    bye()



def oauth_login(consumer_key, consumer_secret):
    """Authenticate with twitter using OAuth"""
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth_url = auth.get_authorization_url()
    verify_code = raw_input("Authenticate at %s and then enter you verification code here > " % auth_url)
    auth.get_access_token(verify_code)
    return tweepy.API(auth)

def delete_all_direct_messages():
    # Retrive DMs to collect IDs
    dms = api.direct_messages()

    # Start Deleting
    for dm in dms.ids():
        api.destroy_direct_message(dm)

    bye()

def delete_some_tweets():
    deleted = 0
    seen = 0
    timeline = tweepy.Cursor(api.user_timeline).items()
    start = int(input("Please enter a starting number"))
    index = 0
    try:
        for tweet in timeline:
            if(index < start):
                index += 1
                continue
            seen += 1
            index += 1
            if query_yes_no("Delete the following tweet: "+ tweet.text + "\n" + "Created at: " + str(tweet.created_at), "no"):
                print("now deleting the tweet")
                api.destroy_status(tweet.id)
                deleted += 1
                time.sleep(1)
    finally:
        print("You've just seen  " + str(seen) + " tweets from yourself an you deleted " + str(deleted) + " tweets")
        print("You're now at index " + str(index) + "(We started counting before you deleted")
        sys.exit(0)
        print("You've just seen  " + str(seen) + " tweets from yourself an you deleted " + str(deleted) + " tweets")
        print("You're now at index " + str(index) + "(We started counting before you deleted")
        bye()

def delete_all_retweets():
    deleted = 0
    seen = 0
    timeline = tweepy.Cursor(api.user_timeline).items()
    start = int(input("Please enter a starting number"))
    index = 0
    try:
        for tweet in timeline:
            t =tweet.text
            if t.startswith("RT @"):
                api.destroy_status(tweet.id)
                deleted +=1
    finally:
        print(str(deleted) +" RT deleted")
    bye()

def bye():
    print("\nHave a nice day!\n")
    sys.exit(0)

def menu():
    print('''
1. Delete all tweets.
2. Delete all likes
3. Delete all DMs.
4. Choose and delete tweets. 
5. Chose and delete likes
6. Delete all Retweets
7. Exit.''')


def delete_all_tweets():
    deleted = 0
    timeline = tweepy.Cursor(api.user_timeline).items()
    for tweet in timeline:
        api.destroy_status(tweet.id)
        deleted += 1
        sleep(0.2)
    print("We deleted "+ str(deleted) + "Tweets")
    bye()


menu()
options = {
        '1': delete_all_tweets,
        '2': delete_all_likes,
        '3': delete_all_direct_messages,
        '4': delete_some_tweets,
        '5': delete_some_likes,
        '6': delete_all_retweets,
        '7': bye
}
choice = input('\nChoice: ')
options[choice]()



