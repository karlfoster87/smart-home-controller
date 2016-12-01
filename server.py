from flask import Flask, render_template
from flask_ask import Ask, statement, convert_errors
from phue import Bridge
import ssl

app = Flask(__name__)
ask = Ask(app, '/alexa/')

global_huebridgeip = '192.168.0.0'
global_away = False
global_jodieaway = False
global_karlaway = False

@app.route('/')
def index():
	return render_template('index.html')

@ask.intent('SmartHomeIntent', mapping={'device': 'device', 'mode': 'mode'})
def smart_home(device, mode):
	lighting_api()
	return statement('Success')

def lighting_api():
	b = Bridge(global_huebridgeip)
	b.connect()
	b.set_light('Floor Lamp', 'bri', 1)


if __name__ == '__main__':
	context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
	context.load_cert_chain('tls.crt', 'tls.key')
	app.run(host='0.0.0.0', port=1337, ssl_context=context, threaded=True, debug=True)
