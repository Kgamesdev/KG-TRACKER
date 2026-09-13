import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

const response = await ai.models.generateContent({
    model: "gemini-3.6-flash",
    contents: "Responde únicamente: GEMINI OK",
});

console.log(response.text);

