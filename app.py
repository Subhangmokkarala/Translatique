from flask import Flask, render_template
import gradio as gr
from transformers import pipeline

app = Flask(__name__)

import pyfiglet
from pyfiglet import Figlet

f = Figlet(font='slant')

def print_figlet(text):
    print(f.renderText(text))

print_figlet('Hello, Mr Mokkarala !')


# Load the T5 model for translation
translator = pipeline("translation_en_to_fr")

# Define a Gradio interface for translation
def translate_text(text):
    translation = translator(text)
    return translation[0]['translation_text']

interface = gr.Interface(fn=translate_text, inputs="text", outputs="text")

# Route for the Gradio interface
@app.route('/')
def index():
    return interface.launch(share=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
