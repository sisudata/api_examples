import config
import datetime
import json

# SQL Statements not needed to operate the flow

class SisuOutputDatabaseConnection:
    insert_Analysis = []
    insert_AnalysisWaterfall = []
    insert_AnalysisResultSummary = []
    insert_TrendResultSummary = []
    insert_AnalysisResultDetail = []
    insert_TrendResultDetail = []

    # init method should establish a connection to the database, and set any connection parameters needed to support executing queries
    def __init__(self):
        print('Successfully configured Fivetran Results Containers!')
    
    # Method should truncate the three tables
    def truncateTables(self):
        print('NOT SUPPORTED: Fivetran does not support table truncation')
    
    # Method should delete the analysis metadata from the database
    #
    # @input analysisId: analysisId to be deleted from the table
    def deleteAnalysisMetadata(self, analysisId: int):
        print('NOT SUPPORTED: Deletes not supported by Fivetran')

    # Method should write the analysis metadata to the database
    #
    # @input vals: a list of fields outlined in DDL for the ANALYSIS table
    def writeAnalysisMetadata(self, vals):
        if len(self.insert_Analysis) != 0:
            for d in self.insert_Analysis:
                if d['ANALYSIS_ID'] == vals[0]:
                    self.insert_Analysis.remove(d)
                    break
    
        self.insert_Analysis.append({
            'ANALYSIS_ID': vals[0],
            'ANALYSIS_NAME': vals[1],
            'ANALYSIS_TYPE': vals[2],
            'APPLICATION_URL': vals[3],
            'CREATED_AT': vals[4],
            'METRIC_ID': vals[5],
            'METRIC_NAME': vals[6],
            'METRIC_DESIRED_DIRECTION': vals[7],
            'METRIC_UNIT': vals[8],
            'METRIC_UNIT_IS_PERCENTAGE': vals[9],
            'METRIC_UNIT_IS_SUFFIX': vals[10],
            'METRIC_UNIT_SCALE': vals[11],
            'METRIC_UNIT_KMB': vals[12],
            'PROJECT_ID': vals[13],
            'PROJECT_NAME': vals[14],
            'LOAD_TS': vals[15]
        })

        print('Analysis metadata added to insert list')
    
    # Method should clear the previous results for this analysisId / analysisResultId from the summary table
    #
    # @input analysisId: the analysisId that will have its' results deleted
    # @input analysisResultId: the analysisResultId that will be deleted
    def deleteAnalysisResultSummary(self, analysisId: int, analysisResultId: int):
        print('NOT SUPPORTED: Delete analysis summary is not supported for Fivetran')

    # Method should write the analysis summary to the database
    #
    # @input vals: a list of fields outlined in DDL for the ANALYSIS_RESULT_SUMMARY table
    def writeAnalysisResultSummary(self, vals):
        self.insert_AnalysisResultSummary.append({
            'ANALYSIS_ID': vals[0],
            'ANALYSIS_RESULT_ID': vals[1],
            'REQUESTED_AT': vals[2],
            'COMPLETED_AT': vals[3],
            'RUN_STATUS': vals[4],
            'RUN_TYPE': vals[5],
            'TIMEFRAME': vals[6],
            'PREVIOUS_PERIOD_START': vals[7],
            'PREVIOUS_PERIOD_END': vals[8],
            'RECENT_PERIOD_START': vals[9],
            'RECENT_PERIOD_END': vals[10],
            'GROUP_A_NAME': vals[11],
            'GROUP_B_NAME': vals[12],
            'METRIC_TYPE_LABEL': vals[13],
            'PERCENT_CHANGE': vals[14],
            'DIRECTION': vals[15],
            'SET1_CARD_LABEL': vals[16],
            'SET1_CATEGORY_FILTER': vals[17],
            'SET1_AVERAGE': vals[18],
            'SET1_MIN': vals[19],
            'SET1_MAX': vals[20],
            'SET1_MEDIAN': vals[21],
            'SET1_SUM': vals[22],
            'SET1_SUMMARY_VALUE': vals[23],
            'SET1_TOTAL_SIZE': vals[24],
            'SET1_TOTAL_NUMERATOR': vals[25],
            'SET1_TOTAL_DENOMINATOR': vals[26],
            'SET1_MATCH_SIZE': vals[27],
            'SET1_WEIGHT': vals[28],
            'SET2_CARD_LABEL': vals[29],
            'SET2_CATEGORY_FILTER': vals[30],
            'SET2_AVERAGE': vals[31],
            'SET2_MIN': vals[32],
            'SET2_MAX': vals[33],
            'SET2_MEDIAN': vals[34],
            'SET2_SUM': vals[35],
            'SET2_SUMMARY_VALUE': vals[36],
            'SET2_TOTAL_SIZE': vals[37],
            'SET2_TOTAL_NUMERATOR': vals[38],
            'SET2_TOTAL_DENOMINATOR': vals[39],
            'SET2_MATCH_SIZE': vals[40],
            'SET2_WEIGHT': vals[41],
            'LOAD_TS': vals[42]
        })

        print('Analysis summary added to insert list')

    # Method should clear the previous results for this analysisId / analysisResultId from the detail table
    #
    # @input analysisId: the analysisId that will have its' results deleted
    # @input analysisResultId: the analysisResultId that will be deleted
    def deleteAnalysisResultDetail(self, analysisId: int, analysisResultId: int):
        print('NOT SUPPORTED: Delete analysis detail is not supported for Fivetran')

    # Method should write the analysis waterfall to the database
    #
    # @input df: a pandas dataframe with the fields outlined in DDL for the ANALYSIS_RESULT_WATERFALL table
    def writeAnalysisResultWaterfall(self, df):
        self.insert_AnalysisWaterfall = df.to_dict('records')

        print('Analysis waterfall added to insert list')

    # Method should clear the previous results for this analysisId / analysisResultId from the waterfall table
    #
    # @input analysisId: the analysisId that will have its' waterfall deleted
    # @input analysisResultId: the analysisResultId that will be deleted
    def deleteAnalysisResultWaterfall(self, analysisId: int, analysisResultId: int):
        print('NOT SUPPORTED: Delete analysis waterfall is not supported for Fivetran')

    # Method should write the analysis details to the database
    #
    # @input df: a pandas dataframe with the fields outlined in DDL for the ANALYSIS_RESULT_DETAIL table
    def writeAnalysisResultDetail(self, df):
        self.insert_AnalysisResultDetail = df.to_dict('records')

        print('Analysis detail added to insert list')
    
    # Method should clear the previous results for this trend / run, and write the trend summary to the database
    #
    # @input vals: a list of fields outlined in DDL for the TREND_RESULT_SUMMARY table
    def writeTrendResultSummary(self, vals):
        self.insert_TrendResultSummary.append({
            'ANALYSIS_ID': vals[0],
            'ANALYSIS_RESULT_ID': vals[1],
            'REQUESTED_AT': vals[2],
            'COMPLETED_AT': vals[3],
            'RUN_STATUS': vals[4],
            'RUN_TYPE': vals[5],
            'CURRENT_PERIOD_CARD_LABEL': vals[6],
            'CURRENT_PERIOD_DENOMINATOR_LABEL': vals[7],
            'CURRENT_PERIOD_PERCENT_CHANGE': vals[8],
            'CURRENT_PERIOD_SLOPE': vals[9],
            'PREVIOUS_PERIOD_CARD_LABEL': vals[10],
            'PREVIOUS_PERIOD_DENOMINATOR_LABEL': vals[11],
            'PREVIOUS_PERIOD_PERCENT_CHANGE': vals[12],
            'PREVIOUS_PERIOD_SLOPE': vals[13],
            'LOAD_TS': vals[14]
        })

        print('Trend summary added to insert list, deletes not supported')

    # Method should clear the previous results for this trend / run, and write the trend details to the database
    #
    # @input df: a pandas dataframe with the fields outlined in DDL for the TREND_RESULT_DETAIL table
    # @input vals: a list of (ANALYSIS_ID, ANALYSIS_RESULT_ID)
    def writeTrendResultDetail(self, df, vals):
        self.insert_TrendResultDetail = df.to_dict('records')

        print('Trend detail added to insert list, deletes not supported')

    # Method should return the ANALYSIS_RESULT_ID's as a list where the time comparison period start / end dates match a corresponding analysis_id
    # 
    # @input ANALYSIS_ID: the ANALYSIS_ID to search for
    # @input RECENT_PERIOD_START: the start date of the recent period
    # @input RECENT_PERIOD_END: the end date of the recent period
    # @input PREVIOUS_PERIOD_START: the start date of the previous period
    # @input PREVIOUS_PERIOD_END: the end date of the previous period
    def getTCAnalysisResultIDs(self, ANALYSIS_ID: int, RECENT_PERIOD_START: str, RECENT_PERIOD_END: str, PREVIOUS_PERIOD_START: str, PREVIOUS_PERIOD_END: str):
        print('NOT SUPPORTED: Deletes are not supported for Fivetran')

        return []

    # Method should return the ANALYSIS_RESULT_ID's as a list where the time comparison period start / end dates match a corresponding analysis_id
    # 
    # @input ANALYSIS_ID: the ANALYSIS_ID to search for
    # @input GROUP_A_NAME: the name of Group A
    # @input GROUP_B_NAME: the name of Group B
    def getGCAnalysisResultIDs(self, ANALYSIS_ID: int, GROUP_A_NAME: str, GROUP_B_NAME: str):
        print('NOT SUPPORTED: Deletes are not supported for Fivetran')

        return []

    # Method should return the ANALYSIS_RESULT_ID's thatmatch a corresponding analysis_id
    # 
    # @input ANALYSIS_ID: the ANALYSIS_ID to search for
    def getGPAnalysisResultIDs(self, ANALYSIS_ID: int):
        print('NOT SUPPORTED: Deletes are not supported for Fivetran')

        return []

    # Method should format output into a JSON string that will be returned as output result of the fucntion call
    def formatResults(self, event: dict):
        event.pop('API_KEY')

        pk_analysisId = {'primary_key': ['ANALYSIS_ID']}
        pk_analysisResultId = {'primary_key': ['ANALYSIS_ID','ANALYSIS_RESULT_ID']}
        pk_subgroupId = {'primary_key': ['ANALYSIS_ID','ANALYSIS_RESULT_ID','SUBGROUP_ID']}
        pk_stepId = {'primary_key': ['ANALYSIS_ID','ANALYSIS_RESULT_ID','STEP_ID']}

        insert = {
            'ANALYSIS': self.insert_Analysis,
            'ANALYSIS_RESULT_SUMMARY': self.insert_AnalysisResultSummary,
            'ANALYSIS_RESULT_DETAIL': self.insert_AnalysisResultDetail,
            'ANALYSIS_RESULT_WATERFALL': self.insert_AnalysisWaterfall,
            'TREND_RESULT_SUMMARY': self.insert_TrendResultSummary,
            'TREND_RESULT_DETAIL': self.insert_TrendResultDetail
        }

        schema = {
            'ANALYSIS': pk_analysisId,
            'ANALYSIS_RESULT_SUMMARY': pk_analysisResultId,
            'ANALYSIS_RESULT_DETAIL': pk_subgroupId,
            'ANALYSIS_RESULT_WATERFALL': pk_stepId,
            'TREND_RESULT_SUMMARY': pk_analysisResultId,
            'TREND_RESULT_DETAIL': pk_subgroupId
        }

        formattedResults = {
            'state': event,
            'insert': insert,
            'schema': schema,
            'hasMore': False
        }

        return json.loads(json.dumps(formattedResults, default=str).replace("NaN", "null"))
    
    