"""
Script de inyección masiva de LLM SEO SOTA:
- Canonical URLs
- Open Graph tags
- JSON-LD contextual (Article + BreadcrumbList)
- Reemplazo de ProfessionalService genérico por schemas contextuales
"""

import re
import os
from datetime import date

BASE_URL = "https://www.economiaia.business"
LOGO_URL = f"{BASE_URL}/logo_economia_ia_neon_v4.png"
TODAY = date.today().isoformat()

# Configuración por página
PAGES = {
    "index.html": {
        "title": "Ecosistema de Marketing IA - Hub Central | Economía IA",
        "description": "Ecosistema de conocimiento y consultoría de Inteligencia Artificial en Latinoamérica. Estrategias, agentes conversacionales y automatización para negocios.",
        "level": None,  # Es la raíz
        "schema_type": "WebSite",
    },
    "nucleo_economia_ia.html": {
        "title": "Núcleo Economía IA | Economía IA",
        "description": "Las 6 claves científicas para vender más usando algoritmos de Matchmaking, reducción de fricción y teoría de la señal.",
        "level": "Fundamentos",
        "schema_type": "Article",
    },
    "presentacion_condicion_cero.html": {
        "title": "Oferta Irresistible | Economía IA",
        "description": "Domina el concepto de Condición Cero para construir una propuesta de valor imposible de rechazar con IA.",
        "level": "Fundamentos",
        "schema_type": "Article",
    },
    "teoria_senal_creativa.html": {
        "title": "Teoría Señal Creativa | Economía IA",
        "description": "Cómo crear videos que atraen clientes automáticamente sin segmentación manual, usando Zero-Targeting y el algoritmo FYP.",
        "level": "Fundamentos",
        "schema_type": "Article",
    },
    "arquitectura_marketing_ia.html": {
        "title": "Marketing | Economía IA",
        "description": "Arquitectura completa de marketing con IA: desde la oferta irresistible hasta la conversión automática en WhatsApp.",
        "level": "Fundamentos",
        "schema_type": "Article",
    },
    "psicologia_precio_regla_oro.html": {
        "title": "Psicología del Precio | Economía IA",
        "description": "El precio como señal de comunicación estratégica. Regla de Oro del pricing y ciencia del valor percibido.",
        "level": "Fundamentos",
        "schema_type": "Article",
    },
    "arquitectura_distribucion_motor.html": {
        "title": "Arquitectura Distribución | Economía IA",
        "description": "El motor automático que usa Meta Advantage+ y TikTok Smart+ para distribuir contenido y convertir clientes 24/7.",
        "level": "Sistemas & Estrategias",
        "schema_type": "Article",
    },
    "operaciones_y_datos_ia.html": {
        "title": "Operaciones y Datos | Economía IA",
        "description": "Automatización operativa, dashboards y flujos de datos con IA para escalar tu negocio.",
        "level": "Sistemas & Estrategias",
        "schema_type": "Article",
    },
    "estrategia_tiktok_ia.html": {
        "title": "Estrategia TikTok IA | Economía IA",
        "description": "TikTok como motor full-funnel algorítmico para negocios en 2026. Spark Ads, Zero-Targeting y contenido orgánico.",
        "level": "Sistemas & Estrategias",
        "schema_type": "Article",
    },
    "ecosistema_meta_ia.html": {
        "title": "Ecosistema Meta IA | Economía IA",
        "description": "Orquestación algorítmica de Facebook, Instagram y WhatsApp con Meta Advantage+ para ventas automáticas.",
        "level": "Sistemas & Estrategias",
        "schema_type": "Article",
    },
    "agentes_conversacionales_ia.html": {
        "title": "Agentes Conversacionales | Economía IA",
        "description": "Sistemas de texto y voz basados en LLMs para atención al cliente, cualificación de leads y ventas automáticas.",
        "level": "Sistemas & Estrategias",
        "schema_type": "Article",
    },
    "arquitectura_manychat_ia.html": {
        "title": "Arquitectura ManyChat | Economía IA",
        "description": "Implementa flujos de automatización ManyChat para capturar leads y escalar ventas en Instagram, TikTok y WhatsApp.",
        "level": "Herramientas IA",
        "schema_type": "Article",
    },
    "stack_tecnologico_ia.html": {
        "title": "Stack Tecnológico | Economía IA",
        "description": "Las herramientas esenciales del marketing IA 2026: Canva, ManyChat, ChatGPT, Meta para un sistema automatizado.",
        "level": "Herramientas IA",
        "schema_type": "Article",
    },
    "jerarquia_meta_whatsapp.html": {
        "title": "Automatización con Meta | Economía IA",
        "description": "Jerarquía técnica de Business Portfolio, WABA y Phone ID para escalar ventas en el ecosistema WhatsApp y Meta.",
        "level": "Herramientas IA",
        "schema_type": "TechArticle",
    },
    "trafico_llm_seo.html": {
        "title": "Tráfico LLM SEO | Economía IA",
        "description": "Monitor en vivo de la visibilidad y tráfico capturado mediante optimización para motores de respuesta de IA.",
        "level": "Herramientas IA",
        "schema_type": "WebApplication",
    },
    "analisis_agencias_ia_latam.html": {
        "title": "Análisis Agencias IA Latinoamérica | Economía IA",
        "description": "Análisis comparativo de servicios de consultoría e implementación de IA en LatAm para 2026.",
        "level": None,
        "schema_type": "Article",
    },
    "estrategia_trafico_local.html": {
        "title": "Estrategia Tráfico Local | Economía IA",
        "description": "Cómo llevar gente a tu local usando Google Maps, Meta Ads y IA de geolocalización.",
        "level": None,
        "schema_type": "Article",
    },
    "flujos_vs_agentes_ia.html": {
        "title": "Flujos vs Agentes IA | Economía IA",
        "description": "Diferencias entre flujos de automatización y agentes conversacionales con IA para negocios.",
        "level": None,
        "schema_type": "Article",
    },
}

RESOURCES_DIR = r"d:\workspace\marketing_ws\resources"


def build_og_tags(filename, config):
    url = f"{BASE_URL}/{filename}"
    return f'''    <meta property="og:title" content="{config['title']}">
    <meta property="og:description" content="{config['description']}">
    <meta property="og:type" content="{'website' if filename == 'index.html' else 'article'}">
    <meta property="og:url" content="{url}">
    <meta property="og:site_name" content="Economía IA">
    <meta property="og:image" content="{LOGO_URL}">'''


def build_canonical(filename):
    url = f"{BASE_URL}/{filename}"
    return f'    <link rel="canonical" href="{url}">'


def build_breadcrumb_jsonld(filename, config):
    if not config.get("level"):
        return ""
    
    items = [
        {"@type": "ListItem", "position": 1, "name": "Ecosistema IA", "item": f"{BASE_URL}/index.html"},
    ]
    
    if config["level"]:
        items.append({"@type": "ListItem", "position": 2, "name": config["level"]})
    
    page_title = config["title"].split(" | ")[0]
    items.append({"@type": "ListItem", "position": 3, "name": page_title, "item": f"{BASE_URL}/{filename}"})
    
    import json
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items
    }
    return json.dumps(schema, ensure_ascii=False, indent=6)


def build_article_jsonld(filename, config):
    import json
    url = f"{BASE_URL}/{filename}"
    page_title = config["title"].split(" | ")[0]
    
    schema = {
        "@context": "https://schema.org",
        "@type": config["schema_type"],
        "headline": page_title,
        "description": config["description"],
        "url": url,
        "datePublished": "2026-01-15",
        "dateModified": TODAY,
        "inLanguage": "es",
        "author": {
            "@type": "Person",
            "name": "Henry Roncancio",
            "url": "https://www.linkedin.com/in/henry-roncancio-a7341015/",
            "jobTitle": "AI Architect",
            "worksFor": {
                "@type": "Organization",
                "name": "Economía IA",
                "url": BASE_URL
            }
        },
        "publisher": {
            "@type": "Organization",
            "name": "Economía IA",
            "url": BASE_URL,
            "logo": {
                "@type": "ImageObject",
                "url": LOGO_URL
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": url
        }
    }
    
    return json.dumps(schema, ensure_ascii=False, indent=6)


def process_file(filename, config):
    filepath = os.path.join(RESOURCES_DIR, filename)
    if not os.path.exists(filepath):
        print(f"  SKIP (no existe): {filename}")
        return
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    modified = False
    
    # 1. Add canonical if missing
    if 'rel="canonical"' not in content:
        canonical = build_canonical(filename)
        # Insert before </head>
        if "</head>" in content:
            content = content.replace("</head>", f"{canonical}\n</head>", 1)
            modified = True
            print(f"  + canonical")
    
    # 2. Add OG tags if missing
    if 'og:title' not in content:
        og_tags = build_og_tags(filename, config)
        if "</head>" in content:
            content = content.replace("</head>", f"{og_tags}\n</head>", 1)
            modified = True
            print(f"  + OG tags")
    
    # 3. Add BreadcrumbList JSON-LD if applicable and missing
    if config.get("level") and "BreadcrumbList" not in content:
        breadcrumb = build_breadcrumb_jsonld(filename, config)
        if breadcrumb and "</head>" in content:
            tag = f'    <script type="application/ld+json">\n    {breadcrumb}\n    </script>\n'
            content = content.replace("</head>", f"{tag}</head>", 1)
            modified = True
            print(f"  + BreadcrumbList")
    
    # 4. Add Article/TechArticle JSON-LD if no per-page article schema exists
    if filename != "index.html":
        has_article = '"@type": "Article"' in content or '"@type": "TechArticle"' in content or '"@type": "WebApplication"' in content
        if not has_article and config["schema_type"] in ("Article", "TechArticle", "WebApplication"):
            article_json = build_article_jsonld(filename, config)
            if "</head>" in content:
                tag = f'    <script type="application/ld+json">\n    {article_json}\n    </script>\n'
                content = content.replace("</head>", f"{tag}</head>", 1)
                modified = True
                print(f"  + {config['schema_type']} schema")
    
    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✅ SAVED: {filename}")
    else:
        print(f"  (sin cambios): {filename}")


if __name__ == "__main__":
    print("=" * 60)
    print("LLM SEO SOTA Injection Script")
    print("=" * 60)
    
    for filename, config in PAGES.items():
        print(f"\n📄 {filename}")
        process_file(filename, config)
    
    print("\n" + "=" * 60)
    print("✅ COMPLETADO")
    print("=" * 60)
