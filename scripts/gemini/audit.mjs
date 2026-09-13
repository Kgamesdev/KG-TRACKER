import { GoogleGenAI } from "@google/genai";
import fs from "node:fs";

const CONTEXT_FILE = "./CONTEXTO_PROYECTO.md";

if (!process.env.GEMINI_API_KEY) {
    console.error("ERROR: GEMINI_API_KEY no está configurada.");
    process.exit(1);
}

if (!fs.existsSync(CONTEXT_FILE)) {
    console.error(`ERROR: No existe ${CONTEXT_FILE}`);
    process.exit(1);
}

const context = fs.readFileSync(CONTEXT_FILE, "utf8");

const prompt = `
Eres un ingeniero de software senior especializado en auditorías técnicas profundas.

Debes analizar el proyecto KG Tracker utilizando EXCLUSIVAMENTE el contexto proporcionado.

IMPORTANTE:
- NO modifiques ningún archivo.
- NO inventes información.
- Distingue claramente entre hechos confirmados e hipótesis.
- Prioriza problemas reales sobre recomendaciones cosméticas.
- Busca bugs, errores de arquitectura, problemas de seguridad, rendimiento,
  mantenibilidad, dependencias, manejo de errores, concurrencia, persistencia,
  APIs, UI/PySide6 y calidad general del código.
- Clasifica cada hallazgo:
  P0 = crítico
  P1 = alto
  P2 = medio
  P3 = bajo
  P4 = mejora/opcional.
- Explica por qué cada problema importa.
- Propón una solución concreta y pragmática.
- No hagas overengineering.

FORMATO DEL INFORME:

# AUDITORÍA TÉCNICA — KG TRACKER

## 1. Resumen ejecutivo
## 2. Arquitectura detectada
## 3. Hallazgos críticos P0
## 4. Hallazgos P1
## 5. Hallazgos P2
## 6. Hallazgos P3/P4
## 7. Seguridad
## 8. Rendimiento
## 9. PySide6 / UI
## 10. APIs, red y persistencia
## 11. Dependencias
## 12. Testing
## 13. Mantenibilidad
## 14. Deuda técnica
## 15. Plan de acción priorizado
## 16. Conclusión

Para cada hallazgo importante utiliza:

### [P0/P1/P2/P3/P4] Título
- Evidencia:
- Problema:
- Impacto:
- Causa probable:
- Solución recomendada:
- Prioridad:

CONTEXTO DEL PROYECTO:

${context}
`;

console.log("Enviando auditoría a Gemini...");
console.log(`Contexto: ${context.length.toLocaleString()} caracteres`);

const ai = new GoogleGenAI({});

const response = await ai.models.generateContent({
    model: "gemini-3.6-flash",
    contents: prompt,
});

const output = response.text ?? "";

if (!output.trim()) {
    console.error("ERROR: Gemini no devolvió contenido.");
    process.exit(1);
}

const timestamp = new Date().toISOString()
    .replace(/[:.]/g, "-");

const outputFile = `./scripts/gemini/AUDITORIA_${timestamp}.md`;

fs.writeFileSync(outputFile, output, "utf8");

console.log("");
console.log("========================================");
console.log("AUDITORÍA COMPLETADA");
console.log("========================================");
console.log(`Informe: ${outputFile}`);
console.log("");
