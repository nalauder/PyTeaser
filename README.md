PyTeaser
========

PyTeaser takes any news article and extract a brief summary from it. It's based on the original [Scala](https://github.com/MojoJolo/textteaser) project.


Summaries are created by ranking sentences in a news article according to how relevant they are to the entire text. The top 5 sentences are used to form a "summary". Each sentence is ranked by using four criteria:

- Relevance to the title
- Relevance to keywords in the article
- Position of the sentence
- Length of the sentence


# Running

For an easy run and installation process use the run file
`./run'

This will complete the installation and run the tests file

# Installation:
Requires Python 3. 

`python setup.py install --user`

These dependency packages will be automatically installed:
```
Pillow
lxml
cssselect
jieba
beautifulsoup
goose3
```

# Run Existing Tests

`python test.py`

# Usage:
## sample command:
`python sample.py`
or
```Python
>>> from pyteaser import Summarizer
>>> url = 'https://www.stuff.co.nz/world/americas/103853951/americas-nuclear-mountain-the-most-secure-facility-in-the-world'
>>> summaries = Summarizer(url=url)
>>> print(summaries.summarize_article())

```

## output
```
['\n\nThe operation has always been run out of Ent or Peterson Air Force Base in Colorado Springs, never Cheyenne Mountain, said Laslie.', 'Rose, the base deputy director, rejected the notion that Cheyenne Mountain is a relic.', 'Asked whether Cheyenne Mountain is vulnerable to more powerful modern nuclear warheads, Rose answered indirectly: "I don\'t think we would be open if it was".\n\n2.', 'To mark the occasion, Norad offered a tour of Cheyenne Mountain on Thursday.', '"We like to say it\'s the most secure facility in the world," said Steve Rose, deputy director of the base.']
```
