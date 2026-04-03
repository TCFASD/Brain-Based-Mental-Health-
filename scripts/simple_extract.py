import re
from html import unescape

def extract_all_text(filepath):
    """Extract all visible text from HTML file"""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Remove scripts and styles - their content
    content = re.sub(r'<script[^>]*>.*?</script>', ' ', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<style[^>]*>.*?</style>', ' ', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<noscript[^>]*>.*?</noscript>', ' ', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Extract title
    title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else "N/A"
    
    # Remove HTML tags but keep spacing
    text = re.sub(r'<[^>]+>', ' ', content)
    
    # Decode HTML entities
    text = unescape(text)
    
    # Clean up multiple spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    # Extract headings and links separately for better structure
    headings = re.findall(r'<h[1-6][^>]*>([^<]+)</h[1-6]>', content, re.IGNORECASE)
    links = re.findall(r'<a[^>]*href="([^"]*)"[^>]*>([^<]+)</a>', content, re.IGNORECASE)
    
    return {
        'title': title,
        'text': text,
        'headings': [h.strip() for h in headings],
        'links': [(url.strip(), text.strip()) for url, text in links]
    }

files = [
    ('raw-html/caregivers.html', 'CAREGIVERS'),
    ('raw-html/self-advocates.html', 'SELF-ADVOCATES'),
    ('raw-html/organizations.html', 'ORGANIZATIONS'),
    ('raw-html/resources.html', 'RESOURCES'),
]

for filepath, name in files:
    try:
        data = extract_all_text(filepath)
        
        print(f"\n{'='*100}")
        print(f"{name}")
        print('='*100)
        print(f"\nTITLE: {data['title']}\n")
        
        if data['headings']:
            print("HEADINGS FOUND:")
            for h in data['headings']:
                if h and len(h) > 3:
                    print(f"  • {h}")
        
        print(f"\nMAIN CONTENT (First 4000 characters):")
        print(data['text'][:4000])
        print("\n[... content continues ...]")
        
        external_links = [(url, text) for url, text in data['links'] if 'http' in url or 'www' in url or 'drive.google' in url]
        if external_links:
            print(f"\n\nEXTERNAL LINKS ({len(external_links)} found):")
            for url, text in external_links[:12]:
                print(f"  [{text}] {url}")
        
    except Exception as e:
        print(f"Error with {filepath}: {e}")

