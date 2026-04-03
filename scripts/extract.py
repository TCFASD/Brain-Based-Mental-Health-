import re

def extract_text(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Remove all script tags
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove all style tags
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove HTML comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    
    # Remove all HTML tags but keep text
    text = re.sub(r'<[^>]+>', ' ', content)
    
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

files = [
    ('raw-html/caregivers.html', 'CAREGIVERS'),
    ('raw-html/self-advocates.html', 'SELF-ADVOCATES'),
    ('raw-html/organizations.html', 'ORGANIZATIONS'),
    ('raw-html/resources.html', 'RESOURCES'),
]

for filepath, name in files:
    try:
        text = extract_text(filepath)
        print(f"\n{'='*80}\n{name}\n{'='*80}\n{text[:3500]}\n\n")
    except Exception as e:
        print(f"Error with {filepath}: {e}")

