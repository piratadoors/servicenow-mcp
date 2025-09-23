
import os
import argparse
import json
from dotenv import load_dotenv
from servicenow_mcp.tools.incident_tools import list_incidents, ListIncidentsParams
from servicenow_mcp.utils.config import ServerConfig, AuthConfig, BasicAuthConfig, AuthType
from servicenow_mcp.auth.auth_manager import AuthManager

def main():
    parser = argparse.ArgumentParser(description="List ServiceNow incidents.")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of incidents to return")
    parser.add_argument("--offset", type=int, default=0, help="Offset for pagination")
    parser.add_argument("--display-value", type=lambda x: (str(x).lower() == 'true'), default=True, help="Return display values for reference fields (default: True)")
    parser.add_argument("--state", help="Filter by incident state")
    parser.add_argument("--assigned-to", help="Filter by assigned user")
    parser.add_argument("--category", help="Filter by category")
    parser.add_argument("--query", help="A ServiceNow encoded query string for filtering incidents")
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

    params = ListIncidentsParams(
        limit=args.limit,
        offset=args.offset,
        display_value=args.display_value,
        state=args.state,
        assigned_to=args.assigned_to,
        category=args.category,
        query=args.query
    )

    result = list_incidents(config, auth_manager, params)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
