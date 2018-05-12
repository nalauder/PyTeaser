from pyteaser import Summarizer
url = 'https://www.stuff.co.nz/world/americas/103853951/americas-nuclear-mountain-the-most-secure-facility-in-the-world'
summaries = Summarizer(url=url)
print(summaries.summarize_article())
