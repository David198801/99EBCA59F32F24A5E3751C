-- 从不同的表复制

insert into 表1 select * from 表2 where id =1
 

-- 同一张表中复制（无主键）

insert into 表1 select * from 表2 where id =1
 

-- 同一张表中复制（有主键）

insert into 表1(字段1,字段2,字段3) select 字段1,字段2,字段3 from 表1 where id=1