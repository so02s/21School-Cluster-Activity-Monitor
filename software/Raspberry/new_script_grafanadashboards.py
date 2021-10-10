#!/usr/bin/env python
import requests
import time
import os
import argparse
import json
import glob
import urllib3
import uuid

def get_grafana_dashboards(g_url, g_token):
    dashboards_array = []
    headers = {'Authorization': str('Bearer ' + g_token), 'Content-type': 'application/json'}
    get_data_req = requests.get(g_url + '/api/search?query=&', headers=headers)

    pars_json = json.loads(get_data_req.text)
    for dash in pars_json:
        # print(dash['uri'][3::])
        dashboards_array.append(dash['uri'][3::])

    return dashboards_array


def export_grafana_dashboards(g_token, g_url, dir_path, e_dash):
    headers = {'Authorization': str('Bearer ' + g_token),
               'Content-type': 'application/json'
               }
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(dir_path, 'has been created')

    dashboard_names = get_grafana_dashboards(g_url, g_token)
    dash_count = 1

    if e_dash == 'all':
        print('I will export ALL DASHes!')
        for d in dashboard_names:
            pn = f'-{str(uuid.uuid4())}'
            dashboard_name_out = dir_path + '/' + d + pn + '.json'
            get_dashboard = requests.get(g_url + '/api/dashboards/db/' + d, headers=headers)
            try:
                f = open(dashboard_name_out, 'w')
                f.write(json.dumps(get_dashboard.json(), indent=4))
                f.close()
                print('[', dash_count, ']', d)
                dash_count += 1
            except EOFError:
                print('I cant write to file: ', EOFError)

    else:
        print('I will export {} dashbourd(s)!'.format(e_dash))
        for d in dashboard_names:
            for dd in e_dash:
                if d == dd:
                    dashboard_name_out = dir_path + '/' + d + '.json'
                    get_dashboard = requests.get(g_url + '/api/dashboards/db/' + d, headers=headers)
                    try:
                        f = open(dashboard_name_out, 'w+')
                        f.write(json.dumps(get_dashboard.json(), indent=4))
                        f.close()
                        print('[', dash_count, ']', d)
                        dash_count += 1
                    except ValueError:
                        print('I cant write to file: ', ValueError)
    #

    return export_grafana_dashboards

def main():
    grafana_token = 'eyJrIjoiVTBmTEtkazYwS3dSNDlsdEo2WkNyWFRGZzNLS0pBNUQiLCJuIjoiMjFkYXNoIiwiaWQiOjF9'
    grafana_url = 'https://grafometheus.21-school.ru/'
    dashboards_dir = '/dashboards'
    dashboard = 'all'

    print('EXPORT function!')
    export_grafana_dashboards(grafana_token, grafana_url, dashboards_dir, dashboard)

if __name__ == '__main__':
    main()
