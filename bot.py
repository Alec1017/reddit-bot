import praw
import time
import random
from facts import RANDOM_FACTS

num_of_comments = 50
num_of_iterations = 10

"""
replies to reddit comments about salad dressings
"""

# looking for the words/phrases about salad dressings
words_to_match = ['vinaigrette',  'vinaigrettes', 'salad dressings', 'salad dressing',
                  'dressing', 'dressings', 'salad-dressing', 'salad-dressings', 'salad',
                  'lettuce']

def load_black_list(filename):
    """
    filename: string pointing to the file that holds all of the previous
    posts that have been replied to separated by newlines

    returns a list of all the previous posts

    raises IOError if file cannot be opened
    """
    with open(filename, 'r') as f:
        black_list = [line.rstrip() for line in f]
    return black_list

def append_to_black_list(path, id):
    """
    path: string path to black_list file

    id: id to black_list

    raises IOError if file cannot be appended to
    """
    with open(path, 'a') as f:
        f.write(id + '\n')

def run_bot(black_list_path):

    # load the id black_list
    black_list = load_black_list(black_list_path)

    print("Logging in...")
    # create the reddit object
    # reddit sees who accesses this info so be descriptive
    r = praw.Reddit(client_id='xxxxxxxxxxxxxx',
                    client_secret='xxxxxxxxxxxxxxxxxxxxx',
                    password='password',
                    user_agent="bot that does blah blah blah",
                    username='username')

    flag = False
    print("Grabbing subreddit...")
    # find the subreddit that you want to scan
    subreddit = r.subreddit("salads")
    print("Grabbing comments...")
    # pull out comments from the subreddit, pulling 25 comments at a time
    comments = subreddit.comments(limit=num_of_comments)

    # list of comment objects in comments
    for comment in comments:
        # get the text in the comment and convert it all to lowercase
        comment_text = comment.body.lower()
        # any of the words in comment_text match any of the words in words_to_match?
        is_match = any(string in comment_text for string in words_to_match)

        # if comment is not in the black_list and it's a match
        if comment.id not in black_list and is_match and not flag:
            print("Match found! Comment ID: " + comment.id)
            # each comment has its own id, append the id to the black_list
            black_list.append(comment.id)

            # place the comment id into the black_list file
            append_to_black_list(comment.id)

            # reply to the comment with a random fact
            comment.reply("A fact about salad dressings: " + random.choice(RANDOM_FACTS))
            print("Reply successful!")
            flag = True


    print("Comment loop finished.")

if __name__ == '__main__':

    BLACK_LIST_PATH = 'black_list.txt'

    # run the bot a specified amount of times
    for i in range(0, num_of_iterations - 1):
        run_bot(BLACK_LIST_PATH)
        time.sleep(5)
