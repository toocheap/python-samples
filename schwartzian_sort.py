#---------- schwartzian_sort.py ----------#
# Timing test for "sort on fourth word"
# Specifically, two lines >= 4 words will be sorted
#   lexographically on the 4th, 5th, etc.. words.
#   Any line with fewer than four words will be sorted to
#   the end, and will occur in "natural" order.

import sys, string, time
wrerr = sys.stderr.write

# naive custom sort
def fourth_word(ln1,ln2):
    lst1 = string.split(ln1)
    lst2 = string.split(ln2)
    #-- Compare "long" lines
    if len(lst1) >= 4 and len(lst2) >= 4:
        return cmp(lst1[3:],lst2[3:])
    #-- Long lines before short lines
    elif len(lst1) >= 4 and len(lst2) < 4:
        return -1
    #-- Short lines after long lines
    elif len(lst1) < 4 and len(lst2) >= 4:
        return 1
    else:                   # Natural order
        return cmp(ln1,ln2)

# Don't count the read itself in the time
lines = open(sys.argv[1]).readlines()

# Time the custom comparison sort
start = time.time()
lines.sort(fourth_word)

end = time.time()
wrerr("Custom comparison func in %3.2f secs\n" % (end-start))
# open('tmp.custom','w').writelines(lines)

# Don't count the read itself in the time
lines = open(sys.argv[1]).readlines()

# Time the Schwartzian sort
start = time.time()
for n in range(len(lines)):       # Create the transform
    lst = string.split(lines[n])
    if len(lst) >= 4:             # Tuple w/ sort info first
        lines[n] = (lst[3:], lines[n])
    else:                         # Short lines to end
        lines[n] = (['\377'], lines[n])

lines.sort()                      # Native sort

for n in range(len(lines)):       # Restore original lines
    lines[n] = lines[n][1]

end = time.time()
wrerr("Schwartzian transform sort in %3.2f secs\n" % (end-start))
# open('tmp.schwartzian','w').writelines(lines)

