import re

def comprehensive_extract(filepath):
    """Extract all meaningful text content from HTML file"""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Remove scripts and styles
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Extract title
    title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else "N/A"
    
    # Extract all headings with levels
    headings = []
    for match in re.finditer(r'<(h[1-6])[^>]*>([^<]+)</\1>', content, re.IGNORECASE):
        level = match.group(1)
        text = match.group(2).strip()
        headings.append((level, text))
    
    # Extract all paragraphs
    paragraphs = []
    for match in re.finditer(r'<p[^>]*>([^<]+(?:<[^>]+>[^<]+)*)</p>', content, re.IGNORECASE | re.DOTALL):
        text = re.sub(r'<[^>]+>', '', match.group(1)).strip()
        if text and len(text) > 10:
            paragraphs.append(text)
    
    # Extract all list items
    list_items = []
    for match in re.finditer(r'<li[^>]*>([^<]+(?:<[^>]*>[^<]*)*)</li>', content, re.IGNORECASE | re.DOTALL):
        text = re.sub(r'<[^>]+>', '', match.group(1)).strip()
        if text:
            list_items.append(text)
    
    # Extract all links
    links = []
    for match in re.finditer(r'<a[^>]*href="([^"]*)"[^>]*>([^<]+(?:<[^>]*>[^<]*)*)</a>', content, re.IGNORECASE | re.DOTALL):
        url = match.group(1).strip()
        text = re.sub(r'<[^>]+>', '', match.group(2)).strip()
        if url and text:
            links.append((url, text))
    
    return {
        'title': title,
        'headings': headings,
        'paragraphs': paragraphs,
        'list_items': list_items,
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
        data = comprehensive_extract(filepath)
        
        print(f"\n{'='*90}")
        print(f"{name}")
        print('='*90)
        print(f"\nPAGE TITLE: {data['title']}\n")
        
        print("SECTION HEADINGS:")
        for level, heading in data['headings']:
            indent = "  " * (int(level[1]) - 1)
            print(f"{indent}{heading}")
        
        print(f"\n\nMAIN CONTENT PARAGRAPHS ({len(data['paragraphs'])} total):")
        for i, para in enumerate(data['paragraphs'][:8], 1):
            print(f"\n{i}. {para}")
        
        if data['list_items']:
            print(f"\n\nLIST ITEMS ({len(data['list_items'])} total):")
            for item in data['list_items'][:15]:
                print(f"  • {item}")
        
        external_links = [(url, text) for url, text in data['links'] if 'http' in url or 'www' in url]
        if external_links:
            print(f"\n\nEXTERNAL RESOURCES & LINKS ({len(external_links)} total):")
            for url, text in external_links:
                print(f"  • [{text}]({url})")
        
    except Exception as e:
        print(f"Error with {filepath}: {e}")

