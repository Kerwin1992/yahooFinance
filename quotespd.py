# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib.finance import quotes_historical_yahoo_ochl
from datetime import date
from datetime import datetime
import pandas as pd

# import numpy
# import scipy.stats



def _wxdate2pydate(date):
    import datetime
    if date.IsValid():
        ymd = map(int, date.FormatISODate().split('-'))
        return datetime.date(*ymd)
    else:
        return None

#code：公司代码；start, end：起止时间；list:所需要显示的指标
def PlotData(code, start, end, list):
    start_date = _wxdate2pydate(start)
    end_date = _wxdate2pydate(end)
    print code
    print start_date
    print end_date
    print list
    #根据公司代码，起止时间得到所有数据
    quotes = quotes_historical_yahoo_ochl(code, start_date, end_date)
    fields = ['date', 'open', 'close', 'high', 'low', 'volume']
    list1 = []
    #格式化时间，将时间参数放入list1列表
    for i in range(0, len(quotes)):
        x = date.fromordinal(int(quotes[i][0]))
        y = datetime.strftime(x, '%Y-%m-%d')
        list1.append(y)
    print list1
    #根据数据，时间列表，所有指标生成dataFrame
    quotesdf = pd.DataFrame(quotes, index=list1, columns=fields)
    #剔除date数据，这里是因为格式不一致
    quotesdf = quotesdf.drop(['date'], axis=1)
    quotesdftemp = pd.DataFrame()
    #将所选择的指标，如close,open的dateFrame赋予一个临时dateFrame中
    for i in range(0, len(list)):
        quotesdftemp[list[i]] = quotesdf[list[i]]
    print quotesdftemp
    print "ready to plot"
    #画图
    quotesdftemp.plot(marker='o')
    plt.show()
