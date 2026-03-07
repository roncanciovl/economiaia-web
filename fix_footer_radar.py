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

# SVG de Radar (Ondas) - Estilo Phosphor 'broadcast' o radar similar
radar_svg = """<svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor"><path d="M128,152a24,24,0,1,0,24,24A24,24,0,0,0,128,152Zm0,32a8,8,0,1,1,8-8A8,8,0,0,1,128,184Zm77.84-98a8,8,0,0,0-11,1.82,88,88,0,0,1-137.6,0,8,8,0,1,0-12.87,9.48,104,104,0,0,0,163.29,0A8,8,0,0,0,205.84,86Zm34-34.86a8,8,0,0,0-11.23,1.13,152,152,0,0,1-201.2,0,8,8,0,0,0-10.1,12.4,168,168,0,0,0,222.53,0A8,8,0,0,0,239.81,51.15Z"></path></svg>"""

# Patrón para el footer
pattern_footer = re.compile(r'(<a\s+href="trafico_llm_seo\.html"[^>]*class="footer-link-item trafico">.*?<div class="icon-wrap">)(.*?)(</div>\s*<span>)(.*?)(</span>\s*</a>)', re.DOTALL)

# Reemplazo en JS del index.html
index_icon_replacement = "{ title: 'ChatGPT nos visitó', file: 'trafico_llm_seo.html', icon: '<i class=\"ph-duotone ph-broadcast\"></i>', type: 'arquitectura' }"

count = 0
for filename in files:
    filepath = os.path.join(root_dir, filename)
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if filename == "index.html":
        # Reemplazar el icono anterior (huellas o robot) por el de radar
        modified_content = re.sub(r'\{ title: \'ChatGPT nos visitó\', file: \'trafico_llm_seo\.html\', icon: \'<i class="ph-duotone ph-(robot|footprints)"></i>\', type: \'arquitectura\' \}', index_icon_replacement, content)
    else:
        # Reemplazo de footer
        modified_content = pattern_footer.sub(fr'\1{radar_svg}\3ChatGPT nos visitó\5', content)
    
    if modified_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        count += 1
        print(f"File updated with Radar waves: {filename}")

print(f"Total files updated: {count}")
