
import os
import argparse
import json
from dotenv import load_dotenv
from servicenow_mcp.tools.request_tools import list_requests, count_requests, ListRequestsParams, CountRequestsParams
from servicenow_mcp.utils.config import ServerConfig, AuthConfig, BasicAuthConfig, AuthType
from servicenow_mcp.auth.auth_manager import AuthManager

def main():
    parser = argparse.ArgumentParser(description="ServiceNow Request CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Sub-parser for the 'list' command
    list_parser = subparsers.add_parser("list", help="List ServiceNow requests.")
    list_parser.add_argument("--limit", type=int, default=10, help="Maximum number of requests to return")
    list_parser.add_argument("--offset", type=int, default=0, help="Offset for pagination")
    list_parser.add_argument("--display-value", type=lambda x: (str(x).lower() == 'true'), default=True, help="Return display values for reference fields (default: True)")
    list_parser.add_argument("--query", help="A ServiceNow encoded query string for filtering requests")

    # Sub-parser for the 'count' command
    count_parser = subparsers.add_parser("count", help="Count ServiceNow requests.")
    count_parser.add_argument("--query", help="A ServiceNow encoded query string for filtering requests")

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

    if args.command == "list":
        params = ListRequestsParams(
            limit=args.limit,
            offset=args.offset,
            display_value=args.display_value,
            query=args.query
        )
        result = list_requests(config, auth_manager, params)
        print(json.dumps(result, indent=2))
    elif args.command == "count":
        params = CountRequestsParams(query=args.query)
        result = count_requests(config, auth_manager, params)
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
