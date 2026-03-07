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

# SVG de Huella / Rastro (Phosphor footprint style)
footprint_svg = """<svg width="20" height="20" viewBox="0 0 256 256" fill="currentColor"><path d="M100,104a32,32,0,1,0,32,32A32,32,0,0,0,100,104Zm0,48a16,16,0,1,1,16-16A16,16,0,0,1,100,152ZM192,80a32,32,0,1,0,32,32A32,32,0,0,0,192,80Zm0,48a16,16,0,1,1,16-16A16,16,0,0,1,192,128ZM112,24a32,32,0,1,0,32,32A32,32,0,0,0,112,24Zm0,48a16,16,0,1,1,16-16A16,16,0,0,1,112,72ZM40,72A32,32,0,1,0,72,104,32,32,0,0,0,40,72Zm0,48a16,16,0,1,1,16-16A16,16,0,0,1,40,120Zm108,80c-15.53,0-29.09-8-36.21-21.26a8,8,0,0,1,14.07-7.64c4.32,8,12.55,12.9,22.14,12.9a26,26,0,0,0,26-26c0-23.77-38.35-43-55.75-51.19a8,8,0,0,1,6.72-14.54C140.24,103.55,190,127,190,168A42,42,0,0,1,148,210c-3.13,0-6,0-9,0a26,26,0,0,1-23.14-14.1,8,8,0,0,1,14.14-7.46A10.06,10.06,0,0,0,139,194h9A26,26,0,1,0,148,200Z"></path></svg>"""

# Patrón para el footer
pattern_footer = re.compile(r'(<a\s+href="trafico_llm_seo\.html"[^>]*class="footer-link-item trafico">.*?<div class="icon-wrap">)(.*?)(</div>\s*<span>)(.*?)(</span>\s*</a>)', re.DOTALL)

# Reemplazo en JS del index.html para que el nodo orbital también tenga el icono de rastro/pisada
# En index.html usamos Phosphor directamente: ph-duotone ph-footprints
index_icon_replacement = "{ title: 'ChatGPT nos visitó', file: 'trafico_llm_seo.html', icon: '<i class=\"ph-duotone ph-footprints\"></i>', type: 'arquitectura' }"

count = 0
for filename in files:
    filepath = os.path.join(root_dir, filename)
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if filename == "index.html":
        # Manejo especial para el objeto JS en index.html
        modified_content = re.sub(r'\{ title: \'ChatGPT nos visitó\', file: \'trafico_llm_seo\.html\', icon: \'<i class="ph-duotone ph-robot"></i>\', type: \'arquitectura\' \}', index_icon_replacement, content)
    else:
        # Reemplazo estándar de footer para los demás archivos
        modified_content = pattern_footer.sub(fr'\1{footprint_svg}\3ChatGPT nos visitó\5', content)
    
    if modified_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        count += 1
        print(f"File updated with Footprint: {filename}")

print(f"Total files updated: {count}")
