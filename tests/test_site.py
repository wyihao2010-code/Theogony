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
    def test_portal_links_to_mortals(self):
        self.assertIn('./mortals.html', links('index.html'))
        self.assertTrue((ROOT / 'mortals.html').is_file())

    def test_existing_genealogies_link_to_mortals(self):
        for page in ('gods.html', 'heroes.html'):
            with self.subTest(page=page):
                self.assertIn('./mortals.html', links(page))

    def test_mortals_links_to_the_other_pages(self):
        self.assertTrue((ROOT / 'mortals.html').is_file())
        for href in ('./index.html', './gods.html', './heroes.html',
                     'https://wyihao2010-code.github.io/portfolio/'):
            with self.subTest(href=href):
                self.assertIn(href, links('mortals.html'))

    def test_mortals_has_expandable_source_notes(self):
        class Notes(HTMLParser):
            def __init__(self):
                super().__init__()
                self.found = False

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if tag == 'div' and attrs.get('id') == 'footNoteFull':
                    self.found = 'foot-note-full' in attrs.get('class', '').split()

        notes = Notes()
        notes.feed((ROOT / 'mortals.html').read_text(encoding='utf-8'))
        self.assertTrue(notes.found)

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
