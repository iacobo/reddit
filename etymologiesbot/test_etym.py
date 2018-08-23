from postFormattingFunctions import grab_word, grab_translation, grab_etymology

#cd into directory and run "pytest"

def test_grab_word():
    """Tests that program accurately pulls words from titles"""
    assert grab_word("hello") == ["hello"]
    assert grab_word("Request: hello") == ["hello"]
    assert grab_word("Request: 'hello'") == ["hello"]
    assert grab_word('Request: "hello"') == ["hello"]
    assert grab_word("Request: etymology of hello") == ["hello"]
    assert grab_word("Request: what does hello mean?") == ["hello"]
    assert grab_word("Request: how do you say hello?") == ["hello"]
    assert grab_word("Request: what's the word for hello?") == ["hello"]
    assert grab_word("Request: what is the word for hello?") == ["hello"]
    assert grab_word("Request: what does the word hello mean?") == ["hello"]
    assert grab_word("Request: what is hello in other languages?") == ["hello"]
    assert grab_word("Request: how to say hello in other languages") == ["hello"]
    
    assert grab_word("Request: umbrella/parasol") == ["umbrella", "parasol"]
    
    assert grab_word("Check out this cool map") == False
    assert grab_word("Nonsense string should return nothing") == False
    
    assert grab_word('Etymology for "dog"?') == ["dog"]
    assert grab_word('Etymology Map [Request] - "Earth"') == ["earth"]
    assert grab_word("(Request) The word strawberry in Europe)") == ["strawberry"]
    assert grab_word("Request: How to say AND in your language?") == ["and"]
    assert grab_word('[Request] "Fog" European and/or Italy map') == ["fog"]
    assert grab_word('[Request] "Election" among the languages of europe.') == ["election"]
    assert grab_word("Request: How do you say breakfast in your language, what does it means?") == ["breakfast"]
    assert grab_word("[REQUEST] Mom/Mommy/.. in indigenous languages of Africa, America, Asia and Oceania") == ["mom", "mommy"]
    assert grab_word("[Request] The maximum limits of a language's native counting system before it has to use a loanword") == False
    #assert grab_word('Request: etymology for "nothing" and "nor"') == ["nothing", "nor"]
    #assert grab_word('Request: "hello/goodbye"') == ["hello", "goodbye"]
    
def test_grab_translation():
    assert grab_translation("hello", "es").lower() == "hola"
    assert grab_translation("hello", "fr").lower() == "bonjour"
    
def test_grab_etymology():
    assert grab_etymology("día", "spanish") == "From Vulgar Latin *dia, from Latin diēs (“day”) (reanalyzed as a 1st declension noun), ultimately from Proto-Indo-European *dyḗws (“heaven, sky”). Akin to Catalan and Portuguese dia, etc. Not related to English day, from Proto-Germanic *dagaz."
    