import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime

# Carrega variáveis do .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Inicializa cliente da Groq
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

@app.route('/analyze', methods=['POST'])
def analyze_transcript():
    data = request.get_json()

    if not data or 'transcription' not in data or 'emotion_analysis' not in data:
        print("❌ Dados incompletos recebidos.")
        return jsonify({"error": "Transcrição e análise emocional são obrigatórias."}), 400

    transcription = data['transcription']
    emotion_analysis = data['emotion_analysis']

    print("\n📥 Dados recebidos com sucesso:")
    print("📝 Transcrição:", transcription[:100], "...")  # Exibe só os primeiros 100 chars
    print("😶‍🌫️ Análise emocional:", emotion_analysis)

    # Prompt combinando os dois contextos
    prompt = f"""
    Você é um assistente inteligente. Abaixo está a transcrição de uma apresentação em vídeo, seguida da análise de emoções detectadas no rosto da pessoa durante a apresentação.

    Seu trabalho é:
    - Resumir o conteúdo da apresentação.
    - Comentar sobre o tom emocional observado.
    - Sugerir melhorias para o roteiro e a entrega, com foco em evitar emoções negativas como raiva, tristeza, desânimo, etc.

    Transcrição:
    \"\"\"{transcription}\"\"\"

    Análise facial de emoções:
    \"\"\"{emotion_analysis}\"\"\"
    """

    try:
        print("🤖 Enviando dados para a IA da Groq...")
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
        )

        ai_response = chat_completion.choices[0].message.content
        print("✅ Resposta recebida da IA.")
        print("📤 Enviando resposta para o frontend.\n")

        # Log opcional
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()}:\nTranscrição: {transcription}\nEmoções: {emotion_analysis}\nResposta: {ai_response}\n\n")

        return jsonify({"response": ai_response}), 200

    except Exception as e:
        print("❌ Erro ao chamar a IA da Groq:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("🚀 API de Análise (Groq) iniciada em http://localhost:5001")
    app.run(port=5001, debug=True)
