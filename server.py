from flask import Flask, render_template
from flask_ask import Ask, statement, convert_errors
from phue import Bridge
import ssl
import nmap
import subprocess
#sudo apt-get install nmap
#sudo pip install python-nmap

app = Flask(__name__)
ask = Ask(app, '/alexa/')

global_huebridgeip = '192.168.0.0'
global_userip_scanrange = '192.168.0.0-2'
global_user1mac = '00:00:00:00:00:00'
global_user2mac = '00:00:00:00:00:00'
global_user3mac = '00:00:00:00:00:00'

global_user1away = False
global_user2away = False
global_user3away = False

global_nest_away = False
global_nest_currenttemp = 0
global_nest_targettemp = 20
global_nest_active = False

global_hue_light1_status = 'Off'
global_hue_light2_status = 'Off'
global_hue_light3_status = 'Off'
global_hue_light4_status = 'Off'
global_hue_light5_status = 'Inactive'
global_hue_light6rgb_status = 'Inactive'
global_hue_light6w_status = 'Inactive'
global_hue_light1_value = {254,0,0,254}
global_hue_light2_value = {254,0,0,254}
global_hue_light3_value = {254,0,0,254}
global_hue_light4_value = {254,0,0,254}
global_hue_light5_value = {254,0,0,254}
global_hue_light6rgb_value = {254,0,0,254}
global_hue_light6w_value = {254}

@app.route('/')
def index():
	return render_template('index.html')

@ask.intent('SmartHomeIntent', mapping={'device': 'device', 'mode': 'mode'})
def smart_home(device, mode):
	test_lighting_api()
	return statement('Success')

def determineUserLocations():
	global global_user1away
	global global_user2away
	global global_user3away

	global_user1away = True
	global_user2away = True
	global_user3away = True

	nm = nmap.PortScanner()
	nm.scan(hosts=global_userip_scanrange, arguments='-sP')
	host_list = nm.all_hosts()

	for host in host_list:
        if  'mac' in nm[host]['addresses']:
                print(host+' : '+nm[host]['addresses']['mac'])
                if global_user1mac == nm[host]['addresses']['mac']:
                    global_user1away = False
                else if global_user2mac == nm[host]['addresses']['mac']:
                	global_user2away = False
                else if global_user3mac == nm[host]['addresses']['mac']:
                	global_user3away = False

# initial test functionality, to be removed
def test_lighting_api():
	b = Bridge(global_huebridgeip)
	b.connect()
	b.set_light('Floor Lamp', 'bri', 1)

if __name__ == '__main__':
	context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
	context.load_cert_chain('tls.crt', 'tls.key')
	app.run(host='0.0.0.0', port=1337, ssl_context=context, threaded=True, debug=True)
