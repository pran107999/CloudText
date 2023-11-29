from flask import Flask, render_template, request, jsonify
from PyPDF2 import PdfReader
import openai
import logging

app = Flask(__name__)
summaries = {}

logging.basicConfig(filename='app.log',level=logging.DEBUG, format='%(asctime)s %(levelname)s %(threadName)s : %(message)s')

openai.api_key = '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'
MAX_TOKENS = 4000

@app.route('/')
def index():
    logging.info('Inside' + index.__name__ + '()')
    return render_template('index1.html')

@app.route('/api/upload_and_summarize', methods=['POST'])
def upload_and_summarize():
    logging.info('Inside' + upload_and_summarize.__name__+ '()')
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

@app.route('/summary/<int:summary_id>')
def show_summary(summary_id):
    logging.info('Inside' + show_summary.__name__+ '()')
    summary = summaries.get(summary_id)
    if summary:
        return render_template('summary1.html', summary=summary)
    else:
        return "Summary not found."

def extract_text_from_pdf(pdf_file):
    logging.info('Inside' + extract_text_from_pdf.__name__+ '()')
    pdf_reader = PdfReader(pdf_file)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

def generate_summary(content):
    logging.info('Inside' + generate_summary.__name__+ '()')
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

if __name__ == '__main__':
    app.run(debug=True)
