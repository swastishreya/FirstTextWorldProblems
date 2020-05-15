f = open("vocab.txt", "r")
line = f.read().split('\n')
print(line)
i = 0
d = {}
for var in line:
    print(var)
    d[var] = i
    i += 1
f.close()

f = open("w2id.txt","w")
f.write( str(d) )
f.close()