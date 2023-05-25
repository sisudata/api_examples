# import connection libraries
import datetime
from dateutil.relativedelta import relativedelta
import pandas
import numpy
from pysisu import PySisu
from pysisu.formats import LatestAnalysisResultsFormats
from pysisu.proto.sisu.v1.api import ModifyAnalysisRequestAnalysis, AnalysisResultRunStatus, UnitsConfigUnitType
from time import sleep
import io
import config

# ACTION_TYPE should be one of:
#   DOD: Day Over Day
#   WOW: Week Over Week
#   MOM: Month Over Month
#
# START_DATE should be a datetime object
# END_DATE should be a datetime object
def process_tc_action(API_KEY: str, ANALYSIS_ID: int, RETURN_RESULTS: bool, ACTION_TYPE: str, START_DATE: datetime, END_DATE: datetime):
    print('Starting process_tc_action at ' + str(datetime.datetime.now()))

    # Connect to Sisu
    sisu = PySisu(API_KEY)
    print('Successfully connected to Sisu!')

    recentStartDate = recentEndDate = previousStartDate = previousEndDate = datetime.date(1900, 1, 1)

    timeDelta = ''

    # Sisu Time Comparisons require four dates corresponding to the start/end dates of the recent/previous period
    # Recent period must be chronologically AFTER previous period
    # End Dates should be one day AFTER the ACTUAL calendar end date desired (i.e. if you want to run for 1 Dec 2018, end date should be 2 Dec 2018)

    # For a Day Over Day history run, we advance dates by one day, update the analysis, and execute the load
    if(ACTION_TYPE == 'DOD'):
        # Set the timeDelta to be one day
        timeDelta = relativedelta(days=1)
    # For a Week Over Week history run, we advance dates by seven days, update the analysis, and execute the load
    elif(ACTION_TYPE == 'WOW'):
        # Set the timeDelta to be one day
        timeDelta = relativedelta(days=7)
    # For a Month Over Month history run, we advance dates by one month, update the analysis, and execute the load
    elif(ACTION_TYPE == 'MOM'):
        # Set the timeDelta to be one day
        timeDelta = relativedelta(months=1)

    # Set the period start / end dates
    recentStartDate = START_DATE
    recentEndDate = START_DATE + timeDelta
    previousStartDate = START_DATE - timeDelta
    previousEndDate = START_DATE

    conn = None

    # We'll update the analysis, execute the load, and then advance the dates, until we complete the last date in the date range
    while(recentStartDate <= END_DATE):
        print('Updating analysis configuration for recentStartDate=' + str(recentStartDate) + '; recentEndDate=' + str(recentEndDate) + '; previousStartDate=' + str(previousStartDate) + '; previousEndDate=' + str(previousEndDate))

        previous_period = {'startDate': str(previousStartDate), 'endDate': str(previousEndDate)}
        recent_period = {'startDate': str(recentStartDate), 'endDate': str(recentEndDate)}

        expression = {'previous_range': previous_period, 'recent_range': recent_period}
        req = ModifyAnalysisRequestAnalysis().from_dict(expression)

        if(config.DEBUG):
            print('Request JSON=' + req.to_json())

        result = sisu.modify_analysis(ANALYSIS_ID, req)

        print('Updated Analysis Configuration!')
        conn = execute_load(API_KEY, ANALYSIS_ID, True, RETURN_RESULTS, conn)

        previousStartDate += timeDelta
        previousEndDate += timeDelta
        recentStartDate += timeDelta
        recentEndDate += timeDelta
    
    # All done!
    print('Completing process_tc_action at ' + str(datetime.datetime.now()))

    if RETURN_RESULTS:
        return conn
    else:
        return None

def execute_load(API_KEY: str, ANALYSIS_ID: int, EXECUTE_ANALYSIS: bool, RETURN_RESULTS: bool, _conn):
    # So... get to it!
    print('Starting execute_load at ' + str(datetime.datetime.now()))

    # If we have an existing database connection, reuse it
    if _conn:
        # Reuse database connection
        print('Reusing existing database connection!')
        conn = _conn
    else:
        # Get a database connection
        conn = config.getDatabaseConnection()

    # If we're truncating tables as part of this workflow, do it
    if config.TRUNCATE_TABLES:
        print('TRUNCATE REQUESTED!')
        conn.truncateTables()

    # Connect to Sisu
    sisu = PySisu(API_KEY)
    print('Successfully connected to Sisu!')

    # Get the analysis information
    analysis = sisu.get_analysis(ANALYSIS_ID)
    print('Getting analysis info...')

    ANALYSIS_TYPE = ''
    METRIC_NAME = ''
    METRIC_UNIT = ''
    METRIC_UNIT_IS_PERCENTAGE = 0
    METRIC_UNIT_IS_SUFFIX = 0
    METRIC_UNIT_SCALE = ''
    METRIC_UNIT_KMB = ''
    project_name = ''

    # get the metric ID from the analysis, NOT from the analysis results
    ANALYSIS_TYPE = analysis.type.name

    project = sisu.get_project(analysis.project_id)

    print('Getting project info...')
    project_name = project.name

    metric = sisu.get_metric(analysis.metric_id)

    print('Gettimg mettic info...')
    METRIC_NAME = metric.name

    # Decode the metric units information
    if metric.kpi_units_config.type == UnitsConfigUnitType.UNIT_TYPE_PERCENT:
        METRIC_UNIT_IS_PERCENTAGE = 1
        METRIC_UNIT_IS_SUFFIX = 1
        METRIC_UNIT = '%'
    elif metric.kpi_units_config.type == UnitsConfigUnitType.UNIT_TYPE_CURRENCY:
        METRIC_UNIT_IS_PERCENTAGE = 0
        METRIC_UNIT_IS_SUFFIX = 0

        if metric.kpi_units_config.currency == 'EUR':
            METRIC_UNIT = '€'
        elif metric.kpi_units_config.currency == 'USD':
            METRIC_UNIT = '$'
        elif metric.kpi_units_config.currency == 'CAD':
            METRIC_UNIT = 'CA$'
        elif metric.kpi_units_config.currency == 'AUD':
            METRIC_UNIT = 'A$'
        elif metric.kpi_units_config.currency == 'JPY':
            METRIC_UNIT = '¥'
        elif metric.kpi_units_config.currency == 'GBP':
            METRIC_UNIT = '£'

    elif metric.kpi_units_config.type == UnitsConfigUnitType.UNIT_TYPE_NUMBER:
        METRIC_UNIT_IS_PERCENTAGE = 0
        METRIC_UNIT_IS_SUFFIX = 1
        METRIC_UNIT = ''
    elif metric.kpi_units_config.type == UnitsConfigUnitType.UNIT_TYPE_BPS:
        METRIC_UNIT_IS_PERCENTAGE = 0
        METRIC_UNIT_IS_SUFFIX = 1
        METRIC_UNIT = 'bps'
    elif metric.kpi_units_config.type == UnitsConfigUnitType.UNIT_TYPE_CUSTOM:
        METRIC_UNIT_IS_PERCENTAGE = 0
        METRIC_UNIT_IS_SUFFIX = 1
        METRIC_UNIT = metric.kpi_units_config.label
    elif metric.kpi_units_config.label != None:
        METRIC_UNIT_IS_PERCENTAGE = 0
        METRIC_UNIT_IS_SUFFIX = 1
        METRIC_UNIT = metric.kpi_units_config.label
    else:
        METRIC_UNIT_IS_PERCENTAGE = 0
        METRIC_UNIT_IS_SUFFIX = 1
        METRIC_UNIT = ''

    if metric.kpi_units_config.scale == None:
        METRIC_UNIT_SCALE = 1
    else:
        METRIC_UNIT_SCALE = metric.kpi_units_config.scale

    METRIC_UNIT_KMB = metric.kpi_units_config.kmb

    # Delete the analysis metadata
    conn.deleteAnalysisMetadata(ANALYSIS_ID)
    # Insert the analysis metadata
    conn.writeAnalysisMetadata((ANALYSIS_ID, analysis.name, analysis.type.name, analysis.application_url, analysis.created_at, analysis.metric_id, metric.name, metric.desired_direction.name, METRIC_UNIT, METRIC_UNIT_IS_PERCENTAGE, METRIC_UNIT_IS_SUFFIX, METRIC_UNIT_SCALE, str(METRIC_UNIT_KMB), analysis.project_id, project_name, datetime.datetime.now()))

    # If we're not in EXECUTE mode, don't run the analysis, just reuse the results
    if EXECUTE_ANALYSIS == False:
        print('***** NOT IN EXECUTE MODE - Skipping running analysis *****')
    else:
        # Run the analysis synchronously
        sisu.run(ANALYSIS_ID)
        print("Running Analysis Synchronously...")

        errorCount = 0

        # Poll the analysis status and wait until it's finished running
        while True:
            run_status = ''
            try:
                run_status = sisu.get_results(ANALYSIS_ID, format=LatestAnalysisResultsFormats.PROTO).analysis_result.run_status
                print(f"Status of ANALYSIS_ID={ANALYSIS_ID} is {run_status.name}")
            except:
                print('Error checking execution status! Retrying...')
                errorCount += 1
            finally:
                if errorCount >= 5:
                    break

            if run_status != AnalysisResultRunStatus.RUN_STATUS_COMPLETED:
                sleep(5)
            else:
                break

    # Get the analysis summary and details (segments,) and the waterfall
    summary = sisu.get_results(ANALYSIS_ID, format=LatestAnalysisResultsFormats.PROTO, round_to_decimal_place=10).analysis_result
    detail = sisu.get_results(ANALYSIS_ID, confidence_gte='LOW', round_to_decimal_place=10)

    if config.DEBUG:
        print('detail={\n' + detail.to_csv(config.DELIMITER).replace('\'', '') + '\n}')

    print('Analysis summary and detail loaded')

    # Pull out the summary information
    ANALYSIS_RESULT_ID = summary.id
    REQUESTED_AT = summary.requested_at
    COMPLETED_AT = summary.completed_at
    RUN_STATUS = summary.run_status.name
    RUN_TYPE = summary.run_type.name

    if ('TREND' in ANALYSIS_TYPE):
        CURRENT_PERIOD_CARD_LABEL = summary.trend_analysis_result.summary_card.current_period.card_label
        CURRENT_PERIOD_DENOMINATOR_LABEL = summary.trend_analysis_result.summary_card.current_period.denominator_label
        CURRENT_PERIOD_PERCENT_CHANGE = summary.trend_analysis_result.summary_card.current_period.percent_change
        CURRENT_PERIOD_SLOPE = summary.trend_analysis_result.summary_card.current_period.slope
        PREVIOUS_PERIOD_CARD_LABEL = summary.trend_analysis_result.summary_card.previous_period.card_label
        PREVIOUS_PERIOD_DENOMINATOR_LABEL = summary.trend_analysis_result.summary_card.previous_period.denominator_label
        PREVIOUS_PERIOD_PERCENT_CHANGE = summary.trend_analysis_result.summary_card.previous_period.percent_change
        PREVIOUS_PERIOD_SLOPE = summary.trend_analysis_result.summary_card.previous_period.slope

        # Delete any existing summary for this TD run, and insert the summary information into the database
        conn.writeTrendResultSummary((ANALYSIS_ID,
                                                    ANALYSIS_RESULT_ID,
                                                    REQUESTED_AT,
                                                    COMPLETED_AT,
                                                    RUN_STATUS,
                                                    RUN_TYPE,
                                                    CURRENT_PERIOD_CARD_LABEL,
                                                    CURRENT_PERIOD_DENOMINATOR_LABEL,
                                                    CURRENT_PERIOD_PERCENT_CHANGE,
                                                    CURRENT_PERIOD_SLOPE,
                                                    PREVIOUS_PERIOD_CARD_LABEL,
                                                    PREVIOUS_PERIOD_DENOMINATOR_LABEL,
                                                    PREVIOUS_PERIOD_PERCENT_CHANGE,
                                                    PREVIOUS_PERIOD_SLOPE,
                                                    datetime.datetime.now()))

        # Convert the segment table into a dataframe
        df = pandas.read_csv(io.StringIO(detail.to_csv(config.DELIMITER).replace('\'', '')), delimiter=config.DELIMITER)
        df.insert(0, 'ANALYSIS_RESULT_ID', ANALYSIS_RESULT_ID)
        df.insert(0, 'ANALYSIS_ID', ANALYSIS_ID)

        pandas.set_option('display.max_columns', None) 
        pandas.set_option('display.max_rows', 100)
        pandas.set_option('display.width', 1000)

        df.insert(15, 'LOAD_TS', str(datetime.datetime.now().isoformat(timespec='milliseconds')))

        # Make the column names upper case to match the database
        df.columns = map(str.upper, df.columns)

        # Rename a few columns and fix some data types
        df.rename(columns={'START_DATE_INCLUSIVE': 'START_DATE', 'END_DATE_INCLUSIVE': 'END_DATE'}, inplace=True)
        df['START_DATE'] = pandas.to_datetime(df['START_DATE'])
        df['END_DATE'] = pandas.to_datetime(df['END_DATE'])

        if config.DEBUG:
            print(df.dtypes)
            print(df)

        # Write the analysis result details to the database
        conn.writeTrendResultDetail(df, (ANALYSIS_ID, ANALYSIS_RESULT_ID))
    else:
        resultsToDelete = ''

        METRIC_TYPE_LABEL = summary.key_driver_analysis_result.summary_card.metric_type_label

        # If it's a time comparison, get the time compare summary
        if summary.key_driver_analysis_result.time_comparison:
            PREVIOUS_PERIOD_START = summary.key_driver_analysis_result.time_comparison.previous_period.start_date_inclusive
            PREVIOUS_PERIOD_END = summary.key_driver_analysis_result.time_comparison.previous_period.end_date_inclusive
            RECENT_PERIOD_START = summary.key_driver_analysis_result.time_comparison.recent_period.start_date_inclusive
            RECENT_PERIOD_END = summary.key_driver_analysis_result.time_comparison.recent_period.end_date_inclusive
            GROUP_A_NAME = None
            GROUP_B_NAME = None
            PERCENT_CHANGE = summary.key_driver_analysis_result.summary_card.time_comparison_card.percent_change
            SET1_CARD_LABEL = summary.key_driver_analysis_result.summary_card.time_comparison_card.current_period_card.card_label
            SET1_CATEGORY_FILTER = summary.key_driver_analysis_result.summary_card.time_comparison_card.current_period_card.category_filter
            SET1_AVERAGE = summary.key_driver_analysis_result.summary_card.time_comparison_card.current_period_card.average
            SET1_MIN = summary.key_driver_analysis_result.summary_card.time_comparison_card.current_period_card.min
            SET1_MAX = summary.key_driver_analysis_result.summary_card.time_comparison_card.current_period_card.max
            SET1_MEDIAN = summary.key_driver_analysis_result.summary_card.time_comparison_card.current_period_card.median
            SET1_SUM = summary.key_driver_analysis_result.summary_card.time_comparison_card.current_period_card.sum
            SET1_SUMMARY_VALUE = summary.key_driver_analysis_result.summary_card.time_comparison_card.current_period_card.summary_value
            SET1_TOTAL_SIZE = summary.key_driver_analysis_result.summary_card.time_comparison_card.current_period_card.total_size
            SET1_TOTAL_NUMERATOR = summary.key_driver_analysis_result.summary_card.time_comparison_card.current_period_card.total_numerator
            SET1_TOTAL_DENOMINATOR = summary.key_driver_analysis_result.summary_card.time_comparison_card.current_period_card.total_denominator
            SET1_MATCH_SIZE = summary.key_driver_analysis_result.summary_card.time_comparison_card.current_period_card.match_size
            SET1_WEIGHT = summary.key_driver_analysis_result.summary_card.time_comparison_card.current_period_card.weight
            SET2_CARD_LABEL = summary.key_driver_analysis_result.summary_card.time_comparison_card.previous_period_card.card_label
            SET2_CATEGORY_FILTER = summary.key_driver_analysis_result.summary_card.time_comparison_card.previous_period_card.category_filter
            SET2_AVERAGE = summary.key_driver_analysis_result.summary_card.time_comparison_card.previous_period_card.average
            SET2_MIN = summary.key_driver_analysis_result.summary_card.time_comparison_card.previous_period_card.min
            SET2_MAX = summary.key_driver_analysis_result.summary_card.time_comparison_card.previous_period_card.max
            SET2_MEDIAN = summary.key_driver_analysis_result.summary_card.time_comparison_card.previous_period_card.median
            SET2_SUM = summary.key_driver_analysis_result.summary_card.time_comparison_card.previous_period_card.sum
            SET2_SUMMARY_VALUE = summary.key_driver_analysis_result.summary_card.time_comparison_card.previous_period_card.summary_value
            SET2_TOTAL_SIZE = summary.key_driver_analysis_result.summary_card.time_comparison_card.previous_period_card.total_size
            SET2_TOTAL_NUMERATOR = summary.key_driver_analysis_result.summary_card.time_comparison_card.previous_period_card.total_numerator
            SET2_TOTAL_DENOMINATOR = summary.key_driver_analysis_result.summary_card.time_comparison_card.previous_period_card.total_denominator
            SET2_MATCH_SIZE = summary.key_driver_analysis_result.summary_card.time_comparison_card.previous_period_card.match_size
            SET2_WEIGHT = summary.key_driver_analysis_result.summary_card.time_comparison_card.previous_period_card.weight

            resultsToDelete = conn.getTCAnalysisResultIDs(ANALYSIS_ID, RECENT_PERIOD_START, RECENT_PERIOD_END, PREVIOUS_PERIOD_START, PREVIOUS_PERIOD_END)

        # Else if this is a group comparison
        elif summary.key_driver_analysis_result.group_comparison:
            PREVIOUS_PERIOD_START = None
            PREVIOUS_PERIOD_END = None
            RECENT_PERIOD_START = None
            RECENT_PERIOD_END = None
            GROUP_A_NAME = summary.key_driver_analysis_result.group_comparison.group_a.name
            GROUP_B_NAME = summary.key_driver_analysis_result.group_comparison.group_b.name
            PERCENT_CHANGE = summary.key_driver_analysis_result.summary_card.group_comparison_card.percent_change
            SET1_CARD_LABEL = summary.key_driver_analysis_result.summary_card.group_comparison_card.group_a_card.card_label
            SET1_CATEGORY_FILTER = summary.key_driver_analysis_result.summary_card.group_comparison_card.group_a_card.category_filter
            SET1_AVERAGE = summary.key_driver_analysis_result.summary_card.group_comparison_card.group_a_card.average
            SET1_MIN = summary.key_driver_analysis_result.summary_card.group_comparison_card.group_a_card.min
            SET1_MAX = summary.key_driver_analysis_result.summary_card.group_comparison_card.group_a_card.max
            SET1_MEDIAN = summary.key_driver_analysis_result.summary_card.group_comparison_card.group_a_card.median
            SET1_SUM = summary.key_driver_analysis_result.summary_card.group_comparison_card.group_a_card.sum
            SET1_SUMMARY_VALUE = summary.key_driver_analysis_result.summary_card.group_comparison_card.group_a_card.summary_value
            SET1_TOTAL_SIZE = summary.key_driver_analysis_result.summary_card.group_comparison_card.group_a_card.total_size
            SET1_TOTAL_NUMERATOR = summary.key_driver_analysis_result.summary_card.group_comparison_card.group_a_card.total_numerator
            SET1_TOTAL_DENOMINATOR = summary.key_driver_analysis_result.summary_card.group_comparison_card.group_a_card.total_denominator
            SET1_MATCH_SIZE = summary.key_driver_analysis_result.summary_card.group_comparison_card.group_a_card.match_size
            SET1_WEIGHT = summary.key_driver_analysis_result.summary_card.group_comparison_card.group_a_card.weight
            SET2_CARD_LABEL = summary.key_driver_analysis_result.summary_card.group_comparison_card.group_b_card.card_label
            SET2_CATEGORY_FILTER = summary.key_driver_analysis_result.summary_card.group_comparison_card.group_b_card.category_filter
            SET2_AVERAGE = summary.key_driver_analysis_result.summary_card.group_comparison_card.group_b_card.average
            SET2_MIN = summary.key_driver_analysis_result.summary_card.group_comparison_card.group_b_card.min
            SET2_MAX = summary.key_driver_analysis_result.summary_card.group_comparison_card.group_b_card.max
            SET2_MEDIAN = summary.key_driver_analysis_result.summary_card.group_comparison_card.group_b_card.median
            SET2_SUM = summary.key_driver_analysis_result.summary_card.group_comparison_card.group_b_card.sum
            SET2_SUMMARY_VALUE = summary.key_driver_analysis_result.summary_card.group_comparison_card.group_b_card.summary_value
            SET2_TOTAL_SIZE = summary.key_driver_analysis_result.summary_card.group_comparison_card.group_b_card.total_size
            SET2_TOTAL_NUMERATOR = summary.key_driver_analysis_result.summary_card.group_comparison_card.group_b_card.total_numerator
            SET2_TOTAL_DENOMINATOR = summary.key_driver_analysis_result.summary_card.group_comparison_card.group_b_card.total_denominator
            SET2_MATCH_SIZE = summary.key_driver_analysis_result.summary_card.group_comparison_card.group_b_card.match_size
            SET2_WEIGHT = summary.key_driver_analysis_result.summary_card.group_comparison_card.group_b_card.weight

            resultsToDelete = conn.getGCAnalysisResultIDs(ANALYSIS_ID, GROUP_A_NAME, GROUP_B_NAME)

        # Otherwise, it's a general performance
        else:
            PREVIOUS_PERIOD_START = None
            PREVIOUS_PERIOD_END = None
            RECENT_PERIOD_START = None
            RECENT_PERIOD_END = None
            GROUP_A_NAME = None
            GROUP_B_NAME = None
            PERCENT_CHANGE = None
            SET1_CARD_LABEL = summary.key_driver_analysis_result.summary_card.general_performance_card.card_label
            SET1_CATEGORY_FILTER = summary.key_driver_analysis_result.summary_card.general_performance_card.category_filter
            SET1_AVERAGE = summary.key_driver_analysis_result.summary_card.general_performance_card.average
            SET1_MIN = summary.key_driver_analysis_result.summary_card.general_performance_card.min
            SET1_MAX = summary.key_driver_analysis_result.summary_card.general_performance_card.max
            SET1_MEDIAN = summary.key_driver_analysis_result.summary_card.general_performance_card.median
            SET1_SUM = summary.key_driver_analysis_result.summary_card.general_performance_card.sum
            SET1_SUMMARY_VALUE = summary.key_driver_analysis_result.summary_card.general_performance_card.summary_value
            SET1_TOTAL_SIZE = summary.key_driver_analysis_result.summary_card.general_performance_card.total_size
            SET1_TOTAL_NUMERATOR = summary.key_driver_analysis_result.summary_card.general_performance_card.total_numerator
            SET1_TOTAL_DENOMINATOR = summary.key_driver_analysis_result.summary_card.general_performance_card.total_denominator
            SET1_MATCH_SIZE = summary.key_driver_analysis_result.summary_card.general_performance_card.match_size
            SET1_WEIGHT = summary.key_driver_analysis_result.summary_card.general_performance_card.weight
            SET2_CARD_LABEL = None
            SET2_CATEGORY_FILTER = None
            SET2_AVERAGE = None
            SET2_MIN = None
            SET2_MAX = None
            SET2_MEDIAN = None
            SET2_SUM = None
            SET2_SUMMARY_VALUE = None
            SET2_TOTAL_SIZE = None
            SET2_TOTAL_NUMERATOR = None
            SET2_TOTAL_DENOMINATOR = None
            SET2_MATCH_SIZE = None
            SET2_WEIGHT = None

            resultsToDelete = conn.getGPAnalysisResultIDs(ANALYSIS_ID)

        if config.DEBUG:
            print(resultsToDelete)

        # Calculate any derived columns
        DIRECTION = ''
        TIMEFRAME = '' # PLACEHOLDER FOR TIMEFRAME, WHICH IS NOT YET AVAILABLE
        
        if PERCENT_CHANGE == None:
            DIRECTION = ''
        elif PERCENT_CHANGE > 0.005:
            DIRECTION = 'Increase'
        elif PERCENT_CHANGE < -0.005:
            DIRECTION = 'Decrease'
        else:
            DIRECTION = 'Flat'

        # Delete any existing summary / details for these KDA runs
        for r in resultsToDelete:
            conn.deleteAnalysisResultSummary(ANALYSIS_ID, r)
            conn.deleteAnalysisResultDetail(ANALYSIS_ID, r)
            conn.deleteAnalysisResultWaterfall(ANALYSIS_ID, r)

        # Insert the summary information into the database
        conn.writeAnalysisResultSummary((ANALYSIS_ID,
                                                    ANALYSIS_RESULT_ID,
                                                    REQUESTED_AT,
                                                    COMPLETED_AT,
                                                    RUN_STATUS,
                                                    RUN_TYPE,
                                                    TIMEFRAME,
                                                    PREVIOUS_PERIOD_START,
                                                    PREVIOUS_PERIOD_END,
                                                    RECENT_PERIOD_START,
                                                    RECENT_PERIOD_END,
                                                    GROUP_A_NAME,
                                                    GROUP_B_NAME,
                                                    METRIC_TYPE_LABEL,
                                                    PERCENT_CHANGE,
                                                    DIRECTION,
                                                    SET1_CARD_LABEL,
                                                    SET1_CATEGORY_FILTER,
                                                    SET1_AVERAGE,
                                                    SET1_MIN,
                                                    SET1_MAX,
                                                    SET1_MEDIAN,
                                                    SET1_SUM,
                                                    SET1_SUMMARY_VALUE,
                                                    SET1_TOTAL_SIZE,
                                                    SET1_TOTAL_NUMERATOR,
                                                    SET1_TOTAL_DENOMINATOR,
                                                    SET1_MATCH_SIZE,
                                                    SET1_WEIGHT,
                                                    SET2_CARD_LABEL,
                                                    SET2_CATEGORY_FILTER,
                                                    SET2_AVERAGE,
                                                    SET2_MIN,
                                                    SET2_MAX,
                                                    SET2_MEDIAN,
                                                    SET2_SUM,
                                                    SET2_SUMMARY_VALUE,
                                                    SET2_TOTAL_SIZE,
                                                    SET2_TOTAL_NUMERATOR,
                                                    SET2_TOTAL_DENOMINATOR,
                                                    SET2_MATCH_SIZE,
                                                    SET2_WEIGHT,
                                                    datetime.datetime.now()))

        # Requesting a waterfall for a trend or a general performance results in an error, so only get it for TC or GC KDA's
        if summary.key_driver_analysis_result.time_comparison or summary.key_driver_analysis_result.group_comparison:
            # Get the waterfall results
            waterfall = sisu.get_analysis_waterfall(ANALYSIS_ID)

            # Set the column set, and create a container for the rows
            cols = ['ANALYSIS_ID', 'ANALYSIS_RESULT_ID', 'STEP_ID', 'STEP_TYPE', 'FACTOR_0_DIMENSION', 'FACTOR_0_VALUE', 'FACTOR_1_DIMENSION', 'FACTOR_1_VALUE', 'FACTOR_2_DIMENSION', 'FACTOR_2_VALUE', 'STEP_IMPACT', 'CUMULATIVE_IMPACT_BEFORE_STEP', 'CUMULATIVE_IMPACT_AFTER_STEP', 'OVERLAPPING_IMPACT', 'CHANGE_IN_SIZE_SET1', 'CHANGE_IN_SIZE_SET2', 'CHANGE_IN_TYPE_SET1', 'CHANGE_IN_TYPE_SET2']
            rows = []

            # We'll process each step in the waterfall one at a time
            _i = 0

            # For each step in the waterfall, work in sequence
            while _i < len(waterfall.waterfall):
                # Start building the row with linkage and ordering data
                row = []
                row.append(ANALYSIS_ID)
                row.append(ANALYSIS_RESULT_ID)
                row.append(_i)

                # Get the step record
                step = waterfall.waterfall[_i]

                if _i == 0:
                    # This is the first step. It's an absolute value step
                    row.append('absolute')
                elif _i == len(waterfall.waterfall) - 1:
                    # This is the last step. It's a total value step
                    row.append('total')
                else:
                    # This is a middle step. It's a relative step
                    row.append('relative')

                # We're starting with a -1 here because we will increment the counter for each step we encounter
                _j = -1

                # There can be up to three factors, so we need to loop over them
                for k in step.factors.keys():
                    _j += 1

                    row.append(k)
                    if step.factors.get(k).keyword.keyword:
                        row.append(str(step.factors.get(k).keyword.keyword))
                    elif step.factors.get(k).bin:
                        b = step.factors.get(k).bin
                        row.append(str(b.lower_bound) + '-' + str(b.upper_bound))
                    else:
                        for v in step.factors.get(k).value.to_dict().values():
                            row.append(str(v))

                if _j == -1:
                    # If we are processing the first or last two steps, we won't get any factors
                    row.append('')
                    row.append('')
                    row.append('')
                    row.append('')
                    row.append('')
                    row.append('')
                elif _j == 0:
                    # If we only had one factor, factor 1 and 2 should be null
                    row.append('')
                    row.append('')
                    row.append('')
                    row.append('')
                elif _j == 1:
                    # If we only had two factors, factor 2 should be null
                    row.append('')
                    row.append('')
                
                # Add the rest of the data for the step
                row.append(step.cumulative_impact_after_step - step.cumulative_impact_before_step)
                row.append(step.cumulative_impact_before_step)
                row.append(step.cumulative_impact_after_step)
                row.append(step.overlapping_impact)

                row.append(step.change_in_size.subgroup_a)
                row.append(step.change_in_size.subgroup_b)
                row.append(step.change_in_type.subgroup_a)
                row.append(step.change_in_type.subgroup_b)
                
                # Put the row into the rowset
                rows.append(row)
                _i+=1

            # After processing the waterfall, create a dataframe so that we can easily insert into Snowflake
            wf = pandas.DataFrame(data=rows, columns=cols)

            wf['LOAD_TS'] = str(datetime.datetime.now().isoformat(timespec='milliseconds'))

            if config.DEBUG:
                print(wf)
            
            conn.writeAnalysisResultWaterfall(wf)

        # Convert the segment table into a dataframe
        df = pandas.read_csv(io.StringIO(detail.to_csv(config.DELIMITER).replace('\'', '')), delimiter=config.DELIMITER)
        df.insert(0, 'ANALYSIS_RESULT_ID', ANALYSIS_RESULT_ID)
        df.insert(0, 'ANALYSIS_ID', ANALYSIS_ID)

        pandas.set_option('display.max_columns', None) 
        pandas.set_option('display.max_rows', 100)
        pandas.set_option('display.width', 1000)

        # Reset some of the column names, and prune off unneeded columns
        # If it's a time comparison
        if summary.key_driver_analysis_result.time_comparison:
            df.drop('previous_period_start_date_inclusive', axis=1, inplace=True)
            df.drop('previous_period_end_date_inclusive', axis=1, inplace=True)
            df.drop('recent_period_start_date_inclusive', axis=1, inplace=True)
            df.drop('recent_period_end_date_inclusive', axis=1, inplace=True)
            df.rename(columns={'previous_period_size': 'set2_size', 'recent_period_size': 'set1_size', 'previous_period_value': 'set2_value', 'recent_period_value': 'set1_value'}, inplace=True)
        # It's a group comparison
        elif summary.key_driver_analysis_result.group_comparison:
            df.drop('group_a_name', axis=1, inplace=True)
            df.drop('group_b_name', axis=1, inplace=True)
            df.rename(columns={'group_a_size': 'set1_size', 'group_b_size': 'set2_size', 'group_a_value': 'set1_value', 'group_b_value': 'set2_value'}, inplace=True)
        # Otherwise it's a general performance
        else:
            df.rename(columns={'size': 'set1_size', 'value': 'set1_value', 'weighted_sum': 'WEIGHTED_CHANGE_IN_SUM', 'unweighted_average': 'UNWEIGHTED_CHANGE_IN_AVERAGE'}, inplace=True)
            df.insert(12, 'set2_size', numpy.nan)
            df.insert(14, 'set2_value', numpy.nan)
            df.insert(14, 'change', numpy.nan)
            df.insert(14, 'PERCENT_CHANGE_IN_SIZE', numpy.nan)
            df.insert(14, 'change_in_impact', numpy.nan)
            df.insert(14, 'mix_effect', numpy.nan)
            df.insert(14, 'net_effect', numpy.nan)
            df.insert(14, 'net_relative_effect', numpy.nan)
            df.insert(14, 'rate_effect', numpy.nan)
            df.insert(14, 'relative_change', numpy.nan)
            df.insert(14, 'relative_mix_effect', numpy.nan)
            df.insert(14, 'relative_percent_change', numpy.nan)

        df.drop('change_in_impact', axis=1, inplace=True)
        df.rename(columns={'change_in_size': 'PERCENT_CHANGE_IN_SIZE', 'change_in_average': 'UNWEIGHTED_CHANGE_IN_AVERAGE', 'change_in_sum': 'WEIGHTED_CHANGE_IN_SUM'}, inplace=True)

        df.insert(15, 'LOAD_TS', str(datetime.datetime.now().isoformat(timespec='milliseconds')))
        # Make the column names upper case to match the database
        df.columns = map(str.upper, df.columns)

        if config.DEBUG:
            print(df.dtypes)
            print(df)

        # Add the derived columns to the dataframe
        df.insert(10, 'FACTOR_0_DIMENSION_FRIENDLY', df['FACTOR_0_DIMENSION'].str.title().str.replace("_", " "))
        df.insert(11, 'FACTOR_1_DIMENSION_FRIENDLY', df['FACTOR_1_DIMENSION'].str.title().str.replace("_", " "))
        df.insert(12, 'FACTOR_2_DIMENSION_FRIENDLY', df['FACTOR_2_DIMENSION'].str.title().str.replace("_", " "))
        df.insert(13, 'FACTOR_0_VALUE_FRIENDLY', df['FACTOR_0_VALUE'].str.title().str.replace("_", " "))
        df.insert(14, 'FACTOR_1_VALUE_FRIENDLY', df['FACTOR_1_VALUE'].str.title().str.replace("_", " "))
        df.insert(15, 'FACTOR_2_VALUE_FRIENDLY', df['FACTOR_2_VALUE'].str.title().str.replace("_", " "))

        df.insert(16, 'FACTOR_0_TEXT', '')

        def F_FACTOR_0_TEXT(x):
            if pandas.isna(x['FACTOR_0_DIMENSION_FRIENDLY']): return pandas.NA
            elif isinstance(x['FACTOR_0_VALUE'], float): return x['FACTOR_0_DIMENSION_FRIENDLY'] + ' is ' + str(round(x['FACTOR_0_VALUE'],2))
            else: return x['FACTOR_0_DIMENSION_FRIENDLY'] + ' is ' + str(x['FACTOR_0_VALUE'])

        df['FACTOR_0_TEXT'] = df.apply(F_FACTOR_0_TEXT, axis=1)
        
        df.insert(17, 'FACTOR_1_TEXT', '')

        def F_FACTOR_1_TEXT(x):
            if pandas.isna(x['FACTOR_1_DIMENSION_FRIENDLY']): return pandas.NA
            elif isinstance(x['FACTOR_1_VALUE'], float): return x['FACTOR_1_DIMENSION_FRIENDLY'] + ' is ' + str(round(x['FACTOR_1_VALUE'],2))
            else: return x['FACTOR_1_DIMENSION_FRIENDLY'] + ' is ' + str(x['FACTOR_1_VALUE'])

        df['FACTOR_1_TEXT'] = df.apply(F_FACTOR_1_TEXT, axis=1)

        df.insert(17, 'FACTOR_2_TEXT', '')

        def F_FACTOR_2_TEXT(x):
            if pandas.isna(x['FACTOR_2_DIMENSION_FRIENDLY']): return pandas.NA
            elif isinstance(x['FACTOR_2_VALUE'], float): return x['FACTOR_2_DIMENSION_FRIENDLY'] + ' is ' + str(round(x['FACTOR_2_VALUE'],2))
            else: return x['FACTOR_2_DIMENSION_FRIENDLY'] + ' is ' + str(x['FACTOR_2_VALUE'])

        df['FACTOR_2_TEXT'] = df.apply(F_FACTOR_2_TEXT, axis=1)
        
        df.insert(19, 'SEGMENT_TEXT', '')

        def F_SEGMENT_TEXT(x):
            if pandas.isna(x['FACTOR_1_DIMENSION_FRIENDLY']) and pandas.isna(x['FACTOR_2_DIMENSION_FRIENDLY']): return x['FACTOR_0_TEXT']
            elif pandas.isna(x['FACTOR_2_DIMENSION_FRIENDLY']): return x['FACTOR_0_TEXT'] + ', ' + x['FACTOR_1_TEXT']
            else: return x['FACTOR_0_TEXT'] + ', ' + x['FACTOR_1_TEXT'] + ', ' + x['FACTOR_2_TEXT']
        
        df['SEGMENT_TEXT'] = df.apply(F_SEGMENT_TEXT, axis=1)

        df.insert(21, 'IMPACT_MAGNITUDE', df['IMPACT'].abs())
        df.insert(22, 'IMPACT_RANK', pandas.NA)

        df.insert(27, 'PERCENT_CHANGE', '')
        
        def F_PERCENT_CHANGE(x):
            if pandas.isna(x['SET2_VALUE']) or x['SET2_VALUE'] == 0: return 100.0
            else: return (x['SET1_VALUE'] - x['SET2_VALUE'])/x['SET2_VALUE']

        df['PERCENT_CHANGE'] = df.apply(F_PERCENT_CHANGE, axis=1)

        df.insert(28, 'DIRECTION', '')

        def F_DIRECTION(x):
            if pandas.isna(x['PERCENT_CHANGE']): return pandas.NA
            elif x['PERCENT_CHANGE'] > 0.005: return 'Increase'
            elif x['PERCENT_CHANGE'] < -0.005: return 'Decrease'
            else: return 'Flat'

        df['DIRECTION'] = df.apply(F_DIRECTION, axis=1)

        df.insert(29, 'DIRECTION_TEXT', '')

        def F_DIRECTION_TEXT(x):
            if pandas.isna(x['PERCENT_CHANGE']): return pandas.NA
            elif x['PERCENT_CHANGE'] > 0: return 'increases by'
            elif x['PERCENT_CHANGE'] < -0: return 'decreases by'
            else: return 'remains the same'
        
        df['DIRECTION_TEXT'] = df.apply(F_DIRECTION_TEXT, axis=1)

        df.insert(30, 'ORIENTATION_MATCHES_METRIC', '')
        
        def F_ORIENTATION_MATCHES_METRIC(x):
            if str(x['DIRECTION']) == DIRECTION: return 'True'
            else: return 'False'
        
        df['ORIENTATION_MATCHES_METRIC'] = df.apply(F_ORIENTATION_MATCHES_METRIC, axis=1)
        
        df.insert(31, 'SEGMENT_ORDER', '')

        def F_SEGMENT_ORDER(x):
            if pandas.isna(x['FACTOR_1_DIMENSION']) and pandas.isna(x['FACTOR_2_DIMENSION']): return 1
            elif pandas.isna(x['FACTOR_2_DIMENSION']): return 2
            else: return 3
        
        df['SEGMENT_ORDER'] = df.apply(F_SEGMENT_ORDER, axis=1)

        df.insert(32, 'SEGMENT_ORDER_TEXT', '')

        def F_SEGMENT_ORDER_TEXT(x):
            if pandas.isna(x['FACTOR_1_DIMENSION']) and pandas.isna(x['FACTOR_2_DIMENSION']): return 'First Order'
            elif pandas.isna(x['FACTOR_2_DIMENSION']): return 'Second Order'
            else: return 'Third Order'
        
        df['SEGMENT_ORDER_TEXT'] = df.apply(F_SEGMENT_ORDER_TEXT, axis=1)

        # This should be index 34, but we need it to calculate the INSIGHT_TEXT, so we'll set it in index 33 for now, and then insert INSIGHT_TEXT
        #     into index 33 again later
        #
        # Also, the "change_in_size" field that's returned from get_results() is actually the "percent_change_in_size" field, so we have to 
        #     calculate the "change_in_size" field ourselves
        df.insert(33, 'CHANGE_IN_SIZE', df['SET1_SIZE'] - df['SET2_SIZE'])

        # This is the REAL index 33 column
        df.insert(33, 'INSIGHT_TEXT', '')

        def F_INSIGHT_TEXT(x):
            return METRIC_NAME + ' ' + x['DIRECTION_TEXT'] + ' ' + str(x['IMPACT']) + ' when ' + x['SEGMENT_TEXT']
        
        df['INSIGHT_TEXT'] = df.apply(F_INSIGHT_TEXT, axis=1)

        df.insert(43, 'SEGMENT_NAME', pandas.NA)
        df.insert(44, 'SEGMENT_RANK', pandas.NA)

        df.insert(45, 'SEGMENT_HASH', df['FACTOR_0_DIMENSION'].astype(str) + df['FACTOR_0_VALUE'].astype(str) + df['FACTOR_1_DIMENSION'].astype(str) + df['FACTOR_1_VALUE'].astype(str) + df['FACTOR_2_DIMENSION'].astype(str) + df['FACTOR_2_VALUE'].astype(str))

        new_cols = ['ANALYSIS_ID', 'ANALYSIS_RESULT_ID', 'SUBGROUP_ID', 'CONFIDENCE', 'FACTOR_0_DIMENSION TEXT', 'FACTOR_0_VALUE TEXT', 'FACTOR_1_DIMENSION TEXT', 'FACTOR_1_VALUE TEXT', 'FACTOR_2_DIMENSION TEXT', 'FACTOR_2_VALUE TEXT', 'FACTOR_0_DIMENSION_FRIENDLY TEXT', 'FACTOR_1_DIMENSION_FRIENDLY', 'FACTOR_2_DIMENSION_FRIENDLY', 'FACTOR_0_VALUE_FRIENDLY', 'FACTOR_1_VALUE_FRIENDLY', 'FACTOR_2_VALUE_FRIENDLY', 'FACTOR_0_TEXT', 'FACTOR_1_TEXT', 'FACTOR_2_TEXT', 'SEGMENT_TEXT', 'CHANGE', 'IMPACT', 'IMPACT_MAGNITUDE', 'IMPACT_RANK', 'SET1_SIZE', 'SET2_SIZE', 'SET1_VALUE', 'SET2_VALUE', 'PERCENT_CHANGE', 'DIRECTION', 'DIRECTION_TEXT', 'ORIENTATION_MATCHES_METRIC', 'SEGMENT_ORDER', 'SEGMENT_ORDER_TEXT', 'INSIGHT_TEXT', 'CHANGE_IN_SIZE', 'MIX_EFFECT', 'NET_EFFECT', 'NET_RELATIVE_EFFECT', 'PERCENT_CHANGE_IN_SIZE', 'RATE_EFFECT', 'RELATIVE_PERCENT_CHANGE', 'RATE_CHANGE', 'RELATIVE_MIX_EFFECT', 'SEGMENT_NAME', 'SEGMENT_RANK', 'SEGMENT_HASH', 'UNWEIGHTED_CHANGE_IN_AVERAGE', 'WEIGHT', 'WEIGHTED_CHANGE_IN_SUM','LOAD_TS']
        df.reindex(columns=new_cols)

        if config.DEBUG:
            print(df.dtypes)
            print(df)

        # Write the analysis result details to the database
        conn.writeAnalysisResultDetail(df)

    # All done!
    print('Completing execute_load at ' + str(datetime.datetime.now()))

    if RETURN_RESULTS:
        return conn
    else:
        return None

