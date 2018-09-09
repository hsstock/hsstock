delete from ft_history_kline  where code = 'US.BIOA' in ('US.IRDM','US.EBF','US.BBSI','US.RLH','US.CSGP','US.TGS')
delete from ft_history_kline_K_5M where code = 'US.BIOA' in ('US.IRDM','US.EBF','US.BBSI','US.RLH','US.CSGP','US.TGS')

show variables LIKE 'AUTOCOMMIT'
show table status like 'ft_history_kline'
show global status
SHOW session status like 'Handler%'
SHOW session status like 'Sort%'
SHOW session status like 'Created%'
show profiles
 alter table ft_history_kline_1 engine=myisam;
select count(*) from ft_history_kline_K_5M_1
alter table ft_history_kline_2 engine=myisam;
alter table ft_history_kline_3 engine=myisam;
alter table ft_history_kline_4 engine=myisam;

alter table ft_history_kline_K_5M_1 engine=myisam;
alter table ft_history_kline_K_5M_2 engine=myisam;
alter table ft_history_kline_K_5M_3 engine=myisam;
alter table ft_history_kline_K_5M_4 engine=myisam;
#Error : Lost connection to MySQL server during query

show global variables like '%timeout%';
set global net_read_timeout = 190;
set global net_write_timeout = 900;
#Error : Access denied; you need (at least one of) the SUPER or SYSTEM_VARIABLES_ADMIN privilege(s) for this operation
mysql -u root -p
B123!@#


select count( * ) from ft_history_kline_10  group by code

SELECT COUNT(*)  FROM (SELECT DISTINCT(code) FROM ft_history_kline_10 ) as a


SELECT  DISTINCT(code) FROM ft_history_kline_10
SELECT  DISTINCT(code) FROM sys_sharding

select count(*) from ft_history_kline_K_5M_11  where code = 'SH.519956'

delete from ft_history_kline_11
delete from ft_history_kline_K_5M_11

delete from ft_history_kline where time_key > '2018-07-18'
delete from ft_history_kline_K_5M where time_key > '2018-07-18'

INSERT INTO sys_sharding (code, dtype,tindex)
SELECT code, 'hk' as dtype, 1 as tindex from (SELECT DISTINCT(code) FROM ft_history_kline_1) as tmp1

INSERT INTO sys_sharding (code, dtype,tindex)
SELECT code, 'hk' as dtype, 2 as tindex from (SELECT DISTINCT(code) FROM ft_history_kline_2) as tmp1

INSERT INTO sys_sharding (code, dtype,tindex)
SELECT code, 'hk' as dtype, 3 as tindex from (SELECT DISTINCT(code) FROM ft_history_kline_3) as tmp1

INSERT INTO sys_sharding (code, dtype,tindex)
SELECT code, 'hk' as dtype, 4 as tindex from (SELECT DISTINCT(code) FROM ft_history_kline_4) as tmp1

INSERT INTO sys_sharding (code, dtype,tindex)
SELECT code, 'hk' as dtype, 5 as tindex from (SELECT DISTINCT(code) FROM ft_history_kline_5) as tmp1

INSERT INTO sys_sharding (code, dtype,tindex)
SELECT code, 'hk' as dtype, 6 as tindex from (SELECT DISTINCT(code) FROM ft_history_kline_6) as tmp1

INSERT INTO sys_sharding (code, dtype,tindex)
SELECT code, 'hk' as dtype, 7 as tindex from (SELECT DISTINCT(code) FROM ft_history_kline_7) as tmp1

INSERT INTO sys_sharding (code, dtype,tindex)
SELECT code, 'hk' as dtype, 8 as tindex from (SELECT DISTINCT(code) FROM ft_history_kline_8) as tmp1

INSERT INTO sys_sharding (code, dtype,tindex)
SELECT code, 'hk' as dtype, 9 as tindex from (SELECT DISTINCT(code) FROM ft_history_kline_9) as tmp1

INSERT INTO sys_sharding (code, dtype,tindex)
SELECT code, 'hk' as dtype, 10 as tindex from (SELECT DISTINCT(code) FROM ft_history_kline_10) as tmp1

select max(tindex) from sys_sharding group by tindex
select * from sys_sharding where dtype='hk_5m'

INSERT INTO sys_sharding (code, dtype,tindex)
SELECT code, 'hk_5m' as dtype, 10 as tindex from (SELECT DISTINCT(code) FROM ft_history_kline_10) as tmp1

INSERT INTO sys_sharding (code, dtype,tindex)
SELECT code, 'hk_5m' as dtype, 9 as tindex from (SELECT DISTINCT(code) FROM ft_history_kline_9) as tmp1

INSERT INTO sys_sharding (code, dtype,tindex)
SELECT code, 'hk_5m' as dtype, 8 as tindex from (SELECT DISTINCT(code) FROM ft_history_kline_8) as tmp1

INSERT INTO sys_sharding (code, dtype,tindex)
SELECT code, 'hk_5m' as dtype, 7 as tindex from (SELECT DISTINCT(code) FROM ft_history_kline_7) as tmp1

INSERT INTO sys_sharding (code, dtype,tindex)
SELECT code, 'hk_5m' as dtype, 6 as tindex from (SELECT DISTINCT(code) FROM ft_history_kline_6) as tmp1

INSERT INTO sys_sharding (code, dtype,tindex)
SELECT code, 'hk_5m' as dtype, 5 as tindex from (SELECT DISTINCT(code) FROM ft_history_kline_5) as tmp1

INSERT INTO sys_sharding (code, dtype,tindex)
SELECT code, 'hk_5m' as dtype, 4 as tindex from (SELECT DISTINCT(code) FROM ft_history_kline_4) as tmp1

INSERT INTO sys_sharding (code, dtype,tindex)
SELECT code, 'hk_5m' as dtype, 3 as tindex from (SELECT DISTINCT(code) FROM ft_history_kline_3) as tmp1

INSERT INTO sys_sharding (code, dtype,tindex)
SELECT code, 'hk_5m' as dtype, 2 as tindex from (SELECT DISTINCT(code) FROM ft_history_kline_2) as tmp1

INSERT INTO sys_sharding (code, dtype,tindex)
SELECT code, 'hk_5m' as dtype, 1 as tindex from (SELECT DISTINCT(code) FROM ft_history_kline_1) as tmp1
select count(*) from ft_history_kline
select max(time_key) from ft_history_kline  where code = 'HK.04231' order by  time_key desc limit 10


delete from sys_sharding where id in
(
		select * from
		(
			select id from sys_sharding   where code in
			(
				select code from
					(select code,dtype,tindex from sys_sharding  group by code,dtype,tindex having count(code)>1 and count(dtype)>1 and count(tindex)>1)
				as tmp1
			)
			and id in
			(
				select max(id) from sys_sharding  group by code,dtype,tindex having count(code)>1 and count(dtype)>1 and count(tindex)>1 order by max(id) asc
			)
		)	tmp2
)

select max(time_key) from ft_history_kline group by code having count(code)> 1 order by max(time_key) DESC limit 10




delete from ft_history_kline_1 where id in
(
		select * from
		(
			select id from ft_history_kline_1   where code in
			(
				select code from
					(select code,time_key from ft_history_kline_1 group by code,time_key having count(code)>1 and count(time_key)>1)
				as tmp1
			)
			and id in
			(
				select max(id) from ft_history_kline_1  group by code,time_key having count(code)>1 and count(time_key)>1 order by max(id) asc
			)
		)	tmp2
)


show processlist

SELECT ft_history_kline.time_key AS ft_history_kline_time_key
FROM ft_history_kline
WHERE ft_histo


set profiling=on;
show profiles
show profile for query query_id查看详细信息

show table status

select count(*) from sys_sharding

select code from sys_sharding where code  in (select DISTINCT(code) from ft_history_kline_K_5M_11 as tmp1)

select count(code) from ft_stock_basicinfo where code not in
	(select DISTINCT(code) from ft_history_kline_K_5M_11 as tmp1)
	and code not in
	(select DISTINCT(code) from ft_history_kline_11 as tmp2)
	and code not in
	(select DISTINCT(code) from sys_sharding as tmp3)

Lost connection to MySQL server during query



explain
SELECT count(ft_history_kline.time_key)
FROM ft_history_kline
WHERE  code= 'US.BEN' limit



show status
show variables like '%query%'


select min(time_key) from ft_history_kline order by time_key


#没有历史数据的stock表
insert into  ft_stock_basicinfo_now_nohistdata select * from  ft_stock_basicinfo
	where code not in
	(select DISTINCT(code) from ft_history_kline_K_5M_11 as tmp1)
	and code not in
	(select DISTINCT(code) from ft_history_kline_11 as tmp2)
	and code not in
	(select DISTINCT(code) from sys_sharding as tmp3)

# 表拆分
select count(*) from ft_history_kline_K_5M_10 '32660808'
select min(id) from ft_history_kline_K_5M_10 1
select max(id) from ft_history_kline_K_5M_10 '32780514'
guess id 32780514/2  16390257
seperated id > 16394310 US.PACE
select * from ft_history_kline_K_5M_10 where id > 16394257 limit 1000
insert into ft_history_kline_K_5M_10_copy select * from ft_history_kline_K_5M_10 where id > 16394310

select count(*) from ft_history_kline_K_5M_10_copy '16311840'
select count(*) from ft_history_kline_K_5M_10 where id <= 16394310  16348968
select count(*) from ft_history_kline_K_5M_10 where id <= 16394310 '16348968'
select * from ft_history_kline_K_5M_10 where id > 16394310 limit 10
delete from ft_history_kline_K_5M_10 where id > 16394310

use hsstock;

SELECT DISTINCT(id) FROM ft_history_kline_K_5M_10 group by id having count(id)>1

update sys_sharding set tindex = 16  where  dtype = 'hk_5m' and code in
(
		select code from
		(
			SELECT DISTINCT(code) FROM ft_history_kline_K_5M_16 as tmp1
		)	tmp2
)

select * from sys_sharding where code = 'US.PACE'

# Lost  connection to mysql server during query



order by last_price



# LESS 5 DOLLOARS

insert into  ft_stock_basicinfo_less5 select * from  ft_stock_basicinfo
	where code in
	(
		select code from
			(select DISTINCT(code),last_price from ft_market_snapshot where last_price <5 and code like '%US.%' order by last_price desc)
			as tmp1
	)


select * from ft_stat_week_probability where up_probability<>1 and up_probability<> 0 and week_of_day = 3 and up_count > 50 order by up_probability desc




select * from ft_stat_week_probability where week_of_day = 3  and code in
  (
select code from ft_stock_basicinfo as tmp1 where stock_type='STOCK' and code in
	(
	select code from ft_stat_week_probability as tmp2 where up_probability<>1 and up_probability<> 0 and up_count > 50 and week_of_day = 3 and  (up_probability/down_probability)>1.5  and code like '%SH.%' or code like '%SZ.%' order by up_probability desc
    )
)


select * from ft_history_kline where (change_rate > 9.8 or change_rate < -9.8)  and open <> 0 and last_close > 0


insert LOW_PRIORITY into  ft_history_kline_more98(code,time_key,open,close,high,low,pe_ratio,turnover_rate,
		volume,turnover,change_rate,last_close) select code,
																										time_key,
																										open,
																										close,
																										high,
																										low,
																										pe_ratio,
																										turnover_rate,
																										volume,
																										turnover,
																										change_rate,
																										last_close
																						 from ft_history_kline
																						 				where abs(change_rate) > 9.8 and open > 0 and close > 0 and high > 0 and low > 0







select DISTINCT(stock_type) from ft_stock_basicinfo
stock_type
BOND,ETF,IDX, STOCK,WARRANT
1127(HK),4060(SZ,SH,US,HK),941(SZ,SH,US,HK) ,13929,11861
select * from ft_stock_basicinfo where stock_type ='BOND'
select * from ft_stock_basicinfo where stock_type ='ETF'
select * from ft_stock_basicinfo where stock_type ='IDX'
select * from ft_stock_basicinfo where stock_type ='WARRANT'
select * from ft_stock_basicinfo where stock_type ='STOCK'es

