#!/usr/bin/env python
# conding: -*- utf8 -*-
import getopt
import sys

def usage():
    print "usage here"

def main():
#    try:
#         opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])
#    except getopt.GetoptError:
#        usage()
#        sys.exit(2)

    opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])
    print opts
    print args

    output = None
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        if o in ("-o", "--output"):
            output = a
    # ...

if __name__ == "__main__":
    main()
