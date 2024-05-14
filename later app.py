from flask import Flask, request
import gradio as gr
from transformers import pipeline

app = Flask(__name__)

# Load the T5 model for translation
translator = pipeline("translation_en_to_fr", model="google-t5/t5-base")

# Define a Gradio interface for translation
def translate_text(input_lang, output_lang, text):
    # Determine the translation model based on input and output languages
    if input_lang == 'English' and output_lang == 'French':
        translation_model = "translation_en_to_fr"
    elif input_lang == 'French' and output_lang == 'English':
        translation_model = "translation_fr_to_en"
    else:
        return "Invalid translation request"

    # Translate the text using the appropriate model
    translation = translator(text, model=translation_model)
    
    # Log the user input, translation request, and translation
    with open("translation_logs.txt", "a") as logfile:
        logfile.write(f"User: {request.remote_addr}\n")
        logfile.write(f"Name: {request.form['name']}\n")
        logfile.write(f"Input Language: {input_lang}\n")
        logfile.write(f"Output Language: {output_lang}\n")
        logfile.write(f"Input Text: {text}\n")
        logfile.write(f"Translation: {translation[0]['translation_text']}\n\n")
    
    return translation[0]['translation_text']

interface = gr.Interface(fn=translate_text, inputs=["text", "text", "text"], outputs="text",
                         title="Translator", description="Translate text between languages.")

# Route for the Gradio interface
@app.route('/')
def index():
    return interface.launch(share=True)

# Route to handle form submission
@app.route('/translate', methods=['POST'])
def translate():
    input_lang = request.form['input_lang']
    output_lang = request.form['output_lang']
    text = request.form['text']
    result = translate_text(input_lang, output_lang, text)
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
