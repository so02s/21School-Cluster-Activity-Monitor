import requests
import json

URL = "https://edu-api.21-school.ru/services/21-school/api"
API_KEY = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ5V29landCTmxROWtQVEpFZnFpVzRrc181Mk1KTWkwUHl2RHNKNlgzdlFZIn0.eyJleHAiOjE3NDQxNTM4NDQsImlhdCI6MTc0NDExNzg0NCwianRpIjoiNTEzYTU1OGItNTQ4ZS00NGI2LTkxM2ItNTdjYjc5NzRjMGI5IiwiaXNzIjoiaHR0cHM6Ly9hdXRoLnNiZXJjbGFzcy5ydS9hdXRoL3JlYWxtcy9FZHVQb3dlcktleWNsb2FrIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6ImM1OWQzZjczLTBmYTktNGNlYi05NzdlLTAxZWQ2NWQ1Y2MzYyIsInR5cCI6IkJlYXJlciIsImF6cCI6InMyMS1vcGVuLWFwaSIsInNlc3Npb25fc3RhdGUiOiJhZGM0MzlmOS1jYWQ4LTRhMTAtOWM4NC1jNGUyZjkwNzYwMTIiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHBzOi8vZWR1LjIxLXNjaG9vbC5ydSJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1lZHVwb3dlcmtleWNsb2FrIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoicHJvZmlsZSBlbWFpbCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJ1c2VyX2lkIjoiZDVhMmQwYzEtZjY2MS00YzY3LWJlZjgtM2NlMTUyMDM5OWMxIiwibmFtZSI6IlNvcmVuIENvYXJzZSIsImF1dGhfdHlwZV9jb2RlIjoiZGVmYXVsdCIsInByZWZlcnJlZF91c2VybmFtZSI6InNvcmVuY29hIiwiZ2l2ZW5fbmFtZSI6IlNvcmVuIiwiZmFtaWx5X25hbWUiOiJDb2Fyc2UiLCJlbWFpbCI6InNvcmVuY29hQHN0dWRlbnQuMjEtc2Nob29sLnJ1In0.DN1SxwRIsgjc2IM-s7GY8fc_J-V8x_d0JVgfeXtqJb0CGoVDInOu6Ac5k__6BglnJTFG_kWeNiIA7ROuO4ggtGB-r4YJ0xDStI_0useKVDLzgBRMBDJHNoTq_3FziFuaVBbudWUqA_jeZ2h_kz8N90Z0WvmLzs15-R35-2sCQogeA_ZpQPIGzTijcVu08pEgSEj4lxLEo9hRri15t7ymAZ98NFfyS1qOkfVwxz6WSLjGHgalO3ufa2WsDxdKLk4Ev-a0LEmy8JU3WmybYDivQ-qiWWqzH6Ehw2hpcHPDvEI0_POLlaEe6Y3rF8TyHHMrFNThoVUxS6ebEKp7xP9gxQ"
headers = {'Authorization': 'Bearer %s' % (API_KEY)}
# login = "barbaraa"
# campusId = "6bfe3c56-0211-4fe1-9e59-51616caac4dd"
# request = f'/v1/campuses/{campusId}/clusters'

# 6bfe3c56-0211-4fe1-9e59-51616caac4dd -- id кампуса Москвы
clusters = {34715: "Atlantis", 34718: "Illusion", 34719: "Mirage", 34720: "Oasis"}
for clusterId, cluster_name in clusters.items():
    request = f'/v1/clusters/{clusterId}/map'
    params = {'occupied': True, 'limit': 140}
    r = requests.get('%s%s' % (URL, request), headers=headers, params=params)
    data = r.json()
    # occupied_seats = list(filter(lambda x: x['login'] is not None, data['clusterMap']))
    print(cluster_name)
    # print(data)

    for record in data["clusterMap"]:
        req = f'/v1/participants/{record["login"]}/coalition'
        r = requests.get('%s%s' % (URL, req), headers=headers)
        tribe = r.json()
        print(record['login'], tribe)


