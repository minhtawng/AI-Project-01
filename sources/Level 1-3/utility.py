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
# Kết hợp với việc gỡ ngoặc và đổi dấu toán tử
def inputFrom(fileName=""):
    f = open(fileName)

    temp = f.read()

    res = ""
    SignReverse = 0
    
    for i in temp:
        if i.isalpha():
            res += i
        else:
            if i == '(':
                SignReverse = 1
                continue
            if i == ')':
                SignReverse = 0
                continue
            if SignReverse == 1:
                if i == '+':
                    res += '-'
                else:
                    if i == '-': res += '+'
            else:
                res += i

    f.close()

    return res


# Xử lí khởi tạo dữ liệu từ input data
def init(data=str()):
    # Khởi tạo trạng thái bắt đầu
    for i in data:
        if i.isalpha():
            start.update({i: -1})

    operators = list()  # Operators list

    # Mặc định thêm 1 dấu '+' vào danh sách toán tử nếu phần tử đầu tiên của data là chữ cái
    if data[0] not in ('+', '-'):
        operators.append('+')

    # Thêm các toán tử còn lại trong phép toán
    for char in data:
        if char in ('+', '-'):
            operators.append(char)

    # Sau khi đã lưu trữ, ta replace tất cả bằng ' ' để tiện cho việc split và
    # xử lí lưu toán hạng về sau
    data = data.replace('+', ' ')
    data = data.replace('-', ' ')

    temp = data.split('=')  # Tách kết quả với các toán hạng
    operands = temp[0].split(' ')  # Tách các toán hạng với nhau
    result = temp[1]

    # Một subtree tương ứng với một cột tính của phép toán

    # Khởi tạo subtree là một list có size bằng với maximum độ dài của result và độ dài các toán hạng, trong đó
    # mỗi phần tử của subtree là một list chứa các node của subtree đó

    # impact là list có cùng size với subtree,
    # với mỗi phần tử là một dict chứa mức độ ảnh hưởng của các toán hạng trong subtree đó
    tmp = len(result)
    for i in range(0, len(operands)):
        tmp = max(tmp, len(operands[i]))

    for i in range(0, tmp):
        subtree.append(list())
        impact.append(dict())

    # Thêm các kí tự (node) của các toán hạng vào các subtree tương ứng
    for i in range(0, len(operands)):
        opr = operands[i]   # toán hạng thứ i trong list toán hạng
        for j in range(0, len(opr)):
            # Đánh dấu index ngược lại vì giải từ phải sang, nên subtree 0 là hàng đơn vị, 1 là hàng chục, ...
            id = len(opr) - j - 1

            # Xử lí khi kí tự chưa được thêm vào dict
            if not opr[j] in impact[id]:
                if operators[i] == '+':
                    pos = 1
                    neg = 0
                else:
                    pos = 0
                    neg = 1

                subtree[id].append(opr[j])
                impact[id].update({opr[j]: (pos, neg)})
            else:
                # Ngược lại, xử lí khi kí tự đã được thêm vào dict
                # Chỉ cần update tuple value của kí tự (key) được thêm vào dựa vào toán tử liền trước
                pos = impact[id][opr[j]][0]
                neg = impact[id][opr[j]][1]

                if operators[i] == '+':
                    pos = pos + 1
                else:
                    neg = neg + 1

                impact[id].update({opr[j]: (pos, neg)})

    # Thêm các kí tự (node) của result vào các subtree tương ứng
    for i in range(0, len(result)):
        char = result[len(result)-i-1]

        if char not in subtree[i]:
            subtree[i].append(char)
            impact[i].update({char: (0, 1)})
        else:
            pos = impact[i][char][0]
            neg = impact[i][char][1] + 1
            impact[i].update({char: (pos, neg)})

    # print(len(operands))
    # print(subtree)
    # print(impact)


# Kiểm tra assgin của subproblem có thỏa hay không
# Nếu thỏa thì trả về carry
# Ngược lại, None
def SAT(problem=list(), assign=dict(), factor=dict(), preCarry=0):
    pos = 0
    neg = 0

    for char in problem:
        pos = pos + assign[char]*factor[char][0]
        neg = neg + assign[char]*factor[char][1]

    A = pos + preCarry
    B = neg
    if A < 0: return None

    temp = A % 10 - B % 10

    if (temp == 0):
        return int(A/10) - int(B/10)

    return None


# Xử lí sub problem
def solveSub(idSP=int(), carry=int(), id=int(), localState=dict()):
    if id == len(subtree[idSP]):
        temp = SAT(subtree[idSP], localState, impact[idSP], carry)

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
