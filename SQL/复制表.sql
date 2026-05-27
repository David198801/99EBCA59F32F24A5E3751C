-- 新表不存在
create table new_table
AS
select * from old_talbe;
/*这种方法会将old_table中所有的内容都拷贝过来,用这种方法需要注意,
new_table中没有了old_table中的primary key,Extra,auto_increment等属性,
需要自己手动加,具体参看后面的修改表即字段属性

在开启gtid情况下，会报语法错误
*/

create table tbl_test_bak like tbl_test; 
insert into tbl_test_bak select * from tbl_test;
/*
reate table tbl_test_bak like不拷贝数据，只创建一模一样的表结构，包括索引约束等，
结合insert into语句可以实现复制一个表的结构和数据的目的
*/

-- mysql不支持
-- 不复制表结构
SELECT column_name(s)
INTO newtable [IN externaldb]
FROM table1;



-- 新表存在
-- 复制旧表数据到新表(假设两个表结构一样)
insert into new_table
select * from old_table;
复制旧表数据到新表(假设两个表结构不一样)
insert into new_table(field1,field2,.....)
select field1,field2,field3 from old_table;
-- 复制全部数据
select * into new_table from old_table;
-- 只复制表结构到新表
select * into new_talble from old_table where 1=2;