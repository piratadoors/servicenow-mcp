import os
import argparse
import json
from dotenv import load_dotenv
from servicenow_mcp.tools.generic_tools import get_table_record, query_table, GetTableRecordParams, QueryTableParams
from servicenow_mcp.utils.config import ServerConfig, AuthConfig, BasicAuthConfig, AuthType
from servicenow_mcp.auth.auth_manager import AuthManager

def main():
    parser = argparse.ArgumentParser(description="ServiceNow Generic CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Sub-parser for the 'get-table-record' command
    record_parser = subparsers.add_parser("get-table-record", help="Get a record from a table.")
    record_parser.add_argument("--table-name", required=True, help="The name of the table.")
    record_parser.add_argument("--sys-id", required=True, help="The sys_id of the record.")

    # Sub-parser for the 'query-table' command
    query_parser = subparsers.add_parser("query-table", help="Query a table.")
    query_parser.add_argument("--table-name", required=True, help="The name of the table.")
    query_parser.add_argument("--query", required=True, help="The query to filter the records.")

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

    if args.command == "get-table-record":
        params = GetTableRecordParams(
            table_name=args.table_name,
            sys_id=args.sys_id,
        )
        result = get_table_record(config, auth_manager, params)
        print(json.dumps(result, indent=2))
    elif args.command == "query-table":
        params = QueryTableParams(
            table_name=args.table_name,
            query=args.query,
        )
        result = query_table(config, auth_manager, params)
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
