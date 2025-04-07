import requests
import json
# from rpi_DB import Status
from decouple import config
from typing import Any

class Grafana:
    def __init__(self):
        self.host = config("HOST")
        self.headers = {'Authorization': f'Bearer {config("API_KEY")}'}
        self.clusters = {'oa' : 'oasis', 'il' : 'illusion', 'mi' : 'mirage', 'at' : 'atlantis', 'am' : 'atrium'}
    
    # TODO метод для трайбов
    def get_metrics_tribes(self):
        data_url = '/api/v1/query?query=iMacUser_status{login!="empty"}'
        r = requests.get('%s%s' % (self.host, data_url,), headers=self.headers)
        j = r.json()
        for i in j['data']['result']:
            print(i['metric']['login'], i['metric']['host'])


    # def get_metrics(self):
    #     data = self.get_request_data('/api/datasources/proxy/1/api/v1/query?query=iMacUser_status{instance=~\".*\"}')

    #     for each in data['data']['result']:
    #         data = each['metric']['instance']
    #         mac = data.split(".")[0]
    #         cluster = mac.split("-")[0]
    #         mac = mac.split("-")[1]
    #         login = each['metric']['login']
    #         cluster = self.clusters.get(cluster)
    #         if cluster == None:
    #             continue
    #         status = Status.USED
    #         if login == 'empty':
    #             status = Status.FREE
    #         self.db.change_mac_status(cluster, mac, int(status))
        
    #     self.get_exams()

    # def get_exams(self):
    #     data = self.get_request_data('/api/datasources/proxy/1/api/v1/query?query=iMacExam_status{instance=~\".*\"}')

    #     for each in data['data']['result']:
    #         if each['value'][1] == '0':
    #             continue
    #         data = each['metric']['instance']
    #         mac = data.split(".")[0]
    #         cluster = mac.split("-")[0]
    #         mac = mac.split("-")[1]
    #         cluster = self.clusters.get(cluster)
    #         if cluster == None:
    #             continue
    #         status = Status.EXAM
    #         self.db.change_mac_status(cluster, mac, int(status))

    # def get_request_data(self, base_url) -> Any:
    #     r = requests.get(
    #         url=f"{config('HOST')}{base_url}",
    #         headers=self.headers
    #     )
    #     return r.json()
        


