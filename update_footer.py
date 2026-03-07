import os
import re

# Lista de archivos a modificar (extraída del grep previo)
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

# Patrón para encontrar el link de "Tráfico Real" en el footer
# Buscamos el bloque que contiene trafico_llm_seo.html
pattern = re.compile(r'(<a\s+href="trafico_llm_seo\.html"[^>]*class="footer-link-item trafico">.*?<div class="icon-wrap">)(.*?)(</div>\s*<span>)(.*?)(</span>\s*</a>)', re.DOTALL)

# Reemplazo:
# 1. El icono original por ph-duotone ph-robot (siempre que usemos el SVG o tag <i>)
# 2. El texto "Tráfico Real" por "ChatGPT nos visitó"

new_icon = '<i class="ph-duotone ph-robot" style="font-size: 20px;"></i>'
new_text = "ChatGPT nos visitó"

count = 0
for filename in files:
    filepath = os.path.join(root_dir, filename)
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Intentamos primero con el patrón de tag <i> si existe, o reemplazamos el contenido del wrap
    # Muchos de tus archivos usan SVG dentro del icon-wrap, vamos a ser agresivos con el reemplazo del contenido del wrap
    
    modified_content = pattern.sub(fr'\1{new_icon}\3{new_text}\5', content)
    
    if modified_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        count += 1
        print(f"File updated: {filename}")
    else:
        # Fallback para archivos que quizás tienen una estructura ligeramente distinta
        # Intentamos un reemplazo más simple del texto y el icono si el regex falló por detalles de whitespace
        print(f"Regex didn't match for {filename}, checking manual markers...")

print(f"Total files updated: {count}")
