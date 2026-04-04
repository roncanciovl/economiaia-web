import os
import glob

# Ensure we're in resources dir
html_files = glob.glob('*.html')

hook_html = '''            <!-- Círculo Interno -->
            <a href="comunidad_b2b.html" class="footer-link-item circle-hook" style="background: rgba(162, 155, 254, 0.1); border: 1px solid #6C5CE7;">
                <div class="icon-wrap" style="color: #a29bfe;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="16" x2="12" y2="12"></line>
                        <line x1="12" y1="8" x2="12.01" y2="8"></line>
                    </svg>
                </div>
                <span style="font-weight: 600; color: #a29bfe;">Circulo B2B</span>
            </a>'''

count = 0
for file in html_files:
    if file == 'index.html' or file == 'comunidad_b2b.html':
        continue # skip index
        
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    target = '<div class="footer-premium-links">'
    if target in content and 'comunidad_b2b.html' not in content:
        content = content.replace(target, target + '\n' + hook_html)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1

print(f'Actualizados {count} archivos.')
