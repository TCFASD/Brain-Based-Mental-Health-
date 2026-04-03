import re
from html.parser import HTMLParser
from html import unescape

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_script = False
        self.in_style = False
        self.title = ""
        self.headings = []
        self.paragraphs = []
        self.list_items = []
        self.links = []
        self.current_text = []
        self.current_heading_level = None
        
    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            self.in_script = True
        elif tag == 'style':
            self.in_style = True
        elif tag == 'title':
            pass  # Will handle with data
        elif tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.current_heading_level = tag
        elif tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    self.current_text.append(('LINK_START', value))
                    break
    
    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_script = False
        elif tag == 'style':
            self.in_style = False
        elif tag == 'title':
            pass
        elif tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            text = ''.join([t for t in self.current_text if t != ('LINK_START', None)]).strip()
            if text:
                self.headings.append((tag, text))
            self.current_text = []
            self.current_heading_level = None
        elif tag == 'p':
            text = ''.join([t[1] if isinstance(t, tuple) else t for t in self.current_text]).strip()
            if text and len(text) > 5:
                self.paragraphs.append(text)
            self.current_text = []
        elif tag == 'li':
            text = ''.join([t[1] if isinstance(t, tuple) else t for t in self.current_text]).strip()
            if text:
                self.list_items.append(text)
            self.current_text = []
        elif tag == 'a':
            # Finalize link
            text = ''.join([t for t in self.current_text if not isinstance(t, tuple)])
            if self.current_text and isinstance(self.current_text[0], tuple) and self.current_text[0][0] == 'LINK_START':
                url = self.current_text[0][1]
                self.links.append((url, text.strip()))
            self.current_text = []

    def handle_data(self, data):
        if not self.in_script and not self.in_style:
            text = data.strip()
            if text:
                if isinstance(self.current_text, list) and self.current_text and isinstance(self.current_text[0], tuple):
                    self.current_text.append(text)
                else:
                    self.current_text.append(text)

def extract_full(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    parser = TextExtractor()
    try:
        parser.feed(content)
    except:
        pass
    
    return parser

files = [
    ('raw-html/caregivers.html', 'CAREGIVERS'),
    ('raw-html/self-advocates.html', 'SELF-ADVOCATES'),
    ('raw-html/organizations.html', 'ORGANIZATIONS'),
    ('raw-html/resources.html', 'RESOURCES'),
]

for filepath, name in files:
    try:
        parser = extract_full(filepath)
        
        print(f"\n{'='*80}\n{name}\n{'='*80}\n")
        
        # Get headings
        if parser.headings:
            print("KEY HEADINGS:")
            for level, heading in parser.headings:
                indent = "  " * (int(level[1]) - 1)
                print(f"{indent}• {unescape(heading)}")
        
        # Get first few paragraphs
        if parser.paragraphs:
            print("\nCONTENT (First 5 paragraphs):")
            for para in parser.paragraphs[:5]:
                cleaned = unescape(para)
                if len(cleaned) > 150:
                    print(f"  {cleaned[:150]}...")
                else:
                    print(f"  {cleaned}")
        
        # Get list items
        if parser.list_items:
            print("\nKEY LIST ITEMS:")
            for item in parser.list_items[:10]:
                print(f"  • {unescape(item)}")
        
        # Get links
        if parser.links:
            external_links = [(url, text) for url, text in parser.links if 'http' in url or 'www' in url]
            if external_links:
                print("\nEXTERNAL LINKS:")
                for url, text in external_links[:8]:
                    print(f"  [{unescape(text)}]({url})")
                    
    except Exception as e:
        print(f"Error with {filepath}: {e}")

