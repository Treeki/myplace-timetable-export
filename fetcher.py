import hashlib
import json
import requests
import time

def generate_strath_mac(service_name, timestamp, token_id, device_id):
	full_string = service_name + token_id + timestamp
	char_sum = sum(map(ord, full_string))
	md5 = hashlib.md5()
	md5.update(str(char_sum).encode('utf-8'))
	md5.update(device_id.encode('utf-8'))
	return md5.hexdigest().upper()


with open('config.json', 'r') as f:
	config = json.load(f)

URL = 'https://api.is.strath.ac.uk/api/service/class_timetable'
TOKEN_ID = config['token_id']
USER_AGENT = config['user_agent']
DEVICE_ID = config['device_id']

timestamp = '%.3f' % time.time()
mac = generate_strath_mac('CLASS_TIMETABLE', timestamp, TOKEN_ID, DEVICE_ID)

headers = {
	'Accept': 'application/json',
	'Accept-Language': 'en-gb',
	'User-Agent': USER_AGENT,
	'x-strath-api-tokenid': TOKEN_ID,
	'x-strath-api-mac': mac,
	'x-strath-api-timestamp': timestamp,
	'x-strath-api-servicetype': 'MENU'
}

post_data = {
	'version': '1',
	'portalGroup': 'MPEG_MOBILE_PORTALS',
	'tokenId': TOKEN_ID,
	'deviceId': DEVICE_ID,
	'timestamp': timestamp,
	'mac': mac
}

request = requests.get(URL, headers=headers, data=post_data)
with open('calendar.json', 'w') as f:
	f.write(request.text)

