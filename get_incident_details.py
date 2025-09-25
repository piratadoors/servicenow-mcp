
import os
import argparse
import json
from dotenv import load_dotenv
from servicenow_mcp.tools.incident_tools import get_incident_by_number, GetIncidentByNumberParams
from servicenow_mcp.utils.config import ServerConfig, AuthConfig, BasicAuthConfig, AuthType
from servicenow_mcp.auth.auth_manager import AuthManager

def main():
    parser = argparse.ArgumentParser(description="Get ServiceNow incident details.")
    parser.add_argument("--number", required=True, help="Incident number")
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

    params = GetIncidentByNumberParams(incident_number=args.number)

    result = get_incident_by_number(config, auth_manager, params)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
