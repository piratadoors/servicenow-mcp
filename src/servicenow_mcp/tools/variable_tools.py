import logging
from typing import List
import requests
from pydantic import BaseModel, Field

from servicenow_mcp.auth.auth_manager import AuthManager
from servicenow_mcp.utils.config import ServerConfig

logger = logging.getLogger(__name__)

class GetRITMVariablesParams(BaseModel):
    ritm_sys_id: str = Field(..., description="The sys_id of the Requested Item.")

def get_ritm_variables(
    config: ServerConfig,
    auth_manager: AuthManager,
    params: GetRITMVariablesParams,
) -> dict:
    """
    Get the variables for a specific Requested Item (RITM).
    """
    # Step 1: Get the list of variable sys_ids from the sc_item_option_mtom table
    mtom_api_url = f"{config.api_url}/table/sc_item_option_mtom"
    mtom_query = f"request_item={params.ritm_sys_id}"
    mtom_query_params = {"sysparm_query": mtom_query}

    try:
        mtom_response = requests.get(
            mtom_api_url,
            params=mtom_query_params,
            headers=auth_manager.get_headers(),
            timeout=config.timeout,
        )
        mtom_response.raise_for_status()
        mtom_data = mtom_response.json()
        option_sys_ids = [item.get("sc_item_option") for item in mtom_data.get("result", [])]

    except requests.RequestException as e:
        logger.error(f"Failed to get RITM variable mappings: {e}")
        return {
            "success": False,
            "message": f"Failed to get RITM variable mappings: {str(e)}",
        }

    # Step 2 & 3: Get the details for each variable
    variables = []
    option_api_url = f"{config.api_url}/table/sc_item_option"
    question_api_url = f"{config.api_url}/table/item_option_new"

    for option_sys_id in option_sys_ids:
        if not option_sys_id:
            continue
        
        # Get the sc_item_option record
        option_query = f"sys_id={option_sys_id.get('value')}"
        option_query_params = {"sysparm_query": option_query}

        try:
            option_response = requests.get(
                option_api_url,
                params=option_query_params,
                headers=auth_manager.get_headers(),
                timeout=config.timeout,
            )
            option_response.raise_for_status()
            option_data = option_response.json()
            option_result = option_data.get("result", [])
            if not option_result:
                continue

            item_option = option_result[0]
            value = item_option.get("value")
            item_option_new_sys_id = item_option.get("item_option_new", {}).get("value")

            if not item_option_new_sys_id:
                continue

            # Get the item_option_new record (the question)
            question_query = f"sys_id={item_option_new_sys_id}"
            question_query_params = {"sysparm_query": question_query}
            question_response = requests.get(
                question_api_url,
                params=question_query_params,
                headers=auth_manager.get_headers(),
                timeout=config.timeout,
            )
            question_response.raise_for_status()
            question_data = question_response.json()
            question_result = question_data.get("result", [])
            if question_result:
                question_item = question_result[0]
                question_text = question_item.get("question_text")
                variables.append({
                    "question": question_text,
                    "value": value,
                })

        except requests.RequestException as e:
            logger.error(f"Failed to get RITM variable details: {e}")
            # Continue to next variable if one fails
            continue

    return {
        "success": True,
        "variables": variables,
    }
