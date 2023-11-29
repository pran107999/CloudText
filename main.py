from flask import Flask, render_template, request, jsonify
from PyPDF2 import PdfReader
from google.cloud import secretmanager
from time import strftime
import openai
import google.cloud.logging
import logging


client = google.cloud.logging.Client()
client.setup_logging()

app = Flask(__name__)
summaries = {}

logging.basicConfig(level=logging.INFO)

def getOpenaiSecret():
    client = secretmanager.SecretManagerServiceClient()
    return client.access_secret_version(request={"name": "projects/1018379038222/secrets/OPENAI_API_KEY/versions/1"}).payload.data.decode("UTF-8")

openai.api_key = getOpenaiSecret()
MAX_TOKENS = 4000

@app.route('/')
def index():
    logging.info('Inside ' + index.__name__ + '()')
    try:
        return render_template('index1.html')
    except ValueError:
        logging.exception(index.__name__ + '(): ' + ValueError)

@app.route('/api/upload_and_summarize', methods=['POST'])
def upload_and_summarize():
    logging.info('Inside ' + upload_and_summarize.__name__+ '()')
    try:
        if 'file' in request.files:
            pdf_file = request.files['file']
            if pdf_file.filename != '':
    
                # Extract text from the uploaded PDF file
                content = extract_text_from_pdf(pdf_file)
    
                # Generate summary from the extracted text
                summary = generate_summary(content)
                summary_id = len(summaries) + 1
                summaries[summary_id] = summary
    
                return jsonify({'summary_id': summary_id})
        
        elif 'text' in request.json:
            text = request.json['text']
            if text:
                # Generate summary from the input text
                summary = generate_summary(text)
                summary_id = len(summaries) + 1
                summaries[summary_id] = summary
    
                return jsonify({'summary_id': summary_id})
        
        return jsonify({'error': 'Invalid input'})
    except ValueError:
        logging.exception(upload_and_summarize.__name__ + '(): ' + ValueError)

@app.route('/summary/<int:summary_id>')
def show_summary(summary_id):
    logging.info('Inside ' + show_summary.__name__+ '()')
    try:
        summary = summaries.get(summary_id)
        if summary:
            return render_template('summary1.html', summary=summary)
        else:
            return "Summary not found."
    except ValueError:
        logging.exception(show_summary.__name__ + '(): ' + 'summary_id ' + summary_id + ' ' + ValueError)

def extract_text_from_pdf(pdf_file):
    logging.info('Inside ' + extract_text_from_pdf.__name__+ '()')
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text
    except ValueError:
        logging.exception(extract_text_from_pdf.__name__ + '(): ' + ValueError)

def generate_summary(content):
    logging.info('Inside ' + generate_summary.__name__+ '()')
    try:
        chunks = [content[i:i + MAX_TOKENS] for i in range(0, len(content), MAX_TOKENS)]
        summaries = []
        for chunk in chunks:
            prompt = f"Summarize the following text:\n\n{chunk}"
    
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=150,
                temperature=0.9,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
            summary = response.choices[0].text.strip()
            summaries.append(summary)
    
        return ' '.join(summaries)
    except ValueError:
        logging.exception(generate_summary.__name__ + '(): ' + ValueError)

if __name__ == '__main__':
    app.run(debug=True)
