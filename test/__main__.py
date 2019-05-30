from flask import Flask
from netaddr import IPAddress
import netifaces as ni
import nmap
import json


app = Flask(__name__)


#print(f)
@app.route('/camera')
def devices():
	print("hello")
	ip = ni.ifaddresses('wlp2s0')[ni.AF_INET][0]['addr']
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
	print(up_host)
	print(type(up_host))
	f = json.dumps(up_host,indent=4) 
	return f



if __name__ == '__main__':
   app.run(host="0.0.0.0", port=9006)