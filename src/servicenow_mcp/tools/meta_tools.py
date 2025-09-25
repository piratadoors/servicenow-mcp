import logging
from typing import List
import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)

class GetFieldChoicesParams(BaseModel):
    table_name: str = Field(..., description="The name of the table.")
    field_name: str = Field(..., description="The name of the field.")
    language: str = Field("pt", description="The language of the choices.")

def get_field_choices(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetFieldChoicesParams,
) -> dict:
    """
    Get the choice list for a specific field on a specific table.
    """
    api_url = f"{config.api_url}/table/sys_choice"
    query = f"name={params.table_name}^element={params.field_name}^language={params.language}^inactive=false"
    query_params = {"sysparm_query": query}

    try:
        response = requests.get(
            api_url,
            params=query_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()
        data = response.json()
        choices = [
            {"label": choice.get("label"), "value": choice.get("value")}
            for choice in data.get("result", [])
        ]
        return {
            "success": True,
            "choices": choices,
        }
    except requests.RequestException as e:
        logger.error(f"Failed to get field choices: {e}")
        return {
            "success": False,
            "message": f"Failed to get field choices: {str(e)}",
        }
