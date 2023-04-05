import json
import orchestrator as o

# Fivetran Google Cloud Function Handler
# 
# Accepts input matching Fivetran documentation here: https://fivetran.com/docs/functions/google-cloud-functions
#       {
#           "agent" : "Fivetran Google Cloud Functions Connector/<external_id>/<schema>",
#           "state": {
#               "cursor": "2020-01-01T00:00:00Z"
#           },
#           "secrets": {
#               "apiToken": "abcdefghijklmnopqrstuvwxyz_0123456789"
#           },
#           "sync_id": "468b681-c376-4117-bbc0-25d8ae02ace1"
#       }
#
# See Sisu's docs for the required input parameters to specify in the "secrets" block. "state" block will be returned with the analysis ID and 
# the start / end dates if specified
def main(req):
    #req_dict = req.json
    req_dict = json.loads(req)

    event = req_dict['secrets']

    return o.main(event)
    
    