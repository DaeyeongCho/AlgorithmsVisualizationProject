def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

# 함수를 딕셔너리의 값으로 할당
operations = {
    'add': add,
    'subtract': subtract
}

# 딕셔너리의 키를 사용하여 함수 호출
result_add = operations['add'](10, 5)
result_subtract = operations['subtract'](10, 5)

print(f"Addition: {result_add}, Subtraction: {result_subtract}")
