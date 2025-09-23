
import os
import argparse
from dotenv import load_dotenv
from servicenow_mcp.tools.incident_tools import create_incident, CreateIncidentParams
from servicenow_mcp.utils.config import ServerConfig, AuthConfig, BasicAuthConfig, AuthType
from servicenow_mcp.auth.auth_manager import AuthManager

def main():
    parser = argparse.ArgumentParser(description="Create a ServiceNow incident.")
    parser.add_argument("--short-description", required=True, help="Short description of the incident")
    parser.add_argument("--description", help="Detailed description of the incident")
    parser.add_argument("--caller-id", help="User who reported the incident")
    parser.add_argument("--opened-by", help="User who opened the incident")
    parser.add_argument("--sc-cat-item-producer", help="Service catalog item producer")
    parser.add_argument("--category", help="Category of the incident")
    parser.add_argument("--subcategory", help="Subcategory of the incident")
    parser.add_argument("--priority", help="Priority of the incident")
    parser.add_argument("--impact", help="Impact of the incident")
    parser.add_argument("--urgency", help="Urgency of the incident")
    parser.add_argument("--assigned-to", help="User assigned to the incident")
    parser.add_argument("--assignment-group", help="Group assigned to the incident")
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

    params = CreateIncidentParams(
        short_description=args.short_description,
        description=args.description,
        caller_id=args.caller_id,
        opened_by=args.opened_by,
        sc_cat_item_producer=args.sc_cat_item_producer,
        category=args.category,
        subcategory=args.subcategory,
        priority=args.priority,
        impact=args.impact,
        urgency=args.urgency,
        assigned_to=args.assigned_to,
        assignment_group=args.assignment_group
    )

    result = create_incident(config, auth_manager, params)
    print(result)

if __name__ == "__main__":
    main()
