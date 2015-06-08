-- 商家和菜品结构定义
create table dealer (id serial primary key, name varchar(100) not null, address varchar(500) not null, logo varchar(200), status int default 1 check  (status in (1, 2)), min_price  float, service_price float default 0);

create table products(id serial primary key, dealer varchar(50), name varchar(50), price float, logo varchar(200), orders_per_month int default 0, tag varchar(200),  describe varchar(500));
