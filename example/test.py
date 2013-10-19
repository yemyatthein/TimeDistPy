import sys
sys.path.append("./../")
from timely_view import *
from datetime import datetime

def test():
    x = datetime(2012, 2, 1)
    y = datetime(2012, 3, 1)
    tv = TimelyView()
    tv.set_input_from_file('data/sample_data.csv')
    tv.distribute_and_aggregate()

    r1 = tv.aggregation_between(x, y, SUM)
    r2 = tv.aggregation_between(x, y, AVG)
    r3 = tv.aggregation_between(x, y, MAX)

    print r1
    print '--------------------'
    print r2
    print '--------------------'
    print r3

test()
