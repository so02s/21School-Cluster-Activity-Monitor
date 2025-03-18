import requests
import json

URL = "https://edu-api.21-school.ru/services/21-school/api"
API_KEY = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ5V29landCTmxROWtQVEpFZnFpVzRrc181Mk1KTWkwUHl2RHNKNlgzdlFZIn0.eyJleHAiOjE3NDA2MDUzMzksImlhdCI6MTc0MDU2OTMzOSwianRpIjoiYzIzZjY2MjgtYWFkMC00YzUzLThiZjEtYjBlZjFiYWY4NzhjIiwiaXNzIjoiaHR0cHM6Ly9hdXRoLnNiZXJjbGFzcy5ydS9hdXRoL3JlYWxtcy9FZHVQb3dlcktleWNsb2FrIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6ImM1OWQzZjczLTBmYTktNGNlYi05NzdlLTAxZWQ2NWQ1Y2MzYyIsInR5cCI6IkJlYXJlciIsImF6cCI6InMyMS1vcGVuLWFwaSIsInNlc3Npb25fc3RhdGUiOiIxNjFhZTNhNC03ZWQwLTQ2ZDItYjAxZi1hODAwMWQ1YTEzZjUiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHBzOi8vZWR1LjIxLXNjaG9vbC5ydSJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1lZHVwb3dlcmtleWNsb2FrIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoicHJvZmlsZSBlbWFpbCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJ1c2VyX2lkIjoiZDVhMmQwYzEtZjY2MS00YzY3LWJlZjgtM2NlMTUyMDM5OWMxIiwibmFtZSI6IlNvcmVuIENvYXJzZSIsImF1dGhfdHlwZV9jb2RlIjoiZGVmYXVsdCIsInByZWZlcnJlZF91c2VybmFtZSI6InNvcmVuY29hIiwiZ2l2ZW5fbmFtZSI6IlNvcmVuIiwiZmFtaWx5X25hbWUiOiJDb2Fyc2UiLCJlbWFpbCI6InNvcmVuY29hQHN0dWRlbnQuMjEtc2Nob29sLnJ1In0.vq8XBKvbLedfs8wlgLirQnekDYJIEaV5sFXHps6wcKyS_3xkjDFiv0yNIcyL0LbMSbiC-RCnDS-yNNT-v9BBIxzLpxfSIqZiM1l6219eqC-DMtyNev-tYIsAecyCsItyK4kdXTX4_lrwRadyDw0epT7BoUzJArfcYBM-Ex7GEhcZHpO1CXJqTK2rJey-fdbFnLkvwiVXVm_SrKfkDjID53I8XRFseiFkTLVa2LhzbxX5nE96Z2_cl2qeP7aoY7pgBMhpGHDWGxUGiwVGVMkO0ErGhjH9dR4wU5iQuPUABdxLjVUUp6bYtAH9lQhB_c3psOWPCRZokuGQseujrdi_oQ"
headers = {'Authorization': 'Bearer %s' % (API_KEY)}
login = "barbaraa"
request = f'/v1/participants/{login}/coalition'

r = requests.get('%s%s' % (URL, request), headers=headers)
data = r.json()

print(data['name'])