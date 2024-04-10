from flask import Flask, request, Response
import boto3
import os
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <html>
    <head>
        <title>Texto para Áudio</title>
    </head>
    <body>
        <h1>Insira uma frase para converter em áudio:</h1>
        <form action="/gerar_audio" method="post">
            <textarea name="texto" rows="4" cols="50"></textarea><br><br>
            <input type="submit" value="Gerar Áudio">
        </form>
    </body>
    </html>
    """

@app.route('/gerar_audio', methods=['POST'])
def gerar_audio():
    texto = request.form['texto']

    polly = boto3.client('polly',
                         region_name='us-east-1',  # Defina a região corretamente aqui
                         aws_access_key_id=os.environ.get('ASIAVRUVVZTSY4YYUS57'),
                         aws_secret_access_key=os.environ.get('kX+NaZNApSvNPvjqlOGP4HrPfzeRLnkdXt1Jhb0b'))

    response = polly.synthesize_speech(
        Text=texto,
        OutputFormat='mp3',
        VoiceId='Joanna',
        LanguageCode='pt-PT'  # Configura o idioma para português de Portugal
    )

    audio_data = response['AudioStream'].read()

    return """
    <html>
    <head>
        <title>Áudio Gerado</title>
    </head>
    <body>
        <h1>Áudio Gerado:</h1>
        <audio controls>
            <source src="data:audio/mpeg;base64,{}" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
        <br><br>
        <a href="/">Voltar</a>
    </body>
    </html>
    """.format(base64.b64encode(audio_data).decode())

if __name__ == '__main__':
    app.run(debug=True)
