import snowflake.connector
import snowflake.connector.pandas_tools as pt
import config
import datetime

# SQL Statements to operate the workflow
SELECT_TC_ANALYSIS_RESULT_IDS = """SELECT ANALYSIS_RESULT_ID FROM ANALYSIS_RESULT_SUMMARY WHERE ANALYSIS_ID = %s AND RECENT_PERIOD_START = %s AND RECENT_PERIOD_END = %s AND PREVIOUS_PERIOD_START = %s AND PREVIOUS_PERIOD_END = %s"""
SELECT_GC_ANALYSIS_RESULT_IDS = """SELECT ANALYSIS_RESULT_ID FROM ANALYSIS_RESULT_SUMMARY WHERE ANALYSIS_ID = %s AND GROUP_A_NAME = %s AND GROUP_B_NAME = %s"""
SELECT_GP_ANALYSIS_RESULT_IDS = """SELECT ANALYSIS_RESULT_ID FROM ANALYSIS_RESULT_SUMMARY WHERE ANALYSIS_ID = %s"""

ANALYSIS_INSERT_STATEMENT = """INSERT INTO ANALYSIS VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
ANALYSIS_RESULT_SUMMARY_INSERT_STATEMENT = """INSERT INTO ANALYSIS_RESULT_SUMMARY VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
ANALYSIS_RESULT_DETAIL_TABLE_NAME = 'ANALYSIS_RESULT_DETAIL'
ANALYSIS_RESULT_WATERFALL_TABLE_NAME = 'ANALYSIS_RESULT_WATERFALL'

TREND_RESULT_SUMMARY_INSERT_STATEMENT = """INSERT INTO TREND_RESULT_SUMMARY VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
TREND_RESULT_DETAIL_TABLE_NAME = 'TREND_RESULT_DETAIL'

DELETE_ANALYSIS_STATEMENT = """DELETE FROM ANALYSIS WHERE ANALYSIS_ID = %s"""
DELETE_ANALYSIS_RESULT_SUMMARY_STATEMENT = """DELETE FROM ANALYSIS_RESULT_SUMMARY WHERE ANALYSIS_ID = %s AND ANALYSIS_RESULT_ID = %s"""
DELETE_ANALYSIS_RESULT_DETAIL_STATEMENT = """DELETE FROM ANALYSIS_RESULT_DETAIL WHERE ANALYSIS_ID = %s AND ANALYSIS_RESULT_ID = %s"""
DELETE_ANALYSIS_RESULT_WATERFALL_STATEMENT = """DELETE FROM ANALYSIS_RESULT_WATERFALL WHERE ANALYSIS_ID = %s AND ANALYSIS_RESULT_ID = %s"""

DELETE_TREND_RESULT_SUMMARY_STATEMENT = """DELETE FROM TREND_RESULT_SUMMARY WHERE ANALYSIS_ID = %s AND ANALYSIS_RESULT_ID = %s"""
DELETE_TREND_RESULT_DETAIL_STATEMENT = """DELETE FROM TREND_RESULT_DETAIL WHERE ANALYSIS_ID = %s AND ANALYSIS_RESULT_ID = %s"""

TRUNCATE_ANALYSIS_STATEMENT = 'TRUNCATE TABLE ANALYSIS'
TRUNCATE_ANALYSIS_RESULT_SUMMARY_STATEMENT = 'TRUNCATE TABLE ANALYSIS_RESULT_SUMMARY'
TRUNCATE_ANALYSIS_RESULT_DETAIL_STATEMENT = 'TRUNCATE TABLE ANALYSIS_RESULT_DETAIL'
TRUNCATE_ANALYSIS_RESULT_WATERFALL_STATEMENT = 'TRUNCATE TABLE ANALYSIS_RESULT_WATERFALL'

TRUNCATE_TREND_RESULT_SUMMARY_STATEMENT = 'TRUNCATE TABLE TREND_RESULT_SUMMARY'
TRUNCATE_TREND_RESULT_DETAIL_STATEMENT = 'TRUNCATE TABLE TREND_RESULT_DETAIL'

class SisuOutputDatabaseConnection:
    conn = ''
    curs = ''

    # init method should establish a connection to the database, and set any connection parameters needed to support executing queries
    def __init__(self):
        USE_ROLE_STATEMENT = 'USE ROLE '

        self.conn = snowflake.connector.connect(user=config.USERNAME,
                                            password=config.PASSWORD,
                                            account=config.ACCOUNT_IDENTIFIER, 
                                            warehouse=config.WAREHOUSE_NAME,
                                            database=config.DATABASE_NAME,       
                                            schema=config.SCHEMA_NAME,
                                            autocommit=True)

        print('Successfully connected to Snowflake!')
        USE_ROLE_STATEMENT = USE_ROLE_STATEMENT + config.ROLE_NAME

        # Get a cursor and switch to a role with permissions to write
        self.curs = self.conn.cursor()
        self.curs.execute(USE_ROLE_STATEMENT)
        print('Set Snowflake connection role!')
    
    # Method should truncate the three tables
    def truncateTables(self):
        print('Truncating tables...')

        self.curs.execute(TRUNCATE_ANALYSIS_STATEMENT)
        self.curs.execute(TRUNCATE_ANALYSIS_RESULT_SUMMARY_STATEMENT)
        self.curs.execute(TRUNCATE_ANALYSIS_RESULT_DETAIL_STATEMENT)
        self.curs.execute(TRUNCATE_ANALYSIS_RESULT_WATERFALL_STATEMENT)
        self.curs.execute(TRUNCATE_TREND_RESULT_SUMMARY_STATEMENT)
        self.curs.execute(TRUNCATE_TREND_RESULT_DETAIL_STATEMENT)

        print('Tables truncated!')
    
    # Method should delete the analysis metadata from the database
    #
    # @input analysisId: analysisId to be deleted from the table
    def deleteAnalysisMetadata(self, analysisId: int):
        self.curs.execute(DELETE_ANALYSIS_STATEMENT, str(analysisId))

        print('Analysis metadata deleted from the database')

    # Method should write the analysis metadata to the database
    #
    # @input vals: a list of fields outlined in DDL for the ANALYSIS table
    def writeAnalysisMetadata(self, vals):
        self.curs.execute(ANALYSIS_INSERT_STATEMENT, params=vals)

        print('Analysis metadata written to the database')
    
    # Method should clear the previous results for this analysisId / analysisResultId from the summary table
    #
    # @input analysisId: the analysisId that will have its' results deleted
    # @input analysisResultId: the analysisResultId that will be deleted
    def deleteAnalysisResultSummary(self, analysisId: int, analysisResultId: int):
        self.curs.execute(DELETE_ANALYSIS_RESULT_SUMMARY_STATEMENT, (str(analysisId), str(analysisResultId)))

        print('Analysis summary deleted from the database')

    # Method should write the analysis summary to the database
    #
    # @input vals: a list of fields outlined in DDL for the ANALYSIS_RESULT_SUMMARY table
    def writeAnalysisResultSummary(self, vals):
        self.curs.execute(ANALYSIS_RESULT_SUMMARY_INSERT_STATEMENT, vals)

        print('Analysis summary written to the database')

    # Method should clear the previous results for this analysisId / analysisResultId from the detail table
    #
    # @input analysisId: the analysisId that will have its' results deleted
    # @input analysisResultId: the analysisResultId that will be deleted
    def deleteAnalysisResultDetail(self, analysisId: int, analysisResultId: int):
        self.curs.execute(DELETE_ANALYSIS_RESULT_DETAIL_STATEMENT, (str(analysisId), str(analysisResultId)))

        print('Analysis detail deleted from the database')

    # Method should write the analysis waterfall to the database
    #
    # @input df: a pandas dataframe with the fields outlined in DDL for the ANALYSIS_RESULT_WATERFALL table
    def writeAnalysisResultWaterfall(self, df):
        pt.write_pandas(self.conn, df, ANALYSIS_RESULT_WATERFALL_TABLE_NAME)

        print('Analysis waterfall written to the database')

    # Method should clear the previous results for this analysisId / analysisResultId from the waterfall table
    #
    # @input analysisId: the analysisId that will have its' waterfall deleted
    # @input analysisResultId: the analysisResultId that will be deleted
    def deleteAnalysisResultWaterfall(self, analysisId: int, analysisResultId: int):
        self.curs.execute(DELETE_ANALYSIS_RESULT_WATERFALL_STATEMENT, (str(analysisId), str(analysisResultId)))

        print('Analysis waterfall deleted from the database')

    # Method should write the analysis details to the database
    #
    # @input df: a pandas dataframe with the fields outlined in DDL for the ANALYSIS_RESULT_DETAIL table
    def writeAnalysisResultDetail(self, df):
        pt.write_pandas(self.conn, df, ANALYSIS_RESULT_DETAIL_TABLE_NAME)

        print('Analysis detail written to the database')
    
    # Method should clear the previous results for this trend / run, and write the trend summary to the database
    #
    # @input vals: a list of fields outlined in DDL for the TREND_RESULT_SUMMARY table
    def writeTrendResultSummary(self, vals):
        self.curs.execute(DELETE_TREND_RESULT_SUMMARY_STATEMENT, params=(vals[0], vals[1]))
        self.curs.execute(TREND_RESULT_SUMMARY_INSERT_STATEMENT, vals)

        print('Trend summary written to the database')

    # Method should clear the previous results for this trend / run, and write the trend details to the database
    #
    # @input df: a pandas dataframe with the fields outlined in DDL for the TREND_RESULT_DETAIL table
    # @input vals: a list of (ANALYSIS_ID, ANALYSIS_RESULT_ID)
    def writeTrendResultDetail(self, df, vals):
        self.curs.execute(DELETE_TREND_RESULT_DETAIL_STATEMENT, params=vals)
        pt.write_pandas(self.conn, df, TREND_RESULT_DETAIL_TABLE_NAME)

        print('Trend detail written to the database')

    # Method should return the ANALYSIS_RESULT_ID's as a list where the time comparison period start / end dates match a corresponding analysis_id
    # 
    # @input ANALYSIS_ID: the ANALYSIS_ID to search for
    # @input RECENT_PERIOD_START: the start date of the recent period
    # @input RECENT_PERIOD_END: the end date of the recent period
    # @input PREVIOUS_PERIOD_START: the start date of the previous period
    # @input PREVIOUS_PERIOD_END: the end date of the previous period
    def getTCAnalysisResultIDs(self, ANALYSIS_ID: int, RECENT_PERIOD_START: str, RECENT_PERIOD_END: str, PREVIOUS_PERIOD_START: str, PREVIOUS_PERIOD_END: str):
        self.curs.execute(SELECT_TC_ANALYSIS_RESULT_IDS, (str(ANALYSIS_ID), RECENT_PERIOD_START, RECENT_PERIOD_END, PREVIOUS_PERIOD_START, PREVIOUS_PERIOD_END))
        
        vals = []

        for rec in self.curs:
            vals.append(rec[0])

        return vals

    # Method should return the ANALYSIS_RESULT_ID's as a list where the time comparison period start / end dates match a corresponding analysis_id
    # 
    # @input ANALYSIS_ID: the ANALYSIS_ID to search for
    # @input GROUP_A_NAME: the name of Group A
    # @input GROUP_B_NAME: the name of Group B
    def getGCAnalysisResultIDs(self, ANALYSIS_ID: int, GROUP_A_NAME: str, GROUP_B_NAME: str):
        self.curs.execute(SELECT_GC_ANALYSIS_RESULT_IDS, (str(ANALYSIS_ID), GROUP_A_NAME, GROUP_B_NAME))
        
        vals = []

        for rec in self.curs:
            vals.append(rec[0])

        return vals

    # Method should return the ANALYSIS_RESULT_ID's thatmatch a corresponding analysis_id
    # 
    # @input ANALYSIS_ID: the ANALYSIS_ID to search for
    def getGPAnalysisResultIDs(self, ANALYSIS_ID: int):
        self.curs.execute(SELECT_GP_ANALYSIS_RESULT_IDS, (str(ANALYSIS_ID)))
        
        vals = []

        for rec in self.curs:
            vals.append(rec[0])

        return vals

