from os import stat
from typing import Dict
import object as obj
from object import *


# Convert dict to string
def toStr(li=dict()):
    res = ""
    for i in li.values():
        res += str(i)
    return res


# xử lí đọc input từ file
def inputFrom(fileName=""):
    f = open(fileName)

    res = f.read()

    f.close()

    return res


# Xử lí khởi tạo dữ liệu từ input data
def init(data=str()):
    # Khởi tạo trạng thái bắt đầu
    for i in data:
        if i.isalpha():
            start.update({i: -1})

    data = data.replace('*', ' ')

    temp = data.split('=')  # Tách kết quả với các nhân tử

    operands = temp[0].split(' ')  # Tách các nhân tử với nhau  
    MaxLenOperand = 0
    for i in range(0, len(operands)):
        operands[i] = operands[i][::-1] # Reverse từng nhân tử
        MaxLenOperand = max(MaxLenOperand, len(operands[i]))

    global result
    result = temp[1]
    result = result[::-1] #Reverse kết quả

    # Một subtree tương ứng với một cột tính của phép toán nhân

    # Khởi tạo subtree là một list có size bằng với độ dài của result (vì level này chỉ tập trung giải quyết phép nhân với 2 nhân tử)
    # trong đó, mỗi phần tử của subtree là một list chứa các node của subtree đó

    # impact là list có cùng size với subtree,
    # với mỗi phần tử là một dict chứa mức độ ảnh hưởng của các kí tự (node) trong subtree đó

    for i in range(0, len(result)):
        subtree.append(list())
        impact.append(dict())

    for i in range(0, len(operands[0])):
        for j in range(0, len(operands[1])):
            id = i + j
            char1 = operands[0][i]
            char2 = operands[1][j]

            if char1 not in subtree[id]:
                subtree[id].append(char1)
            if char2 not in subtree[id]:
                subtree[id].append(char2)

            if char1 not in impact[id]:
                impact[id].update({char1: {char2: 1}})
            else:
                if char2 not in impact[id][char1]:
                    impact[id][char1].update({char2: 1})
                else:
                    temp = impact[id][char1][char2] + 1
                    impact[id][char1].update({char2: temp})

    # Thêm các kí tự (node) của result vào các subtree tương ứng
    for i in range(0, len(result)):
        if result[i] not in subtree[i]:
            subtree[i].append(result[i])

    # print("Input size:", len(data))
    # print("Number of operands:", len(operands))
    # print("Longest operand:", MaxLenOperand)


# Kiểm tra assgin của subproblem có thỏa hay không
# Nếu thỏa thì trả về carry
# Ngược lại, None
def SAT(problem=list(), assign=dict(), subRes="", factor=dict(), preCarry=0):
    pos = 0

    for char1 in problem:
        if char1 in factor:
            for item in factor[char1].items():
                char2 = item[0]
                imp = item[1]

                pos += assign[char1]*assign[char2]*imp

    pos += preCarry

    if pos % 10 == assign[subRes]:
        return int(pos/10)

    return None


# Xử lí sub problem
def solveSub(idSP=int(), carry=int(), id=int(), localState=dict()):
    if id == len(subtree[idSP]):
        temp = SAT(subtree[idSP], localState,
                   result[idSP], impact[idSP], carry)

        if temp != None:
            res = Try(idSP+1, localState, temp)

            if res != None:
                return res

        return None

    # subtree(set))
    char = subtree[idSP][id]
    res = dict()

    if localState[char] == -1:
        for val in range(0, 10):
            if val not in localState.values():
                localState[char] = val

                res = solveSub(idSP, carry, id+1, localState)
                if res != None:
                    return res

                localState[char] = -1
    else:
        res = solveSub(idSP, carry, id+1, localState)

    return res


# Xử lí chính
def Try(idSP=int(), state=dict(), carry=int()):
    if len(state) > 10:
        return

    if idSP == len(subtree):
        if carry == 0:
            return state
        else:
            return None

    strState = toStr(state)

    if strState in StateSpace:
        return None

    res = solveSub(idSP, carry, 0, state)
    StateSpace.add(strState)

    return res
