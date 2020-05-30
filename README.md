# TFS_Team_Room_Client
A front end client for the TFS 2015 Team Room back end.

## Required Tools
Windows  
Python 3.7 (https://www.python.org/downloads/release/python-377/)  
Poetry 1.0.5+ (https://python-poetry.org/docs/#installation)

## Build and Run Instructions (Developer)
From the root directory:  
`poetry install`  
`poetry run python .\tfs_chatclient\gui\main.py`

# Configuration File Settings
In order to run properly, a configuration file must exist in the users current directory. See tfs_chatclient/tfs_config.json.example for an example configuration. Each entry will be defined below:  

- domain: The network domain used for NTLM based logins. If left empty, domains can still be entered manually during login. For example, DOMAIN\username.  
- base_url: The base URL of the TFS server. For example, "http://TFS-SERVER:8080/tfs/TFS_Team_Site/".
