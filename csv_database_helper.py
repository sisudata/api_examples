import os
import csv
import config
import pandas
import datetime

class SisuOutputDatabaseConnection:
    filepath = ''
    overwrite = 'a'
    delimiter = '^'

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
        f = open(self.filepath + '/ANALYSIS.CSV', self.overwrite)
        w = csv.writer(f, delimiter=self.delimiter)
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
        f = open(self.filepath + '/ANALYSIS_RESULT_SUMMARY.CSV', self.overwrite)
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
        f = open(self.filepath + '/ANALYSIS_RESULT_WATERFALL.CSV', self.overwrite)
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
        f = open(self.filepath + '/ANALYSIS_RESULT_DETAIL.CSV', self.overwrite)
        df.to_csv(f, sep=self.delimiter, doublequote=True, na_rep='', header=False, index=False)

        print('Analysis detail written to the CSV file')
    
    # Method should clear the previous results for this trend / run, and write the trend summary to the database
    #
    # @input vals: a list of fields outlined in DDL for the TREND_RESULT_SUMMARY table
    def writeTrendResultSummary(self, vals):
        f = open(self.filepath + '/TREND_RESULT_SUMMARY.CSV', self.overwrite)
        w = csv.writer(f, delimiter=self.delimiter)
        w.writerow(vals)

        print('Trend summary written to the CSV file')

    # Method should clear the previous results for this trend / run, and write the trend details to the database
    #
    # @input df: a pandas dataframe with the fields outlined in DDL for the TREND_RESULT_DETAIL table
    # @input vals: a list of (ANALYSIS_ID, ANALYSIS_RESULT_ID)
    def writeTrendResultDetail(self, df, vals):
        f = open(self.filepath + '/TREND_RESULT_DETAIL.CSV', self.overwrite)
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
    
    