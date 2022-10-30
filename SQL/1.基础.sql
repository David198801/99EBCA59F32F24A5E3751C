-- mysql -u root -p

CREATE DATABASE 数据库名;
drop database 数据库名;
use 数据库名;


-- 创建表
CREATE TABLE table_name (column_name column_type);
--   EG
CREATE TABLE IF NOT EXISTS `runoob_tbl`(
   `runoob_id` INT UNSIGNED AUTO_INCREMENT,
   `runoob_title` VARCHAR(100) NOT NULL,
   `runoob_author` VARCHAR(40) NOT NULL,
   `submission_date` DATE,
   PRIMARY KEY ( `runoob_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 删除表
DROP TABLE table_name ;


-- 插入行
INSERT INTO table_name ( field1, field2,...fieldN )
                       VALUES
                       ( value1, value2,...valueN );
-- 插入多行
INSERT INTO table_name ( field1, field2,...fieldN )
                       VALUES
                       ( value1, value2,...valueN ),( value1, value2,...valueN )...;


             
                       
-- 查询数据
select * from runoob_tbl;
SELECT column_name,column_name FROM table_name;

-- DISTINCT 非重复值
SELECT DISTINCT column_name,column_name FROM table_name;

-- WHERE 指定条件
SELECT column_name,column_name
FROM table_name
[WHERE] column_name operator value;
 -- LIMIT行数 OFFSET偏移量 OFFSET必须和limit共用 limit 1 offset 2 可以写成limit 2,1
[LIMIT N][ OFFSET M]
--   EG
SELECT * FROM Websites WHERE country='CN';
SELECT * FROM Websites WHERE id=1;
/*
WHERE 可用运算符
=	等于
<>	不等于
>	大于
<	小于
>=	大于等于
<=	小于等于
BETWEEN	在某个范围内
LIKE	搜索某种模式
*/

-- AND & OR 逻辑运算
SELECT * FROM Websites
WHERE country='CN'
AND alexa > 50;

-- ORDER BY 排序
SELECT column_name,column_name
FROM table_name
ORDER BY column_name,column_name [ASC|DESC]; -- asc升序 desc降序



-- UPDATE 更新行
UPDATE table_name
SET column1=value1,column2=value2,...
WHERE some_column=some_value;  -- 如果您省略了 WHERE 子句，所有的记录都将被更新！


-- DELETE 删除行
DELETE FROM table_name
WHERE some_column=some_value;
