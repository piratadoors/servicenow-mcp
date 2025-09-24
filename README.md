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