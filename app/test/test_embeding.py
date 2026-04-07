import os
import tiktoken
from openai import OpenAI
from dotenv import load_dotenv

# cargar variables de entorno
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

texto = "Las ventas de la categoría uñas crecieron un 20% en marzo."

# Contar tokens
encoding = tiktoken.get_encoding("cl100k_base")
num_tokens = len(encoding.encode(texto))
print(f"Número de tokens: {num_tokens}")

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=texto
)

embedding = response.data[0].embedding

print("Longitud del vector:", len(embedding))
print("Primeros valores:", embedding[:10])
