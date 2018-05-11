# coding=utf-8
from collections import Counter
from math import fabs
from re import split as regex_split, sub as regex_sub, UNICODE as REGEX_UNICODE

stopWords = set([
    "-", " ", ",", ".", "a", "e", "i", "o", "u", "t", "about", "above",
    "above", "across", "after", "afterwards", "again", "against", "all",
    "almost", "alone", "along", "already", "also", "although", "always",
    "am", "among", "amongst", "amoungst", "amount", "an", "and",
    "another", "any", "anyhow", "anyone", "anything", "anyway",
    "anywhere", "are", "around", "as", "at", "back", "be", "became",
    "because", "become", "becomes", "becoming", "been", "before",
    "beforehand", "behind", "being", "below", "beside", "besides",
    "between", "beyond", "both", "bottom", "but", "by", "call", "can",
    "cannot", "can't", "co", "con", "could", "couldn't", "de",
    "describe", "detail", "did", "do", "done", "down", "due", "during",
    "each", "eg", "eight", "either", "eleven", "else", "elsewhere",
    "empty", "enough", "etc", "even", "ever", "every", "everyone",
    "everything", "everywhere", "except", "few", "fifteen", "fifty",
    "fill", "find", "fire", "first", "five", "for", "former",
    "formerly", "forty", "found", "four", "from", "front", "full",
    "further", "get", "give", "go", "got", "had", "has", "hasnt",
    "have", "he", "hence", "her", "here", "hereafter", "hereby",
    "herein", "hereupon", "hers", "herself", "him", "himself", "his",
    "how", "however", "hundred", "i", "ie", "if", "in", "inc", "indeed",
    "into", "is", "it", "its", "it's", "itself", "just", "keep", "last",
    "latter", "latterly", "least", "less", "like", "ltd", "made", "make",
    "many", "may", "me", "meanwhile", "might", "mill", "mine", "more",
    "moreover", "most", "mostly", "move", "much", "must", "my", "myself",
    "name", "namely", "neither", "never", "nevertheless", "new", "next",
    "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing",
    "now", "nowhere", "of", "off", "often", "on", "once", "one", "only",
    "onto", "or", "other", "others", "otherwise", "our", "ours",
    "ourselves", "out", "over", "own", "part", "people", "per",
    "perhaps", "please", "put", "rather", "re", "said", "same", "see",
    "seem", "seemed", "seeming", "seems", "several", "she", "should",
    "show", "side", "since", "sincere", "six", "sixty", "so", "some",
    "somehow", "someone", "something", "sometime", "sometimes",
    "somewhere", "still", "such", "take", "ten", "than", "that", "the",
    "their", "them", "themselves", "then", "thence", "there",
    "thereafter", "thereby", "therefore", "therein", "thereupon",
    "these", "they", "thickv", "thin", "third", "this", "those",
    "though", "three", "through", "throughout", "thru", "thus", "to",
    "together", "too", "top", "toward", "towards", "twelve", "twenty",
    "two", "un", "under", "until", "up", "upon", "us", "use", "very",
    "via", "want", "was", "we", "well", "were", "what", "whatever",
    "when", "whence", "whenever", "where", "whereafter", "whereas",
    "whereby", "wherein", "whereupon", "wherever", "whether", "which",
    "while", "whither", "who", "whoever", "whole", "whom", "whose",
    "why", "will", "with", "within", "without", "would", "yet", "you",
    "your", "yours", "yourself", "yourselves", "the", "reuters", "news",
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday",
    "sunday", "mon", "tue", "wed", "thu", "fri", "sat", "sun",
    "rappler", "rapplercom", "inquirer", "yahoo", "home", "sports",
    "1", "10", "2012", "sa", "says", "tweet", "pm", "home", "homepage",
    "sports", "section", "newsinfo", "stories", "story", "photo",
    "2013", "na", "ng", "ang", "year", "years", "percent", "ko", "ako",
    "yung", "yun", "2", "3", "4", "5", "6", "7", "8", "9", "0", "time",
    "january", "february", "march", "april", "may", "june", "july",
    "august", "september", "october", "november", "december",
    "government", "police"
])
ideal = 20.0

class Summarizer():
    def __init__(self, url=None, title=None, text=None):
        self.url = url
        self.title = title
        self.text = text

        self.article = None

        self.summaries = []
        self.score = None

    def summarize_article(self):
        if self.url:
            self.summarize_url()
        elif self.title and self.text:
            self.summarize_text()
        else:
            print("Summaries could not be created!")
            return None

        return self.get_raw_summary()

    def get_raw_summary(self):
        return self.summaries

    def get_formatted_summary(self):
        return self.summaries.join("")

    def summarize_url(self):
        try:
            self.grab_link()
        except IOError:
            print('IOError')
            return None

        if not (self.article and self.article.cleaned_text and self.article.title):
            return None
        
        self.title = self.article.title
        self.text = self.article.cleaned_text

        self.summaries = self.summarize_text()

    def summarize_text(self):
        parser = Input_Parser(self.title, self.text)

        scores = Scorer(parser)
        #score setences, and use the top 5 sentences
        self.score = scores.score()
        ranks = self.score.most_common(5)
        for rank in ranks:
            self.summaries.append(rank[0])    

    def grab_link(self):
        #extract article information using Python Goose
        from goose3 import Goose
        try:
            self.article = Goose().extract(self.url)
        except ValueError:
            print('Goose failed to extract article from url')

class Input_Parser():
    def __init__(self, title, text):
        self.title  = title
        self.text   = text

        self.words          = self.split_words(self.text)
        self.sentences      = self.split_sentences(self.text)
        self.keywords       = self.get_keywords(self.words)
        self.title_words    = self.split_words(self.title)

    def split_words(self, text):
        #split a string into array of words
        try:
            text = regex_sub(r'[^\w ]', '', text, flags=REGEX_UNICODE)  # strip special chars
            return [x.strip('.').lower() for x in text.split()]
        except TypeError:
            print("Error while splitting characters")
            return None

    def get_keywords(self, text):
        """get the top 10 keywords and their frequency scores
        ignores blacklisted words in stopWords,
        counts the number of occurrences of each word
        """
        numWords = len(text)  # of words before removing blacklist words
        freq = Counter(x for x in text if x not in stopWords)

        minSize = min(10, len(freq))  # get first 10
        keywords = {x: y for x, y in freq.most_common(minSize)}  # recreate a dict

        for k in keywords:
            articleScore = keywords[k]*1.0 / numWords
            keywords[k] = articleScore * 1.5 + 1

        return keywords

    def split_sentences(self, text):
        '''
        The regular expression matches all sentence ending punctuation and splits the string at those points.
        At this point in the code, the list looks like this ["Hello, world", "!" ... ]. The punctuation and all quotation marks
        are separated from the actual text. The first s_iter line turns each group of two items in the list into a tuple,
        excluding the last item in the list (the last item in the list does not need to have this performed on it). Then,
        the second s_iter line combines each tuple in the list into a single item and removes any whitespace at the beginning
        of the line. Now, the s_iter list is formatted correctly but it is missing the last item of the sentences list. The
        second to last line adds this item to the s_iter list and the last line returns the full list.
        '''
        
        sentences = regex_split(r'(?<![A-ZА-ЯЁ])([.!?]"?)(?=\s+\"?[A-ZА-ЯЁ])', text, flags=REGEX_UNICODE)
        s_iter = zip(*[iter(sentences[:-1])] * 2)
        s_iter = [''.join(map(str,y)).lstrip() for y in s_iter]
        s_iter.append(sentences[-1])
        return s_iter

class Scorer():
    def __init__(self, parser):
        self.parser = parser

    def score(self):
        #score sentences based on different features

        senSize = len(self.parser.sentences)
        ranks = Counter()
        for i, s in enumerate(self.parser.sentences):
            sentence = self.parser.split_words(s)
            titleFeature = self.title_score(sentence)
            sentenceLength = self.length_score(sentence)
            sentencePosition = self.sentence_position(i+1, senSize)
            sbsFeature = self.sbs(sentence)
            dbsFeature = self.dbs(sentence)
            frequency = (sbsFeature + dbsFeature) / 2.0 * 10.0

            #weighted average of scores from four categories
            totalScore = (titleFeature*1.5 + frequency*2.0 +
                        sentenceLength*1.0 + sentencePosition*1.0) / 4.0
            ranks[s] = totalScore
        return ranks

    def sbs(self, sentence):
        score = 0.0
        if len(sentence) == 0:
            return 0
        for word in sentence:
            if word in self.parser.keywords:
                score += self.parser.keywords[word]
        return (1.0 / fabs(len(sentence)) * score)/10.0


    def dbs(self, sentence):
        if (len(sentence) == 0):
            return 0

        summ = 0
        first = []
        second = []

        for i, word in enumerate(sentence):
            if word in self.parser.keywords:
                score = self.parser.keywords[word]
                if first == []:
                    first = [i, score]
                else:
                    second = first
                    first = [i, score]
                    dif = first[0] - second[0]
                    summ += (first[1]*second[1]) / (dif ** 2)

        # number of intersections
        k = len(set(self.parser.keywords.keys()).intersection(set(sentence))) + 1
        return (1/(k*(k+1.0))*summ)

    def length_score(self, sentence):
        return 1 - fabs(ideal - len(sentence)) / ideal


    def title_score(self, sentence):
        title = [x for x in self.parser.title_words if x not in stopWords]
        count = 0.0
        for word in sentence:
            if (word not in stopWords and word in title):
                count += 1.0
                
        if len(title) == 0:
            return 0.0
            
        return count/len(title)


    def sentence_position(self, i, size):
        """different sentence positions indicate different
        probability of being an important sentence"""

        normalized = i*1.0 / size
        if normalized < 0:
            return 0
        elif normalized <= 0.1:
            return 0.17
        elif normalized <= 0.2:
            return 0.23
        elif normalized <= 0.3:
            return 0.14
        elif normalized <= 0.4:
            return 0.08
        elif normalized <= 0.5:
            return 0.05
        elif normalized <= 0.6:
            return 0.04
        elif normalized <= 0.7:
            return 0.06
        elif normalized <= 0.8:
            return 0.04
        elif normalized <= 0.9:
            return 0.04
        elif normalized <= 1.0:
            return 0.15
        else:
            return 0
