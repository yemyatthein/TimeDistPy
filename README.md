#TimeDistPy

TimeDistPy (Timely Distribution of Data in Python) allows you view the data that has an active period. An example would be a software outsourcing company that has many projects it developed, wants to see the time-oriented view of how much they make in a certain period. Assume the company has projects data as follows in some data store.

## Input data

PROJECT_NAME | START_DATE | END_DATE | PROJECT_PROFIT
-------------|------------|----------|---------------
project1     |2012-02-3   |2013-01-05|20500
project2     |2012-02-6   |2012-04-21|45000
project3     |2012-02-4   |2013-02-12|32000
project4     |2012-10-12  |2013-05-7 |98000
    
Using the above data, TimeDistPy distributes data to lowest time granularity and calculates aggregation types for each time instance. Currently, the smallest time granularity is "Daily" and available aggregation types are SUM, AVG, MIN, MAX and COUNT.  

##Data Distribution

First thing it does after receiving input data is distributing the projects according to time axes. Result of this step is shown below. Each project's profit value is divided by the number of active date of the project. For example, project2 is active from 6th Feb, 2012 to 21st Apr, 2012, i.e. 75 days. So each date in that period will have value (45000/75) for the project2. In the table below, because on 3rd Feb, 2012 project2 is not active its value for that row is put 0.

DATE       |PROJECT1 |PROJECT2 |PROJECT3 |PROJECT4 
-----------|---------|---------|---------|---------
2012-02-3  |1000     |0        |0        |0
2012-02-4  |1000     |0        |300      |0
2012-02-5  |1000     |0        |300      |0
2012-02-6  |1000     |500      |300      |0
    .      |         |         |         |
    .      |         |         |         |
    .      |         |         |         |

##Aggregation Calculation

Once the distribution is in place, predefined set of aggregations are calculated for each row/Date. The values are then stored as member variables of RowData object. Data can be visualized as follows.

DATE      | AGGREGATION_RESULT
----------|----------------------------------------
2012-02-3 |RowData(SUM=xxxx, AVG=xxx, MIN=xxx, ...)
2012-02-4 |RowData(SUM=xxxx, AVG=xxx, MIN=xxx, ...)
2012-02-5 |RowData(SUM=xxxx, AVG=xxx, MIN=xxx, ...)
.         |...
.         |...
.         |...

##Query Data

After these two steps are performed, we can query the aggregations results using start and end date. For example, we can query

* Give result of AVG on date "10th Apr, 2013".
* Give results of SUM between "10th May, 2012" and "20th Jun, 2013"

See the example.py for usage in code.
