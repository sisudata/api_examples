import json
import datetime
from dateutil.relativedelta import relativedelta
import load_analysis_results as lar
import config

def main(event):
    if config.DEBUG:
        print('Input - API_KEY=' + event['API_KEY'])
    
    print('Input - ANALYSIS_ID=' + event['ANALYSIS_ID'])

    conn = None

    RETURN_RESULTS = False

    if 'RETURN_RESULTS' in event:
        print('Input - RETURN_RESULTS=' + event['RETURN_RESULTS'])

        if event['RETURN_RESULTS'] == 'True' or event['RETURN_RESULTS'] == 'true' or event['RETURN_RESULTS'] == 'TRUE':
            RETURN_RESULTS = True

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
        conn = lar.process_tc_action(event['API_KEY'], int(event['ANALYSIS_ID']), RETURN_RESULTS, ACTION_TYPE, START_DATE, END_DATE)
    else:
        EXECUTE_ANALYSIS = True
        
        if 'EXECUTE_ANALYSIS' in event:
            print('Input - EXECUTE_ANALYSIS=' + event['EXECUTE_ANALYSIS'])

            if event['EXECUTE_ANALYSIS'] == 'False' or event['EXECUTE_ANALYSIS'] == 'false' or event['EXECUTE_ANALYSIS'] == 'FALSE':
                EXECUTE_ANALYSIS = False

        print('Executing Load...')
        conn = lar.execute_load(event['API_KEY'], int(event['ANALYSIS_ID']), EXECUTE_ANALYSIS, RETURN_RESULTS, None)

    if RETURN_RESULTS:
        return conn.formatResults(event)
    else:
        return {
            'statusCode': 200,
            'body': json.dumps('Execution for ANALYSIS_ID ' + event['ANALYSIS_ID'] + ' completed successfully')
        }
