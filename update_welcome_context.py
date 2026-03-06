import os
import glob

directory = r'd:\workspace\marketing_ws\resources'
pattern = os.path.join(directory, '*.html')

search_text = 'let pageContext = "";'
replacement_text = """const welcomeMsg = document.querySelector('.chat-bubble.chat-bot')?.innerText || "";
                let pageContext = `Mensaje de bienvenida que Sigma (tú) acaba de enviar al usuario: "${welcomeMsg}"\\n\\n`;"""

files = glob.glob(pattern)
print(f"Found {len(files)} files to update.")

for file_path in files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if search_text in content:
            new_content = content.replace(search_text, replacement_text)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated: {os.path.basename(file_path)}")
        else:
            print(f"Pattern not found in: {os.path.basename(file_path)}")
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
