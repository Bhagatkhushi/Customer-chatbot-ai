import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = (
    "You are a friendly customer support chatbot for an e-commerce website. "
    "Reply VERY SHORT (1-2 sentences max), helpful, polite, and use relevant "
    "emojis. If the user asks about orders, payments, returns, or delivery, "
    "give practical, realistic guidance."
)

model = genai.GenerativeModel(
    model_name="gemini-3.5-flash-lite",
    system_instruction=SYSTEM_PROMPT,
)

# Fallback models to try if the primary one is unavailable/retired.
FALLBACK_MODEL_NAMES = ["gemini-3.6-flash", "gemini-flash-latest"]


def get_response(user_input: str) -> str:
    if not user_input or not user_input.strip():
        return "Please type something so I can help you! 🙂"

    models_to_try = [model.model_name] + FALLBACK_MODEL_NAMES
    last_error = None

    for model_name in models_to_try:
        try:
            m = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=SYSTEM_PROMPT,
            )
            response = m.generate_content(
                user_input,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=100,  # shorter = faster response
                ),
            )
            return response.text
        except Exception as e:
            last_error = e
            continue

    return "⚠️ Sorry, I'm having trouble connecting right now. Error: " + str(last_error)