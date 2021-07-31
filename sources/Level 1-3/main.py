from utility import *

data = inputFrom("input.txt")

# print(data)


init(data)

res = Try(0, start, 0)
if res != None:
    print(res)
else:
    print("NO SOLUTION")
    
