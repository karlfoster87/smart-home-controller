from flask import Flask, render_template
from flask_ask import Ask, statement, convert_errors

app = Flask(__name__)
ask = Ask(app, '/alexa/')

@app.route('/')
def index():
    return render_template('index.html')

@ask.intent('SmartHomeIntent', mapping={'device': 'device', 'mode': 'mode'})
def smart_home(device, mode):
	return statement('Message Recieved! {} / {}'.format(device, mode))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1337)