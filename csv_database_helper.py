import os
import csv
import config
import pandas
import datetime

class SisuOutputDatabaseConnection:
    filepath = ''
    overwrite = 'a'
    delimiter = '^'

    ANALYSIS_HEADER = 'ANALYSIS_ID,ANALYSIS_NAME,ANALYSIS_TYPE,APPLICATION_URL,CREATED_AT,METRIC_ID,METRIC_NAME,METRIC_DESIRED_DIRECTION,METRIC_UNIT,METRIC_UNIT_IS_PERCENTAGE,METRIC_UNIT_IS_SUFFIX,METRIC_UNIT_SCALE,METRIC_UNIT_KMB,PROJECT_ID,PROJECT_NAME,LOAD_TS'
    ANALYSIS_RESULT_WATERFALL_HEADER = 'ANALYSIS_ID,ANALYSIS_RESULT_ID,STEP_ID,STEP_TYPE,FACTOR_0_DIMENSION,FACTOR_0_VALUE,FACTOR_1_DIMENSION,FACTOR_1_VALUE,FACTOR_2_DIMENSION,FACTOR_2_VALUE,STEP_IMPACT,CUMULATIVE_IMPACT_BEFORE_STEP,CUMULATIVE_IMPACT_AFTER_STEP,OVERLAPPING_IMPACT,CHANGE_IN_SIZE_SET1,CHANGE_IN_SIZE_SET2,CHANGE_IN_TYPE_SET1,CHANGE_IN_TYPE_SET2,SEGMENT_TEXT,LOAD_TS'
    ANALYSIS_RESULT_DETAIL_HEADER = 'ANALYSIS_ID,ANALYSIS_RESULT_ID,SUBGROUP_ID,CONFIDENCE,FACTOR_0_DIMENSION,FACTOR_0_VALUE,FACTOR_1_DIMENSION,FACTOR_1_VALUE,FACTOR_2_DIMENSION,FACTOR_2_VALUE,FACTOR_0_DIMENSION_FRIENDLY,FACTOR_1_DIMENSION_FRIENDLY,FACTOR_2_DIMENSION_FRIENDLY,FACTOR_0_VALUE_FRIENDLY,FACTOR_1_VALUE_FRIENDLY,FACTOR_2_VALUE_FRIENDLY,FACTOR_0_TEXT,FACTOR_1_TEXT,FACTOR_2_TEXT,SEGMENT_TEXT,CHANGE,IMPACT,IMPACT_MAGNITUDE,IMPACT_RANK,SET1_SIZE,SET2_SIZE,SET1_VALUE,SET2_VALUE,PERCENT_CHANGE,DIRECTION,DIRECTION_TEXT,ORIENTATION_MATCHES_METRIC,SEGMENT_ORDER,SEGMENT_ORDER_TEXT,INSIGHT_TEXT,CHANGE_IN_SIZE,MIX_EFFECT,NET_EFFECT,NET_RELATIVE_EFFECT,PERCENT_CHANGE_IN_SIZE,RATE_EFFECT,RELATIVE_PERCENT_CHANGE,RELATIVE_CHANGE,RELATIVE_MIX_EFFECT,SEGMENT_NAME,SEGMENT_RANK,SEGMENT_HASH,UNWEIGHTED_CHANGE_IN_AVERAGE,WEIGHT,WEIGHTED_CHANGE_IN_SUM,LOAD_TS'
    ANALYSIS_RESULT_SUMMARY_HEADER = 'ANALYSIS_ID,ANALYSIS_RESULT_ID,REQUESTED_AT,COMPLETED_AT,RUN_STATUS,RUN_TYPE,TIMEFRAME,PREVIOUS_PERIOD_START,PREVIOUS_PERIOD_END,RECENT_PERIOD_START,RECENT_PERIOD_END,GROUP_A_NAME,GROUP_B_NAME,METRIC_TYPE_LABEL,PERCENT_CHANGE,DIRECTION,SET1_CARD_LABEL,SET1_CATEGORY_FILTER,SET1_AVERAGE,SET1_MIN,SET1_MAX,SET1_MEDIAN,SET1_SUM,SET1_SUMMARY_VALUE,SET1_TOTAL_SIZE,SET1_TOTAL_NUMERATOR,SET1_TOTAL_DENOMINATOR,SET1_MATCH_SIZE,SET1_WEIGHT,SET2_CARD_LABEL,SET2_CATEGORY_FILTER,SET2_AVERAGE,SET2_MIN,SET2_MAX,SET2_MEDIAN,SET2_SUM,SET2_SUMMARY_VALUE,SET2_TOTAL_SIZE,SET2_TOTAL_NUMERATOR,SET2_TOTAL_DENOMINATOR,SET2_MATCH_SIZE,SET2_WEIGHT,LOAD_TS'

    TREND_RESULT_DETAIL_HEADER = 'ANALYSIS_ID,ANALYSIS_RESULT_ID,SUBGROUP_ID,FACTOR_0_DIMENSION,FACTOR_0_VALUE,FACTOR_1_DIMENSION,FACTOR_1_VALUE,FACTOR_2_DIMENSION,FACTOR_2_VALUE,IMPACT,START_DATE,END_DATE,INTERCEPT,SLOPE,SIZE,LOAD_TS'
    TREND_RESULT_SUMMARY_HEADER = 'ANALYSIS_ID,ANALYSIS_RESULT_ID,REQUESTED_AT,COMPLETED_AT,RUN_STATUS,RUN_TYPE,CURRENT_PERIOD_CARD_LABEL,CURRENT_PERIOD_DENOMINATOR_LABEL,CURRENT_PERIOD_PERCENT_CHANGE,CURRENT_PERIOD_SLOPE,PREVIOUS_PERIOD_CARD_LABEL,PREVIOUS_PERIOD_DENOMINATOR_LABEL,PREVIOUS_PERIOD_PERCENT_CHANGE,PREVIOUS_PERIOD_SLOPE,LOAD_TS'

    # init method should establish a connection to the database, and set any connection parameters needed to support executing queries
    def __init__(self):
        self.filepath = config.FILEPATH
        if config.OVERWRITE:
            self.overwrite = 'w'
        if config.CSV_DELIMITER:
            self.delimiter = config.CSV_DELIMITER

        if os.path.isdir(self.filepath) == False:
            raise Exception("Filepath " + self.filepath + " does not exist!")

        print('Successfully configured CSV file handler!')
    
    # Method should truncate the three tables
    def truncateTables(self):
        print('Truncate not supported for CSV data sources!')
    
    # Method should delete the analysis metadata from the database
    #
    # @input analysisId: analysisId to be deleted from the table
    def deleteAnalysisMetadata(self, analysisId: int):
        print('Deletes not supported for CSV data sources!')

    # Method should write the analysis metadata to the database
    #
    # @input vals: a list of fields outlined in DDL for the ANALYSIS table
    def writeAnalysisMetadata(self, vals):
        exists = os.path.isfile(self.filepath + '/ANALYSIS.CSV')
        f = open(self.filepath + '/ANALYSIS.CSV', self.overwrite)
        w = csv.writer(f, delimiter=self.delimiter)

        if (config.OVERWRITE or not exists) and config.OUTPUT_HEADERS:
            f.write(self.ANALYSIS_HEADER + '\n')

        w.writerow(vals)

        print('Analysis metadata written to the CSV file')
    
    # Method should clear the previous results for this analysisId / analysisResultId from the summary table
    #
    # @input analysisId: the analysisId that will have its' results deleted
    # @input analysisResultId: the analysisResultId that will be deleted
    def deleteAnalysisResultSummary(self, analysisId: int, analysisResultId: int):
        print('Deletes not supported for CSV data sources!')

    # Method should write the analysis summary to the database
    #
    # @input vals: a list of fields outlined in DDL for the ANALYSIS_RESULT_SUMMARY table
    def writeAnalysisResultSummary(self, vals):
        exists = os.path.isfile(self.filepath + '/ANALYSIS_RESULT_SUMMARY.CSV')
        f = open(self.filepath + '/ANALYSIS_RESULT_SUMMARY.CSV', self.overwrite)

        if (config.OVERWRITE or not exists) and config.OUTPUT_HEADERS:
            f.write(self.ANALYSIS_RESULT_SUMMARY_HEADER + '\n')

        w = csv.writer(f, delimiter=self.delimiter)
        w.writerow(vals)

        print('Analysis summary written to the CSV file')

    # Method should clear the previous results for this analysisId / analysisResultId from the detail table
    #
    # @input analysisId: the analysisId that will have its' results deleted
    # @input analysisResultId: the analysisResultId that will be deleted
    def deleteAnalysisResultDetail(self, analysisId: int, analysisResultId: int):
        print('Deletes not supported for CSV data sources!')

    # Method should write the analysis waterfall to the database
    #
    # @input df: a pandas dataframe with the fields outlined in DDL for the ANALYSIS_RESULT_WATERFALL table
    def writeAnalysisResultWaterfall(self, df):
        exists = os.path.isfile(self.filepath + '/ANALYSIS_RESULT_WATERFALL.CSV')
        f = open(self.filepath + '/ANALYSIS_RESULT_WATERFALL.CSV', self.overwrite)

        if (config.OVERWRITE or not exists) and config.OUTPUT_HEADERS:
            f.write(self.ANALYSIS_RESULT_WATERFALL_HEADER + '\n')

        df.to_csv(f, sep=self.delimiter, doublequote=True, na_rep='', header=False, index=False)

        print('Analysis waterfall written to the CSV file')

    # Method should clear the previous results for this analysisId / analysisResultId from the waterfall table
    #
    # @input analysisId: the analysisId that will have its' waterfall deleted
    # @input analysisResultId: the analysisResultId that will be deleted
    def deleteAnalysisResultWaterfall(self, analysisId: int, analysisResultId: int):
        print('Deletes not supported for CSV data sources!')

    # Method should write the analysis details to the database
    #
    # @input df: a pandas dataframe with the fields outlined in DDL for the ANALYSIS_RESULT_DETAIL table
    def writeAnalysisResultDetail(self, df):
        exists = os.path.isfile(self.filepath + '/ANALYSIS_RESULT_DETAIL.CSV')
        f = open(self.filepath + '/ANALYSIS_RESULT_DETAIL.CSV', self.overwrite)

        if (config.OVERWRITE or not exists) and config.OUTPUT_HEADERS:
            f.write(self.ANALYSIS_RESULT_DETAIL_HEADER + '\n')

        df.to_csv(f, sep=self.delimiter, doublequote=True, na_rep='', header=False, index=False)

        print('Analysis detail written to the CSV file')
    
    # Method should clear the previous results for this trend / run, and write the trend summary to the database
    #
    # @input vals: a list of fields outlined in DDL for the TREND_RESULT_SUMMARY table
    def writeTrendResultSummary(self, vals):
        exists = os.path.isfile(self.filepath + '/TREND_RESULT_SUMMARY.CSV')
        f = open(self.filepath + '/TREND_RESULT_SUMMARY.CSV', self.overwrite)

        if (config.OVERWRITE or not exists) and config.OUTPUT_HEADERS:
            f.write(self.TREND_RESULT_SUMMARY_HEADER + '\n')

        w = csv.writer(f, delimiter=self.delimiter)
        w.writerow(vals)

        print('Trend summary written to the CSV file')

    # Method should clear the previous results for this trend / run, and write the trend details to the database
    #
    # @input df: a pandas dataframe with the fields outlined in DDL for the TREND_RESULT_DETAIL table
    # @input vals: a list of (ANALYSIS_ID, ANALYSIS_RESULT_ID)
    def writeTrendResultDetail(self, df, vals):
        exists = os.path.isfile(self.filepath + '/TREND_RESULT_DETAIL.CSV')
        f = open(self.filepath + '/TREND_RESULT_DETAIL.CSV', self.overwrite)

        if (config.OVERWRITE or not exists) and config.OUTPUT_HEADERS:
            f.write(self.TREND_RESULT_DETAIL_HEADER + '\n')

        df.to_csv(f, sep=self.delimiter, doublequote=True, na_rep='', header=False, index=False)

        print('Trend detail written to the CSV file')

    # Method should return the ANALYSIS_RESULT_ID's as a list where the time comparison period start / end dates match a corresponding analysis_id
    # 
    # @input ANALYSIS_ID: the ANALYSIS_ID to search for
    # @input RECENT_PERIOD_START: the start date of the recent period
    # @input RECENT_PERIOD_END: the end date of the recent period
    # @input PREVIOUS_PERIOD_START: the start date of the previous period
    # @input PREVIOUS_PERIOD_END: the end date of the previous period
    def getTCAnalysisResultIDs(self, ANALYSIS_ID: int, RECENT_PERIOD_START: str, RECENT_PERIOD_END: str, PREVIOUS_PERIOD_START: str, PREVIOUS_PERIOD_END: str):
        print('Deletes not supported for CSV data sources!')

        return []

    # Method should return the ANALYSIS_RESULT_ID's as a list where the time comparison period start / end dates match a corresponding analysis_id
    # 
    # @input ANALYSIS_ID: the ANALYSIS_ID to search for
    # @input GROUP_A_NAME: the name of Group A
    # @input GROUP_B_NAME: the name of Group B
    def getGCAnalysisResultIDs(self, ANALYSIS_ID: int, GROUP_A_NAME: str, GROUP_B_NAME: str):
        print('Deletes not supported for CSV data sources!')

        return []

    # Method should return the ANALYSIS_RESULT_ID's thatmatch a corresponding analysis_id
    # 
    # @input ANALYSIS_ID: the ANALYSIS_ID to search for
    def getGPAnalysisResultIDs(self, ANALYSIS_ID: int):
        print('Deletes not supported for CSV data sources!')

        return []

    # Method should format output into a JSON string that will be returned as output result of the fucntion call
    def formatResults(self, event):
        return 'NOT SUPPORTED: Not supported for CSV data sources!'
    
    