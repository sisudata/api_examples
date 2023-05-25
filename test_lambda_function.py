import lambda_function as lf
import config

print('***** CALLING LAMBDA FUNCTION TO TEST A TREND DETECTION *****')
event = {'ANALYSIS_ID': '', 'API_KEY': config.API_KEY, 'EXECUTE_ANALYSIS': 'True'}
response = lf.lambda_handler(event, None)
print('***** RESPONSE: ' + response['body'])

print('***** CALLING LAMBDA FUNCTION TO TEST A TIME COMPARE *****')
event = {'ANALYSIS_ID': '', 'API_KEY': config.API_KEY, 'EXECUTE_ANALYSIS': 'True'}
response = lf.lambda_handler(event, None)
print('***** RESPONSE: ' + response['body'])

