#*---------- Imperative style line selection ------------#
selected = []                 # temp list to hold matches
fp = open(filename):
for line in fp.readlines():   # Py2.2 -> "for line in fp:"
    if isCond(line):          # (2.2 version reads lazily)
        selected.append(line)
del line                      # Cleanup transient variable
