import os
import re

# Lista de archivos a modificar
files = [
    "agentes_conversacionales_ia.html",
    "analisis_agencias_ia_latam.html",
    "arquitectura_manychat_ia.html",
    "arquitectura_marketing_ia.html",
    "arquitectura_distribucion_motor.html",
    "ecosistema_meta_ia.html",
    "estrategia_trafico_local.html",
    "estrategia_tiktok_ia.html",
    "flujos_vs_agentes_ia.html",
    "jerarquia_meta_whatsapp.html",
    "nucleo_economia_ia.html",
    "operaciones_y_datos_ia.html",
    "presentacion_condicion_cero.html",
    "psicologia_precio_regla_oro.html",
    "stack_tecnologico_ia.html",
    "teoria_senal_creativa.html",
    "trafico_llm_seo.html",
    "_economia_diseno_negocio.html",
    "index.html"
]

root_dir = r"d:\workspace\marketing_ws\resources"

# SVG de Robot (Phosphor style but inline)
robot_svg = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="10" rx="2"></rect><circle cx="12" cy="5" r="2"></circle><path d="M12 7v4"></path><line x1="8" y1="16" x2="8" y2="16"></line><line x1="16" y1="16" x2="16" y2="16"></line></svg>"""

# Buscamos el bloque que contiene trafico_llm_seo.html y reemplazamos el contenido del wrap
pattern = re.compile(r'(<a\s+href="trafico_llm_seo\.html"[^>]*class="footer-link-item trafico">.*?<div class="icon-wrap">)(.*?)(</div>\s*<span>)(.*?)(</span>\s*</a>)', re.DOTALL)

count = 0
for filename in files:
    filepath = os.path.join(root_dir, filename)
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Reemplazamos el icono (sea lo que sea que haya ahora, i o svg) por nuestro SVG robusto
    modified_content = pattern.sub(fr'\1{robot_svg}\3ChatGPT nos visitó\5', content)
    
    if modified_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        count += 1
        print(f"File updated with SVG: {filename}")

print(f"Total files updated: {count}")
