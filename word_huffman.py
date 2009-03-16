#---------- word_huffman.py ----------#
wordchars = '-_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def normalize_text(txt):
    "Convert non-word characters to spaces"
    trans = [' '] * 256
    for c in wordchars: trans[ord(c)] = c
    return txt.translate(''.join(trans))

def build_histogram(txt, hist={}):
    "Incrementally build a histogram table from text source(s)"
    for word in txt.split():
        hist[word] = hist.get(word, 0)+1
    return hist

def optimal_Nbyte(hist, entrylen=2):
    "Build optimal word list for nominal symbol table byte-length"
    slots = 127**entrylen
    words = []
    for word, count in hist.items():
        gain = count * (len(word)-entrylen)
        if gain > 0: words.append((gain, word))
    words.sort()
    words.reverse()
    return [w[1] for w in words[:slots]]

def tables_from_words(words):
    "Create symbol tables for compression and expansion"
    # Determine ACTUAL best symbol table byte length
    if len(words) < 128: entrylen = 1
    elif len(words) <= 16129: entrylen = 2
    else: entrylen = 3 # assume < ~2M distinct words
    comp_table = {}
    # Escape hibit characters
    for hibit_char in map(chr, range(128,256)):
        comp_table[hibit_char] = chr(255)+hibit_char
    # Literal low-bit characters
    for lowbit_char in map(chr, range(128)):
        comp_table[lowbit_char] = lowbit_char
    # Add word entries
    for word, index in zip(words, range(len(words))):
        comp_table[word] = symbol(index, entrylen)
    # Reverse dictionary for expansion table
    exp_table = {}
    for key, val in comp_table.items():
        exp_table[val] = key
    return (comp_table, exp_table, entrylen)

def symbol(index, entrylen):
    "Determine actual symbol from word sequence and symbol length"
    if entrylen == 1:
        return chr(128+index)
    if entrylen == 2:
        byte1, byte2 = divmod(index, 128)
        return chr(128+byte1)+chr(128+byte2)
    if entrylen == 3:
        byte1, rem = divmod(index, 16129)
        byte2, byte3 = divmod(rem, 128)
        return chr(128+byte1)+chr(128+byte2)+chr(128+byte3)
    raise ValueError, "symbol byte len must be 1 <= S <=3: "+`entrylen`

def word_Huffman_compress(text, comp_table):
    "Compress text based on word-to-symbol table"
    comp_text = []
    maybe_entry = []
    for c in text+chr(0):   # force flush of final word
        if c in wordchars:
            maybe_entry.append(c)
        else:
            word = ''.join(maybe_entry)
            comp_text.append(comp_table.get(word, word))
            maybe_entry = []
            comp_text.append(comp_table[c])
    return ''.join(comp_text[:-1])

def word_Huffman_expand(text, exp_table, entrylen):
    "Expand text based on symbol-to-word table"
    exp_text = []
    offset = 0
    end = len(text)
    while offset < end:
        c = text[offset]
        if ord(c) == 255:   # escaped highbit character
            exp_text.append(text[offset+1])
            offset += 2
        elif ord(c) >= 128: # symbol table entry
            symbol = text[offset:offset+entrylen]
            exp_text.append(exp_table[symbol])
            offset += entrylen
        else:
            exp_text.append(c)
            offset += 1
    return ''.join(exp_text)

def Huffman_find(pat, comp_text, comp_table):
    "Find a (plaintext) substring in compressed text"
    comp_pat = word_Huffman_compress(pat, comp_table)
    return comp_text.find(comp_pat)

if __name__=='__main__':
    import sys, glob
    big_text = []
    for fpat in sys.argv[1:]:
        for fname in glob.glob(fpat):
            big_text.append(open(fname).read())
    big_text = ''.join(big_text)
    hist = build_histogram(normalize_text(big_text))
    for entrylen in (1, 2, 3):
        comp_words = optimal_Nbyte(hist, entrylen)
        comp_table, exp_table, entrylen_ = tables_from_words(comp_words)
        comp_text = word_Huffman_compress(big_text, comp_table)
        exp_text = word_Huffman_expand(comp_text, exp_table, entrylen_)
        print "Nominal/actual symbol length (entries): %i/%i (%i)" % \
              (entrylen, entrylen_, len(comp_words))
        print "Compression ratio: %i%%" % \
              ((100*len(comp_text))/len(big_text))
        if big_text == exp_text:
            print "*** Compression/expansion cycle successful!\n"
        else:
            print "*** Failure in compression/expansion cycle!\n"
        # Just for fun, here's a search against compressed text
        pos = Huffman_find('Foobar', comp_text, comp_table)
