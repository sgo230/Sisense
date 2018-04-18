This Python script reviews all the distinct relationships between tables in the ElastiCube Manager and checks the uniqueness of the two keys.

It automates the process of checking the relationships using this syntax from https://documentation.sisense.com/many-many-relationships/:

SELECT 
  [Do I have duplications?]
FROM (
  SELECT 
    distinct_count(t1.col1)<>count(t1.col1) AS [Do I have duplications?]
  FROM 
    [Table1] t1
    
  UNION ALL
  
  SELECT 
    distinct_count(t2.col2)<>count(t2.col2)
  FROM 
    [Table2] t2) AS temp
GROUP BY 
  [Do I have duplications?]
  
Expected output: List of table relationships that are not unique on both sides:

[{'M2M': True,
  'sourceField': 'EmployeeID',
  'sourceTable': 'dbo.EmployeeTerritories',
  'targetField': 'EmployeeID',
  'targetTable': 'dbo.Orders'}]
  
Note: Because of some slow Sisense API endpoints, script will take about 15 seconds to run per table.

Tested in Sisense 7.1 and Python 3.7
