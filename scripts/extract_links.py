import re

def extract_links(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Extract all links
    links = []
    for match in re.finditer(r'<a[^>]*href="([^"]*)"[^>]*>([^<]+(?:<[^>]*>[^<]*)*)</a>', content, re.IGNORECASE | re.DOTALL):
        url = match.group(1).strip()
        text = re.sub(r'<[^>]+>', '', match.group(2)).strip()
        if url and text:
            links.append((url, text))
    
    return links

files = [
    ('raw-html/caregivers.html', 'CAREGIVERS'),
    ('raw-html/self-advocates.html', 'SELF-ADVOCATES'),
    ('raw-html/organizations.html', 'ORGANIZATIONS'),
    ('raw-html/resources.html', 'RESOURCES'),
]

for filepath, name in files:
    try:
        links = extract_links(filepath)
        
        # Filter out internal navigation links and duplicates
        external_links = []
        seen = set()
        for url, text in links:
            if any(ext in url for ext in ['http', 'www', 'drive.google', 'fascets', 'eileendevine']):
                if url not in seen and text.strip():
                    external_links.append((url, text))
                    seen.add(url)
        
        print(f"\n{name} - External Links ({len(external_links)} found):")
        print('='*90)
        for url, text in sorted(external_links):
            print(f"  [{text}]")
            print(f"    {url}\n")
        
    except Exception as e:
        print(f"Error with {filepath}: {e}")

