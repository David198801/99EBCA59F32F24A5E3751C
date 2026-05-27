-- join 用于把来自两个或多个表的行结合起来
-- JOIN 排列组合
-- ！SELECT * 会显示两张表，用SELECT table.col显示所需列

-- INNER JOIN 关键字在表中存在至少一个匹配时返回行。
-- JOIN = INNER JOIN
SELECT column_name(s)
FROM table1 INNER JOIN table2
ON table1.column_name=table2.column_name;

/*
LEFT JOIN 关键字从左表（table1）返回所有的行，即使右表（table2）中没有匹配。
如果右表中没有匹配，则结果为 NULL。

LEFT JOIN = LEFT OUTER JOIN
*/
SELECT column_name(s)
FROM table1 LEFT JOIN table2
ON table1.column_name=table2.column_name;
-- RIGHT JOIN 与LEFT相反

/*
FULL OUTER JOIN 关键字只要左表（table1）和右表（table2）其中一个表中存在匹配，则返回行.
FULL OUTER JOIN 关键字结合了 LEFT JOIN 和 RIGHT JOIN 的结果。
*/
SELECT column_name(s)
FROM table1 FULL OUTER JOIN table2
ON table1.column_name=table2.column_name;
-- mysql中没有FULL OUTER JOIN，用left+right union代替
SELECT *
FROM a1 LEFT JOIN a2
ON a1.interger=a2.interger
UNION
SELECT *
FROM a1 RIGHT JOIN a2
ON a1.interger=a2.interger;

-- 集合减法 A-B 取left join B值为null的
SELECT *
FROM a1 LEFT JOIN a2
ON a1.interger=a2.interger
WHERE a2.interger IS NULL;

