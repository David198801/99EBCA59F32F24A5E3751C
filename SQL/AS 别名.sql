/*
通过使用 SQL，可以为表名称或列名称指定别名。

基本上，创建别名是为了让列名称的可读性更强。

AS 可以省略
*/

-- 列的 SQL 别名语法
SELECT column_name AS alias_name
FROM table_name;
-- eg
SELECT name, CONCAT(url, ', ', alexa, ', ', country) AS site_info
FROM Websites;



-- 表的 SQL 别名语法
SELECT column_name(s)
FROM table_name AS alias_name;
-- eg
SELECT w.name, w.url, a.count, a.date
FROM Websites AS w, access_log AS a
WHERE a.site_id=w.id and w.name="菜鸟教程";
