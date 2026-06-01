from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pdf_generator import generate_survey_pdf
import io
import os

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    lang = data.get('lang', 'es')
    try:
        pdf_bytes = generate_survey_pdf(data, lang)
        client_name = data.get('client', 'survey').replace(' ', '_')
        filename = f"{client_name}_Survey_{lang.upper()}.pdf"
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
