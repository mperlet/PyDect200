import hashlib, urllib, sys, urllib2, json

fritz_url = u'http://fritz.box'

def get_sid(password):
	base_url = u'%s/login_sid.lua' % fritz_url
	try:
		get_challenge = urllib2.urlopen(base_url).read()
	except:
		print(u'error: host not found')
		exit(0)
	
	challenge = get_challenge.split('<Challenge>')[1].split('</Challenge>')[0]
	challenge_b = (challenge + '-' + password).decode('iso-8859-1').encode('utf-16le')
	
	m = hashlib.md5()
	m.update(challenge_b)
	
	response_b = challenge + '-' + m.hexdigest().lower()
	get_sid = urllib2.urlopen('%s?response=%s' % (base_url, response_b)).read()
	sid = get_sid.split('<SID>')[1].split('</SID>')[0]
	return sid

def switch_onoff(sid, device_nr, status):
	url = u'%s/net/home_auto_query.lua' % fritz_url
	http_header = {
					"Origin" : fritz_url,
					"Accept-Encoding" : "gzip,deflate,sdch",
					"Accept-Language" : "de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4",
					"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36",
					"Content-Type" : "application/x-www-form-urlencoded",
					"Accept" : "*/*",
					"Referer": "%s/net/home_auto_overview.lua?sid=%s" % (fritz_url, sid),
					"Connection" : "keep-alive"
					}
					
	params = {
	  'command' : 'SwitchOnOff',
	  'id' : device_nr,
	  'value_to_set' : status,
	  'xhr' : '1',
	  'sid' : sid,
	}


	# create your HTTP request
	req = urllib2.Request(url, urllib.urlencode(params), http_header)
	asd = urllib2.urlopen(req).read()

def get_info(sid):
	command = u'AllOutletStates'
	pre = u'xhr=1&t1390731922458=nocache'
	url = u'%s/net/home_auto_query.lua?sid=%s&command=%s&%s' % (fritz_url,
																sid,
																command,
																pre)
	return json.loads(urllib2.urlopen(url).read())

#### PROG
#sid1 = get_sid('FRITZPW')
#switch_onoff(sid1, 16, sys.argv[1])
#print get_info(sid1)

