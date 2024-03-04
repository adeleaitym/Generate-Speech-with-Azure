from flask import Flask, render_template, request, redirect, url_for
import os
import requests

app = Flask(__name__)

def generate_voice(text, filename):
    subscription_key = "your key"
    url = "https://eastus.tts.speech.microsoft.com/cognitiveservices/v1"

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "audio-48khz-192kbitrate-mono-mp3"
    }

    ssml = "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'><voice name='en-US-AriaNeural'>" + text + "</voice></speak>"
    ssml = ssml.encode('utf-8')

    response = requests.post(url=url, data=ssml, headers=headers)

    with open("static/{}.mp3".format(filename), "wb") as f:
        f.write(response.content)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        filename = request.form['filename']
        generate_voice(text, filename)
        return redirect(url_for('index'))
    files = os.listdir('static')
    return render_template('index.html', files=files)

if __name__ == '__main__':
    app.run(debug=True)
