# Welcome!


This repository contains the code examples for consuming Sisu's insights in BI tools. For more information or to get started, contact your Sisu Customer Success team


# Code Details


## Database Structure

Below is an overview of the tables and columns, along with their semantic meaning:

NOTE: It is intended that **SET1** refers to _Group A_ or the _Recent_ _Period_ value, and **SET2** refers to_ Group B_ or the_ Previous Period_ value. For General Performance analyses, **SET2** will always be <span style="text-decoration:underline;">NULL</span>

**ANALYSIS** - Holds the metadata for this analysis


<table>
  <tr>
   <td><strong>Column Name</strong>
   </td>
   <td><strong>Type</strong>
   </td>
   <td><strong>Semantic Meaning</strong>
   </td>
  </tr>
  <tr>
   <td>ANALYSIS_ID
   </td>
   <td>BIGINT, PRIMARY KEY
   </td>
   <td> The static ID for a given analysis
   </td>
  </tr>
  <tr>
   <td>ANALYSIS_NAME
   </td>
   <td>TEXT
   </td>
   <td> The name of the analysis in Sisu
   </td>
  </tr>
  <tr>
   <td>ANALYSIS_TYPE
   </td>
   <td>TEXT
   </td>
   <td> The type of the analysis
   </td>
  </tr>
  <tr>
   <td>APPLICATION_URL
   </td>
   <td>TEXT
   </td>
   <td> A direct link to the analysis in Sisu
   </td>
  </tr>
  <tr>
   <td>CREATED_AT
   </td>
   <td>TIMESTAMP
   </td>
   <td> Timestamp when this analysis was created
   </td>
  </tr>
  <tr>
   <td>METRIC_ID
   </td>
   <td>BIGINT
   </td>
   <td> The static ID of the metric analyzed
   </td>
  </tr>
  <tr>
   <td>METRIC_NAME
   </td>
   <td>TEXT
   </td>
   <td> The name of the metric analyzed
   </td>
  </tr>
  <tr>
   <td>METRIC_DESIRED_DIRECTION
   </td>
   <td>TEXT
   </td>
   <td> The desired direction of the metric analyzed
   </td>
  </tr>
  <tr>
   <td>PROJECT_ID
   </td>
   <td>BIGINT
   </td>
   <td> The static ID of the project where this analysis is located in Sisu
   </td>
  </tr>
  <tr>
   <td>PROJECT_NAME
   </td>
   <td>TEXT
   </td>
   <td> The name of the Sisu project
   </td>
  </tr>
  <tr>
   <td>LOAD_TS
   </td>
   <td>TIMESTAMP
   </td>
   <td> The timestamp when this record was loaded into the data warehouse
   </td>
  </tr>
</table>


**ANALYSIS_RESULT_SUMMARY** - Holds the summary ribbon information for this analysis


<table>
  <tr>
   <td><strong>Column Name</strong>
   </td>
   <td><strong>Type</strong>
   </td>
   <td><strong>Semantic Meaning</strong>
   </td>
  </tr>
  <tr>
   <td>ANALYSIS_ID
   </td>
   <td>BIGINT, PRIMARY KEY
   </td>
   <td> The static ID for a given analysis
   </td>
  </tr>
  <tr>
   <td>ANALYSIS_RESULT_ID
   </td>
   <td>BIGINT, PRIMARY KEY
   </td>
   <td> The static ID for the results associated with a specific execution of a specific analysis
   </td>
  </tr>
  <tr>
   <td>REQUESTED_AT
   </td>
   <td>TIMESTAMP
   </td>
   <td> Timestamp when this analysis execution began
   </td>
  </tr>
  <tr>
   <td>COMPLETED_AT
   </td>
   <td>TIMESTAMP
   </td>
   <td> Timestamp when this analysis execution completed
   </td>
  </tr>
  <tr>
   <td>RUN_STATUS
   </td>
   <td>TEXT
   </td>
   <td> Status of the analysis execution
   </td>
  </tr>
  <tr>
   <td>RUN_TYPE
   </td>
   <td>TEXT
   </td>
   <td> Type of the analysis execution
   </td>
  </tr>
  <tr>
   <td>TIMEFRAME
   </td>
   <td>TEXT
   </td>
   <td> Currently empty
   </td>
  </tr>
  <tr>
   <td>PREVIOUS_PERIOD_START
   </td>
   <td>TIMESTAMP
   </td>
   <td> Start date for the Previous Period of a Time Comparison analysis
   </td>
  </tr>
  <tr>
   <td>PREVIOUS_PERIOD_END
   </td>
   <td>TIMESTAMP
   </td>
   <td> End date for the Previous Period of a Time Comparison analysis
   </td>
  </tr>
  <tr>
   <td>RECENT_PERIOD_START
   </td>
   <td>TIMESTAMP
   </td>
   <td> Start date for the Recent Period of a Time Comparison analysis
   </td>
  </tr>
  <tr>
   <td>RECENT_PERIOD_END
   </td>
   <td>TIMESTAMP
   </td>
   <td> End date for the Recent Period of a Time Comparison analysis
   </td>
  </tr>
  <tr>
   <td>GROUP_A_NAME
   </td>
   <td>TEXT
   </td>
   <td> The name of Group A for a Group Comparison analysis
   </td>
  </tr>
  <tr>
   <td>GROUP_B_NAME
   </td>
   <td>TEXT
   </td>
   <td> The name of Group B for a Group Comparison analysis
   </td>
  </tr>
  <tr>
   <td>METRIC_TYPE_LABEL
   </td>
   <td>TEXT
   </td>
   <td> The type of metric analyzed
   </td>
  </tr>
  <tr>
   <td>PERCENT_CHANGE
   </td>
   <td>FLOAT
   </td>
   <td> The Percentage Change in metric value between periods or groups
   </td>
  </tr>
  <tr>
   <td>DIRECTION
   </td>
   <td>TEXT
   </td>
   <td> The direction of change of the metric value between periods or groups
   </td>
  </tr>
  <tr>
   <td>SET1_CARD_LABEL
   </td>
   <td>TEXT
   </td>
   <td> Summary card label for set 1
   </td>
  </tr>
  <tr>
   <td>SET1_CATEGORY_FILTER
   </td>
   <td>TEXT
   </td>
   <td> Any filters applied to set 1 data
   </td>
  </tr>
  <tr>
   <td>SET1_AVERAGE
   </td>
   <td>FLOAT
   </td>
   <td> The average value for set 1
   </td>
  </tr>
  <tr>
   <td>SET1_MIN
   </td>
   <td>FLOAT
   </td>
   <td> The minimum value for set 1
   </td>
  </tr>
  <tr>
   <td>SET1_MAX
   </td>
   <td>FLOAT
   </td>
   <td> The maximum value for set 1
   </td>
  </tr>
  <tr>
   <td>SET1_MEDIAN
   </td>
   <td>FLOAT
   </td>
   <td> The median value for set 1
   </td>
  </tr>
  <tr>
   <td>SET1_SUM
   </td>
   <td>FLOAT
   </td>
   <td> The sum value for set 1
   </td>
  </tr>
  <tr>
   <td>SET1_SUMMARY_VALUE
   </td>
   <td>FLOAT
   </td>
   <td> The metric value for set 1
   </td>
  </tr>
  <tr>
   <td>SET1_TOTAL_SIZE
   </td>
   <td>FLOAT
   </td>
   <td> The population size for set 1
   </td>
  </tr>
  <tr>
   <td>SET1_TOTAL_NUMERATOR
   </td>
   <td>FLOAT
   </td>
   <td> For rate metrics, the total numerator value for set 1
   </td>
  </tr>
  <tr>
   <td>SET1_TOTAL_DENOMINATOR
   </td>
   <td>FLOAT
   </td>
   <td> For rate metrics the total denominator value for set 1
   </td>
  </tr>
  <tr>
   <td>SET1_MATCH_SIZE
   </td>
   <td>FLOAT
   </td>
   <td> The match size for set 1
   </td>
  </tr>
  <tr>
   <td>SET1_WEIGHT
   </td>
   <td>FLOAT
   </td>
   <td> The weight value for set 1
   </td>
  </tr>
  <tr>
   <td>SET2_CARD_LABEL
   </td>
   <td>TEXT
   </td>
   <td> Summary card label for set 2
   </td>
  </tr>
  <tr>
   <td>SET2_CATEGORY_FILTER
   </td>
   <td>TEXT
   </td>
   <td> Any filters applied to set 2 data
   </td>
  </tr>
  <tr>
   <td>SET2_AVERAGE
   </td>
   <td>FLOAT
   </td>
   <td> The average value for set 2
   </td>
  </tr>
  <tr>
   <td>SET2_MIN
   </td>
   <td>FLOAT
   </td>
   <td> The minimum value for set 2
   </td>
  </tr>
  <tr>
   <td>SET2_MAX
   </td>
   <td>FLOAT
   </td>
   <td> The maximum value for set 2
   </td>
  </tr>
  <tr>
   <td>SET2_MEDIAN
   </td>
   <td>FLOAT
   </td>
   <td> The median value for set 2
   </td>
  </tr>
  <tr>
   <td>SET2_SUM
   </td>
   <td>FLOAT
   </td>
   <td> The sum value for set 2
   </td>
  </tr>
  <tr>
   <td>SET2_SUMMARY_VALUE
   </td>
   <td>FLOAT
   </td>
   <td> The metric value for set 2
   </td>
  </tr>
  <tr>
   <td>SET2_TOTAL_SIZE
   </td>
   <td>FLOAT
   </td>
   <td> The population size for set 2
   </td>
  </tr>
  <tr>
   <td>SET2_TOTAL_NUMERATOR
   </td>
   <td>FLOAT
   </td>
   <td> For rate metrics, the total numerator value for set 2
   </td>
  </tr>
  <tr>
   <td>SET2_TOTAL_DENOMINATOR
   </td>
   <td>FLOAT
   </td>
   <td> For rate metrics the total denominator value for set 2
   </td>
  </tr>
  <tr>
   <td>SET2_MATCH_SIZE
   </td>
   <td>FLOAT
   </td>
   <td> The match size for set 2
   </td>
  </tr>
  <tr>
   <td>SET2_WEIGHT
   </td>
   <td>FLOAT
   </td>
   <td> The weight value for set 2
   </td>
  </tr>
  <tr>
   <td>LOAD_TS
   </td>
   <td>TIMESTAMP
   </td>
   <td> The timestamp when this record was loaded into the data warehouse
   </td>
  </tr>
</table>


**ANALYSIS_RESULT_WATERFALL** - Holds the waterfall steps for a given analysis, if applicable (NOTE: General Performance analyses do not have waterfall charts)


<table>
  <tr>
   <td><strong>Column Name</strong>
   </td>
   <td><strong>Type</strong>
   </td>
   <td><strong>Semantic Meaning</strong>
   </td>
  </tr>
  <tr>
   <td>ANALYSIS_ID
   </td>
   <td>BIGINT, PRIMARY KEY
   </td>
   <td> The static ID for a given analysis
   </td>
  </tr>
  <tr>
   <td>ANALYSIS_RESULT_ID
   </td>
   <td>BIGINT, PRIMARY KEY
   </td>
   <td> The static ID for the results associated with a specific execution of a specific analysis
   </td>
  </tr>
  <tr>
   <td>STEP_ID
   </td>
   <td>INTEGER, PRIMARY KEY
   </td>
   <td> The step ID for this step of the waterfall chart
   </td>
  </tr>
  <tr>
   <td>STEP_TYPE
   </td>
   <td>TEXT
   </td>
   <td> The type of this step of the waterfall chart
   </td>
  </tr>
  <tr>
   <td>FACTOR_0_DIMENSION
   </td>
   <td>TEXT
   </td>
   <td> Dimension name for the first factor of this step
   </td>
  </tr>
  <tr>
   <td>FACTOR_0_VALUE
   </td>
   <td>TEXT
   </td>
   <td> Dimension value for the first factor of this step
   </td>
  </tr>
  <tr>
   <td>FACTOR_1_DIMENSION
   </td>
   <td>TEXT
   </td>
   <td> Dimension name for the second factor of this step
   </td>
  </tr>
  <tr>
   <td>FACTOR_1_VALUE
   </td>
   <td>TEXT
   </td>
   <td> Dimension value for the second factor of this step
   </td>
  </tr>
  <tr>
   <td>FACTOR_2_DIMENSION
   </td>
   <td>TEXT
   </td>
   <td> Dimension name for the third factor of this step
   </td>
  </tr>
  <tr>
   <td>FACTOR_2_VALUE
   </td>
   <td>TEXT
   </td>
   <td> Dimension value for the third factor of this step
   </td>
  </tr>
  <tr>
   <td>STEP_IMPACT
   </td>
   <td>FLOAT
   </td>
   <td> The net impact of this step of the waterfall
   </td>
  </tr>
  <tr>
   <td>CUMULATIVE_IMPACT_BEFORE_STEP
   </td>
   <td>FLOAT
   </td>
   <td> The cumulative impact before this step of the waterfall
   </td>
  </tr>
  <tr>
   <td>CUMULATIVE_IMPACT_AFTER_STEP
   </td>
   <td>FLOAT
   </td>
   <td> The cumulative impact after this step of the waterfall
   </td>
  </tr>
  <tr>
   <td>OVERLAPPING_IMPACT
   </td>
   <td>FLOAT
   </td>
   <td> The amount of any overlapping impact
   </td>
  </tr>
  <tr>
   <td>CHANGE_IN_SIZE_SET1
   </td>
   <td>FLOAT
   </td>
   <td> The change in the below value type for this metric for set 1
   </td>
  </tr>
  <tr>
   <td>CHANGE_IN_SIZE_SET2
   </td>
   <td>FLOAT
   </td>
   <td> The change in the below value type for this metric for set 2
   </td>
  </tr>
  <tr>
   <td>CHANGE_IN_TYPE_SET1
   </td>
   <td>FLOAT
   </td>
   <td> The type of value changed above for this metric for set 1
   </td>
  </tr>
  <tr>
   <td>CHANGE_IN_TYPE_SET2
   </td>
   <td>FLOAT
   </td>
   <td> The type of value changed above for this metric for set 2
   </td>
  </tr>
  <tr>
   <td>LOAD_TS
   </td>
   <td>TIMESTAMP
   </td>
   <td> The timestamp when this record was loaded into the data warehouse
   </td>
  </tr>
</table>


**ANALYSIS_RESULT_DETAIL** - Holds the segment table information for a given analysis


<table>
  <tr>
   <td><strong>Column Name</strong>
   </td>
   <td><strong>Type</strong>
   </td>
   <td><strong>Semantic Meaning</strong>
   </td>
  </tr>
  <tr>
   <td>ANALYSIS_ID
   </td>
   <td>BIGINT, PRIMARY KEY
   </td>
   <td> The static ID for a given analysis
   </td>
  </tr>
  <tr>
   <td>ANALYSIS_RESULT_ID
   </td>
   <td>BIGINT, PRIMARY KEY
   </td>
   <td> The static ID for the results associated with a specific execution of a specific analysis
   </td>
  </tr>
  <tr>
   <td>SUBGROUP_ID
   </td>
   <td>BIGINT, PRIMARY KEY
   </td>
   <td> The static ID for this subgroup
   </td>
  </tr>
  <tr>
   <td>CONFIDENCE
   </td>
   <td>TEXT
   </td>
   <td> The Sisu calculated confidence bucket for this segment
   </td>
  </tr>
  <tr>
   <td>FACTOR_0_DIMENSION
   </td>
   <td>TEXT
   </td>
   <td> Dimension name for the first factor of this segment
   </td>
  </tr>
  <tr>
   <td>FACTOR_0_VALUE
   </td>
   <td>TEXT
   </td>
   <td> Dimension value for the first factor of this segment
   </td>
  </tr>
  <tr>
   <td>FACTOR_1_DIMENSION
   </td>
   <td>TEXT
   </td>
   <td> Dimension name for the second factor of this segment
   </td>
  </tr>
  <tr>
   <td>FACTOR_1_VALUE
   </td>
   <td>TEXT
   </td>
   <td> Dimension value for the second factor of this segment
   </td>
  </tr>
  <tr>
   <td>FACTOR_2_DIMENSION
   </td>
   <td>TEXT
   </td>
   <td> Dimension name for the third factor of this segment
   </td>
  </tr>
  <tr>
   <td>FACTOR_2_VALUE
   </td>
   <td>TEXT
   </td>
   <td> Dimension value for the third factor of this segment
   </td>
  </tr>
  <tr>
   <td>FACTOR_0_DIMENSION_FRIENDLY
   </td>
   <td>TEXT
   </td>
   <td> Dimension name for the first factor of this segment that has been formatted for easier readability
   </td>
  </tr>
  <tr>
   <td>FACTOR_1_DIMENSION_FRIENDLY
   </td>
   <td>TEXT
   </td>
   <td> Dimension value for the first factor of this segment that has been formatted for easier readability
   </td>
  </tr>
  <tr>
   <td>FACTOR_2_DIMENSION_FRIENDLY
   </td>
   <td>TEXT
   </td>
   <td> Dimension name for the second factor of this segment that has been formatted for easier readability
   </td>
  </tr>
  <tr>
   <td>FACTOR_0_VALUE_FRIENDLY
   </td>
   <td>TEXT
   </td>
   <td> Dimension value for the second factor of this segment that has been formatted for easier readability
   </td>
  </tr>
  <tr>
   <td>FACTOR_1_VALUE_FRIENDLY
   </td>
   <td>TEXT
   </td>
   <td> Dimension name for the third factor of this segment that has been formatted for easier readability
   </td>
  </tr>
  <tr>
   <td>FACTOR_2_VALUE_FRIENDLY
   </td>
   <td>TEXT
   </td>
   <td> Dimension value for the third factor of this segment that has been formatted for easier readability
   </td>
  </tr>
  <tr>
   <td>FACTOR_0_TEXT
   </td>
   <td>TEXT
   </td>
   <td> The combined, formatted, dimension name and value for the first factor of this segment
   </td>
  </tr>
  <tr>
   <td>FACTOR_1_TEXT
   </td>
   <td>TEXT
   </td>
   <td> The combined, formatted, dimension name and value for the second factor of this segment
   </td>
  </tr>
  <tr>
   <td>FACTOR_2_TEXT
   </td>
   <td>TEXT
   </td>
   <td> The combined, formatted, dimension name and value for the third factor of this segment
   </td>
  </tr>
  <tr>
   <td>SEGMENT_TEXT
   </td>
   <td>TEXT
   </td>
   <td> The combined, formatted, dimension names and values for this segment
   </td>
  </tr>
  <tr>
   <td>IMPACT
   </td>
   <td>FLOAT
   </td>
   <td> The Sisu calculated impact for this segment
   </td>
  </tr>
  <tr>
   <td>IMPACT_MAGNITUDE
   </td>
   <td>FLOAT
   </td>
   <td> The absolute value of the Sisu calculated impact for this segment
   </td>
  </tr>
  <tr>
   <td>IMPACT_RANK
   </td>
   <td>TEXT
   </td>
   <td> Currently empty
   </td>
  </tr>
  <tr>
   <td>SET1_SIZE
   </td>
   <td>FLOAT
   </td>
   <td> The Sisu calculated population size for this segment for set 1
   </td>
  </tr>
  <tr>
   <td>SET2_SIZE
   </td>
   <td>FLOAT
   </td>
   <td> The Sisu calculated population size for this segment for set 2
   </td>
  </tr>
  <tr>
   <td>SET1_VALUE
   </td>
   <td>FLOAT
   </td>
   <td> The Sisu calculated metric value for this segment for set 1
   </td>
  </tr>
  <tr>
   <td>SET2_VALUE
   </td>
   <td>FLOAT
   </td>
   <td> The Sisu calculated metric value for this segment for set 2
   </td>
  </tr>
  <tr>
   <td>PERCENT_CHANGE
   </td>
   <td>FLOAT
   </td>
   <td> The percentage change in metric value from set 1 to set 2
   </td>
  </tr>
  <tr>
   <td>DIRECTION
   </td>
   <td>TEXT
   </td>
   <td> The formatted direction of change in metric value for this segment
   </td>
  </tr>
  <tr>
   <td>DIRECTION_TEXT
   </td>
   <td>TEXT
   </td>
   <td> The textual representation of the direction of change in metric value for this segment
   </td>
  </tr>
  <tr>
   <td>ORIENTATION_MATCHES_METRIC
   </td>
   <td>TEXT
   </td>
   <td> True if the direction of change for this segment matches the desired direction of change for this metric. Otherwise, False
   </td>
  </tr>
  <tr>
   <td>SEGMENT_ORDER
   </td>
   <td>SMALLINT
   </td>
   <td> Number of factors involved in this segment (1, 2, or 3)
   </td>
  </tr>
  <tr>
   <td>SEGMENT_ORDER_TEXT
   </td>
   <td>TEXT
   </td>
   <td> A textual representation of whether this segment is a first, second, or third, order fact
   </td>
  </tr>
  <tr>
   <td>INSIGHT_TEXT
   </td>
   <td>TEXT
   </td>
   <td> A textual representation of this segment, its impact, direction of change, etc.
   </td>
  </tr>
  <tr>
   <td>CHANGE_IN_SIZE
   </td>
   <td>FLOAT
   </td>
   <td> Currently empty
   </td>
  </tr>
  <tr>
   <td>MIX_EFFECT
   </td>
   <td>FLOAT
   </td>
   <td> Currently empty
   </td>
  </tr>
  <tr>
   <td>NET_EFFECT
   </td>
   <td>FLOAT
   </td>
   <td> Currently empty
   </td>
  </tr>
  <tr>
   <td>NET_RELATIVE_EFFECT
   </td>
   <td>FLOAT
   </td>
   <td> Currently empty
   </td>
  </tr>
  <tr>
   <td>PERCENT_CHANGE_IN_SIZE
   </td>
   <td>FLOAT
   </td>
   <td> Currently empty
   </td>
  </tr>
  <tr>
   <td>RATE_EFFECT
   </td>
   <td>FLOAT
   </td>
   <td> Currently empty
   </td>
  </tr>
  <tr>
   <td>RELATIVE_PERCENT_CHANGE
   </td>
   <td>FLOAT
   </td>
   <td> Currently empty
   </td>
  </tr>
  <tr>
   <td>RATE_CHANGE
   </td>
   <td>FLOAT
   </td>
   <td> Currently empty
   </td>
  </tr>
  <tr>
   <td>RELATIVE_MIX_EFFECT
   </td>
   <td>FLOAT
   </td>
   <td> Currently empty
   </td>
  </tr>
  <tr>
   <td>SEGMENT_NAME
   </td>
   <td>TEXT
   </td>
   <td> Currently empty
   </td>
  </tr>
  <tr>
   <td>SEGMENT_RANK
   </td>
   <td>TEXT
   </td>
   <td> Currently empty
   </td>
  </tr>
  <tr>
   <td>SEGMENT_HASH
   </td>
   <td>TEXT
   </td>
   <td> Currently empty
   </td>
  </tr>
  <tr>
   <td>UNWEIGHTED_CHANGE_IN_AVERAGE
   </td>
   <td>FLOAT
   </td>
   <td> Currently empty
   </td>
  </tr>
  <tr>
   <td>WEIGHT
   </td>
   <td>FLOAT
   </td>
   <td> Currently empty
   </td>
  </tr>
  <tr>
   <td>WEIGHTED_CHANGE_IN_SUM
   </td>
   <td>FLOAT
   </td>
   <td> Currently empty
   </td>
  </tr>
  <tr>
   <td>UNITS
   </td>
   <td>TEXT
   </td>
   <td> Currently empty
   </td>
  </tr>
  <tr>
   <td>LOAD_TS
   </td>
   <td>TIMESTAMP
   </td>
   <td> The timestamp when this record was loaded into the data warehouse
   </td>
  </tr>
</table>


**TREND_RESULT_SUMMARY** - Holds summary card information for a trend detection


<table>
  <tr>
   <td><strong>Column Name</strong>
   </td>
   <td><strong>Type</strong>
   </td>
   <td><strong>Semantic Meaning</strong>
   </td>
  </tr>
  <tr>
   <td>ANALYSIS_ID
   </td>
   <td>BIGINT, PRIMARY KEY
   </td>
   <td> The static ID for a given analysis
   </td>
  </tr>
  <tr>
   <td>ANALYSIS_RESULT_ID
   </td>
   <td>BIGINT, PRIMARY KEY
   </td>
   <td> The static ID for the results associated with a specific execution of a specific analysis
   </td>
  </tr>
  <tr>
   <td>REQUESTED_AT
   </td>
   <td>TIMESTAMP
   </td>
   <td> Timestamp when this analysis execution began
   </td>
  </tr>
  <tr>
   <td>COMPLETED_AT
   </td>
   <td>TIMESTAMP
   </td>
   <td> Timestamp when this analysis execution completed
   </td>
  </tr>
  <tr>
   <td>RUN_STATUS
   </td>
   <td>TEXT
   </td>
   <td> Status of the analysis execution
   </td>
  </tr>
  <tr>
   <td>RUN_TYPE
   </td>
   <td>TEXT
   </td>
   <td> Type of the analysis execution
   </td>
  </tr>
  <tr>
   <td>CURRENT_PERIOD_CARD_LABEL
   </td>
   <td>TEXT
   </td>
   <td> Summary card label for the current trend
   </td>
  </tr>
  <tr>
   <td>CURRENT_PERIOD_DENOMINATOR_LABEL
   </td>
   <td>TEXT
   </td>
   <td> Summary card denominator label for the current trend
   </td>
  </tr>
  <tr>
   <td>CURRENT_PERIOD_PERCENT_CHANGE
   </td>
   <td>FLOAT
   </td>
   <td> Percent change for the current trend
   </td>
  </tr>
  <tr>
   <td>CURRENT_PERIOD_SLOPE
   </td>
   <td>FLOAT
   </td>
   <td> Trend line slope for the current trend
   </td>
  </tr>
  <tr>
   <td>PREVIOUS_PERIOD_CARD_LABEL
   </td>
   <td>TEXT
   </td>
   <td> Summary card label for the previous trend
   </td>
  </tr>
  <tr>
   <td>PREVIOUS_PERIOD_DENOMINATOR_LABEL
   </td>
   <td>TEXT
   </td>
   <td> Summary card denominator label for the previous trend
   </td>
  </tr>
  <tr>
   <td>PREVIOUS_PERIOD_PERCENT_CHANGE
   </td>
   <td>FLOAT
   </td>
   <td> Percent change for the previous trend
   </td>
  </tr>
  <tr>
   <td>PREVIOUS_PERIOD_SLOPE
   </td>
   <td>FLOAT
   </td>
   <td> Trend line slope for the previous trend
   </td>
  </tr>
  <tr>
   <td>LOAD_TS
   </td>
   <td>TIMESTAMP
   </td>
   <td> The timestamp when this record was loaded into the data warehouse
   </td>
  </tr>
</table>


**TREND_RESULT_DETAIL** - Holds the segment details for a trend detection


<table>
  <tr>
   <td><strong>Column Name</strong>
   </td>
   <td><strong>Type</strong>
   </td>
   <td><strong>Semantic Meaning</strong>
   </td>
  </tr>
  <tr>
   <td>ANALYSIS_ID
   </td>
   <td>BIGINT, PRIMARY KEY
   </td>
   <td> The static ID for a given analysis
   </td>
  </tr>
  <tr>
   <td>ANALYSIS_RESULT_ID
   </td>
   <td>BIGINT, PRIMARY KEY
   </td>
   <td> The static ID for the results associated with a specific execution of a specific analysis
   </td>
  </tr>
  <tr>
   <td>SUBGROUP_ID
   </td>
   <td>BIGINT, PRIMARY KEY
   </td>
   <td> The static ID for this subgroup
   </td>
  </tr>
  <tr>
   <td>FACTOR_0_DIMENSION
   </td>
   <td>TEXT
   </td>
   <td> Dimension name for the first factor of this segment
   </td>
  </tr>
  <tr>
   <td>FACTOR_0_VALUE
   </td>
   <td>TEXT
   </td>
   <td> Dimension value for the first factor of this segment
   </td>
  </tr>
  <tr>
   <td>FACTOR_1_DIMENSION
   </td>
   <td>TEXT
   </td>
   <td> Dimension name for the second factor of this segment
   </td>
  </tr>
  <tr>
   <td>FACTOR_1_VALUE
   </td>
   <td>TEXT
   </td>
   <td> Dimension value for the second factor of this segment
   </td>
  </tr>
  <tr>
   <td>FACTOR_2_DIMENSION
   </td>
   <td>TEXT
   </td>
   <td> Dimension name for the third factor of this segment
   </td>
  </tr>
  <tr>
   <td>FACTOR_2_VALUE
   </td>
   <td>TEXT
   </td>
   <td> Dimension value for the third factor of this segment
   </td>
  </tr>
  <tr>
   <td>IMPACT
   </td>
   <td>FLOAT
   </td>
   <td> The Sisu calculated impact for this segment
   </td>
  </tr>
  <tr>
   <td>START_DATE
   </td>
   <td>TIMESTAMP
   </td>
   <td> The Start Date of the trend for this segment
   </td>
  </tr>
  <tr>
   <td>END_DATE
   </td>
   <td>TIMESTAMP
   </td>
   <td> The End Date of the trend for this segment
   </td>
  </tr>
  <tr>
   <td>INTERCEPT
   </td>
   <td>FLOAT
   </td>
   <td> The intercept of the trend line for this segment
   </td>
  </tr>
  <tr>
   <td>SLOPE
   </td>
   <td>FLOAT
   </td>
   <td> The slope of the trend line for this segment
   </td>
  </tr>
  <tr>
   <td>SIZE
   </td>
   <td>FLOAT
   </td>
   <td> The population size of this segment
   </td>
  </tr>
  <tr>
   <td>LOAD_TS
   </td>
   <td>TIMESTAMP
   </td>
   <td> The timestamp when this record was loaded into the data warehouse
   </td>
  </tr>
</table>



## Description of provided scripts

The following scripts comprise the working solution:


### config.py

Configuration of the project is completed in `config.py`. Each of the project scripts uses different sections of this configuration file:



* **REQUIRED IMPORTS**: In this section we call additional libraries or classes that are required for operation of the project. Note that we import a custom class `SisuOutputDatabaseConnection`. Customers writing segments to Snowflake may use the existing class. Customers writing segments to other databases will need to write a database handler (see Extensions.) We also import `io` to allow input parameters such as passwords and API keys to be hosted in a profile file for security purposes
* **RETURN A DATABASE CONNECTION**: In this section, we define a method called `getDatabaseConnection()` that is to return a new `SisuOutputDatabaseConnection` object that implements the required handler methods (see Extensions.) Customers using Snowflake as their data warehouse require no changes
* **DATABASE CONNECTION PARAMETERS**: This section defines the connection parameters used by the `SisuOutputDatabaseConnection`. <span style="text-decoration:underline;">Customers will need to update the parameter values in this section for their data warehouse</span>. Customers using Snowflake will require new values for each of the existing parameters. Other data warehouse types will require different parameters (see Extensions)
* **SEGMENT LOAD PARAMETERS**: This section defines parameters used by `load_analysis_results.py` to control record insert batch size, the string delimiter to be used for segment load, whether database tables should be truncated at the start of execution, and whether the script should operate in debug mode (verbose logging to the console.) Customers should not need to modify this section unless directed by their Customer Success Manager or Solution Architect. <span style="text-decoration:underline;">NOTE: setting the truncate option to true will truncate all the results tables at the start of execution. This cannot be undone; use with extreme caution</span>
* **USER PARAMETERS**: Customers may put additional parameters for their organization in this section. In Sisu’s default configuration, we show how one may retrieve Sisu API keys stored in the executing user’s `bash` or `zsh` profile


### load_analysis_results.py

This is the main project script that performs the actions of:



* Updating analyses with new time period configurations
* Iterating over time periods for historical load of segments
* Executing an analysis
* Retrieving and formatting Sisu segments
* Passing segments to the database helper to be written to the warehouse

It is split into two main functions:

**<span style="text-decoration:underline;">process_tc_action</span>**

This method takes inputs to allow historical loads of different types for a Time Comparison analysis. For example, we may wish to execute a Time Comparison analysis for each of the previous 12 months, and write the segments to the database

Inputs to this method are all required:



* **API_KEY** - String: A valid Sisu API Key for the customer organization where the analysis to be operated resides
* **ANALYSIS_ID** - Integer: A valid Time Comparison analysis ID
* **ACTION_TYPE** - String: Must be one of:
    * **DOD**: Day Over Day execution
    * **WOW**: Week Over Week
    * **MOM**: Month Over Month
* **START_DATE** - Datetime: The starting date of the <span style="text-decoration:underline;">first Recent Period</span> of the historical load
* **END_DATE** - Datetime: The starting date of the <span style="text-decoration:underline;">last Recent Period</span> of the historical load

Executing historical loads is then automated. The script will perform one of the **ACTION_TYPE** loads as requested by the user. Dates are calculated, the analysis specified in **ANALYSIS_ID** is modified to set the Recent and Previous Period dates as calculated (see below,) and `execute_load()` is called with the provided **API_KEY** and **ANALYSIS_ID**

Dates are calculated and the script operates in the following manner:



1. We first calculate a **timeDelta**, which is a number of days according to the **ACTION_TYPE** specified. For **DOD**, **timeDelta** is one day. For **WOW**, **timeDelta** is seven days. For **MOM**, **timeDelta** is one month
2. We then calculate the initial dates based on the **START_DATE** provided. The Recent Period is set as **START_DATE** to **START_DATE** + **timeDelta**. The Previous Period is set as **START_DATE - timeDelta** to **START_DATE**
3. We then operate a loop of
    1. Update the Time Comparison to set the date ranges as calculated
    2. Call `execute_load()` for the modified analysis
    3. Update the date ranges, adding **timeDelta** to each of the Previous / Recent Period Start / End dates
    4. Stop operating when the Recent Period Start Date is <span style="text-decoration:underline;">AFTER</span> the **END_DATE** provided as input to the function

NOTES:



* Our calculations are based on the Recent Period, that is the later period, start and end dates. The Previous Period is set to the comparison period <span style="text-decoration:underline;">BEFORE</span> the Recent Period. One must ensure that data exists for both the Previous Period and Recent Period, or execution will fail
* The **START_DATE** and **END_DATE** input parameters specify the range of time to operate this historical load, <span style="text-decoration:underline;">NOT</span> as the start and end dates of any period of the analysis
* Sisu’s time period Start Date is <span style="text-decoration:underline;">inclusive</span>, but End Date is <span style="text-decoration:underline;">exclusive</span>. So, the Previous Period End Date may be the same as the Recent Period Start Date without any overlap in data

Examples:

{'ANALYSIS_ID': '174392', 'API_KEY': config.AI_API_KEY, 'ACTION_TYPE': 'DOD', 'START_DATE': '2018-12-04', 'END_DATE': '2018-12-06'}

This configuration will execute the analysis to do a **daily comparison** as follows:


<table>
  <tr>
   <td>Recent Period Start
   </td>
   <td>2018-12-04
   </td>
   <td>2018-12-05
   </td>
   <td>2018-12-06
   </td>
  </tr>
  <tr>
   <td>Recent Period End
   </td>
   <td>2018-12-05
   </td>
   <td>2018-12-06
   </td>
   <td>2018-12-07
   </td>
  </tr>
  <tr>
   <td>Previous Period Start
   </td>
   <td>2018-12-03
   </td>
   <td>2018-12-04
   </td>
   <td>2018-12-05
   </td>
  </tr>
  <tr>
   <td>Previous Period End
   </td>
   <td>2018-12-04
   </td>
   <td>2018-12-05
   </td>
   <td>2018-12-06
   </td>
  </tr>
</table>


{'ANALYSIS_ID': '174392', 'API_KEY': config.AI_API_KEY, 'ACTION_TYPE': WOW, 'START_DATE': '2018-12-04', 'END_DATE': '2019-01-06'}

This configuration will execute the analysis to do a **weekly comparison** as follows:


<table>
  <tr>
   <td>Recent Period Start
   </td>
   <td>2018-12-04
   </td>
   <td>2018-12-11
   </td>
   <td>2018-12-18
   </td>
   <td>2018-12-25
   </td>
   <td>2019-01-01
   </td>
  </tr>
  <tr>
   <td>Recent Period End
   </td>
   <td>2018-12-11
   </td>
   <td>2018-12-18
   </td>
   <td>2018-12-25
   </td>
   <td>2019-01-01
   </td>
   <td>2019-01-08
   </td>
  </tr>
  <tr>
   <td>Previous Period Start
   </td>
   <td>2018-11-27
   </td>
   <td>2018-12-04
   </td>
   <td>2018-12-11
   </td>
   <td>2018-12-18
   </td>
   <td>2018-12-25
   </td>
  </tr>
  <tr>
   <td>Previous Period End
   </td>
   <td>2018-12-04
   </td>
   <td>2018-12-11
   </td>
   <td>2018-12-18
   </td>
   <td>2018-12-25
   </td>
   <td>2019-01-01
   </td>
  </tr>
</table>


{'ANALYSIS_ID': '174392', 'API_KEY': config.AI_API_KEY, 'ACTION_TYPE': MOM, 'START_DATE': '2018-12-04', 'END_DATE': '2019-01-06'}

This configuration will execute the analysis to do a **monthly comparison** as follows:


<table>
  <tr>
   <td>Recent Period Start
   </td>
   <td>2018-12-04
   </td>
   <td>2019-01-04
   </td>
  </tr>
  <tr>
   <td>Recent Period End
   </td>
   <td>2019-01-04
   </td>
   <td>2019-02-04
   </td>
  </tr>
  <tr>
   <td>Previous Period Start
   </td>
   <td>2018-11-04
   </td>
   <td>2018-12-04
   </td>
  </tr>
  <tr>
   <td>Previous Period End
   </td>
   <td>2018-12-04
   </td>
   <td>2019-01-04
   </td>
  </tr>
</table>


**<span style="text-decoration:underline;">execute_load</span>**

This function performs the work of executing an analysis, retrieving and formatting the results, and sending them to the database helper to be stored in the warehouse

Inputs to this method are all required:



* **API_KEY** - String: A valid Sisu API Key for the customer organization where the analysis to be operated resides
* **ANALYSIS_ID** - Integer: A valid Trend Detection, General Performance, Group Comparison, or Time Comparison, analysis ID

This function will then perform the following actions:



1. Get a database connection by calling `config.getDatabaseConnection()`, which will return an object implementing the methods required of a `SisuOutputDatabaseConnection` (see above)
    1. Truncate the database tables if requested in config.py
2. Connect to Sisu with the provided **API_KEY**, and get the Analysis metadata (including some Metric information.) Format it. Delete the existing metadata for this Analysis and write updated metadata for this Analysis to the data warehouse
3. Execute the Analysis and retrieve the result summary and segment detail. Find any existing runs with the same group names or date ranges, and delete them from the summary and detail tables
4. Format the summary information. Calculate some derived columns for the analysis summary table. Insert the summary information into the data warehouse
5. Retrieve the analysis waterfall, format it, and insert it into the data warehouse
6. Format the segment detail information. Calculate some derived columns for the segment detail table, and insert the segment details into the data warehouse


### snowflake_database_helper.py

This script defines a class called `SisuOutputDatabaseConnection` that performs database-related functions to write Sisu analysis and segment information into the data warehouse. As the name suggests, this class operates on Snowflake data warehouses. Customers using other data warehouses will need to create their own implementation of this class that implements all of the same functions available in this object

Class **variables** are declared at the top of the class to define SQL statements that would be used to execute select, insert, delete, and truncate operations for the specific data warehouse. <span style="text-decoration:underline;">These variables are convenience for the developer and not explicitly required as they are not used by callers of the class</span>

Class **functions** are declared inside the class declaration to perform the various database operations required to operate the `execute_load()` function detailed above. <span style="text-decoration:underline;">Unlike class variables, class functions are required and must be implemented for any new data warehouse type a customer desires to use</span>:



* **__init__()**: This is a standard class initialization function. Using configuration in `config.py`, it performs warehouse-specific tasks to establish a connection and create a reusable cursor for database operations that span the life of the execution. At the end of this function, a connection and cursor object should be fully initialized and stored in the class variables
* **truncateTables()**: This function should perform the database operations required to remove all data from all of the database tables defined for the solution. Think of this as a reset button for the data tables. At the end of this function, each of the tables will be empty
* **deleteAnalysisMetadata(ANALYSIS_ID Integer)**: This function should delete the analysis with the **ANALYSIS_ID** provided as input from the **ANALYSIS** table
* **writeAnalysisMetadata(vals List)**: This function should insert a record into the **ANALYSIS** table. The input list **vals** will contain, in order, the column values to be inserted into the table to form a complete record, even if a column value is <span style="text-decoration:underline;">NULL</span>
* **deleteAnalysisResultSummary(ANALYSIS_ID Integer, ANALYSIS_RESULT_ID Integer)**: This function should delete any records from the **ANALYSIS_RESULT_SUMMARY** table with the given **ANALYSIS_ID** and **ANALYSIS_RESULT_ID** combination. In practice, each call to this method should result in the deletion of one record from the table
* **writeAnalysisResultSummary(vals List)**: This function should insert a record into the **ANALYSIS_RESULT_SUMMARY** table. The input list **vals** will contain, in order, the column values to be inserted into the table to form a complete record, even if a column value is <span style="text-decoration:underline;">NULL</span>
* **deleteAnalysisResultDetail(ANALYSIS_ID Integer, ANALYSIS_RESULT_ID Integer)**: This function should delete any records from the **ANALYSIS_RESULT_DETAIL** table with the given **ANALYSIS_ID** and **ANALYSIS_RESULT_ID** combination. In practice, each call to this method should result in the deletion of many records from the table, each corresponding to a segment from the given execution of a specific analysis
* **writeAnalysisResultDetail(df Dataframe)**: This function should write the pandas dataframe containing the segments for a given analysis execution into the **ANALYSIS_RESULT_DETAIL** table. **df** will contain many rows of data that may be inserted in bulk, or as individual records, depending on the capabilities of the data warehouse. Each row of **df** will contain a complete record, even if some of the column values are <span style="text-decoration:underline;">NULL</span>
* **deleteAnalysisResultWaterfall(ANALYSIS_ID Integer, ANALYSIS_RESULT_ID Integer)**: This function should delete any records from the **ANALYSIS_RESULT_WATERFALL** table with the given **ANALYSIS_ID** and **ANALYSIS_RESULT_ID** combination. In practice, each call to this method should result in the deletion of many records from the table, each corresponding to a step in the waterfall chart from the given execution of a specific analysis
* **writeAnalysisResultWaterfall(df Dataframe)**: This function should write the pandas dataframe containing the steps for a given analysis waterfall into the **ANALYSIS_RESULT_WATERFALL** table. **df** will contain many rows of data that may be inserted in bulk, or as individual records, depending on the capabilities of the data warehouse. Each row of **df** will contain a complete record, even if some of the column values are <span style="text-decoration:underline;">NULL</span>
* **writeTrendResultSummary(vals List)**: This function should delete any existing data with the same **ANALYSIS_ID**, and **ANALYSIS_RESULT_ID**, then insert a record into the **TREND_RESULT_SUMMARY** table. The input list **vals** will contain, in order, the column values to be inserted into the table to form a complete record, even if a column value is <span style="text-decoration:underline;">NULL</span>. The first and second fields in **vals** correspond to the **ANALYSIS_ID** and **ANALYSIS_RESULT_ID** respectively, to facilitate deletion of existing records
* **writeTrendResultDetail(df Dataframe, vals List)**: This function should delete any existing data with the **ANALYSIS_ID** and **ANALYSIS_RESULT_ID** found as the first and second entry in the input list **vals**, and then insert the trend details in the pandas dataframe **df** into the **TREND_RESULT_DETAIL** table. Each row of **df** will contain a complete record, even if some of the column values are <span style="text-decoration:underline;">NULL</span>
* **getTCAnalysisResultIDs(ANALYSIS_ID Integer, RECENT_PERIOD_START String, RECENT_PERIOD_END String, PREVIOUS_PERIOD_START String, PREVIOUS_PERIOD_END String)**: This function will return a list of **ANALYSIS_RESULT_ID’s** that correspond to an analysis with the given ID and date ranges. This is to facilitate deletion of previous executions of a time comparison analysis with those date ranges to avoid having duplicate data in the database
* **getGCAnalysisResultIDs(ANALYSIS_ID Integer, GROUP_A_NAME String, GROUP_B_NAME String)**: This function will return a list of **ANALYSIS_RESULT_ID’s** that correspond to an analysis with the given ID and group names. This is to facilitate deletion of previous executions of a group comparison analysis with those group names to avoid having duplicate data in the database
* **getGPAnalysisResultIDs(self, ANALYSIS_ID Integer)**: This function will return a list of **ANALYSIS_RESULT_ID’s** that correspond to an analysis with the given ID. This is to facilitate deletion of previous executions of a general performance analysis to avoid having duplicate data in the database


### lambda_function.py

We provide a script called `lambda_function.py` that can immediately be used with an AWS Lambda Function to support workflow orchestration as outlined above in Step 3. This script may also be useful for customers wishing to integrate scheduled execution / load of Sisu segments into other workflows and tools; this script will work with AWS Lambda Functions directly, but also any other caller that makes execution calls with the same input Event format

This script defines a single function, `lambda_handler(event Dictionary, context Dictionary)`: The input **context** is not used by the function. The input **event** is used to pass execution requests to the `load_analysis_results.py` script for either a one-off execution of an analysis, or a historical execution

Each input event is a dictionary consisting of the following entries:



* **API_KEY** - String - <span style="text-decoration:underline;">Required</span>: A valid Sisu API Key for the customer organization where the analysis to be operated resides
* **ANALYSIS_ID** - Integer - <span style="text-decoration:underline;">Required</span>: A valid Trend Detection, General Performance, Group Comparison, or Time Comparison, analysis ID. NOTE: If **ACTION_TYPE** (below) is specified, the **ANALYSIS_ID** parameter <span style="text-decoration:underline;">MUST</span> correspond to a Time Comparison analysis
* **ACTION_TYPE** - String - <span style="text-decoration:underline;">Optional</span>: Specifying an **ACTION_TYPE** will kick off a historical load as outlined above. Must be one of:
    * **DOD**: Day Over Day execution
    * **WOW**: Week Over Week
    * **MOM**: Month Over Month
* **START_DATE** - String - <span style="text-decoration:underline;">Required iff **ACTION_TYPE** is specified**,** ignored otherwise</span>: The **START_DATE** must be either a String in the format of ‘YYYY-MM’DD’, or one of the following:
    * **YESTERDAY**: Sets the **START_DATE** to the current date - 1 day
    * **TODAY**: Sets the **START_DATE** to the current date
    * **LAST_WEEK**: Sets the **START_DATE** to the current date - 7 days
    * **THIS_WEEK**: Sets the **START_DATE** to the current date
    * **LAST_MONTH**: Sets the **START_DATE** to the current date - 1 month
* **END_DATE** - String - <span style="text-decoration:underline;">Optional iff **ACTION_TYPE** is specified, ignored otherwise</span>: The **END_DATE**, if specified, must be a String in the format of ‘YYYY-MM-DD’. If no **END_DATE** is specified, the **END_DATE** is set to the same value as the decoded **START_DATE**

If an **API_KEY** and **ANALYSIS_ID** are provided, a single call is made to `load_analysis_results.execute_load()`

If an **ACTION_TYPE** is specified, the **START_DATE** parameter is decoded, the **END_DATE** parameter is decoded, and a single call is made to `load_analysis_results.process_tc_action()`

If the calls above complete successfully, a response dictionary is returned with a **statusCode** of <span style="text-decoration:underline;">200</span>, and a JSON **body** indicating successful execution. Otherwise, exceptions raised by the script are thrown to the caller to indicate failure
