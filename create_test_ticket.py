
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

instance_url = os.getenv("SERVICENOW_INSTANCE_URL")
username = os.getenv("SERVICENOW_USERNAME")
password = os.getenv("SERVICENOW_PASSWORD")

if not all([instance_url, username, password]):
    print("Erro: As variáveis de ambiente SERVICENOW_INSTANCE_URL, SERVICENOW_USERNAME e SERVICENOW_PASSWORD devem ser definidas.")
    exit(1)

url = f"{instance_url}/api/now/table/incident"
auth = (username, password)

# Dados para o novo incidente, agora com os campos fornecidos pelo usuário
data = {
    "short_description": "Ticket de Teste - Jarvis",
    "description": "Este é um ticket de teste gerado automaticamente para validar a conexão com a API, usando o payload correto.",
    "caller_id": username,
    "opened_by": username,
    "sc_cat_item_producer": "System/Software Failure"
}

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

print(f"Enviando requisição para: {url}")
print(f"Payload: {json.dumps(data, indent=2)}")

try:
    response = requests.post(url, auth=auth, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    print("--- TICKET CRIADO COM SUCESSO ---")
    print(json.dumps(response.json(), indent=2))
except requests.exceptions.HTTPError as errh:
    print(f"--- ERRO HTTP ---")
    print(f"Status Code: {response.status_code}")
    print(f"Corpo da resposta: {response.text}")
except Exception as err:
    print(f"--- OCORREU UM ERRO INESPERADO ---")
    print(f"{err}")
