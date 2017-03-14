# encoding: utf-8
from DataFecth.DataFetcher import FetcherDataFromUrl
import pandas as pd
import io
from pypinyin import lazy_pinyin


class WYData(object):
    def __init__(self):
        self.reporttype = {
            # 利润表
            'lrb': {'url': 'http://quotes.money.163.com/service/lrb_%s.html'},
            # 主要财务指标
            'zycwzb': {'url': 'http://quotes.money.163.com/service/zycwzb_%s.html'},
            # 资产负债表
            'zcfzb': {'url': 'http://quotes.money.163.com/service/zcfzb_%s.html'},
            # 财务报表摘要
            'cwbbzy': {'url': 'http://quotes.money.163.com/service/cwbbzy_%s.html'},
            # 盈利能力
            'ylnl': {'url': 'http://quotes.money.163.com/service/zycwzb_%s.html?part=ylnl'},
            # 偿还能力
            'chnl': {'url': 'http://quotes.money.163.com/service/zycwzb_%s.html?part=chnl'},
            # 成长能力
            'cznl': {'url': 'http://quotes.money.163.com/service/zycwzb_%s.html?part=cznl'},
            # 营运能力
            'yynl': {'url': 'http://quotes.money.163.com/service/zycwzb_%s.html?part=yynl'},
            # 现金流量表
            'xjllb': {'url': 'http://quotes.money.163.com/service/xjllb_%s.html'}
        }

        self.fdf = FetcherDataFromUrl()

    def get_report_type(self, code, rpt_type):
        rpt_type_url = self.reporttype.get(rpt_type, None)
        assert rpt_type_url, 'Input Report Type : [%s]  NOT FOUND !' % rpt_type
        c = self.fdf.download(rpt_type_url['url'] % code)
        df = pd.read_csv(io.StringIO(c.content.decode('gb18030')))
        # df['type_name'] = df[df.columns[0]].apply(lambda x: '_'.join(lazy_pinyin(x)))
        df['type_name'] = df[df.columns[0]]
        df.drop(df.columns[0], axis=1, inplace=True)
        df = df.convert_objects(convert_numeric=True)
        return df[df.columns[~df.columns.str.contains('Unnamed')]].set_index('type_name').T
