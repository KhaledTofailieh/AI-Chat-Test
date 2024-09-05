from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

from src.processors.input_processors import handle_user_response

tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
pipe = pipeline("ner", model=model, tokenizer=tokenizer)

app = Flask(__name__)


@app.route('/handle_input', methods=['POST'])
def handle_input():
    if 'question_id' not in request.form or 'answer_txt' not in request.form:
        return jsonify({'error': 'question_id and answer_txt are required.'}), 400

    question_id = request.form.get("question_id")
    answer_txt = request.form.get("answer_txt")

    if question_id == '':
        return jsonify({'error': 'question_id cannot be empty.'}), 400

    if answer_txt == '':
        return jsonify({'error': 'answer_txt cannot be empty.'}), 400

    try:
        question_id = int(question_id)
    except Exception as ex:
        return jsonify({'error': 'question_id must be an integer.'}), 400

    answer, success = handle_user_response(pipe, question_id, answer_txt)
    # end processing
    return jsonify({"item": answer, "success": success})


if __name__ == '__main__':
    app.run()
