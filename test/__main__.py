from flask import Flask, render_template, session
from netaddr import IPAddress
import netifaces as ni
import nmap
import json
import subprocess
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Atul'
ip = ""

#print(f)
@app.route('/camera')
def devices():
	print("hello")
	ip = ni.ifaddresses('wlp2s0')[ni.AF_INET][0]['addr']
	session['my_var'] = ip
	netmask = ni.ifaddresses('wlp2s0')[ni.AF_INET][0]['netmask']
	cidraddress = IPAddress(netmask).netmask_bits()
	print(cidraddress)
	host = str(ip) + "/" + str(cidraddress)
	nm = nmap.PortScanner()
	print(host)
	y = nm.scan(hosts=host, arguments='-v -sn')
	#print(nm)
	up_host = []
	for host in nm.all_hosts():
		print(y['scan'][host]['status']['state'])
		if y['scan'][host]['status']['state'] =='up':
			up_host.append({'host':host,'state':y['scan'][host]['status']['state'],'name':y['scan'][host]['hostnames'][0]['name']})
		else:
			pass
	#print(up_host)
	#print(type(up_host))
	keys = up_host[0].keys()
	#print(keys)
	#f = json.dumps(up_host,indent=4) 
	return render_template('record.html', records=up_host, colnames=keys)

@app.route('/script/<string:name>')
def atul(name):
	ip1 = session.get('my_var', None)
	print(ip1)
	randomno = random.randrange(20, 40)
	x = render_template('video.sh', camip=name, localhostip=ip1, randomno=randomno)
	#x = render_template('video.sh', atul='mkdir fffffffffffffff')
	print(x)
	#y = subprocess.check_output(x, shell=True)
	#print(y)
	print("Hello ",name)
	output = "http://"+ ip1 + "/stream_" + str(randomno) + ".m3u8"
	print(output)
	return output
if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5000,debug=True)
