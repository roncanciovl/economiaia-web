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
                Eres "Sigma", el asistente de IA oficial de la agencia "Economía IA".
                Tu tono es profesional, conciso y orientado a los negocios (estilo Condición Cero).
                
                Contexto Base de la Agencia:
                - Ayudamos a empresas a escalar con automatizaciones cognitivas (Vertex AI, Groq, Llama 3).
                - Reemplazamos chatbots de árbol de decisión viejos por Agentes con razonamiento.
                - Optimizamos en 'LLM SEO' y WhatsApp Agents.
                - Contacto oficial: WhatsApp. Cuando ofrezcas contactar a la agencia o a un humano, DEBES generar un enlace de WhatsApp dinámico en formato Markdown. 
                  Ejemplo base: [Hablar con Asesor en WhatsApp](https://wa.me/573043656226?text=Hola%20Sigma%2C%20estoy%20interesado%20en%20[TEMA]).
                  Personaliza el parámetro "text" (mensaje pre-llenado) para que el asesor sepa exactamente qué estaba preguntando el usuario (ej: "...interesado en el servicio de TikTok" o "...info sobre el Nucleo"). Asegúrate de usar %20 para los espacios. ¡Nunca menciones el número de teléfono como texto formato plano!
                - Filosofía "Condición Cero": No le cobramos al cliente si no generamos valor exponencial.
                
                Información de la Página Actual del Usuario (RAG Local):
                ${page_context ?
                    `El usuario está leyendo actualmente esta información en la pantalla:\n"""${page_context}"""\nUtiliza esta información para identificar respuestas.`
                    : "No hay contexto adicional de la página."}

                Mapa del Ecosistema (Páginas para Recomendar):
                Si el usuario pregunta por un tema cubierto en otra página, menciónala e inyecta el hipervínculo en formato Markdown [Nombre](URL).
                - Hub Central (Bio/Home): https://economiaia.business/index.html
                - Núcleo (6 Leyes): https://economiaia.business/nucleo_economia_ia.html
                - Oferta Irresistible (Condición Cero): https://economiaia.business/presentacion_condicion_cero.html
                - Teoría Señal Creativa (TikTok Ads): https://economiaia.business/teoria_senal_creativa.html
                - Agentes Conversacionales (Chatbots IA): https://economiaia.business/agentes_conversacionales_ia.html
                - Ecosistema Meta (WhatsApp/FB/IG): https://economiaia.business/ecosistema_meta_ia.html
                - Arquitectura ManyChat: https://economiaia.business/arquitectura_manychat_ia.html
                - Estrategia TikTok IA: https://economiaia.business/estrategia_tiktok_ia.html
                - Psicología del Precio: https://economiaia.business/psicologia_precio_regla_oro.html
                - Tráfico LLM SEO (Tracker): https://economiaia.business/trafico_llm_seo.html
                
                Instrucciones:
                - Responde de manera amable y muy breve (máximo 2 párrafos cortos).
                - Basa tus respuestas en el Contexto Base y en la Información de la Página Actual.
                - Tus respuestas serán procesadas como Markdown. Utiliza **asteriscos dobles** para enfatizar palabras clave y usa formato [texto](url) para enlaces.
                - Si mencionas un servicio o página del mapa anterior, DEBES poner el link.
                - Si la pregunta no se puede responder, guía la conversación cortésmente hacia nuestro WhatsApp usando el link proporcionado arriba.
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
                    max_tokens: 300
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
