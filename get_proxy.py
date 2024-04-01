# -*- coding: utf-8 -*-
import sys
sys.path.append('/opt/.test/lib/python3.11/site-packages')
import requests as r
import os
import re
from time import strftime

#https://github.com/Jxdn051/Proxy-Checkers/blob/main/list_proxy/proxy.json
proxy_list_server={
	'ipaddress':{'url':'https://www.ipaddress.com/proxy-list/','pase':r'<tr>\s<td><a href="https://www.ipaddress.com/ipv4/(\d|\.){7,15}">(?P<IP>(\d|\.){7,15})</a>\:(?P<PORT>(\d)*)</td>\s<td>(?P<TYPE>(\w|\-)*)</td>\s<td>(?P<CONTORY>(.*?))</td>\s<td>(?P<TIME>(\d|\-|\s|\:)*)</td>\s</tr>'},		
	#'freeproxylistcc':{'url':'http://freeproxylist.cc/','pase':r''}
	'proxy_list':{'url':'https://www.proxy-list.download/api/v1/get?type=http','pase':r'(?P<IP>(\d|\.)*?):(?P<PORT>(\d)*)'},
	'TheSpeedX':{'url':'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt','pase':r'(?P<IP>(\d|\.)*?):(?P<PORT>(\d)*)'},
	'openproxylist':{'url':'https://api.openproxylist.xyz/http.txt','pase':r'(?P<IP>(\d|\.)*?):(?P<PORT>(\d)*)'},
	'lr2b':{'url':'http://alexa.lr2b.com/proxylist.txt','pase':r'(?P<IP>(\d|\.)*?):(?P<PORT>(\d)*)'},
	'proxy-spider':{'url':'https://proxy-spider.com/api/proxies.example.txt','pase':r'(?P<IP>(\d|\.)*?):(?P<PORT>(\d)*)'},
	'multiproxy':{'url':'https://multiproxy.org/txt_all/proxy.txt','pase':r'(?P<IP>(\d|\.)*?):(?P<PORT>(\d)*)'},
	'proxyspace':{'url':'https://proxyspace.pro/http.txt','pase':r'(?P<IP>(\d|\.)*?):(?P<PORT>(\d)*)'},
	'rootjazz':{'url':'https://rootjazz.com/proxies/proxies.txt','pase':r'(?P<IP>(\d|\.)*?):(?P<PORT>(\d)*)'},
}

proxy_check_url='https://www.ctfile.com'
header = {'User-Agent': 'Mozilla/5.0'}
def proxy_check(proxy_ip=""):
	if proxy_ip != "" :
		print(u'%s Checking proxy : %s' %(strftime("%Y%m%d_%H%M%S"), proxy_ip), end="")
		try: # Tries to open google.com with the given proxie.
			req= r.get(proxy_check_url, headers=header, proxies={'https' : proxy_ip}, timeout=5)
			if req.status_code == 200:
				print(u' ## Success get %s bytes' % (len(req.content.decode('utf-8'))), end = "")
				if len(req.content.decode('utf-8')) == 51617 :
					print(u' --> Success 51617')
					return True
				else :
					print(u' --> Length Fail')
					return False
			else:
				print(u' --> Fail')
				return False
		except Exception as e:
			#print(u'Test Fail %s' % (e))
			print(u' --> Fail')
			return False

def main():
	print(u'start get proxy list %s' % strftime("%Y%m%d_%H%M%S") )
	f = open('proxy.list', 'w')
	for p in proxy_list_server :
		print(u'%s Get list : %s' %(strftime("%Y%m%d_%H%M%S"), p ))
		try:
			req = r.get(proxy_list_server[p]['url'],headers=header, timeout=10 )
			if req.status_code == 200 :
				#print(u'proxy list page : %s' % req.content.decode('utf-8'))
				p = re.compile(proxy_list_server[p]['pase'])
				matches=p.finditer(req.content.decode('utf-8'))
				for m in matches:
					proxy=m.groupdict()
					proxy_ip="http://"+proxy['IP']+":"+proxy['PORT']
					#print(u'%s Check proxy : %s (%s) %s ' % (strftime("%Y%m%d_%H%M%S"), proxy_ip, proxy['CONTORY'], proxy['TIME']))
					if proxy_check(proxy_ip) :
						print(u'Success %s' % proxy_ip)
						f.write(proxy_ip + '\n')
		except Exception as e :
			print(u'%s Get proxy list error %s' %(strftime("%Y%m%d_%H%M%S"), e))
	f.close()
	
if __name__ == '__main__':
	main()
