---
name: Obfuscate Social Links
description: Instrucciones y directrices obligatorias para asegurar que los enlaces a WhatsApp y TikTok permanezcan ofuscados frente a bots de scrapeo.
---

# Obfuscate Social Links (Defensa Anti-Scraping)

## Propósito
Este skill define el estándar obligatorio que cualquier agente LLM o desarrollador debe seguir al agregar o modificar enlaces dentro de la carpeta `resources` (o en general en la web), con el objetivo de prevenir ataques de spam basados en el scrapeo masivo de URLs comerciales.

## Regla Estricta
Bajo **ninguna circunstancia** insertar directamente un enlace comercial dentro del atributo `href` que contenga integraciones externas propensas a spam, específicamente:
- `https://www.tiktok.com/...`
- `https://wa.me/...`

Cualquier enlace nuevo de esta índole **debe** insertarse ofuscado usando Base64.

## Formato Requerido (El Estándar)

**❌ Incorrecto (Vulnerable a Bots):**
```html
<a href="https://wa.me/573059293414" target="_blank">Contactar a Ventas</a>
```

**✅ Correcto (A prueba de Bots):**
```html
<a href="javascript:void(0)" 
   data-lk="aHR0cHM6Ly93YS5tZS81NzMwNTkyOTM0MTQ=" 
   onclick="window.open(atob(this.getAttribute('data-lk')), '_blank');">
   Contactar a Ventas
</a>
```

## ¿Por qué funciona?
Los LLM crawlers o los bots "buenos" entenderán el contenido alrededor del ancla, pero los Scrapers automáticos extraen masivamente todo lo que inicie por `href="https...` y descartarán este tag. Cuando el usuario hace clic, JavaScript lo decodifica usando `atob` en tiempo de ejecución.

## Diccionario de Enlaces de Uso Frecuente
Para agilizar el proceso, aquí están los Base64 de las URLs principales de Economía IA:

* **TikTok Economía IA** (`https://www.tiktok.com/@economiaia`): 
  `aHR0cHM6Ly93d3cudGlrdG9rLmNvbS9AZWNvbm9taWFpYQ==`
* **WhatsApp Ventas IA** (`https://wa.me/573059293414`): 
  `aHR0cHM6Ly93YS5tZS81NzMwNTkyOTM0MTQ=`

## Script de Remediación
Si sospechas que se corrompió la base de código o que el cliente escribió los links en plano manualmente, puedes invocar el script de autocorrección `obfuscate_links.py` que se encuentra en la raíz de `resources` usando:
`python obfuscate_links.py`
