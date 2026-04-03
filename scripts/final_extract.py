import re
from html import unescape

def extract_detailed(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Remove scripts and styles
    content = re.sub(r'<script[^>]*>.*?</script>', ' ', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<style[^>]*>.*?</style>', ' ', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<noscript[^>]*>.*?</noscript>', ' ', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Extract title
    title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else "N/A"
    
    # Extract headings
    headings = []
    for match in re.finditer(r'<h[1-6][^>]*>([^<]+(?:<[^>]*>[^<]*)*)</h[1-6]>', content, re.IGNORECASE | re.DOTALL):
        text = re.sub(r'<[^>]+>', '', match.group(1)).strip()
        if text:
            headings.append(text)
    
    # Extract all links
    links = []
    for match in re.finditer(r'<a[^>]*href="([^"]*)"[^>]*>([^<]+(?:<[^>]*>[^<]*)*)</a>', content, re.IGNORECASE | re.DOTALL):
        url = match.group(1).strip()
        text = re.sub(r'<[^>]+>', '', match.group(2)).strip()
        if url and text:
            links.append((url, text))
    
    # Remove tags for full text extraction
    text = re.sub(r'<[^>]+>', ' ', content)
    text = unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return {
        'title': title,
        'full_text': text,
        'headings': headings,
        'links': links
    }

files = [
    ('raw-html/caregivers.html', 'CAREGIVERS'),
    ('raw-html/self-advocates.html', 'SELF-ADVOCATES'),
    ('raw-html/organizations.html', 'ORGANIZATIONS'),
    ('raw-html/resources.html', 'RESOURCES'),
]

for filepath, name in files:
    try:
        data = extract_detailed(filepath)
        
        # Clean up full text to remove navigation
        full_text = data['full_text']
        # Remove repeated navigation menus
        full_text = re.sub(r'(Brain-Based Community.*?More\s+)+', '', full_text)
        full_text = re.sub(r'Privacy Policy Disclaimer Contact Report abuse Page details.*', '', full_text)
        full_text = re.sub(r'\s+', ' ', full_text).strip()
        
        print(f"\n{'='*100}")
        print(f"{name}")
        print('='*100)
        print(f"\nPAGE TITLE: {data['title']}\n")
        
        print("HEADINGS FOUND:")
        for h in data['headings']:
            if h and not any(nav in h.lower() for nav in ['brain-based community', 'skip to', 'search this site']):
                print(f"  • {h}")
        
        print(f"\n\nFULL PAGE CONTENT:\n{full_text}\n")
        
        external_links = [(url, text) for url, text in data['links'] if 'http' in url or 'www' in url or 'drive.google' in url or 'fascets' in url]
        if external_links:
            print(f"\nEXTERNAL LINKS & RESOURCES ({len(external_links)} total):")
            seen = set()
            for url, text in external_links:
                if url not in seen and text.strip():
                    print(f"  [{text}] {url}")
                    seen.add(url)
        
    except Exception as e:
        print(f"Error with {filepath}: {e}")

