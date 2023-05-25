import fivetran_gcf_main as fgm
import config
import json

print('***** CALLING FIVETRAN GOOGLE CLOUD FUNCTION TO TEST A TREND DETECTION *****')
event = {'ANALYSIS_ID': '', 'API_KEY': config.API_KEY, 'EXECUTE_ANALYSIS': 'False', 'RETURN_RESULTS': 'True'}
req_dict = {
    'agent': 'Fivetran Google Cloud Functions Connector/<external_id>/<schema>',
    'state': {
        'cursor': '2020-01-01T00:00:00Z'
    },
    'secrets': event,
    'sync_id': '468b681-c376-4117-bbc0-25d8ae02ace1'
}
req = json.dumps(req_dict, default=str)
response = json.dumps(fgm.main(req), default=str)
print('***** RESPONSE: ' + response)

print('***** CALLING FIVETRAN GOOGLE CLOUD FUNCTION TO TEST A TIME COMPARE *****')
event = {'ANALYSIS_ID': '', 'API_KEY': config.API_KEY, 'EXECUTE_ANALYSIS': 'False', 'RETURN_RESULTS': 'True'}
req_dict = {
    'agent': 'Fivetran Google Cloud Functions Connector/<external_id>/<schema>',
    'state': {
        'cursor': '2020-01-01T00:00:00Z'
    },
    'secrets': event,
    'sync_id': '468b681-c376-4117-bbc0-25d8ae02ace1'
}
req = json.dumps(req_dict, default=str)
response = fgm.main(req)
print('***** RESPONSE: ' + response)

