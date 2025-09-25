
import os
import argparse
import json
from dotenv import load_dotenv
from servicenow_mcp.tools.request_tools import list_requests, count_requests, update_request, ListRequestsParams, CountRequestsParams, UpdateRequestParams
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

    # Sub-parser for the 'update' command
    update_parser = subparsers.add_parser("update", help="Update a ServiceNow request.")
    update_parser.add_argument("--request-id", required=True, help="The sys_id of the request to update.")
    update_parser.add_argument("--assigned-to", help="The email or username of the user to assign the request to.")
    update_parser.add_argument("--state", help="The state of the request.")
    update_parser.add_argument("--close-notes", help="The closure notes for the request.")
    update_parser.add_argument("--u-close-code", help="The closure code for the request.")

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
    elif args.command == "update":
        params = UpdateRequestParams(
            request_id=args.request_id,
            assigned_to=args.assigned_to,
            state=args.state,
            close_notes=args.close_notes,
            u_close_code=args.u_close_code
        )
        result = update_request(config, auth_manager, params)
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
