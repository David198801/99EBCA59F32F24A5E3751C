/* MySQL UNION 操作符用于连接两个以上的 SELECT 语句的结果组合到一个结果集合中。*/

SELECT expression1, expression2, ... expression_n
FROM tables
[WHERE conditions]
UNION [ALL | DISTINCT]
SELECT expression1, expression2, ... expression_n
FROM tables
[WHERE conditions];
