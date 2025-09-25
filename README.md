# ServiceNow MCP Server

A Model Context Protocol (MCP) server implementation for ServiceNow, allowing AI assistants like Gemini to interact with ServiceNow instances.

## Core Concepts: A Client/Server Architecture

This project has two main parts:

1.  **The MCP Server**: This is the core of the project. You start it using the `servicenow-mcp` command. It runs in the background and listens for instructions. It's the bridge to your ServiceNow instance.
2.  **The Client Scripts**: These are command-line tools used to send instructions to the server. We have created scripts like `create_incident_cli.py` and `run_list_incidents.py` for this purpose. An AI assistant (like Gemini) or a human user will execute these client scripts to get work done.

You **do not** interact with the tools directly. You run a client script, which then communicates with the MCP server.

## Installation

### Prerequisites

*   Python 3.11 or higher
*   A ServiceNow instance with appropriate access credentials

### 1. Clone the Repository
Clone your fork of the repository (or the original if you are not pushing changes).
```bash
git clone https://github.com/piratadoors/servicenow-mcp.git
cd servicenow-mcp
```

### 2. Create Virtual Environment & Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

### 3. Configure Credentials
This is a critical step. The server needs credentials to connect to your ServiceNow instance.

1.  Create a `.env` file in the root of the project by copying the example file:
    ```bash
    cp .env.example .env
    ```
2.  Edit the `.env` file and fill in your instance details:
    ```
    SERVICENOW_INSTANCE_URL=https://your-instance.service-now.com
    SERVICENOW_USERNAME=your-username
    SERVICENOW_PASSWORD=your-password
    SERVICENOW_AUTH_TYPE=basic
    ```

**Note:** The `.env` file is ignored by Git, so your credentials will never be committed.

## How to Use

Using this project is a two-part process: starting the server and then using the client scripts.

### Part 1: Starting the MCP Server (stdio mode)

The server runs in the background and waits for client scripts to call it.

To start the MCP server:
```bash
servicenow-mcp
```
*You should keep this running in a terminal window.*

### Part 2: Executing Tools with Client Scripts

To ask the server to perform an action, you run one of the client scripts from a **different terminal window**. These scripts are the primary way for an AI assistant or a user to interact with the MCP.

**Example 1: Creating an Incident**
Use the `create_incident_cli.py` script to create a new incident.

```bash
python3 create_incident_cli.py --short-description "My computer is not turning on" --caller-id "your.name" --opened-by "your.name"
```

**Example 2: Listing Open Incidents**
Use the `run_list_incidents.py` script to list incidents. The `--query` parameter accepts a standard ServiceNow encoded query.

```bash
# List incidents that are in state 'New' (state=1)
python3 run_list_incidents.py --query "state=1" --display-value false
```

**Example 3: Counting Open Requests**
Use the `request_cli.py` script to count open requests.

```bash
# Count all open requests (state not in 3, 4, 7)
python3 request_cli.py count --query "stateNOT IN3,4,7"
```

**Example 4: Getting User Details by Email**
Use the `user_cli.py` script to retrieve user information.

```bash
# Get user details for a specific email
python3 user_cli.py get-user --email "user.email@example.com"
```

You can create new client scripts for any of the available tools listed later in this README.

## Project Structure
```
/
├── .env                  # Your local credentials (ignored by Git)
├── .env.example          # Example credentials file
├── create_incident_cli.py  # CLIENT: Script to create incidents
├── run_list_incidents.py   # CLIENT: Script to list incidents
├── count_incidents.py      # CLIENT: Script to count incidents
├── list_groups_cli.py      # CLIENT: Script to list groups
├── request_cli.py          # CLIENT: Script for request management
├── user_cli.py             # CLIENT: Script for user and group management
├── src/
│   └── servicenow_mcp/
│       ├── cli.py          # SERVER: Main entry point for the MCP server
│       └── tools/          # Implementations of all available tools
│           ├── incident_tools.py # Incident management tools
│           ├── request_tools.py  # Request management tools
│           └── user_tools.py     # User and group management tools
└── README.md             # This file
```

## Available Tools

**Note:** The availability of the following tools depends on the loaded tool package (see Tool Packaging section below). By default (`full` package), all tools are available. You can create a `*_cli.py` script for any of them.

#### Incident Management Tools (via `run_list_incidents.py`, `create_incident_cli.py`, `count_incidents.py`)

1.  **create_incident** - Create a new incident in ServiceNow
2.  **update_incident** - Update an existing incident in ServiceNow
3.  **add_comment** - Add a comment to an incident in ServiceNow
4.  **resolve_incident** - Resolve an incident in ServiceNow
5.  **list_incidents** - List incidents from ServiceNow

#### Request Management Tools (via `request_cli.py`)

1.  **list_requests** - List requests (requested items) from ServiceNow
2.  **count_requests** - Count requests (requested items) in ServiceNow

#### User and Group Management Tools (via `user_cli.py`, `list_groups_cli.py`)

1.  **create_user** - Create a new user in ServiceNow
2.  **update_user** - Update an existing user in ServiceNow
3.  **get_user** - Get a user from ServiceNow
4.  **list_users** - List users from ServiceNow
5.  **create_group** - Create a new group in ServiceNow
6.  **update_group** - Update an existing group in ServiceNow
7.  **add_group_members** - Add members to a group in ServiceNow
8.  **remove_group_members** - Remove members from a group in ServiceNow
9.  **list_groups** - List groups from ServiceNow
10. **list_group_members** - List members of a group in ServiceNow

## CLI Tool Reference

This section provides a detailed reference for each of the command-line interface (CLI) scripts available in this project.

### `run_list_incidents.py`

```
usage: run_list_incidents.py [-h] [--limit LIMIT] [--offset OFFSET]
                             [--display-value DISPLAY_VALUE] [--state STATE]
                             [--state-name STATE_NAME]
                             [--assigned-to ASSIGNED_TO] [--category CATEGORY]
                             [--query QUERY]

List ServiceNow incidents.

options:
  -h, --help            show this help message and exit
  --limit LIMIT         Maximum number of incidents to return
  --offset OFFSET       Offset for pagination
  --display-value DISPLAY_VALUE
                        Return display values for reference fields (default:
                        True)
  --state STATE         Filter by incident state ID
  --state-name STATE_NAME
                        Filter by incident state display name
  --assigned-to ASSIGNED_TO
                        Filter by assigned user
  --category CATEGORY   Filter by category
  --query QUERY         A ServiceNow encoded query string for filtering
                        incidents
```

### `create_incident_cli.py`

```
usage: create_incident_cli.py [-h] --short-description SHORT_DESCRIPTION
                              [--description DESCRIPTION]
                              [--caller-id CALLER_ID] [--opened-by OPENED_BY]
                              [--sc-cat-item-producer SC_CAT_ITEM_PRODUCER]
                              [--category CATEGORY]
                              [--subcategory SUBCATEGORY]
                              [--priority PRIORITY] [--impact IMPACT]
                              [--urgency URGENCY] [--assigned-to ASSIGNED_TO]
                              [--assignment-group ASSIGNMENT_GROUP]

Create a ServiceNow incident.

options:
  -h, --help            show this help message and exit
  --short-description SHORT_DESCRIPTION
                        Short description of the incident
  --description DESCRIPTION
                        Detailed description of the incident
  --caller-id CALLER_ID
                        User who reported the incident
  --opened-by OPENED_BY
                        User who opened the incident
  --sc-cat-item-producer SC_CAT_ITEM_PRODUCER
                        Service catalog item producer
  --category CATEGORY   Category of the incident
  --subcategory SUBCATEGORY
                        Subcategory of the incident
  --priority PRIORITY   Priority of the incident
  --impact IMPACT       Impact of the incident
  --urgency URGENCY     Urgency of the incident
  --assigned-to ASSIGNED_TO
                        User assigned to the incident
  --assignment-group ASSIGNMENT_GROUP
                        Group assigned to the incident
```

### `request_cli.py`

```
usage: request_cli.py [-h] {list,count} ...

ServiceNow Request CLI

positional arguments:
  {list,count}
    list        List ServiceNow requests.
    count       Count ServiceNow requests.

options:
  -h, --help    show this help message and exit
```

#### `request_cli.py list`

```
usage: request_cli.py list [-h] [--limit LIMIT] [--offset OFFSET]
                           [--display-value DISPLAY_VALUE] [--query QUERY]

options:
  -h, --help            show this help message and exit
  --limit LIMIT         Maximum number of requests to return
  --offset OFFSET       Offset for pagination
  --display-value DISPLAY_VALUE
                        Return display values for reference fields (default:
                        True)
  --query QUERY         A ServiceNow encoded query string for filtering
                        requests
```

#### `request_cli.py count`

```
usage: request_cli.py count [-h] [--query QUERY]

options:
  -h, --help     show this help message and exit
  --query QUERY  A ServiceNow encoded query string for filtering requests
```

### `user_cli.py`

```
usage: user_cli.py [-h]
                   {get-user,add-group-member,list-users,list-groups,list-group-members}
                   ...

ServiceNow User and Group CLI

positional arguments:
  {get-user,add-group-member,list-users,list-groups,list-group-members}
    get-user            Get details of a ServiceNow user.
    add-group-member    Add a user to a ServiceNow group.
    list-users          List ServiceNow users.
    list-groups         List ServiceNow groups.
    list-group-members  List members of a ServiceNow group.

options:
  -h, --help            show this help message and exit
```

#### `user_cli.py get-user`

```
usage: user_cli.py get-user [-h] [--email EMAIL] [--user-name USER_NAME]
                            [--user-id USER_ID]

options:
  -h, --help            show this help message and exit
  --email EMAIL         Email address of the user
  --user-name USER_NAME
                        Username of the user
  --user-id USER_ID     Sys_id of the user
```

#### `user_cli.py add-group-member`

```
usage: user_cli.py add-group-member [-h] --group-id GROUP_ID --member MEMBER

options:
  -h, --help           show this help message and exit
  --group-id GROUP_ID  The name or sys_id of the group
  --member MEMBER      The email or username of the user to add
```

#### `user_cli.py list-users`

```
usage: user_cli.py list-users [-h] [--limit LIMIT] [--offset OFFSET]
                              [--active ACTIVE] [--department DEPARTMENT]
                              [--query QUERY]

options:
  -h, --help            show this help message and exit
  --limit LIMIT         Maximum number of users to return
  --offset OFFSET       Offset for pagination
  --active ACTIVE       Filter by active status
  --department DEPARTMENT
                        Filter by department
  --query QUERY         Case-insensitive search term that matches against
                        name, username, or email fields.
```

#### `user_cli.py list-groups`

```
usage: user_cli.py list-groups [-h] [--limit LIMIT] [--offset OFFSET]
                               [--active ACTIVE] [--query QUERY] [--type TYPE]

options:
  -h, --help       show this help message and exit
  --limit LIMIT    Maximum number of groups to return
  --offset OFFSET  Offset for pagination
  --active ACTIVE  Filter by active status
  --query QUERY    Case-insensitive search term that matches against group
                   name or description fields.
  --type TYPE      Filter by group type
```

#### `user_cli.py list-group-members`

```
usage: user_cli.py list-group-members [-h] --group-id GROUP_ID [--limit LIMIT]
                                      [--offset OFFSET]

options:
  -h, --help           show this help message and exit
  --group-id GROUP_ID  The name or sys_id of the group
  --limit LIMIT        Maximum number of members to return
  --offset OFFSET      Offset for pagination
```

### `list_groups_cli.py`

```
usage: list_groups_cli.py [-h] [--limit LIMIT] [--offset OFFSET]
                          [--active ACTIVE] [--query QUERY] [--type TYPE]

List ServiceNow groups.

options:
  -h, --help       show this help message and exit
  --limit LIMIT    Maximum number of groups to return
  --offset OFFSET  Offset for pagination
  --active ACTIVE  Filter by active status
  --query QUERY    A ServiceNow encoded query string for filtering groups
  --type TYPE      Filter by group type
```

### `resolve_incident_cli.py`

```
usage: resolve_incident_cli.py [-h] --number NUMBER --resolution-code
                               RESOLUTION_CODE --resolution-notes
                               RESOLUTION_NOTES --solution-type SOLUTION_TYPE
                               [--assignee ASSIGNEE] [--caller-id CALLER_ID]

Resolve a ServiceNow incident with all fields.

options:
  -h, --help            show this help message and exit
  --number NUMBER       Incident number
  --resolution-code RESOLUTION_CODE
                        Resolution code
  --resolution-notes RESOLUTION_NOTES
                        Resolution notes
  --solution-type SOLUTION_TYPE
                        Solution type
  --assignee ASSIGNEE   Assignee email
  --caller-id CALLER_ID
                        Caller ID
```

### `count_incidents.py`

```
usage: count_incidents.py [-h] [--query QUERY] [--state-name STATE_NAME]

Count ServiceNow incidents.

options:
  -h, --help            show this help message and exit
  --query QUERY         A ServiceNow encoded query string for filtering
                        incidents
  --state-name STATE_NAME
                        Filter by incident state display name
```