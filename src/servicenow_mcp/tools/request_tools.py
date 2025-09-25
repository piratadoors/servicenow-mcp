
"""
Request tools for the ServiceNow MCP server.
"""

import logging
from typing import Optional

import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)


class ListRequestsParams(BaseModel):
    """Parameters for listing requests."""    
    limit: int = Field(10, description="Maximum number of requests to return")
    offset: int = Field(0, description="Offset for pagination")
    display_value: bool = Field(True, description="Return display values for reference fields.")
    query: Optional[str] = Field(None, description="A ServiceNow encoded query string for filtering requests.")

class CountRequestsParams(BaseModel):
    """Parameters for counting requests."""
    query: Optional[str] = Field(None, description="A ServiceNow encoded query string for filtering requests.")

class UpdateRequestParams(BaseModel):
    """Parameters for updating a request."""
    request_id: str = Field(..., description="Request ID or sys_id")
    assigned_to: Optional[str] = Field(None, description="User assigned to the request")

def update_request(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: UpdateRequestParams,
) -> dict:
    """
    Update an existing request in ServiceNow.
    """
    api_url = f"{config.api_url}/table/sc_req_item/{params.request_id}"

    data = {}
    if params.assigned_to:
        data["assigned_to"] = params.assigned_to

    try:
        response = requests.put(
            api_url,
            json=data,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()
        result = response.json().get("result", {})
        return {
            "success": True,
            "message": "Request updated successfully",
            "request": result,
        }
    except requests.RequestException as e:
        logger.error(f"Failed to update request: {e}")
        return {
            "success": False,
            "message": f"Failed to update request: {str(e)}",
        }

def list_requests(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: ListRequestsParams,
) -> dict:
    """
    List requests (requested items) from ServiceNow.
    """
    api_url = f"{config.api_url}/table/sc_req_item"

    query_params = {
        "sysparm_limit": params.limit,
        "sysparm_offset": params.offset,
        "sysparm_display_value": str(params.display_value).lower(),
        "sysparm_exclude_reference_link": "true",
    }
    
    if params.query:
        query_params["sysparm_query"] = params.query
    
    try:
        response = requests.get(
            api_url,
            params=query_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()
        
        data = response.json()
        requests_list = []
        
        for req_data in data.get("result", []):
            assignment_group = req_data.get("assignment_group")
            if isinstance(assignment_group, dict):
                assignment_group = assignment_group.get("display_value")
            
            request = {
                "sys_id": req_data.get("sys_id"),
                "number": req_data.get("number"),
                "short_description": req_data.get("short_description"),
                "description": req_data.get("description"),
                "state": req_data.get("state"),
                "assignment_group": assignment_group,
                "created_on": req_data.get("sys_created_on"),
                "updated_on": req_data.get("sys_updated_on"),
            }
            requests_list.append(request)
        
        return {
            "success": True,
            "message": f"Found {len(requests_list)} requests",
            "requests": requests_list
        }
        
    except requests.RequestException as e:
        logger.error(f"Failed to list requests: {e}")
        return {
            "success": False,
            "message": f"Failed to list requests: {str(e)}",
            "requests": []
        }

def count_requests(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: CountRequestsParams,
) -> dict:
    """
    Count requests (requested items) in ServiceNow.
    """
    api_url = f"{config.api_url}/stats/sc_req_item"
    
    query_params = {
        "sysparm_count": "true"
    }
    if params.query:
        query_params["sysparm_query"] = params.query

    try:
        response = requests.get(
            api_url,
            params=query_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        response.raise_for_status()
        
        data = response.json()
        count = data.get("result", {}).get("stats", {}).get("count", 0)
        
        return {"success": True, "count": count}
        
    except requests.RequestException as e:
        logger.error(f"Failed to count requests: {e}")
        return {"success": False, "message": f"Failed to count requests: {str(e)}"}
