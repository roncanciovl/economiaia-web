import glob
import re
import os

footer_html = '''    <!-- Footer Economía IA -->
    <footer
        style="width: 100%; max-width: 1000px; margin: 1rem auto; padding: 1rem; border-top: 1px solid rgba(255,255,255,0.05); text-align: center;">
        <div
            style="display: flex; justify-content: center; align-items: center; gap: 0.8rem; flex-wrap: wrap; margin-bottom: 0.4rem;">
            <span style="color: #475569; font-size: 0.7rem; font-weight: 600;">ECONOMÍA IA</span>
            <span style="color: #1e293b;">·</span>
            <a href="https://www.tiktok.com/@economiaia" target="_blank" rel="noopener noreferrer"
                style="color: #64748b; font-size: 0.7rem; text-decoration: none; transition: color 0.2s;"
                onmouseover="this.style.color='#ff0050';" onmouseout="this.style.color='#64748b';">🎵 TikTok</a>
            <span style="color: #1e293b;">·</span>
            <a href="https://descubre.economiaia.business" target="_blank" rel="noopener noreferrer"
                style="color: #64748b; font-size: 0.7rem; text-decoration: none; transition: color 0.2s;"
                onmouseover="this.style.color='#8b5cf6';" onmouseout="this.style.color='#64748b';">🔗 Enlaces</a>
            <span style="color: #1e293b;">·</span>
            <a href="https://descubre.economiaia.business" target="_blank" rel="noopener noreferrer"
                style="color: #64748b; font-size: 0.7rem; text-decoration: none; transition: color 0.2s;"
                onmouseover="this.style.color='#10b981';" onmouseout="this.style.color='#64748b';">💼 Consultoría</a>
            <span style="color: #1e293b;">·</span>
            <a href="trafico_llm_seo.html" target="_blank" rel="noopener noreferrer"
                style="color: #10b981; font-weight: bold; font-size: 0.7rem; text-decoration: none; transition: all 0.2s;"
                onmouseover="this.style.textShadow='0 0 8px rgba(16, 185, 129, 0.6)';" onmouseout="this.style.textShadow='none';">🟢 Tráfico Real</a>
            <span style="color: #1e293b;">·</span>
            <a href="https://wa.me/573043656226" target="_blank" rel="noopener noreferrer"
                style="color: #64748b; font-size: 0.7rem; text-decoration: none; transition: color 0.2s;"
                onmouseover="this.style.color='#25d366';" onmouseout="this.style.color='#64748b';">📱 WhatsApp</a>
        </div>
        <p style="color: #334155; font-size: 0.6rem; margin: 0; opacity: 0.5;">© 2026</p>
    </footer>'''

def get_cta(filename):
    if filename == "agentes_conversacionales_ia.html":
        return {
            "title": "Auditoría Técnica de Agentes",
            "desc": "Define el alcance de tu arquitectura (RAG, Multi-Agente) antes de producir.",
            "wa": "https://wa.me/573043656226?text=Hola,%20estoy%20evaluando%20opciones%20para%20un%20agente%20conversacional%20y%20quiero%20la%20auditor%C3%ADa%20t%C3%A9cnica.",
            "btn": "🔍 Solicitar Auditoría"
        }
    elif filename == "arquitectura_marketing_ia.html":
        return {
            "title": "Recomendación en Motores de IA",
            "desc": "Configuramos tu web para que la IA recomiende tu negocio de inmediato.",
            "wa": "https://wa.me/573043656226?text=Hola,%20quiero%20que%20la%20IA%20recomiende%20mi%20negocio.",
            "btn": "📩 Quiero aparecer en la IA"
        }
    elif filename == "teoria_senal_creativa.html":
        return {
            "title": "Ruta Técnica de Ventas",
            "desc": "Escríbenos 'MOTOR' para analizar la recomendación de tu negocio por la IA.",
            "wa": "https://wa.me/573043656226?text=MOTOR",
            "btn": "📩 Enviar MOTOR"
        }
    else:
        return {
            "title": "Consultoría Estratégica IA",
            "desc": "Diseñamos el ecosistema que tu negocio necesita para escalar sin depender de ti.",
            "wa": "https://wa.me/573043656226?text=Hola,%20quisiera%20agendar%20una%20consultor%C3%ADa%20estrat%C3%A9gica%20para%20mi%20negocio.",
            "btn": "💼 Agendar Consultoría"
        }

cta_template = '''
    <section class="final-cta-block" style="background: transparent; border-top: 1px solid rgba(255,255,255,0.05); padding: 1.5rem 1rem; text-align: center; width: 100%; box-sizing: border-box; margin-top: 1rem;">
        <div style="max-width: 600px; margin: 0 auto;">
            <h2 style="color: #fff; font-size: 1.1rem; margin-bottom: 0.5rem; font-family: 'Inter', sans-serif; font-weight: 700;">{title}</h2>
            <p style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 1.2rem; line-height: 1.4;">
                {desc}
            </p>
            <a href="{wa}" 
               target="_blank" rel="noopener noreferrer" 
               style="display: inline-flex; align-items: center; gap: 0.5rem; background: #1e293b; color: #fff; padding: 0.6rem 1.4rem; border-radius: 0.3rem; text-decoration: none; font-weight: 600; border: 1px solid #334155; transition: all 0.2s; font-size: 0.8rem;"
               onmouseover="this.style.background='#334155'; this.style.transform='translateY(-1px)';" 
               onmouseout="this.style.background='#1e293b'; this.style.transform='translateY(0)';"
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
