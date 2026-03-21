import os
import re
import base64

def obfuscate_links_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        def replace_link(match):
            quote = match.group(1)
            url = match.group(2)
            
            # Encode URL to base64
            encoded_url = base64.b64encode(url.encode('utf-8')).decode('utf-8')
            
            # Protect against single/double quotes mismatch
            onclick_quote = "'" if quote == '"' else '"'
            
            replacement = (
                f'href="javascript:void(0)" '
                f'data-lk={quote}{encoded_url}{quote} '
                f'onclick={quote}window.open(atob(this.getAttribute({onclick_quote}data-lk{onclick_quote})), {onclick_quote}_blank{onclick_quote});{quote}'
            )
            return replacement

        # regex: href=(['"])(https?://(?:www\.)?(?:tiktok\.com|wa\.me)[^'"]*)(['"])
        pattern = re.compile(r'href=(["\'])(https?://(?:www\.)?(?:tiktok\.com|wa\.me)[^"\']+)\1')
        
        new_content = pattern.sub(replace_link, content)
        
        if new_content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Obfuscated links in {filepath}")
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    directory = "."
    obfuscated_count = 0
    for root, dirs, files in os.walk(directory):
        # Ignorar directorios que no interesan
        if '.git' in root or 'node_modules' in root:
            continue
            
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                obfuscate_links_in_file(filepath)
                obfuscated_count += 1
                
    print("Process complete.")
