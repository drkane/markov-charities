import markovify
import gzip
import titlecase
import re
import io

class FileMarkov:
    
    def __init__(self, filename=None, encoding='utf8', state_size=1):
        self.encoding = encoding
        self.state_size = state_size
        if filename is not None:
            if filename[-2:]=="gz":
                self.read_gz( filename )
            else:
                self.read_file( filename )

    def read_file( self, filename ):
        with io.open(filename, 'r', encoding=self.encoding) as f:
            text = f.read()

        # Build the model
        self.model = markovify.NewlineText(text, state_size=self.state_size)

    def read_gz( self, filename ):
        with gzip.open(filename, 'r') as f:
            text = f.read()

        # Build the model
        self.model = markovify.NewlineText(text, state_size=self.state_size)
    
    def get_sentences( self, max_sentences=10 ):
        for i in range(max_sentences):
           yield self.get_sentence()
        
    def get_sentence( self ):
        while True:
            s = self.model.make_sentence()
            if s is not None:
                s = titlecase.titlecase( s, title_exceptions )
                return s
        
    def get_tweet( self ):
        while True:
            s = self.model.make_short_sentence(140)
            if s is not None:
                s = titlecase.titlecase( s, title_exceptions )
                return s


def title_exceptions(word, **kwargs):

    word_test = word.strip("(){}<>.")

    # lowercase words
    if word_test.lower() in ['a', 'an', 'of', 'the', 'is', 'or']:
        return word.lower()
        
    # uppercase words
    if word_test.upper() in ['UK', 'FM', 'YMCA', 'PTA', 'PTFA', 
            'NHS', 'CIO', 'U3A', 'RAF', 'PFA', 'ADHD', 
            'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 
            'AFC', 'CE', 'CIC'
        ]:
        return word.upper()
        
    # words with only vowels that aren't all uppercase
    if word_test.lower() in ['st','mr','mrs','ms','ltd','dr','cwm','clwb','drs']:
        return None
        
    # words with number ordinals
    ord_numbers_re = re.compile("([0-9]+(?:st|nd|rd|th))")
    if bool(ord_numbers_re.search(word_test.lower())):
        return word.lower()
    
    # words with dots/etc in the middle
    for s in [".", "'", ")"]:
        dots = word.split(s)
        if(len(dots)>1):
            # check for possesive apostrophes
            if s=="'" and dots[-1].upper()=="S":
                return s.join( [titlecase.titlecase( i, title_exceptions ) for i in dots[:-1]] + [dots[-1].lower()] )
            # check for you're and other contractions
            if word_test.upper() in ["YOU'RE","DON'T","HAVEN'T"]:
                return s.join( [titlecase.titlecase( i, title_exceptions ) for i in dots[:-1]] + [dots[-1].lower()] )
            return s.join( [titlecase.titlecase( i, title_exceptions ) for i in dots] )
        
    # words with only vowels in (treat as acronyms)
    vowels = re.compile("[AEIOUYaeiouy]")
    if not bool(vowels.search(word_test)):
        return word.upper()
    
    return None