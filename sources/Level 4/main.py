from utility import *

data = inputFrom("input.txt")

print(data)

init(data)

res = Try(0, start, 0)
if res != None:
    for item in sorted(res.items(), key = lambda x: x[0]):
        print(item[1], end = "")
    # print(res)
else:
    print("NO SOLUTION")
    
