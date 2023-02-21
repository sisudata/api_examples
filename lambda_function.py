import json
import datetime
from dateutil.relativedelta import relativedelta
import load_analysis_results as lar
import config

def lambda_handler(event, context):
    if config.DEBUG:
        print('Input - API_KEY=' + event['API_KEY'])
    
    print('Input - ANALYSIS_ID=' + event['ANALYSIS_ID'])

    if 'ACTION_TYPE' in event:
        print('Input - ACTION_TYPE=' + event['ACTION_TYPE'])
        print('Input - START_DATE=' + event['START_DATE'])

        ACTION_TYPE = event['ACTION_TYPE']
        START_DATE = event['START_DATE']

        if START_DATE == 'YESTERDAY':
            START_DATE = datetime.date.today() - relativedelta(days=1)
        elif START_DATE == 'TODAY':
            START_DATE = datetime.date.today()
        elif START_DATE == 'LAST_WEEK':
            START_DATE = datetime.date.today() - relativedelta(days=7)
        elif START_DATE == 'THIS_WEEK':
            START_DATE = datetime.date.today()
        elif START_DATE == 'LAST_MONTH':
            START_DATE = datetime.date.today() - relativedelta(months=1)
        else:
            START_DATE = datetime.datetime.strptime(event['START_DATE'], '%Y-%m-%d')

        END_DATE = ''

        if 'END_DATE' in event:
            print('Input - END_DATE=' + event['END_DATE'])
            END_DATE = datetime.datetime.strptime(event['END_DATE'], '%Y-%m-%d')
        else:
            END_DATE = START_DATE

        print('Processing Action...')
        lar.process_tc_action(event['API_KEY'], int(event['ANALYSIS_ID']), ACTION_TYPE, START_DATE, END_DATE)
    else:
        print('Executing Load...')
        lar.execute_load(event['API_KEY'], int(event['ANALYSIS_ID']))

    return {
        'statusCode': 200,
        'body': json.dumps('Execution completed successfully')
    }
