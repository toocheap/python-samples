import hashlib,sys

m = hashlib.sha1()
m.update(sys.argv[1])
print m.hexdigest()
