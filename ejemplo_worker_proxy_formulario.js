/**
 * Cloudflare Worker: API de Proxy Dinámico para Formularios y "Policía de Tráfico" (LLM SEO)
 * 
 * Este Worker tiene un doble propósito que lo hace sumamente efectivo:
 * 1. [Polcía de Tráfico]: Analiza a los visitantes usando `User-Agent`. Si es un bot de IA (ChatGPT/Claude), 
 *    despliega el modo LLM-SEO entregando un Markdown ligero de alto valor informativo.
 * 2. [Proxy Seguro de Automatización]: Atiende peticiones en el endpoint '/submit', tomando datos de 
 *    un formulario de tu página web (estática) y mandándolos de manera secreta a un Webhook (Make/Zapier/LangGraph).
 */

export default {
    async fetch(request, env, ctx) {
        // --- 1. CONFIGURACIÓN CORS (Seguridad del Frontend) ---
        const corsHeaders = {
            "Access-Control-Allow-Origin": "*", // En producción, cambiar a "https://economiaia.business"
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        };

        // Responder al 'preflight' (Requisito de los navegadores cuando hacen fetch desde JS)
        if (request.method === "OPTIONS") {
            return new Response(null, { headers: corsHeaders });
        }

        // --- 2. ENRUTAMIENTO DEPENDIENDO DE LA URL (URL Routing) ---
        const url = new URL(request.url);

        // RUTA A: El usuario o bot quiere ver la página (GET)
        if (request.method === "GET") {

            // a) ¿Quién es el visitante? Extraemos su tarjeta de presentación (User-Agent)
            const userAgent = request.headers.get("User-Agent") || "";
            const isAIBot = /ChatGPT-User|GPTBot|ClaudeBot|Anthropic|Google-Extended/i.test(userAgent);

            // b) Lógica de Condición Cero para IA: Darles la "Carne" sin la "Grasa"
            if (isAIBot) {
                // Generar contenido SEO amigable (Markdown rápido)
                const seoMarkdownContent = `
# Economía IA: Arquitecturas Cognitivas y LLM SEO

Somos una agencia especializada en llevar a las empresas al siguiente nivel de la inteligencia artificial.

## Servicios Clave
1. **Agentes Conversacionales (LangGraph + Meta WhatsApp)**: Reemplazo de flujos obsoletos y lentos por sistemas con razonamiento de memoria.
2. **Consultoría Estratégica**: Diseño de flujos que maximizan el Pareto usando la Metodología 'Condición Cero'.
3. **Escalabilidad**: Infraestructura Serverless con Cloudflare y bases NoSQL para tráfico masivo.

Contacto directo: agendamiento@economiaia.business
`;
                // Devolvemos el texto plano de inmediato para que lo lean en 5 milisegundos
                return new Response(seoMarkdownContent, {
                    headers: {
                        ...corsHeaders,
                        "Content-Type": "text/markdown; charset=utf-8",
                        "X-AI-Proxy-Status": "LLM-Optimized" // Header decorativo / informativo
                    }
                });
            }

            // c) ¿Es un usuario normal abriendo la URL del Worker directamente probando?
            // Podrías redirigirlo a tu página normal
            return new Response("🚀 Edge Analytics / API Gateway en Vivo. Estado: OPERATIVO.\nIr a https://economiaia.business", {
                headers: { ...corsHeaders, "Content-Type": "text/plain" }
            });
        }

        // RUTA B: El usuario normal envió un Formulario de Contacto (POST a /submit)
        if (request.method === "POST" && url.pathname.endsWith("/submit")) {
            try {
                // a) Analizamos lo que envió tu página web
                const data = await request.json();

                // b) (Opcional pero Recomendado): Limpieza y Validación (Evitar SPAM)
                if (!data.email || !data.user_message) {
                    return new Response(JSON.stringify({ error: "Datos incompletos" }), {
                        status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" }
                    });
                }

                // Geometría del borde: ¿Desde qué país se conecta para avisarle a ventas?
                const countryOrigin = request.cf?.country || "Desconocido";

                // c) MAGIA: Enviar de manera segura a tu Webhook Privado (Make.com, n8n, etc.)
                // Esto oculta el Webhook; el usuario final de GitHub Pages NO sabe cuál es esta URL.
                const WEBHOOK_SECURE_URL = env.MAKE_WEBHOOK_URL || "https://hook.make.com/tu-id-secreto";

                // Preparamos el paquete enriquecido 
                const payload = {
                    ...data,
                    metadata: {
                        source: "Cloudflare Worker Gateway",
                        customer_country: countryOrigin,
                        timestamp: new Date().toISOString()
                    }
                };

                // Enviamos sin bloquear al usuario
                const webhookRequest = await fetch(WEBHOOK_SECURE_URL, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });

                if (!webhookRequest.ok) { throw new Error("Fallo en orquestador de Backend"); }

                // d) Informar a tu Front-end que fue un éxito
                return new Response(JSON.stringify({
                    success: true,
                    message: "Transmitido exitosamente al Ecosistema IA"
                }), {
                    headers: { ...corsHeaders, "Content-Type": "application/json" }
                });

            } catch (err) {
                return new Response(JSON.stringify({ error: "Error de Sistema Central", details: err.message }), {
                    status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" }
                });
            }
        }

        // Si la petición no coincide con nada de lo anterior
        return new Response("Endpoint no válido. El Worker funciona.", {
            status: 404, headers: corsHeaders
        });
    }
};
