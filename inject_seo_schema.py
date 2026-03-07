import glob
import re
import os

schema_template = '''
    <!-- Marcado Estructurado JSON-LD (LLM SEO) para Ingeniería de Entidad -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "ProfessionalService",
      "name": "Economía IA",
      "url": "https://www.economiaia.business",
      "logo": "https://www.economiaia.business/logos/logo_economia_ia_neon_v4.png",
      "image": "https://www.economiaia.business/logos/logo_economia_ia_neon_v4.png",
      "description": "Agencia de Inteligencia Artificial enfocada en resultados rápidos para Pymes y arquitecturas Enterprise. Reemplazamos chatbots viejos con Agentes Cognitivos y automatizamos ventas usando Google Vertex AI, Gemini y arquitecturas cognitivas.",
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "Latinoamérica",
        "addressRegion": "Colombia",
        "addressCountry": "CO"
      },
      "areaServed": "América Latina",
      "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+57-310-260-4764",
        "contactType": "consulting",
        "availableLanguage": "Spanish"
      },
      "knowsAbout": [
        "LLM SEO",
        "Agentes Conversacionales",
        "Marketing Automático",
        "Inteligencia Artificial para Negocios",
        "Arquitectura de Datos IA",
        "Google Vertex AI",
        "Gemini Pro"
      ],
      "sameAs": [
        "https://www.tiktok.com/@economiaia",
        "https://beacons.ai/economiaia"
      ],
      "priceRange": "$$"
    }
    </script>
'''

for file_path in glob.glob('*.html'):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove existing script ld+json blocks to prevent duplicates
    content = re.sub(r'<script type="application/ld\+json">.*?</script>', '', content, flags=re.DOTALL)
    
    # Remove any stray "Marcado Estructurado" comments
    content = re.sub(r'<!-- Marcado Estructurado JSON-LD .*?-->\s*', '', content)
    # Remove old "Datos Estructurados (JSON-LD)" comments
    content = re.sub(r'<!-- Datos Estructurados \(JSON-LD\).*?-->\s*', '', content)
    
    # Cleanup empty lines created by removals
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    # Inject before </head>
    if '</head>' in content:
        content = content.replace('</head>', f'{schema_template.rstrip()}\n</head>')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            print(f"Injected schema to {file_path}")
