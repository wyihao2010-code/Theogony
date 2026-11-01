from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.links.append(dict(attrs).get('href'))

def links(file):
    parser = Links()
    parser.feed((ROOT / file).read_text(encoding='utf-8'))
    return parser.links

class SiteTest(unittest.TestCase):
    def test_portal_links_to_both_genealogies(self):
        self.assertIn('./gods.html', links('index.html'))
        self.assertIn('./heroes.html', links('index.html'))
        for page in ('gods.html', 'heroes.html'):
            self.assertTrue((ROOT / page).is_file())
    def test_every_page_links_back_to_portfolio(self):
        for page in ('index.html', 'gods.html', 'heroes.html'):
            self.assertIn('https://wyihao2010-code.github.io/portfolio/', links(page), page)

    def test_genealogies_link_to_portal_and_each_other(self):
        self.assertIn('./index.html', links('gods.html'))
        self.assertIn('./heroes.html', links('gods.html'))
        self.assertIn('./index.html', links('heroes.html'))
        self.assertIn('./gods.html', links('heroes.html'))

if __name__ == '__main__':
    unittest.main()
