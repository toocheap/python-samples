import hashlib,sys

m = hashlib.md5()
m.update(sys.argv[1])
print m.hexdigest()
