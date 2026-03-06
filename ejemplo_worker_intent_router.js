/**
 * Cloudflare Worker: Intent Router para Sigma / Economia IA
 *
 * Uso:
 * - Endpoint: POST /api/intent
 * - Entrada: señales de pagina + sesion + ultimo mensaje de chat
 * - Salida: estado de intencion, CTA recomendado y contexto para Sigma
 */

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

const COMMERCIAL_KEYWORDS = [
  "precio",
  "precios",
  "plan",
  "planes",
  "servicio",
  "servicios",
  "contratar",
  "implementacion",
  "implementar",
  "auditoria",
  "consultoria",
  "hablar con alguien",
  "whatsapp",
  "demo",
  "propuesta",
  "cuanto cuesta",
];

const DIAGNOSTIC_KEYWORDS = [
  "me sirve",
  "mi negocio",
  "como aplico",
  "tengo leads",
  "no convierto",
  "automatizar",
  "embudo",
  "cual me conviene",
  "cuello de botella",
];

const SIGNAL_KEYWORDS = [
  "que es",
  "como funciona",
  "explicame",
  "teoria",
  "aprender",
  "entender",
  "diferencia",
];

const ALLOWED_INTENTS = new Set(["signal", "diagnostic", "commercial"]);
const ALLOWED_PLANS = new Set(["Starter", "Growth", "Aceleracion", "Consultoria Express"]);

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      ...CORS_HEADERS,
      "Content-Type": "application/json; charset=utf-8",
    },
  });
}

function normalizeText(input) {
  return String(input || "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .trim();
}

function containsAny(text, keywords) {
  return keywords.some((keyword) => text.includes(keyword));
}

function safeNumber(value, fallback = 0) {
  return Number.isFinite(Number(value)) ? Number(value) : fallback;
}

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}

function scoreIntentFallback(payload) {
  const path = normalizeText(payload.path);
  const message = normalizeText(payload.chat?.last_user_message);
  const events = Array.isArray(payload.events) ? payload.events.map(normalizeText) : [];
  const session = payload.session || {};

  let signal = 0;
  let diagnostic = 0;
  let commercial = 0;

  if (
    path.includes("nucleo") ||
    path.includes("teoria") ||
    path.includes("arquitectura") ||
    path.includes("stack")
  ) {
    signal += 2;
  }
  if (path.includes("precios")) {
    commercial += 6;
  }
  if (path.includes("agentes_conversacionales")) {
    diagnostic += 2;
  }

  if (safeNumber(session.pages_viewed) >= 2) {
    signal += 1;
  }
  if (Boolean(session.chat_opened)) {
    diagnostic += 3;
  }
  if (safeNumber(session.time_on_site_sec) > 120) {
    diagnostic += 2;
  }
  if (safeNumber(session.scroll_depth) > 0.6) {
    diagnostic += 1;
  }
  if (Boolean(session.pricing_visited)) {
    commercial += 2;
  }
  if (safeNumber(session.whatsapp_clicks) > 0) {
    commercial += 3;
  }

  if (events.includes("view_pricing")) {
    commercial += 3;
  }
  if (events.includes("open_chat")) {
    diagnostic += 2;
  }
  if (events.includes("click_commercial_cta")) {
    commercial += 4;
  }

  if (containsAny(message, SIGNAL_KEYWORDS)) {
    signal += 2;
  }
  if (containsAny(message, DIAGNOSTIC_KEYWORDS)) {
    diagnostic += 4;
  }
  if (containsAny(message, COMMERCIAL_KEYWORDS)) {
    commercial += 6;
  }

  return { signal, diagnostic, commercial };
}

function resolveIntentState(scores) {
  if (scores.commercial >= 6) {
    return "commercial";
  }
  if (scores.diagnostic >= 4) {
    return "diagnostic";
  }
  return "signal";
}

function computeConfidence(scores, state) {
  const total = scores.signal + scores.diagnostic + scores.commercial;
  if (total <= 0) {
    return 0.5;
  }
  const selected = safeNumber(scores[state], 0);
  return Math.max(0.5, Math.min(0.99, selected / total));
}

function detectPainAngle(path, message) {
  const text = `${normalizeText(path)} ${normalizeText(message)}`;
  if (text.includes("whatsapp") || text.includes("responder")) {
    return "friccion_operativa_en_whatsapp";
  }
  if (text.includes("precio") || text.includes("plan")) {
    return "comparacion_de_planes_e_inversion";
  }
  if (text.includes("trafico") || text.includes("leads")) {
    return "captura_y_conversion_de_demanda";
  }
  return "claridad_estrategica";
}

function pickPlan(state, path, message) {
  if (state !== "commercial") {
    return null;
  }

  const text = `${normalizeText(path)} ${normalizeText(message)}`;
  if (text.includes("empresa") || text.includes("equipo") || text.includes("crm")) {
    return "Aceleracion";
  }
  if (text.includes("whatsapp") || text.includes("catalogo") || text.includes("pagos")) {
    return "Growth";
  }
  if (text.includes("autonomo") || text.includes("micro") || text.includes("emprendedor")) {
    return "Starter";
  }
  return "Growth";
}

function buildWhatsAppUrl(message) {
  return `https://wa.me/573043656226?text=${encodeURIComponent(message)}`;
}

function buildCtas(state, recommendedPlan, painAngle) {
  if (state === "commercial") {
    const planName = recommendedPlan || "Growth";
    const primaryText = `Hola Sigma, quiero avanzar con ${planName}. Llego por ${painAngle}.`;
    return {
      primary: {
        label: "Solicitar auditoria por WhatsApp",
        url: buildWhatsAppUrl(primaryText),
      },
      secondary: {
        label: "Ver comparativa de planes",
        url: "/precios_y_planes_ia.html",
      },
    };
  }

  if (state === "diagnostic") {
    return {
      primary: {
        label: "Ver arquitectura recomendada",
        url: "/arquitectura_marketing_ia.html",
      },
      secondary: {
        label: "Comparar planes",
        url: "/precios_y_planes_ia.html",
      },
    };
  }

  return {
    primary: {
      label: "Explorar el nucleo",
      url: "/nucleo_economia_ia.html",
    },
    secondary: {
      label: "Ver oferta irresistible",
      url: "/presentacion_condicion_cero.html",
    },
  };
}

function buildSigmaOpening(state, painAngle) {
  if (state === "commercial") {
    return `Si tu dolor principal es ${painAngle.replaceAll("_", " ")}, el siguiente paso es elegir plan y ejecutar sin friccion.`;
  }
  if (state === "diagnostic") {
    return "Antes de hablar de herramientas, definamos tu cuello de botella exacto para recomendar la arquitectura correcta.";
  }
  return "Te guio por el ecosistema para que entiendas la estrategia antes de tomar una decision comercial.";
}

function buildNextPage(state, painAngle) {
  if (state === "commercial") {
    return "/precios_y_planes_ia.html";
  }
  if (state === "diagnostic") {
    if (painAngle === "friccion_operativa_en_whatsapp") {
      return "/agentes_conversacionales_ia.html";
    }
    return "/arquitectura_marketing_ia.html";
  }
  return "/nucleo_economia_ia.html";
}

function buildProofHint(state, painAngle) {
  if (state === "commercial") {
    return "mostrar_prueba_de_implementacion_y_garantia_operativa";
  }
  if (state === "diagnostic" && painAngle === "friccion_operativa_en_whatsapp") {
    return "mostrar_caso_de_reduccion_de_tiempos_de_respuesta";
  }
  return "mostrar_marco_estrategico_de_6_leyes";
}

function buildIntentFromRules(payload) {
  const scores = scoreIntentFallback(payload);
  const intentState = resolveIntentState(scores);
  const painAngle = detectPainAngle(payload.path, payload.chat?.last_user_message);
  const recommendedPlan = pickPlan(intentState, payload.path, payload.chat?.last_user_message);

  return {
    intent_state: intentState,
    intent_confidence: computeConfidence(scores, intentState),
    scores,
    pain_angle: painAngle,
    recommended_plan: recommendedPlan,
  };
}

function extractJsonObject(text) {
  if (typeof text !== "string") return null;
  const trimmed = text.trim();

  try {
    return JSON.parse(trimmed);
  } catch (_) {
    // continue
  }

  const match = trimmed.match(/\{[\s\S]*\}/);
  if (!match) return null;

  try {
    return JSON.parse(match[0]);
  } catch (_) {
    return null;
  }
}

function sanitizeModelIntent(raw, fallbackIntent) {
  if (!raw || typeof raw !== "object") return null;

  const normalizedIntent = normalizeText(raw.intent_state);
  const intentState = ALLOWED_INTENTS.has(normalizedIntent) ? normalizedIntent : null;
  if (!intentState) return null;

  const confidenceRaw = safeNumber(raw.intent_confidence, fallbackIntent.intent_confidence);
  const confidence = clamp(confidenceRaw, 0.5, 0.99);

  const painAngle = typeof raw.pain_angle === "string" && raw.pain_angle.trim().length
    ? normalizeText(raw.pain_angle).replaceAll(" ", "_")
    : fallbackIntent.pain_angle;

  let recommendedPlan = null;
  if (raw.recommended_plan === null || raw.recommended_plan === "null") {
    recommendedPlan = null;
  } else if (typeof raw.recommended_plan === "string") {
    const candidate = raw.recommended_plan.trim();
    const normalizedCandidate = normalizeText(candidate);
    if (ALLOWED_PLANS.has(candidate)) {
      recommendedPlan = candidate;
    } else if (normalizedCandidate === "aceleracion") {
      recommendedPlan = "Aceleracion";
    } else if (normalizedCandidate === "consultoria express") {
      recommendedPlan = "Consultoria Express";
    } else if (normalizedCandidate === "growth") {
      recommendedPlan = "Growth";
    } else if (normalizedCandidate === "starter") {
      recommendedPlan = "Starter";
    } else {
      recommendedPlan = fallbackIntent.recommended_plan;
    }
  } else {
    recommendedPlan = fallbackIntent.recommended_plan;
  }

  return {
    intent_state: intentState,
    intent_confidence: confidence,
    pain_angle: painAngle,
    recommended_plan: recommendedPlan,
    llm_reason: typeof raw.reason === "string" ? raw.reason.slice(0, 160) : null,
  };
}

async function inferIntentWithGroq(payload, env, fallbackIntent) {
  const groqApiKey = env.GROQ_API_KEY;
  if (!groqApiKey) return null;

  const model = env.GROQ_INTENT_MODEL || env.GROQ_MODEL || "llama-3.1-8b-instant";
  const timeoutMs = clamp(safeNumber(env.GROQ_INTENT_TIMEOUT_MS, 1400), 600, 3000);

  const userInput = {
    path: payload.path || "",
    referrer: payload.referrer || "",
    utm_source: payload.utm_source || "",
    utm_campaign: payload.utm_campaign || "",
    device: payload.device || "",
    session: payload.session || {},
    chat: payload.chat || {},
    events: Array.isArray(payload.events) ? payload.events : [],
  };

  const systemPrompt = [
    "Eres un clasificador de intencion comercial para un sitio de ventas/marketing.",
    "Debes responder SOLO con JSON valido, sin markdown, sin texto extra.",
    'Campos obligatorios: intent_state, intent_confidence, pain_angle, recommended_plan, reason.',
    'intent_state debe ser uno de: "signal", "diagnostic", "commercial".',
    "intent_confidence debe estar entre 0 y 1.",
    'recommended_plan debe ser uno de: "Starter", "Growth", "Aceleracion", "Consultoria Express", o null.',
    "No inventes campos adicionales.",
  ].join(" ");

  const userPrompt = [
    "Clasifica la intencion del siguiente visitante:",
    JSON.stringify(userInput),
    "Si hay evidencia de compra (precios/planes/servicios/implementacion), prioriza commercial.",
    "Si esta explorando teoria o navegacion general, usa signal.",
    "Si tiene un problema concreto pero aun sin pedir compra directa, usa diagnostic.",
  ].join("\n");

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${groqApiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model,
        temperature: 0,
        max_tokens: 180,
        response_format: { type: "json_object" },
        messages: [
          { role: "system", content: systemPrompt },
          { role: "user", content: userPrompt },
        ],
      }),
      signal: controller.signal,
    });

    if (!response.ok) {
      return null;
    }

    const data = await response.json();
    const content = data?.choices?.[0]?.message?.content;
    const parsed = typeof content === "object" ? content : extractJsonObject(content);
    return sanitizeModelIntent(parsed, fallbackIntent);
  } catch (_) {
    return null;
  } finally {
    clearTimeout(timeoutId);
  }
}

export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: CORS_HEADERS });
    }

    const url = new URL(request.url);
    if (request.method !== "POST" || !url.pathname.endsWith("/api/intent")) {
      return json({ error: "Endpoint no valido. Usa POST /api/intent" }, 404);
    }

    let payload = {};
    try {
      payload = await request.json();
    } catch {
      return json({ error: "JSON invalido" }, 400);
    }

    const fallbackIntent = buildIntentFromRules(payload);
    const modelIntent = await inferIntentWithGroq(payload, env, fallbackIntent);

    const intentState = modelIntent?.intent_state || fallbackIntent.intent_state;
    const confidence = modelIntent?.intent_confidence || fallbackIntent.intent_confidence;
    const painAngle = modelIntent?.pain_angle || fallbackIntent.pain_angle;
    const recommendedPlan = modelIntent?.recommended_plan !== undefined
      ? modelIntent.recommended_plan
      : fallbackIntent.recommended_plan;
    const ctas = buildCtas(intentState, recommendedPlan, painAngle);

    return json({
      intent_state: intentState,
      intent_confidence: confidence,
      scores: fallbackIntent.scores,
      pain_angle: painAngle,
      recommended_next_page: buildNextPage(intentState, painAngle),
      recommended_plan: recommendedPlan,
      cta_mode: intentState,
      primary_cta: ctas.primary,
      secondary_cta: ctas.secondary,
      sigma_mode: intentState === "commercial" ? "close_with_diagnosis" : intentState === "diagnostic" ? "diagnose" : "guide",
      sigma_opening: buildSigmaOpening(intentState, painAngle),
      proof_hint: buildProofHint(intentState, painAngle),
      inference_source: modelIntent ? "groq" : "fallback",
      llm_reason: modelIntent?.llm_reason || null,
    });
  },
};
