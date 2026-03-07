import os
import re

# List of files to modify
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

# Concentric Circles SVG (Target style)
concentric_svg = """<svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor"><path d="M128,80a48,48,0,1,0,48,48A48.05,48.05,0,0,0,128,80Zm0,80a32,32,0,1,1,32-32A32,32,0,0,1,128,160Zm0-136a104,104,0,1,0,104,104A104.11,104.11,0,0,0,128,24Zm0,192a88,88,0,1,1,88-88A88.1,88.1,0,0,1,128,216Z"></path></svg>"""

# Pattern for the footer
pattern_footer = re.compile(r'(<a\s+href="trafico_llm_seo\.html"[^>]*class="footer-link-item trafico">.*?<div class="icon-wrap">)(.*?)(</div>\s*<span>)(.*?)(</span>\s*</a>)', re.DOTALL)

# JS replacement for index.html node
index_icon_replacement = "{ title: 'ChatGPT nos visitó', file: 'trafico_llm_seo.html', icon: '<i class=\"ph-duotone ph-target\"></i>', type: 'arquitectura' }"

count = 0
for filename in files:
    filepath = os.path.join(root_dir, filename)
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if filename == "index.html":
        # Replacing the previous icon (broadcast, robot or footprints) with target
        modified_content = re.sub(r'\{ title: \'ChatGPT nos visitó\', file: \'trafico_llm_seo\.html\', icon: \'<i class="ph-duotone ph-(robot|footprints|broadcast)"></i>\', type: \'arquitectura\' \}', index_icon_replacement, content)
    else:
        # Footer replacement
        modified_content = pattern_footer.sub(fr'\1{concentric_svg}\3ChatGPT nos visitó\5', content)
    
    if modified_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        count += 1
        print(f"File updated with Concentric Circles (Target): {filename}")

print(f"Total files updated: {count}")
