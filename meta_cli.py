import os
import argparse
import json
from dotenv import load_dotenv
from servicenow_mcp.tools.meta_tools import get_field_choices, GetFieldChoicesParams
from servicenow_mcp.utils.config import ServerConfig, AuthConfig, BasicAuthConfig, AuthType
from servicenow_mcp.auth.auth_manager import AuthManager

def main():
    parser = argparse.ArgumentParser(description="ServiceNow Meta CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Sub-parser for the 'get-field-choices' command
    choices_parser = subparsers.add_parser("get-field-choices", help="Get the choice list for a field.")
    choices_parser.add_argument("--table-name", required=True, help="The name of the table.")
    choices_parser.add_argument("--field-name", required=True, help="The name of the field.")
    choices_parser.add_argument("--language", default="pt", help="The language of the choices.")

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

    if args.command == "get-field-choices":
        params = GetFieldChoicesParams(
            table_name=args.table_name,
            field_name=args.field_name,
            language=args.language,
        )
        result = get_field_choices(config, auth_manager, params)
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
