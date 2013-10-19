import pandas as pd
from datetime import datetime, timedelta
import sys

SUM = 'summation'
AVG = 'average'
MAX = 'maximum'
MIN = 'minimum'
COUNT = 'count'

class TimelyView(object):
    """
    Timely distribution of data value
    """
    def __init__(self):
        self.pdtable = None
        self.datalines = []
        self.min_date = None
        self.max_date = None
    
    def set_input_directly(self, ls):
        self.datalines = ls
        for x in ls:
            start = x[1]
            end = x[2]
            self._compare_start_end(start, end)
            
    def _compare_start_end(self, start, end):
        if not self.min_date or start < self.min_date:
            self.min_date = start
        if not self.max_date or end > self.max_date:
            self.max_date = end
            
    def _distribute_data(self):
        ls = self.datalines
        num_rows = (self.max_date - self.min_date).days + 1
        dindex = pd.date_range(self.min_date, self.max_date, freq='D')
        cols = [x[0] for x in ls]
        self.pdtable = pd.DataFrame([[0. for _ in xrange(len(ls))] for x in xrange(num_rows)], index=dindex, columns=cols)

        for i, x in enumerate(ls):
            num_slots = (x[2] - x[1]).days + 1
            value_share = x[3] / num_slots
            for j in xrange(num_slots):
                self.pdtable.ix[x[1] + timedelta(j)][cols[i]] = value_share
        
    def _calculate_aggregations(self):
        df = self.pdtable
        
        def get_sum(ls):
            return sum(ls)
        def get_avg(ls):
            non_zeros = [x for x in ls if x > 0]
            return sum(ls) / len(non_zeros)
        def get_max(ls):
            mx_val = -(sys.maxint)
            mx_item_index = 0
            for i, x in enumerate(ls):
                if x > mx_val:
                    mx_val = x
                    mx_item_index = i
            return mx_item_index, mx_val
        def get_min(ls):
            mn_val = sys.maxint
            mn_item_index = 0
            for i, x in enumerate(ls):
                if x < mn_val and x > 0:
                    mn_val = x
                    mn_item_index = i
            return mn_item_index, mn_val
        def get_count(ls):
            return len([x for x in ls if x > 0])
        
        self.pdresult = pd.DataFrame([None for _ in xrange(len(df))], index=df.index)
        for i in xrange(len(df)):
            rowlist = df.ix[i].tolist()

            summation = get_sum(rowlist)
            average = get_avg(rowlist)
            mxindex, maximum = get_max(rowlist)
            mnindex, minimum = get_min(rowlist)
            count = get_count(rowlist)

            self.pdresult.ix[i] = RowData(summation, average, maximum, minimum, count)
        return self.pdresult
            
    def set_input_from_file(self, filename):
        with open(filename, 'rb') as f:
            for i, x in enumerate(f):
                if i > 10000:
                    break
                parts = x.split(',')
                start = datetime.strptime(parts[1], '%Y-%m-%d')
                end = datetime.strptime(parts[2], '%Y-%m-%d')
                val = float(parts[3])
                row = (parts[0], start, end, val)
                self.datalines.append(row)
                self._compare_start_end(start, end)
        
    def distribute_and_aggregate(self):
        self._distribute_data()
        self._calculate_aggregations()
        
    def aggregation_between(self, start, end, agg_type):
        to_get = (end - start).days + 1
        sindex = (start - self.min_date).days
        eindex = sindex + to_get
        rows = self.pdresult.ix[sindex:eindex]
        agg_data = []
        dates = []
        for i in xrange(len(rows)):
            row = rows.ix[i][0]
            agg_data.append(getattr(row, agg_type))
            dates.append(rows.ix[i].name.date())
        return agg_data, dates

class RowData(object):
    def __init__(self, summation, average, maximum, minimum, count):
        self.summation = summation
        self.average = average
        self.maximum = maximum
        self.minimum = minimum
        self.count = count
    def set_mxmin_resp(mxresp, mnresp):
        self.mxresp = mxresp
        self.mnresp = mnresp
    def __repr__(self):
        return str((self.summation, self.average, self.maximum, self.minimum, self.count))

def test():
    x = datetime(2012, 2, 1)
    y = datetime(2012, 3, 1)
    tv = TimelyView()
    tv.set_input_from_file('sample_data.csv')
    tv.distribute_and_aggregate()

    r1 = tv.aggregation_between(x, y, SUM)
    r2 = tv.aggregation_between(x, y, AVG)
    r3 = tv.aggregation_between(x, y, MAX)

    print r1
    print '--------------------'
    print r2
    print '--------------------'
    print r3
