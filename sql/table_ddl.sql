-- 建库
CREATE schema investment;

-- 创建网易财报数据表
DROP TABLE IF EXISTS investment.t_163_data;
CREATE TABLE investment.t_163_data (
  symbol     VARCHAR(11) DEFAULT NULL,
  date       DATE DEFAULT NULL,
  item_key   INT DEFAULT NULL,
  item_value FLOAT DEFAULT NULL,
  primary key(symbol,date)
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
DROP TABLE IF EXISTS t_k_line;
CREATE TABLE t_k_line (
  symbol   VARCHAR(20) NOT NULL DEFAULT ''
  COMMENT '股票代码',
  date     DATE        NOT NULL DEFAULT '0000-00-00'
  COMMENT '日期',
  open     FLOAT DEFAULT NULL
  COMMENT '开盘价',
  close    FLOAT DEFAULT NULL
  COMMENT '收盘价',
  high     FLOAT DEFAULT NULL
  COMMENT '最高价',
  low      FLOAT DEFAULT NULL
  COMMENT '最低价',
  chg      FLOAT DEFAULT NULL
  COMMENT '涨跌价格',
  percent  FLOAT DEFAULT NULL
  COMMENT '涨跌率',
  turnrate FLOAT DEFAULT NULL
  COMMENT '换手率',
  ma5      FLOAT DEFAULT NULL
  COMMENT '5日均价',
  ma10     FLOAT DEFAULT NULL
  COMMENT '10日均价',
  ma20     FLOAT DEFAULT NULL
  COMMENT '20日均价',
  ma30     FLOAT DEFAULT NULL
  COMMENT '30日均价',
  PRIMARY KEY (symbol, date)
);

-- 创建股票代码对应表
DROP TABLE IF EXISTS t_stock;
CREATE TABLE t_stock (
  symbol   VARCHAR(11) NOT NULL DEFAULT '',
  name     VARCHAR(11) DEFAULT NULL,
  optional TINYINT(2)  NOT NULL,
  PRIMARY KEY (symbol)
);
