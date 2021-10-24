import requests
import json
from credentials import HOST, API_KEY
from rpi_DB import Status

# mi-g6.msk.21-school.ru: empty
# ox-o4.msk.21-school.ru: empty
# at-k8.msk.21-school.ru: empty
# ga-o4.msk.21-school.ru: empty

class Grafana:
    def __init__(self, db):
        self.db = db
        self.headers = {'Authorization': 'Bearer %s' % (API_KEY,)}
        self.clusters = {'oa' : 'oasis', 'il' : 'illusion', 'mi' : 'mirage', 'at' : 'atlantis', 'am' : 'atrium'}
    
    def get_metrics(self):
        data_url ='/api/datasources/proxy/1/api/v1/query?query=iMacUser_status{instance=~\".*\"}'
        r = requests.get('%s%s' % (HOST, data_url,), headers=self.headers)
        data = r.json()
        # macs = {}
        print('getting metrics')
        for each in data['data']['result']:
            status = each['metric']['instance']+': '+each['metric']['login']
            # 'am-i2.msk.21-school.ru'
            mac = status.split(": ")[0].split(".")[0]
            cluster = mac.split("-")[0]
            mac = mac.split("-")[1]
            status = status.split(": ")[1]
            cluster = self.clusters.get(cluster)
            if cluster == None:
                continue
            if status == 'empty':
                status = Status.FREE
            else:
                status = Status.USED
            self.db.change_mac_status(cluster, mac, int(status))
            # macs[each['metric']['instance']] = each['metric']['login']
