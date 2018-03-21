import argparse
import datetime
from prettytable import PrettyTable
from collections import OrderedDict

parser = argparse.ArgumentParser()
parser.add_argument('filename', help="Log file path")
group = parser.add_mutually_exclusive_group()
group.add_argument("-u", help="Summary failed login log and sort log by user", action="store_true")
group.add_argument("-r", help="Sort in reverse order", action="store_true")
group2 = parser.add_mutually_exclusive_group()
group2.add_argument("-n", help="Show only the user of most N-th tims", default=-1)
group2.add_argument("-t", help="Show only the user of attacking equal or more than T times", default=-1)
parser.add_argument('-after', help="Filter log after date. format YYYY-MM-DD-HH:MM:SS", default="0000-01-01-00-00-00")
parser.add_argument('-before', help="Filter log before date. format YYYY-MM-DD-HH:MM:SS", default="3000-12-31-12-00-00")
args = parser.parse_args()

after_t = datetime.datetime.strptime(args.after, '%Y-%m-%d-%H-%M-%S')
before_t = datetime.datetime.strptime(args.before, '%Y-%m-%d-%H-%M-%S')

dict = {}
file = open(args.filename)
for str in file:
    if str.find('Invalid user') > 0:
        s = str.split(' ')
        log_t = datetime.datetime.strptime('2018 ' + ' '.join(s[0:3]), '%Y %b %d %H:%M:%S')
        # Delete <{facility}.{severity level}>
        if s[3].find('<') > 0:
            s.pop(3)
        # Add data into dict
        if after_t <= log_t <= before_t:
            if s[7] in dict:
                dict[s[7]] += 1
            else:
                dict[s[7]] = 1

dd = {}
if int(args.n) >= 0:
    for key in dict.keys():
        print(key)
        if dict[key] <= int(args.n):
            dd[key] = dict[key]
elif int(args.t) >= 0:
    for key in dict.keys():
        print(key)
        if dict[key] >= int(args.t):
            dd[key] = dict[key]
else:
    dd = dict

# Sorting
if args.u:
    d = OrderedDict(sorted(dd.items(), key=lambda x: x[0]))
elif args.r:
    d = OrderedDict(sorted(dd.items(), key=lambda x: x[1]))
else:
    d = OrderedDict(sorted(dd.items(), key=lambda x: x[1], reverse=True))

pt = PrettyTable()
pt.add_column("user", list(d.keys()))
pt.add_column("count", list(d.values()))
print(pt)

