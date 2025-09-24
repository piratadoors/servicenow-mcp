import os
import argparse
import json
import requests
from dotenv import load_dotenv
from servicenow_mcp.utils.config import ServerConfig, AuthConfig, BasicAuthConfig, AuthType
from servicenow_mcp.auth.auth_manager import AuthManager

STATE_MAP = {
    "Novo(a)": "1",
    "Em andamento": "2",
    "Em espera": "3",
    "Resolvido": "6",
    "Encerrado": "7",
    "Cancelado(a)": "8",
}

def main():
    parser = argparse.ArgumentParser(description="Count ServiceNow incidents.")
    parser.add_argument("--query", help="A ServiceNow encoded query string for filtering incidents")
    parser.add_argument("--state-name", help="Filter by incident state display name")
    args = parser.parse_args()

    load_dotenv()

    instance_url = os.getenv("SERVICENOW_INSTANCE_URL")
    username = os.getenv("SERVICENOW_USERNAME")
    password = os.getenv("SERVICENOW_PASSWORD")

    if not all([instance_url, username, password]):
        print("Erro: As variáveis de ambiente SERVICENOW_INSTANCE_URL, SERVICENOW_USERNAME e SERVICENOW_PASSWORD devem ser definidas.")
        return

    basic_auth_config = BasicAuthConfig(username=username, password=password)
    auth_config = AuthConfig(type=AuthType.BASIC, basic=basic_auth_config)
    
    config = ServerConfig(
        instance_url=instance_url,
        auth=auth_config,
        debug=False,
        timeout=30,
        script_execution_api_resource_path=None 
    )

    auth_manager = AuthManager(config.auth, config.instance_url)

    api_url = f"{config.instance_url}/api/now/stats/incident"
    
    query_params = {
        "sysparm_count": "true"
    }

    if args.query:
        query_params["sysparm_query"] = args.query
    elif args.state_name:
        if args.state_name in STATE_MAP:
            query_params["sysparm_query"] = f"state={STATE_MAP[args.state_name]}"
        else:
            print(f"Erro: Nome de estado inválido. Valores válidos: {list(STATE_MAP.keys())}")
            return

    try:
        response = requests.get(
            api_url,
            params=query_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()
        
        data = response.json()
        count = data.get("result", {}).get("stats", {}).get("count", 0)
        
        print(json.dumps({"success": True, "count": count}, indent=2))
        
    except requests.RequestException as e:
        print(json.dumps({"success": False, "message": f"Failed to count incidents: {str(e)}"}, indent=2))

if __name__ == "__main__":
    main()