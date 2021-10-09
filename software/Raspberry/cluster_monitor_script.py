#!/usr/bin/env python

import requests
import json
import time

HOST = 'https://grafometheus.21-school.ru'
API_KEY = 'eyJrIjoiVTBmTEtkazYwS3dSNDlsdEo2WkNyWFRGZzNLS0pBNUQiLCJuIjoiMjFkYXNoIiwiaWQiOjF9'
user = 'am-a1.msk.21-school.ru'
query_user = 'iMacUser_status{instance=\"' + user + '\"}'



def get_data():
    headers = {'Authorization': 'Bearer %s' % (API_KEY,)}
    data_url ='/api/datasources/proxy/1/api/v1/query?query=\"' + query_user + '\"'
    r = requests.get('%s%s' % (HOST, data_url,), headers=headers)
    data = r.json()
    print(data)
#    r = requests.get('%s/api/search?query=&' % (HOST,), headers=headers)
#    dashboards = r.json()
#    print (dashboards) # we can get all dashboards uid and other
    
#    print ('----- GET data from DB/query -----')
    
# in data_url need place url with query_request
#    data_url ='/api/datasources/proxy/1/api/v1/query?query=iMacUser_status{instance=~\".*\"}'
#    r = requests.get('%s%s' % (HOST, data_url,), headers=headers)
#    data = r.json()
#    macs = {}
#    print('----- Save each host status in {host:status} -----')
#    print(data)
    #for each in data['data']['result']:
       # uncomment for print data in tty
       # status = each['metric']['instance']+': '+each['metric']['login']
       # print(status)
       # macs[each['metric']['instance']] = each['metric']['login']

def main():
    get_data();

        #time.sleep(3);


if __name__ == '__main__':
    main()
