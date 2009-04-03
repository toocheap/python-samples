# http://www.python.jp/doc/release/lib/module-optparse.html
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",help="write report to FILE", metavar="FILE")
parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True, help="don't print status messages to stdout")

(options, args) = parser.parse_args()
print options
print args

