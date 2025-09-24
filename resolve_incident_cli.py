
import os
import argparse
import json
from dotenv import load_dotenv
from servicenow_mcp.tools.incident_tools import resolve_incident_with_all_fields, ResolveIncidentWithAllFieldsParams
from servicenow_mcp.utils.config import ServerConfig, AuthConfig, BasicAuthConfig, AuthType
from servicenow_mcp.auth.auth_manager import AuthManager

def main():
    parser = argparse.ArgumentParser(description="Resolve a ServiceNow incident with all fields.")
    parser.add_argument("--number", required=True, help="Incident number")
    parser.add_argument("--resolution-code", required=True, help="Resolution code")
    parser.add_argument("--resolution-notes", required=True, help="Resolution notes")
    parser.add_argument("--solution-type", required=True, help="Solution type")
    parser.add_argument("--assignee", help="Assignee email")
    parser.add_argument("--caller-id", help="Caller ID")
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

    params = ResolveIncidentWithAllFieldsParams(
        incident_id=args.number, 
        resolution_code=args.resolution_code, 
        resolution_notes=args.resolution_notes,
        solution_type=args.solution_type,
        assigned_to=args.assignee,
        caller_id=args.caller_id
    )

    result = resolve_incident_with_all_fields(config, auth_manager, params)
    print(json.dumps(result.__dict__, indent=2))

if __name__ == "__main__":
    main()
