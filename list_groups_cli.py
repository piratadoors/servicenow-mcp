
import os
import argparse
import json
from dotenv import load_dotenv
from servicenow_mcp.tools.user_tools import list_groups, ListGroupsParams
from servicenow_mcp.utils.config import ServerConfig, AuthConfig, BasicAuthConfig, AuthType
from servicenow_mcp.auth.auth_manager import AuthManager

def main():
    parser = argparse.ArgumentParser(description="List ServiceNow groups.")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of groups to return")
    parser.add_argument("--offset", type=int, default=0, help="Offset for pagination")
    parser.add_argument("--active", type=lambda x: (str(x).lower() == 'true'), help="Filter by active status")
    parser.add_argument("--query", help="A ServiceNow encoded query string for filtering groups")
    parser.add_argument("--type", help="Filter by group type")
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

    params = ListGroupsParams(
        limit=args.limit,
        offset=args.offset,
        active=args.active,
        query=args.query,
        type=args.type
    )

    result = list_groups(config, auth_manager, params)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
