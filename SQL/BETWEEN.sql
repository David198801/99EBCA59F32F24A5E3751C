-- BETWEEN 操作符选取介于两个值之间的数据范围内的值。这些值可以是数值、文本或者日期。


SELECT column_name(s)
FROM table_name
WHERE column_name BETWEEN value1 AND value2;


-- eg
SELECT * FROM Websites
WHERE alexa BETWEEN 1 AND 20; -- 显示alexa为1-20的值

SELECT * FROM Websites
WHERE alexa NOT BETWEEN 1 AND 20;  -- 取反

-- 下面的 SQL 语句选取 alexa 介于 1 和 20 之间但 country 不为 USA 和 IND 的所有网站：
SELECT * FROM Websites
WHERE (alexa BETWEEN 1 AND 20)
AND country NOT IN ('USA', 'IND');

select * from runoob_tbl where (runoob_id not between 2 and 3) and not runoob_id=4 ;

-- 下面的 SQL 语句选取 name 以介于 'A' 和 'H' 之间字母开始的所有网站：
SELECT * FROM Websites
WHERE name BETWEEN 'A' AND 'H';

-- 下面的 SQL 语句选取 date 介于 '2016-05-10' 和 '2016-05-14' 之间的所有访问记录：
SELECT * FROM access_log
WHERE date BETWEEN '2016-05-10' AND '2016-05-14';
