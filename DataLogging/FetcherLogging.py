# -*- encoding:utf-8 -*-
import logging
import logging.config


class DataLogging(object):
    def __init__(self):
        logging.basicConfig(
            level=logging.WARNING,
            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
            datefmt='%a, %d %b %Y %H:%M:%S',
        )

        # create logger
        logger_name = "DataFetcher"
        self.logger = logging.getLogger(logger_name)

    def logs(self, log_type=1):
        logs_level = {
            0: self.logger.debug,
            1: self.logger.info,
            2: self.logger.warn,
            3: self.logger.error,
            4: self.logger.critical
        }
        return logs_level.get(log_type)

if __name__ == '__main__':
    dl = DataLogging()
    dl.logs(1)('test1')

