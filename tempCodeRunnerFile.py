from flask import Flask, render_template, request, jsonify
from PyPDF2 import PdfReader
import openai

app = Flask(__name__)
summaries = {} 


openai.api_key = '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'
MAX_TOKENS = 4000  

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/api/summarize_text', methods=['POST'])
def summarize_text():
    if request.method == 'POST':
        data = request.get_json()
        text = data.get('text')
        if not text:
            return jsonify({'error': 'No text found'})
        summary = generate_summary(text)
        summary_id = len(summaries) + 1
        summaries[summary_id] = summary
        return jsonify({'summary_id': summary_id})

@app.route('/api/summarize_file', methods=['POST'])
def summarize_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file found'})
        
        pdf_file = request.files['file']
        content = extract_text_from_pdf(pdf_file)
        if not content:
            return jsonify({'error': 'Failed to extract text from the PDF'})
        
        summary = generate_summary(content)
        summary_id = len(summaries) + 1
        summaries[summary_id] = summary
        return jsonify({'summary_id': summary_id})

@app.route('/summary/<int:summary_id>')
def show_summary(summary_id):
    summary = summaries.get(summary_id)
    if summary:
        return render_template('summary1.html', summary=summary)
    else:
        return "Summary not found."

def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

def generate_summary(content):
    # Split content into chunks of maximum token length
    chunks = [content[i:i + MAX_TOKENS] for i in range(0, len(content), MAX_TOKENS)]
    summaries = []
    for chunk in chunks:
        prompt = f"Summarize the following text:\n\n{chunk}"

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )

        summary = response.choices[0].text.strip()
        summaries.append(summary)

    return ' '.join(summaries)

if __name__ == '__main__':
    app.run(debug=True)
