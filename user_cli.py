
import os
import argparse
import json
from dotenv import load_dotenv
from servicenow_mcp.tools.user_tools import get_user, create_user, update_user, add_group_members, remove_group_members, list_users, list_groups, list_group_members, GetUserParams, CreateUserParams, UpdateUserParams, AddGroupMembersParams, RemoveGroupMembersParams, ListUsersParams, ListGroupsParams, ListGroupMembersParams
from servicenow_mcp.utils.config import ServerConfig, AuthConfig, BasicAuthConfig, AuthType
from servicenow_mcp.auth.auth_manager import AuthManager

def main():
    parser = argparse.ArgumentParser(description="ServiceNow User and Group CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Sub-parser for the 'get-user' command
    get_user_parser = subparsers.add_parser("get-user", help="Get details of a ServiceNow user.")
    get_user_parser.add_argument("--email", help="Email address of the user")
    get_user_parser.add_argument("--user-name", help="Username of the user")
    get_user_parser.add_argument("--user-id", help="Sys_id of the user")

    # Sub-parser for the 'add-group-member' command
    add_group_member_parser = subparsers.add_parser("add-group-member", help="Add a user to a ServiceNow group.")
    add_group_member_parser.add_argument("--group-id", required=True, help="The name or sys_id of the group")
    add_group_member_parser.add_argument("--member", required=True, help="The email or username of the user to add")

    # Sub-parser for the 'list-users' command
    list_users_parser = subparsers.add_parser("list-users", help="List ServiceNow users.")
    list_users_parser.add_argument("--limit", type=int, default=10, help="Maximum number of users to return")
    list_users_parser.add_argument("--offset", type=int, default=0, help="Offset for pagination")
    list_users_parser.add_argument("--active", type=lambda x: (str(x).lower() == 'true'), help="Filter by active status")
    list_users_parser.add_argument("--department", help="Filter by department")
    list_users_parser.add_argument("--query", help="Case-insensitive search term that matches against name, username, or email fields.")

    # Sub-parser for the 'list-groups' command
    list_groups_parser = subparsers.add_parser("list-groups", help="List ServiceNow groups.")
    list_groups_parser.add_argument("--limit", type=int, default=10, help="Maximum number of groups to return")
    list_groups_parser.add_argument("--offset", type=int, default=0, help="Offset for pagination")
    list_groups_parser.add_argument("--active", type=lambda x: (str(x).lower() == 'true'), help="Filter by active status")
    list_groups_parser.add_argument("--query", help="Case-insensitive search term that matches against group name or description fields.")
    list_groups_parser.add_argument("--type", help="Filter by group type")

    # Sub-parser for the 'list-group-members' command
    list_group_members_parser = subparsers.add_parser("list-group-members", help="List members of a ServiceNow group.")
    list_group_members_parser.add_argument("--group-id", required=True, help="The name or sys_id of the group")
    list_group_members_parser.add_argument("--limit", type=int, default=100, help="Maximum number of members to return")
    list_group_members_parser.add_argument("--offset", type=int, default=0, help="Offset for pagination")


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

    if args.command == "get-user":
        params = GetUserParams(
            email=args.email,
            user_name=args.user_name,
            user_id=args.user_id
        )
        result = get_user(config, auth_manager, params)
        print(json.dumps(result, indent=2))
    elif args.command == "add-group-member":
        params = AddGroupMembersParams(
            group_id=args.group_id,
            members=[args.member]
        )
        result = add_group_members(config, auth_manager, params)
        print(json.dumps(result.model_dump(), indent=2))
    elif args.command == "list-users":
        params = ListUsersParams(
            limit=args.limit,
            offset=args.offset,
            active=args.active,
            department=args.department,
            query=args.query
        )
        result = list_users(config, auth_manager, params)
        print(json.dumps(result, indent=2))
    elif args.command == "list-groups":
        params = ListGroupsParams(
            limit=args.limit,
            offset=args.offset,
            active=args.active,
            query=args.query,
            type=args.type
        )
        result = list_groups(config, auth_manager, params)
        print(json.dumps(result, indent=2))
    elif args.command == "list-group-members":
        params = ListGroupMembersParams(
            group_id=args.group_id,
            limit=args.limit,
            offset=args.offset
        )
        result = list_group_members(config, auth_manager, params)
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
