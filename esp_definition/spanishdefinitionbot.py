import os
import re
import pdb
import praw
import requests
import bs4
from bs4 import BeautifulSoup

######################################################
#                                                    #
#             SpanishDefinitionBot V0.1              #
#----------------------------------------------------#
#                                                    #
#   Automatically replies to posts on the given      #
# subreddits with a Spanish/English definition of    #
#     the requested English/Spanish word.            #
#                                                    #
######################################################


######################################################

# Params

debug = 1
lim = 10 # Depth limit for subreddit posts
subreddit_list = ["Spanish",
                  "learnspanish",
                  "spanishhelp",
                  "AP_Spanish",
                  "APSpanish",
                  "BeginnerSpanish",
                  "LANL_Spanish"
                  ]

# TODO: multi word phrases unquoted

test_cases = [#u'Interest in a "short story a week" in Spanish?',
             #u'"Dale candela"',
             u"Help with 'se' before a verb?"#,
             #u"What is olvido? I forgot",
             #u'"saving"',
             #u'¿Por qué está usado la palabra "tocar" asi?',
             #u'What is the slang for "dude" in your Spanish speaking country?'
             ]

######################################################

# Define functions

def grab_word(text):
    """Grabs word(s) to be defined from title."""
    text = text.lower()
    text = text.replace('?','').replace(',','').replace('.','').replace("what's", "what is")
    words = text.strip().split()
    if '"' in text:
        matches=re.findall(r'\"(.+?)\"',text)
        return list(match.strip('\"') for match in matches)
    elif " '" in text or "' " in text:
        matches=re.findall(r"\'(.+?)\'",text)
        return list(match.strip("\'") for match in matches)
    elif "meaning of" in text:
        for i, word in enumerate(words):
            if words[i-1] == "of" and words[i-2] == "meaning":
                return [word]
    elif "means" in text:
        for i, word in enumerate(words):
            if words[i+1] == "means":
                return [word]
    elif "mean" in text:
        for i, word in enumerate(words):
            if words[i+1] == "mean":
                return [word]
    elif "what does" in text:
        for i, word in enumerate(words):
            if words[i-1] == "does" and words[i-2] == "what":
                return [word]
    elif "what is a " in text or "what is an " in text:
        for i, word in enumerate(words):
            if words[i-1] in ("a", "an") and words[i-2] == "is" and words[i-3] == "what":
                return [word]
    elif "what is" in text:
        for i, word in enumerate(words):
            if words[i-1] == "is" and words[i-2] == "what":
                return [word]
    else:
        return False

  
def grab_definition(word):
    """Grabs definition from SpanishDict.com"""
    
    page = requests.get(u"http://www.spanishdict.com/translate/{}".format(word.strip().replace(' ', '%20')))
    soup = BeautifulSoup(page.content, 'html.parser')
    
    try:
        condensed_soup = soup.find_all(class_="dictionary-entry dictionary-neodict")
        quickdefs  = soup.find_all(class_="quickdef")
        results = [c.find_all(True, {'class':['dictionary-neodict-entry-title',
                                              'part_of_speech',
                                              'dictionary-neodict-translation',
                                              'dictionary-neodict-example',
                                              'exB',
                                              'context']}) for c in condensed_soup]
        
        results2 = [q.find_all(True, {'class':['source-text', 'el']}) for q in quickdefs]
        results_temp = []
        
        for result in results:
            result_temp = []
            for item in result:
                if item['class'][-1] == "context" and item.parent['class'][-1] != "dictionary-neodict-indent-1":
                    pass
                else:
                    result_temp.append(item)
            results_temp.append(result_temp)
        results = results_temp

        return results, results2
    except:
        print("Page Status Code: " + str(page.status_code))
        return False

def prettify_definition(results):
    """Returns definition in a reddit formatted string."""
    definitions = []
    for result in results:
        definition = u''
        for item in result:
            if item['class'][-1] == "dictionary-neodict-entry-title":
                definition += u'\n\n----------\n\n###'
                definition += item.get_text()
                definition += u'\n\n'
            elif item['class'][-1] == "part_of_speech":
                try:
                    pos_link = item['href']
                except:    # In case there is no hyperlink
                    pos_link = u'https://www.spanishdict.com'
                try:
                    pos_title = item['title'].replace(")","\)")
                except:
                    pos_title = u'?'
                definition += u'[^(**'
                definition += item.get_text().upper()
                definition += u'**)]({} "{}")\n\n'.format(pos_link, pos_title)
            elif item['class'][-1] == "context":
                definition += u'1. {}\n\n'.format(item.get_text())
            elif item['class'][-1] == "dictionary-neodict-translation":
                definition += u' **'
                definition += item.get_text().replace('(', '**(').replace(')', ')**')
                definition += u'**'
            elif item['class'][-1] == "dictionary-neodict-example":
                definition += u'\n >*'
                definition += item.get_text()
            elif item['class'][-1] == "exB":
                definition = definition.replace(item.get_text(), '* - ' + item.get_text())
                definition = definition.replace(' * - ','* - ')
                definition += u'\n\n'
        definitions.append(definition)
    return definitions

def prettify_quickdef(quickdefs):
    results = []
    for quickdef in quickdefs:
        text = u''
        i=0
        for item in quickdef:
            if item['class'][-1] == "source-text":
                text += u"\n\n-------------\n\n"
                if i == 1:
                    text += u"\n\n&nbsp;\n\n\n&nbsp;\n\n"
                text += u'#[{}](http://www.spanishdict.com/translate/{})'.format(item.get_text(), item.get_text())
                # Spacer for second definition eng-esp if exists
                i += 1
            elif item['class'][-1] == "el":
                text += u"\n\n##*{}*".format(item.get_text())
                text += u"\n\n"
        results.append(text)
    return results

def format_reply(quickdefs, definitions):
    """Returns definition in a Reddit formatted comment."""
    reply = u''
    for quickdef, definition in zip(quickdefs, definitions):
        part4 = u"^[SpanishDefinitionBot](https://www.reddit.com/user/SpanishDefinitionBot) ^v0.1 ^| "
        part5 = u"^Definitions ^provided ^by ^[SpanishDict](http://www.spanishdict.com)"
        divider = u"\n\n-------------\n\n"
        #ender = u"^| ^Maintained ^by ^/u/tjfuke"
        reply += u''.join((quickdef,definition,divider,part4,part5,divider))
    reply += divider
    return reply


######################################################


if __name__ == "__main__":

# Create the Reddit instance

    reddit = praw.Reddit('bot1')

# Prep
    if not os.path.isfile("posts_replied_to.txt"):
        posts_replied_to = []
    else:
        with open("posts_replied_to.txt", "r") as f:
            posts_replied_to = f.read()
            posts_replied_to = posts_replied_to.split("\n")
            posts_replied_to = list(filter(None, posts_replied_to))

    ### REMOVE    
    #subreddit = reddit.subreddit("pythonforengineers")

# Post to Reddit

    if debug == 1:
        for sr in subreddit_list:
            subreddit = reddit.subreddit(sr)
            for submission in subreddit.hot(limit=lim):
            #for submission in test_cases:
                try:
                    #words = grab_word(submission)
                    words = grab_word(submission.title)
                    for word in words:
                        definition, quickdef = grab_definition(word)
                        if definition == False:
                            print("ERROR: Could not obtain definition.")
                        else:
                            pretty_definition = prettify_definition(definition)
                            pretty_quickdef = prettify_quickdef(quickdef)
                            if len(words) > 0:
                                print(format_reply(pretty_quickdef, pretty_definition))
                except:
                   print("No useable submissions found.")

    elif debug == 0:
        for sr in subreddit_list:
            subreddit = reddit.subreddit(sr)
            for submission in subreddit.hot(limit=lim):
                if submission.id not in posts_replied_to:
                    try:
                        words = grab_word(submission.title)
                        for word in words:
                            definition, quickdef = grab_definition(word)
                            if definition == False:
                                print("ERROR: Could not obtain definition.")
                            else:
                                pretty_definition = prettify_definition(definition)
                                pretty_quickdef = prettify_quickdef(quickdef)
                                if len(words) > 0:
                                    submission.reply(format_reply(pretty_quickdef, pretty_definition))
                                    print("Bot replying to : {}", submission.title)
                                    posts_replied_to.append(submission.id)
                    except:
                      print("No useable submissions found.")
    else:
        print("ERROR: Debug parameter badly set.")


######################################################

#Housecleaning

    with open("posts_replied_to.txt", "w") as f:
        for post_id in posts_replied_to:
            f.write(post_id + "\n")
