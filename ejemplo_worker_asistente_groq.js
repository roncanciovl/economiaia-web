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
            // 2. Extraer la pregunta y el contexto de la página desde el body del request
            const { user_question, page_context } = await request.json();

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
                - Número de contacto o WhatsApp: +57-304-365-6226.
                - Filosofía "Condición Cero": No le cobramos al cliente si no generamos valor exponencial.
                
                Información de la Página Actual del Usuario (RAG Local):
                ${page_context ?
                    `El usuario está leyendo actualmente esta información en la pantalla:\n"""${page_context}"""\nUtiliza esta información para darle una respuesta ultra-precisa sobre el tema específico que está viendo.`
                    : "No hay contexto adicional de la página."}
                
                Instrucciones:
                - Responde a la siguiente pregunta del usuario de manera amable y muy breve (máximo 2 párrafos cortos).
                - Basa tus respuestas en el Contexto Base y en la Información de la Página Actual.
                - Si la pregunta no se puede responder con este contexto, guía la conversación hacia una agenda de consultoría IA al número de contacto de Economía IA.
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
                    model: "llama3-8b-8192", // Modelo ultra-rápido de Llama 3 en Groq
                    messages: [
                        { role: "system", content: systemPrompt },
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
