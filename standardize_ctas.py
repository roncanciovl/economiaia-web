import glob
import re
import os

footer_html = '''    <!-- Footer Economía IA -->
    <footer
        style="width: 100%; max-width: 1000px; margin: 2rem auto 0; padding: 1rem 1rem; border-top: 1px solid #1e293b; text-align: center;">
        <div
            style="display: flex; justify-content: center; align-items: center; gap: 0.8rem; flex-wrap: wrap; margin-bottom: 0.5rem;">
            <span style="color: #64748b; font-size: 0.75rem; font-weight: 600;">Economía IA</span>
            <span style="color: #334155;">·</span>
            <a href="https://www.tiktok.com/@economiaia" target="_blank" rel="noopener noreferrer"
                style="color: #94a3b8; font-size: 0.75rem; text-decoration: none; transition: color 0.2s;"
                onmouseover="this.style.color='#ff0050';" onmouseout="this.style.color='#94a3b8';">🎵 @economiaia</a>
            <span style="color: #334155;">·</span>
            <a href="https://beacons.ai/economiaia" target="_blank" rel="noopener noreferrer"
                style="color: #94a3b8; font-size: 0.75rem; text-decoration: none; transition: color 0.2s;"
                onmouseover="this.style.color='#8b5cf6';" onmouseout="this.style.color='#94a3b8';">🔗 Enlaces</a>
            <span style="color: #334155;">·</span>
            <a href="https://beacons.ai/economiaia" target="_blank" rel="noopener noreferrer"
                style="color: #94a3b8; font-size: 0.75rem; text-decoration: none; transition: color 0.2s;"
                onmouseover="this.style.color='#10b981';" onmouseout="this.style.color='#94a3b8';">💼 Consultoría</a>
            <span style="color: #334155;">·</span>
            <a href="trafico_llm_seo.html" target="_blank" rel="noopener noreferrer"
                style="color: #94a3b8; font-size: 0.75rem; text-decoration: none; transition: color 0.2s;"
                onmouseover="this.style.color='#f59e0b';" onmouseout="this.style.color='#94a3b8';">📈 Tráfico en Vivo</a>
            <span style="color: #334155;">·</span>
            <a href="https://wa.me/573102604764" target="_blank" rel="noopener noreferrer"
                style="color: #94a3b8; font-size: 0.75rem; text-decoration: none; transition: color 0.2s;"
                onmouseover="this.style.color='#25d366';" onmouseout="this.style.color='#94a3b8';">📱 WhatsApp</a>
        </div>
        <p style="color: #334155; font-size: 0.65rem; margin: 0;">© 2026 Economía IA</p>
    </footer>'''

def get_cta(filename):
    if filename == "agentes_conversacionales_ia.html":
        return {
            "title": "Auditoría de Arquitectura Gratuita",
            "desc": "Define el alcance técnico exacto de tu agente (RAG, LangGraph, Multi-Agente) antes de producir.",
            "wa": "https://wa.me/573102604764?text=Hola,%20estoy%20evaluando%20opciones%20para%20un%20agente%20conversacional%20y%20quiero%20la%20auditor%C3%ADa%20t%C3%A9cnica.",
            "btn": "🔍 Solicitar Auditoría Técnica"
        }
    elif filename == "arquitectura_marketing_ia.html":
        return {
            "title": "💎 Aparece en las recomendaciones de la IA",
            "desc": "Configuramos tu web para que ChatGPT y Gemini recomienden tu negocio a nuevos clientes de inmediato.",
            "wa": "https://wa.me/573102604764?text=Hola,%20quiero%20que%20la%20IA%20recomiende%20mi%20negocio.",
            "btn": "📩 Quiero que la IA me recomiende"
        }
    elif filename == "teoria_senal_creativa.html":
        return {
            "title": "🚀 IA trabajando para encontrar tus clientes",
            "desc": "Escríbenos 'MOTOR' para recibir una ruta técnica gratuita y analizar la recomendación de tu negocio.",
            "wa": "https://wa.me/573102604764?text=MOTOR",
            "btn": "📩 Enviar Mensaje (MOTOR)"
        }
    else:
        return {
            "title": "💎 ¿Listo para automatizar tu facturación?",
            "desc": "Diseñamos el ecosistema de IA que tu negocio necesita para escalar sin depender 100% de ti.",
            "wa": "https://wa.me/573102604764?text=Hola,%20quisiera%20agendar%20una%20consultor%C3%ADa%20estrat%C3%A9gica%20para%20mi%20negocio.",
            "btn": "💼 Solicitar Consultoría Estratégica"
        }

cta_template = '''
    <section class="final-cta-block" style="background: #1e293b; border-top: 1px solid #334155; padding: 2.5rem 1.5rem; text-align: center; width: 100%; box-sizing: border-box;">
        <div style="max-width: 700px; margin: 0 auto;">
            <h2 style="color: #fff; font-size: 1.3rem; margin-bottom: 0.8rem; font-family: 'Inter', sans-serif;">{title}</h2>
            <p style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 1.5rem; line-height: 1.5;">
                {desc}
            </p>
            <a href="{wa}" 
               target="_blank" rel="noopener noreferrer" 
               style="display: inline-flex; align-items: center; gap: 0.6rem; background: #334155; color: #fff; padding: 0.7rem 1.8rem; border-radius: 0.4rem; text-decoration: none; font-weight: 700; border: 1px solid #475569; transition: all 0.2s; font-size: 0.9rem;"
               onmouseover="this.style.background='#475569'; this.style.transform='translateY(-2px)';" 
               onmouseout="this.style.background='#334155'; this.style.transform='translateY(0)';"
               onmousedown="this.style.transform='translateY(0)';"
            >
                {btn}
            </a>
        </div>
    </section>
'''

for file_path in glob.glob('*.html'):
    if "trafico_llm_seo" in file_path or "index.html" in file_path: continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    filename = os.path.basename(file_path)
    cta = get_cta(filename)
    new_cta_html = cta_template.format(**cta)
    
    # Clean old versions
    content = re.sub(r'<footer.*?</footer>', '', content, flags=re.DOTALL)
    content = re.sub(r'<!-- Footer Economía IA -->.*?(?:</footer>)', '', content, flags=re.DOTALL)
    content = re.sub(r'<section class="final-cta-block".*?</section>', '', content, flags=re.DOTALL)
    
    # Inject
    if "</body>" in content:
        content = content.replace("</body>", f"{new_cta_html}\n\n{footer_html}\n\n</body>")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
