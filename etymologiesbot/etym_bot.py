import os
import io
import praw
import time
import random
from datetime import datetime
from postFormattingFunctions import grab_word, grab_defs, format_footer


######################################################
#                                                    #
#                EtymologiesBot V0.1                 #
#----------------------------------------------------#
#                                                    #
#   Automatically provides etymology of words in     #
#                 given languages                    #
#                                                    #
######################################################


######################################################


###############################################################################
#                                                                             #
#                             ISSUES                                          #
#                                                                             #
### Issue with pip install of wiktionaryparser                                #
#   Main script says                                                          #
#                       'from utils import WordData, Definition, RelatedWord' #
#   ambiguous, leads to error                                                 #
#   should say                                                                #
#      'from wiktionaryparser.utils import WordData, Definition, RelatedWord' #
#                                                                             #
### Glosbe has query limit. Do not abuse their resources.                     #
#                                                                             #
### Cannot query multi-word, unquoted requests                                #
#                                                                             #
### Often no etymology for feminine/plural forms of words.                    #
#                                                                             #
###############################################################################


# Params

debug = 0 # whether uses test cases (1) or hot reddit posts (0)
live = 1 # whether posts to reddit (1) or prints result (0)
lim = 5 # Depth limit for subreddit posts

enc ="utf-8" # Encoding of .txt file containing post ID's already replied to
subreddit_list = ["etymologymaps"]

test_cases = [
              'Request: "pot"'
             ]

def writeToLog(reply, submission, filename="log.txt"):
    with io.open(filename, "a", encoding=enc) as f:
        timestamp = str(datetime.now())
        f.write("\n{}\n{}\n{}\n".format(timestamp, submission, reply))

######################################################


if __name__ == "__main__":

# Create the Reddit instance
    reddit = praw.Reddit('bot1')

# Post to Reddit
    if not debug:
        # Prep
        if not os.path.isfile("posts_replied_to.txt"):
            posts_replied_to = []
        else:
            with io.open("posts_replied_to.txt", "r", encoding=enc) as f:
                posts_replied_to = f.read().split("\n")
        
        for sr in subreddit_list:
            subreddit = reddit.subreddit(sr)
            for submission in subreddit.new(limit=lim): 
                #print(submission.title)
                if "request" in submission.title.lower() and (not live or submission.id not in posts_replied_to):
                    words = grab_word(submission.title)
                    if words:
                        reply = ""
                        for word in words:
                            reply += grab_defs(word)
                        reply = format_footer(reply)
                        if live:
                            submission.reply(reply)
                            writeToLog(reply, submission.title)
                            print(("Bot replying to : {}".format(submission.title)))
                            posts_replied_to.append(submission.id)
                            #Housecleaning
                            with io.open("posts_replied_to.txt", "w", encoding=enc) as f:
                                for post_id in posts_replied_to:
                                    f.write(post_id + "\n")
                            #Avoid reddit post frequency spam filter
                            time.sleep(random.uniform(600,610))
                        elif not live:
                            print(reply)
                            writeToLog(reply, submission.title)
    elif debug:
        for submission in test_cases:
            words = grab_word(submission)
            if words:
                reply = ""
                for word in words:
                    reply += grab_defs(word)
                reply = format_footer(reply)    
                print(reply)
                writeToLog(reply, submission)
    else:
        print("ERROR: Debug parameter badly set.")