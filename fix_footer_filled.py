import os
import re

# Lista de archivos a modificar (incluyendo index.html por si acaso, aunque ya lo toque)
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
    "_economia_diseno_negocio.html"
]

root_dir = r"d:\workspace\marketing_ws\resources"

# SVG de Robot con Fill (Phosphor path real)
robot_svg_filled = """<svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor"><path d="M216,48V96a8,8,0,0,1-16,0V48a8,8,0,0,1,16,0ZM56,96V48a8,8,0,0,1,16,0V96a8,8,0,0,1-16,0Zm176,56V208a24,24,0,0,1-24,24H48a24,24,0,0,1-24-24V152a24,24,0,0,1,24-24H208A24,24,0,0,1,232,152Zm-16,0a8,8,0,0,0-8-8H48a8,8,0,0,0-8,8V208a8,8,0,0,0,8,8H208a8,8,0,0,0,8-8Zm-40-28H80a12,12,0,0,1-12-12V64A12,12,0,0,1,80,52h96a12,12,0,0,1,12,12v48A12,12,0,0,1,176,124Zm-80-56V96h64V68ZM128,144H80a8,8,0,0,0,0,16h48a8,8,0,0,0,0-16Z"></path></svg>"""

pattern = re.compile(r'(<a\s+href="trafico_llm_seo\.html"[^>]*class="footer-link-item trafico">.*?<div class="icon-wrap">)(.*?)(</div>\s*<span>)(.*?)(</span>\s*</a>)', re.DOTALL)

count = 0
for filename in files:
    filepath = os.path.join(root_dir, filename)
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified_content = pattern.sub(fr'\1{robot_svg_filled}\3ChatGPT nos visitó\5', content)
    
    if modified_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        count += 1
        print(f"File updated with FILLED SVG: {filename}")

print(f"Total files updated: {count}")
