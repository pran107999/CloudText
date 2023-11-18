from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)
summaries = {}  # Dictionary to store summaries

# Set your OpenAI API key
openai.api_key = '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'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/summarize', methods=['POST'])
def summarize_text():
    if request.method == 'POST':
        content = request.json.get('text')
        summary = generate_summary(content)
        summary_id = len(summaries) + 1
        summaries[summary_id] = summary
        return jsonify({'summary_id': summary_id, 'summary': summary})

@app.route('/summary/<int:summary_id>')
def show_summary(summary_id):
    summary = summaries.get(summary_id)
    if summary:
        return render_template('summary.html', summary=summary)
    else:
        return "Summary not found."

def generate_summary(content):
    prompt = f"Summarize the following text:\n\n{content}"

    response = openai.Completion.create(
        engine="text-davinci-002",  # Choose the appropriate GPT-3.5 engine
        prompt=prompt,
        max_tokens=150,  # Adjust as needed
        temperature=0.7,  # Adjust as needed
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )

    summary = response.choices[0].text.strip()
    return summary

if __name__ == '__main__':
    app.run(debug=True)
