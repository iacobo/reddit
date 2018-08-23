import re
import json
import urllib.request, urllib.parse, urllib.error
from googletrans import Translator
from wiktionaryparser import WiktionaryParser
from languageCodes import major_langs, minor_langs, mappy, lang_codes, googleSupportedLangs


def code_to_language(code):
    """Returns verbose language name given ISO code."""
    return mappy[code]

def grab_word(text):
    """Grabs word(s) to be defined from title."""
    badchars = '?,.[]:'
    map_table = str.maketrans('', '', badchars)
    text = text.lower()
    text = text.translate(map_table)
    text = text.replace("what's", "what is")
    words = text.strip().split()
    if '"' in text:
        matches=re.findall(r'\"(.+?)\"',text)
        return list(match.strip('\"') for match in matches)
    elif " '" in text or "' " in text:
        matches=re.findall(r"\'(.+?)\'",text)
        return list(match.strip("\'") for match in matches)
    elif "word for" in text:
        i = words.index("for")
    elif "word" in words:
        i = words.index("word")
    elif "mean" in words:
        i = words.index("mean") - 2
    elif "etymology of" in text:
        i = words.index("of")
    elif "how to say" in text or "how do you say" in text:
        i = words.index("say")
    elif "what is" in text:
        i = words.index("is")
    elif "in" in words:
        i = words.index("in") - 2
    elif "request" in text and len(words) == 2:
        i = words.index("request")
    elif len(words) == 1:
        i = -1
    else:
        return False
    result = words[i+1:i+2]
    if "/" in result[0]:
        return result[0].strip("/").split("/")
    else:
        return result

def grab_translation(word, destination, source="en"):
    """Translates given word to destination language."""
    if destination in googleSupportedLangs:
        translator = Translator()
        word_tr = translator.translate(word, src=source, dest=destination)
        return word_tr.text
    else:
        url = "https://glosbe.com/gapi/translate?from=eng&dest={}&format=json&phrase={}&pretty=true".format(destination, word)
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        words_tr = []
        # Pulls meaningful part of json
        if "tuc" in data:
            words_tr = [x["phrase"]["text"] for x in data["tuc"] if "phrase" in x]
        return ", ".join(words_tr)

def grab_etymology(word, language):
    """Grabs etymology from Wiktionary"""
    parser = WiktionaryParser()
    json = parser.fetch(word, language)
    ans = ""
    for element in json:
        if 'etymology' in element:
            if len(ans)>1:
                ans += "; __Etymology 2:__ "
            ans += (element['etymology'].strip("\n"))
    return ans

def grab_defs(word):
    """Workhorse - grabs translations, searches for etymologies. Returns result."""
    ans = []
    for code in lang_codes:
        language = code_to_language(code)
        translated_word = grab_translation(word, code).lower()
                            
        # Try es/fr > xx (for less well documented langs in Google Translate)
        # NOTE: This may not actually be working for some language pairs
        #       since google's algorithm may translate two languages via English
        for new_source in major_langs:
            if translated_word == word and code in minor_langs:
                new_word = grab_translation(word, new_source).lower()
                translated_word = grab_translation(new_word, code, source=new_source).lower()

        etym = ""        
        for temp_word in translated_word.split(", "):
            if not etym:
                # Need to add proper raise exception here
                try:
                    etym = grab_etymology(temp_word, language)
                except:
                    # NEED TO ADD FUNCTIONALITY FOR GENDER NUMBER CONVERSION
                    # IN EVENT THAT CURRENT FORM OF WORD HAS NO ETYM INFO
                    #try:
                    #    sm_word = sing_masc(translated_word, language)
                    #    etym = grab_etymology(sm_word, language)
                    print("\n---\nCOULD NOT GRAB ETYMOLOGY\n{}\n{}\n---\n".format(language, translated_word))
                        
        if translated_word:
            ans.append((translated_word, language, etym))
            
    return format_table(ans, word)


#######################################
# Reddit comment formatting functions #
#######################################

def format_table(ans, word):
    """Returns etymologies in a Reddit formatted comment (table in markdown)."""
    pretty_ans = "###{}\n|Language|Word|Etymology|\n|-|-|-|\n".format(word)
    for entry in ans:
        pretty_ans += "|{}|{}|{}|\n".format(entry[1], entry[0], entry[2])
    pretty_ans += "\n\n-------------\n"
    return pretty_ans

def format_footer(reply):
    """Appends footer to reply."""
    reply += "\n-------------\n\n"
    reply += "^[EtymologiesBot](https://www.reddit.com/user/EtymologiesBot) ^v0.5 ^| "
    reply += "^Etymologies ^provided ^by ^[Wiktionary](http://www.wiktionary.org) ^| "
    reply += "^Translations ^provided ^by ^[GoogleTranslate](https://translate.google.com/) ^and ^[Glosbe](https://glosbe.com)"
    reply += "\n\n-------------\n"
    return reply