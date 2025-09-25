import logging
import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)

class GetTableRecordParams(BaseModel):
    table_name: str = Field(..., description="The name of the table.")
    sys_id: str = Field(..., description="The sys_id of the record.")

class QueryTableParams(BaseModel):
    table_name: str = Field(..., description="The name of the table.")
    query: str = Field(..., description="The query to filter the records.")

def get_table_record(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetTableRecordParams,
) -> dict:
    """
    Get a single record from a specified table by its sys_id.
    """
    api_url = f"{config.api_url}/table/{params.table_name}/{params.sys_id}"

    try:
        response = requests.get(
            api_url,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()
        data = response.json()
        return {
            "success": True,
            "record": data.get("result", {}),
        }
    except requests.RequestException as e:
        logger.error(f"Failed to get table record: {e}")
        return {
            "success": False,
            "message": f"Failed to get table record: {str(e)}",
        }

def query_table(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: QueryTableParams,
) -> dict:
    """
    Query a table with a given query.
    """
    api_url = f"{config.api_url}/table/{params.table_name}"
    query_params = {"sysparm_query": params.query}

    try:
        response = requests.get(
            api_url,
            params=query_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()
        data = response.json()
        return {
            "success": True,
            "records": data.get("result", []),
        }
    except requests.RequestException as e:
        logger.error(f"Failed to query table: {e}")
        return {
            "success": False,
            "message": f"Failed to query table: {str(e)}",
        }
