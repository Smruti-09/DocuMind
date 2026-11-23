import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "openai/gpt-4o-mini"
)


def generate_answer(question: str, context: str):

    prompt = f"""
You are an intelligent document analysis assistant.

Answer the user's question using ONLY the provided document context.

Instructions:
1. Answer only using information explicitly supported by the document context.
2. Do not introduce technologies, methods or facts absent from the context.
3. Preserve technical terminology exactly.
4. Never confuse GNN (Graph Neural Network) with GAN (Generative Adversarial Network).
5. Explain the core innovations separately from supporting infrastructure.
6. Do not guess missing information.
7. Use clear bullet points.
8. If information is unavailable, explicitly mention it.
9. If extracted text contains incomplete or corrupted phrases, do not guess their meaning. Omit them if they cannot be interpreted reliably.
10. Prefer complete, meaningful statements over incomplete PDF-extracted text.
11. When discussing extreme preservation, use the document's explicit statement:
    "Preserves critical rainfall and wind peaks."
    Do not interpret "preserving inference" as a technical feature.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content