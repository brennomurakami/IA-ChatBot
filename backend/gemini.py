import google.generativeai as genai
from flask import Flask
import os

# Inicialização do Flask
app = Flask(__name__)

# Configuração do Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

generation_config = {
    "temperature": 0.4,           # Controla a criatividade e a imprevisibilidade das respostas do modelo vai de 0 a 1 quanto mais próximo de 1 mais criativo a resposta é.
    "top_p": 1,                   # Parâmetro que controla a fluência e a coerência das respostas do modelo vai de 0 a 1 quanto mais próximo de 1 mais coerente a resposta é.
    "top_k": 1,                   # Filtro de tokens para considerar apenas os tokens mais prováveis. Quanto maior, mais restrito.
    "max_output_tokens": 2000,    # Limite máximo de tokens na saída gerada. Isso ajuda a evitar respostas muito longas.
}

model = genai.GenerativeModel('gemini-pro', generation_config=generation_config)
