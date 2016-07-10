import time,hmac,hashlib,json,requests
from urllib.parse import urlencode
import urllib.error
from get_info import *

REAL_MONEY = False

with open('../api.txt') as f:
	data = f.read().splitlines()
	API_KEY = data[0]
	API_SEC = bytes(data[1].encode('ascii','ignore'))
	URL_BASE = data[2]
	#URL_BASE = "https://yobit.net/api/3/"

def NONCE():
	return str(int(time.time()))

def request(method='info',values=None):
	assert(not REAL_MONEY)	
	if(values == None): values = {}
	reqURL = URL_BASE

	values["method"] = method
	values["nonce"] = NONCE()

	body = urlencode(values).encode('utf-8')
	signature = hmac.new(API_SEC, body, hashlib.sha512).hexdigest()
	headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Key': API_KEY,
            'Sign': signature,
        }
	req = requests.post(reqURL,data=values,headers=headers)
	j = json.loads(req.text)
	return j

def makeBid(coinPair,price,amount):
	values = {'pair':coinPair,'type': 'buy','rate':price,'amount':amount}		
	return request('Trade',values)

def makeAsk(coinPair,price,amount):
	values = {'pair':coinPair,'type': 'sell','rate':price,'amount':amount}		
	return request('Trade',values)

def bestAsk(coinPair,amount):
	a,_ = getAskBid(coinPair)
	dec = getCoinInfo(coinPair)['decimal_places']
	ask = a - 10 ** -dec
	if(ask != 0):
		makeAsk(coinPair,amount)	

def bestBid(coinPair,amount):
	_,b = getAskBid(coinPair)
	dec = getCoinInfo(coinPair)['decimal_places']
	bid = b + 10**-dec
	makeBid(coinPair,amount)
	
