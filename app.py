import os
import uuid
import json
from flask import Flask, request, jsonify, send_file
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime

app = Flask(__name__)

# Configuração básica
API_KEY = os.environ.get('API_KEY', 'your-default-api-key')  # Definir no Azure App Service
TEMP_FOLDER = os.environ.get('TEMP_FOLDER', 'temp')

# Garantir que a pasta temp exista
if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)

def verify_api_key():
    """Verifica se a requisição contém a chave API válida."""
    provided_key = request.headers.get('X-API-Key')
    return provided_key == API_KEY

def generate_pdf(data):
    """Gera um PDF com os dados recebidos."""
    # Criar nome de arquivo único
    filename = f"{TEMP_FOLDER}/document_{uuid.uuid4()}.pdf"
    
    # Criar o PDF
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Relatório Gerado")
    
    # Data e hora
    c.setFont("Helvetica", 12)
    now = datetime.now()
    c.drawString(50, height - 80, f"Gerado em: {now.strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Conteúdo dinâmico baseado nos dados recebidos
    y_position = height - 120
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "Dados Recebidos:")
    y_position -= 20
    
    c.setFont("Helvetica", 10)
    for key, value in data.items():
        if y_position < 50:  # Verificar espaço na página
            c.showPage()  # Nova página
            y_position = height - 50
            
        text_line = f"{key}: {value}"
        c.drawString(50, y_position, text_line)
        y_position -= 15
    
    # Finalizar o PDF
    c.save()
    return filename

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificação de saúde da aplicação."""
    return jsonify({"status": "ok"})

@app.route('/generate-pdf', methods=['POST'])
def create_pdf():
    """Endpoint para gerar PDF a partir dos dados recebidos."""
    # Verificar API Key
    if not verify_api_key():
        return jsonify({"error": "Unauthorized access"}), 401
    
    # Verificar se há dados JSON
    if not request.is_json:
        return jsonify({"error": "Missing JSON data"}), 400
    
    try:
        data = request.json
        pdf_path = generate_pdf(data)
        
        # Retornar o PDF como resposta
        return send_file(pdf_path, 
                         mimetype='application/pdf',
                         as_attachment=True,
                         download_name='generated_document.pdf')
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Limpar arquivos temporários (opcional, pode remover se quiser manter histórico)
        try:
            if 'pdf_path' in locals() and os.path.exists(pdf_path):
                os.remove(pdf_path)
        except:
            pass

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 