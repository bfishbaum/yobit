import time,hmac,hashlib,json,requests
from urllib.parse import urlencode
import urllib.error

with open('../api.txt') as f:
	data = f.read().splitlines()
	API_KEY = data[0]
	API_SEC = bytes(data[1].encode('ascii','ignore'))
	URL_BASE = data[3]

def NONCE():
	return str(int(time.time()))

def getInfo():
	return request(method='info')

def getTicker(key):
	x = request(method='ticker',coinKey=key)
	return x[key]

def getDepth(key):
	x = request(method='depth',coinKey=key)
	return x[key]

def request(method='ticker',coinKey='btc_usd'):
	if(method == 'info'):
		coinKey = ''
	reqURL = URL_BASE + method + '/' + coinKey
	values = {"method": method, "nonce": NONCE()}
	body = urlencode(values).encode('utf-8')
	signature = hmac.new(API_SEC, body, hashlib.sha512).hexdigest()
	headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Key': API_KEY,
            'Sign': signature
        }
	req = requests.post(reqURL,data=values,headers=headers)
	j = json.loads(req.text)
	#print(j)
	return j

def getAskBid(key):
	d = getDepth(key)
	return d['asks'][0][0], d['bids'][0][0]

def getCoinInfo(key):
	return request(method='info')['pairs'][key]

