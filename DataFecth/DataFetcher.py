# encoding: utf-8
import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from DataLogging.FetcherLogging import DataLogging
DataLog = DataLogging()


class FetcherDataFromUrl(object):
    def __init__(self):
        self.dl = DataLogging()
        self.msg = " Start Fetch Data From URL : "
        self.s = requests.Session()
        retries = Retry(total=5,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])

        self.s.mount('http://', HTTPAdapter(max_retries=retries))
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
                          'Safari/537.36'}

    def download(self, url, stream=False):
        DataLog.logs()(self.msg + url)
        r = self.s.get(url, stream=stream, timeout=5, headers=self.headers)
        #r.encoding = 'utf-8'
        return r


if __name__ == '__main__':
    fdf = FetcherDataFromUrl()
    content = fdf.download('http://quotes.money.163.com/service/zycwzb_600779.html')
    print(content.content)
