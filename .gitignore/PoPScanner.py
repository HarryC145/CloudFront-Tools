import json
import requests
from typing import List
from netaddr import IPNetwork

IPList = requests.get('http://d7uri8nf7uskq.cloudfront.net/tools/list-cloudfront-ips').json()
IPGlobal = (IPList['CLOUDFRONT_GLOBAL_IP_LIST'])
print(IPGlobal)
working_ips = 0
IPCounter = 0
good_ips = []
headers_dict = {"Host": "www.reuters.com", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) "
                                                         "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 "
                                                         "Safari/605.1.15"}
for s in IPGlobal:
    for IP in IPNetwork(str(s)):
        with open("results.json", "a") as resultsfile:
            if IPCounter == 100:
                # TODO: Tidy up, load the finished json every 100 lines to ensure we don't duplicate data
                print("Found", working_ips, "so far")
                json.dump(good_ips, resultsfile)
                resultsfile.close()
                good_ips = []
                IPCounter = 0
        print('%s' % IP)
        IPTester = 'http://' + '%s' % IP
        try:
            r = requests.get(IPTester, headers=headers_dict, timeout=1)
            print(r.status_code)
            location = r.headers["X-Amz-Cf-Pop"]
            print(location)
        except:
            continue
        if r.ok:
            good_ips.append({'IP': ('%s' % IP), 'Location': location[:3]})
            print(good_ips)
            working_ips = working_ips + 1
            IPCounter = IPCounter + 1
json.dump(good_ips, resultsfile)
resultsfile.close()
print("We have", len(working_ips), "working IPs!, and they are")
print(working_ips)
