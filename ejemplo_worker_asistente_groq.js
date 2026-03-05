/**
 * Cloudflare Worker: Asistente IA conectado a Groq (Llama 3)
 * 
 * PROPÓSITO:
 * Este worker recibe una pregunta desde el frontend (GitHub Pages), 
 * le inyecta el contexto de tu negocio (Economía IA) como System Prompt,
 * hace la llamada segura a la API rápida de Groq y devuelve la respuesta.
 * 
 * SEGURIDAD:
 * La llave de Groq (GROQ_API_KEY) vive de forma segura en las variables 
 * de entorno de Cloudflare. Nadie que inspeccione tu página web podrá verla ni robarla.
 */

export default {
    async fetch(request, env, ctx) {
        // 1. Configuración de Seguridad y CORS (Para GitHub Pages)
        const corsHeaders = {
            "Access-Control-Allow-Origin": "*", // O "https://economiaia.business"
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        };

        if (request.method === "OPTIONS") {
            return new Response(null, { headers: corsHeaders });
        }

        // Solo aceptamos POST para preguntas
        if (request.method !== "POST") {
            return new Response("Método no permitido. Usa POST para enviar preguntas al asistente.", {
                status: 405, headers: corsHeaders
            });
        }

        try {
            // 2. Extraer la pregunta, el contexto de la página y el historial de la conversación
            const { user_question, page_context, chat_history } = await request.json();

            if (!user_question) {
                return new Response(JSON.stringify({ error: "Falta la pregunta del usuario" }), {
                    status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" }
                });
            }

            // 3. El "Cerebro" / Contexto Dinámico (RAG Local Inyectado)
            const systemPrompt = `
                Eres "Sigma", el estratega de IA oficial del acelerador de negocios "Economía IA".
                Tu tono es audaz, ultra-estratégico y analítico. No eres un chatbot de soporte ni una agencia convencional; eres un motor de aceleración cognitiva. Utiliza la filosofía de "Condición Cero": solo importa la generación de valor exponencial y la eliminación total de la fricción e ineficiencia.
                
                Contexto Base:
                - Aceleramos empresas escalándolas con automatizaciones cognitivas (Vertex AI, Groq, Llama 3).
                - Reemplazamos chatbots de árbol de decisión obsoletos por Agentes con Razonamiento Real.
                - Somos expertos en 'LLM SEO' y WhatsApp Agents.
                - Contacto oficial: WhatsApp. Cuando el usuario requiera hablar con un humano o profundizar, DEBES generar un enlace de WhatsApp dinámico en formato Markdown. 
                  Ejemplo: [Hablar con Estratega en WhatsApp](https://wa.me/573043656226?text=Hola%20Sigma%2C%20estoy%20listo%20para%20acelerar%20mi%20negocio%20con%20[TEMA]).
                  Personaliza el parámetro "text" para que el estratega sepa el contexto exacto. No uses el número como texto plano.
                - Filosofía "Condición Cero": No facturamos si no demostramos el potencial de valor exponencial.
                
                Información de la Página Actual (RAG Local):
                ${page_context ?
                    `El usuario está analizando actualmente esto en pantalla:\n"""${page_context}"""\nUtiliza esta data para tus diagnósticos y recomendaciones.`
                    : "No hay contexto adicional de la página."}

                Mapa del Ecosistema (Conocimiento Global):
                Si el usuario pregunta por un tema, usa esta guía para responder y dar el link Markdown [Nombre](URL):
                - Hub Central: https://economiaia.business/index.html (Punto de entrada y mapa orbital del ecosistema).
                - Núcleo Economía IA: https://economiaia.business/nucleo_economia_ia.html (Las 6 leyes científicas de ventas: Matchmaking, Fricción, Señalización, Upselling, Escasez y Predicción).
                - Oferta Irresistible (Condición Cero): https://economiaia.business/presentacion_condicion_cero.html (Metodología para crear propuestas de valor irrechazables).
                - Teoría Señal Creativa: https://economiaia.business/teoria_senal_creativa.html (Zero-Targeting y creación de anuncios que atraen clientes por su contenido, no por segmentación manual).
                - Agentes Conversacionales: https://economiaia.business/agentes_conversacionales_ia.html (Sistemas de texto y voz basados en LLMs para ventas y atención autónoma).
                - Ecosistema Meta: https://economiaia.business/ecosistema_meta_ia.html (Orquestación de WhatsApp, FB e IG con Meta Advantage+).
                - Arquitectura ManyChat: https://economiaia.business/arquitectura_manychat_ia.html (Automatización de DMs y captura de leads).
                - Estrategia TikTok IA: https://economiaia.business/estrategia_tiktok_ia.html (TikTok como motor de búsqueda y distribución algorítmica).
                - Psicología del Precio: https://economiaia.business/psicologia_precio_regla_oro.html (El precio como señal estratégica y la Regla de Oro del pricing).
                - Tráfico LLM SEO: https://economiaia.business/trafico_llm_seo.html (Monitor en vivo de visibilidad en motores de IA como Perplexity o ChatGPT).
                - Stack Tecnológico: https://economiaia.business/stack_tecnologico_ia.html (Herramientas esenciales: Canva, ManyChat, Meta, Groq).
                
                Instrucciones Cruciales:
                1. NO expliques todo en el chat. Tu objetivo es actuar como un **Navegador Estratégico**. Da una respuesta breve e impactante (máximo 1 párrafo) y redirige INMEDIATAMENTE al usuario a la página específica del ecosistema que resuelve su duda usando el [Nombre](URL) del mapa previo.
                2. Sé audaz y autoritario. Si el usuario pregunta algo general, dale una "píldora" de sabiduría y di: "Para implementar esto a fondo, analiza nuestra sección de [TEMA](URL)".
                3. CIERRE OBLIGATORIO: Todas, absolutamente todas tus respuestas deben terminar con una invitación a la acción (CTA) hacia WhatsApp. 
                   Formato de cierre: "Si estás listo para acelerar tu negocio ahora, [Habla con un Estratega en WhatsApp](https://wa.me/573043656226?text=Hola%20Sigma%2C%20estoy%20viendo%20la%20página%20de%20[PAGINA_ACTUAL]%20y%20quiero%20acelerar%20mis%20resultados)."
                
                Formato:
                - Usa Markdown (**negritas**, [links](url)).
                - Máximo 2 párrafos en total (Respuesta + Cierre).
            `;


            // 4. Preparar la llamada a la API de Groq
            // Asegúrate de tener GROQ_API_KEY configurada en los Settings del Worker -> Variables
            const groqApiKey = env.GROQ_API_KEY;

            if (!groqApiKey) {
                throw new Error("No se ha configurado la variable de entorno GROQ_API_KEY en Cloudflare.");
            }

            const groqResponse = await fetch("https://api.groq.com/openai/v1/chat/completions", {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${groqApiKey}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    model: "llama-3.3-70b-versatile", // Modelo avanzado y versátil de Llama 3 en Groq
                    messages: [
                        { role: "system", content: systemPrompt },
                        ...(chat_history || []),
                        { role: "user", content: user_question }
                    ],
                    temperature: 0.3, // Baja temperatura para respuestas más precisas y corporativas
                    max_tokens: 500
                })
            });

            if (!groqResponse.ok) {
                const errorData = await groqResponse.text();
                throw new Error(`Error de la API de Groq: ${errorData}`);
            }

            const data = await groqResponse.json();
            const assistantAnswer = data.choices[0].message.content;

            // 5. Devolver la respuesta al Frontend (Tu HTML)
            return new Response(JSON.stringify({
                answer: assistantAnswer
            }), {
                headers: { ...corsHeaders, "Content-Type": "application/json" }
            });

        } catch (err) {
            console.error("Error en Asistente Worker:", err);
            return new Response(JSON.stringify({
                error: "Ocurrió un error procesando tu solicitud.",
                details: err.message
            }), {
                status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" }
            });
        }
    }
};
