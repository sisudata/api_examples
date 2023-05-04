# REQUIRED IMPORTS
import os
from snowflake_database_helper import SisuOutputDatabaseConnection
#from fivetran_database_helper import SisuOutputDatabaseConnection
#from csv_database_helper import SisuOutputDatabaseConnection

# RETURN A DATABASE CONNECTION
def getDatabaseConnection():
    return SisuOutputDatabaseConnection()
# END - RETURN A DATABASE CONNECTION

# DATABASE CONNECTION PARAMETERS
USERNAME = ''
PASSWORD = ''
ACCOUNT_IDENTIFIER = ''
DATABASE_NAME = 'SISU_OUTPUTS'
WAREHOUSE_NAME = ''
SCHEMA_NAME = 'PUBLIC'
ROLE_NAME = ''
# END - DATABASE CONNECTION PARAMETERS

# CSV PARAMETERS
FILEPATH = '/Users/jdoe/Documents'
OVERWRITE = True
CSV_DELIMITER = ','
# END - CSV PARAMETERS

# SEGMENT LOAD PARAMETERS
BATCH_SIZE = 1000
TRUNCATE_TABLES = False
DELIMITER = '^'
DEBUG = False
# END - SEGMENT LOAD PARAMETERS

# USER PARAMETERS
API_KEY = ''

