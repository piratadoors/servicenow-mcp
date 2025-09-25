import os
import argparse
import json
from dotenv import load_dotenv
from servicenow_mcp.tools.variable_tools import get_ritm_variables, GetRITMVariablesParams
from servicenow_mcp.utils.config import ServerConfig, AuthConfig, BasicAuthConfig, AuthType
from servicenow_mcp.auth.auth_manager import AuthManager

def main():
    parser = argparse.ArgumentParser(description="ServiceNow Variable CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Sub-parser for the 'get-ritm-variables' command
    vars_parser = subparsers.add_parser("get-ritm-variables", help="Get the variables for a RITM.")
    vars_parser.add_argument("--ritm-sys-id", required=True, help="The sys_id of the RITM.")

    args = parser.parse_args()

    load_dotenv()

    instance_url = os.getenv("SERVICENOW_INSTANCE_URL")
    username = os.getenv("SERVICENOW_USERNAME")
    password = os.getenv("SERVICENOW_PASSWORD")

    if not all([instance_url, username, password]):
        print(json.dumps({"success": False, "message": "Erro: As variáveis de ambiente SERVICENOW_INSTANCE_URL, SERVICENOW_USERNAME e SERVICENOW_PASSWORD devem ser definidas."}))
        return

    basic_auth_config = BasicAuthConfig(username=username, password=password)
    auth_config = AuthConfig(type=AuthType.BASIC, basic=basic_auth_config)
    
    config = ServerConfig(
        instance_url=instance_url,
        auth=auth_config
    )

    auth_manager = AuthManager(config.auth, config.instance_url)

    if args.command == "get-ritm-variables":
        params = GetRITMVariablesParams(
            ritm_sys_id=args.ritm_sys_id,
        )
        result = get_ritm_variables(config, auth_manager, params)
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
