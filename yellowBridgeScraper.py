"""This script is for use in conjunction with the Anki Chinese Support Redux Add-on found here https://github.com/luoliyan/chinese-support-redux
It takes a single chinese character as input and returns the first entry in the "common words with this character" table from yellowbridge.com.
I plan to use this to auto fill examples into single-character flashcards."""

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import urllib.parse

from .hanzi import has_hanzi
from .util import cleanup, no_color
from .sound import no_sound

def buildUrl(hanzi):
    url_gtts = 'https://www.yellowbridge.com/chinese/charsearch.php'
    # Parse character into UTF-8
    query = urllib.parse.quote(hanzi)
    # Create URL
    return url_gtts + "?zi=" + query

def scraper(hanzi):
    # Cleanup hanzi
    from .ruby import ruby_bottom, has_ruby
    if not has_hanzi(hanzi):
        return ''
    if has_ruby(hanzi):
        hanzi = ruby_bottom(hanzi)
    hanzi = cleanup(no_color(no_sound(hanzi)))

    if not hanzi:
        return ''
    if len(hanzi) != 1:
        # raise Exception('You must input a single hanzi')
        return''

    url = buildUrl(hanzi)

    # Read page into bs4 object
    req = Request(url, headers={
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    })
    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')

    # Isolate first row of common words table
    common_words = soup.find('table', attrs={'id': 'commonWords'})
    first_row = common_words.findChildren(['tr'])[0]

    # Pull string data from first row
    characters = first_row.find("a", attrs={"class": "zh"}).string
    pronounce = first_row.find("span", attrs={"class": "phonetic pronouncer0"}).string
    definition = first_row.findAll("a", attrs={"class": "definition"})
    definition_strings = []
    for i in definition:
        value = i.string
        definition_strings.append(value)

    return(characters + " &nbsp; &nbsp; &nbsp; &nbsp;" + pronounce + "&nbsp;<div>" + ', '.join(definition_strings) + "</div>")