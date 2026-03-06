import re
filepath = r'd:\workspace\marketing_ws\resources\trafico_llm_seo.html'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'<h2 class="panel-title">.*?Auditoría', '<h2 class="panel-title">📡 Auditoría', text)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)
