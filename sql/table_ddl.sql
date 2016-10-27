-- 建库
CREATE schema investment;

-- 创建网易财报数据表
DROP TABLE IF EXISTS investment.t_163_data;
CREATE TABLE investment.t_163_data (
  symbol     VARCHAR(11) DEFAULT NULL,
  date       DATE DEFAULT NULL,
  item_key   INT DEFAULT NULL,
  item_value FLOAT DEFAULT NULL,
  primary key(symbol,date,item_key)
);

COMMENT ON TABLE investment.t_163_data IS '网易财报数据表';
COMMENT on column investment.t_163_data.symbol is '股票代码';
COMMENT on column investment.t_163_data.date is '报表日期';
COMMENT on column investment.t_163_data.item_key is '条目类型';
COMMENT on column investment.t_163_data.item_value is '条目值';

-- 创建网易财报类目表
DROP TABLE IF EXISTS investment.t_163_item;
CREATE TABLE investment.t_163_item (
  id      SERIAL PRIMARY KEY ,
  group_id     VARCHAR(100) DEFAULT NULL,
  group_name      VARCHAR(100) DEFAULT NULL,
  parents   INT DEFAULT NULL,
  show_code INT DEFAULT '0'
);
COMMENT ON TABLE  investment.t_163_item IS '网易财报类目表';
COMMENT on column investment.t_163_item.group_name is '组';
COMMENT on column investment.t_163_item.group_name is '条目名字';
COMMENT on column investment.t_163_item.show_code is '展示开关';


-- 创建K线数据表
DROP TABLE IF EXISTS investment.t_k_line;
CREATE TABLE investment.t_k_line (
  symbol   VARCHAR(20) NOT NULL DEFAULT '',
  date     DATE        NOT NULL DEFAULT '1970-01-01',
  open     FLOAT DEFAULT NULL,
  close    FLOAT DEFAULT NULL,
  high     FLOAT DEFAULT NULL,
  low      FLOAT DEFAULT NULL,
  chg      FLOAT DEFAULT NULL,
  percent  FLOAT DEFAULT NULL,
  turnrate FLOAT DEFAULT NULL,
  ma5      FLOAT DEFAULT NULL,
  ma10     FLOAT DEFAULT NULL,
  ma20     FLOAT DEFAULT NULL,
  ma30     FLOAT DEFAULT NULL,
  PRIMARY KEY (symbol, date)
);


COMMENT on column investment.t_k_line.symbol is '股票代码';
COMMENT on column investment.t_k_line.date is '日期';
COMMENT on column investment.t_k_line.open is '开盘价';
COMMENT on column investment.t_k_line.close is '收盘价';
COMMENT on column investment.t_k_line.high is '最高价';
COMMENT on column investment.t_k_line.low is '最低价';
COMMENT on column investment.t_k_line.chg is '涨跌价格';
COMMENT on column investment.t_k_line.percent is '涨跌率';
COMMENT on column investment.t_k_line.turnrate is '换手率';
COMMENT on column investment.t_k_line.ma5 is '5日均价';
COMMENT on column investment.t_k_line.ma10 is '10日均价';
COMMENT on column investment.t_k_line.ma20 is '20日均价';
COMMENT on column investment.t_k_line.ma30 is '30日均价';

-- 创建股票代码对应表
DROP TABLE IF EXISTS investment.t_stock;
CREATE TABLE investment.t_stock (
  symbol   VARCHAR(11) NOT NULL DEFAULT '',
  name     VARCHAR(11) DEFAULT NULL,
  optional int  NOT NULL,
  PRIMARY KEY (symbol)
);
