# encoding: utf-8

from DataFecth.DataFetcher import FetcherDataFromUrl
import pandas as pd
import io

url = 'http://quotes.money.163.com/service/zycwzb_600779.html'

fdf = FetcherDataFromUrl()
c = fdf.download(url)
df = pd.read_csv(io.StringIO(c.content.decode('gb18030')))
print(df.T)
