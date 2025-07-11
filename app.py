from flask import Flask, render_template, request
from openai import OpenAI
import json

# ✅ Coloca aquí tu API Key directamente (solo para pruebas locales)
api_key = "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"  # ← reemplaza esto por tu API key

# Cliente OpenAI
client = OpenAI(api_key=api_key)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generar', methods=['POST'])
def generar():
    grado = request.form['grado']
    tema = request.form['tema']

    prompt = f"""
    Eres un profesor experto en física. Genera 20 preguntas tipo test para estudiantes de {grado} sobre el tema "{tema}".
	Cada pregunta debe tener un enunciado claro y educativo, con al menos 6 líneas explicativas.
	Cada pregunta debe incluir 4 opciones distintas (A, B, C, D).
	Agrega el índice de la opción correcta como "correctIndex".
	Si la pregunta es numérica, la solución debe incluir:
  	- Fórmula usada
  	- Desarrollo paso a paso
  	- Resultado final bien explicado
	Si la pregunta es teórica, la solución debe tener mínimo 4 líneas claras.

	Devuelve solo el resultado en JSON con este formato:
	[
  	    {{
    		"question": "Texto detallado de la pregunta...",
    		"options": ["A", "B", "C", "D"],
    		"correctIndex": 2,
    		"solution": "Solución completa explicada..."
  		}},
  		...
	]
	NO agregues explicaciones fuera del JSON.
	"""

    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        response_text = completion.choices[0].message.content.strip()

        # Limpiar si viene con triple comilla
        if response_text.startswith("```"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()

        preguntas = json.loads(response_text)

        return render_template('juego.html', preguntas=preguntas)

    except Exception as e:
        print("❌ Error:", e)
        return f"<h2>Error generando preguntas</h2><p>{str(e)}</p>"

if __name__ == '__main__':
    app.run(debug=True)
