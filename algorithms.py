import time

class MyAlgorithms():
    def __init__(self):
        self.sort_algorithms = {
            "버블 정렬":self.bubble_sort,
            "선택 정렬":self.selection_sort,
        }
        self.search_algorithms = {
            "선형 탐색":self.linear_search,
        }

## ========================================================================== 정렬 알고리즘 ========================================================================== ##
# 사용 가능한 전역 변수: array, pivot, compare, other_compare, compare_list, fix


    def bubble_sort(self): # 버블 정렬
        global array
        global pivot
        global compare
        global fix

        for i in range(len(array) - 1, 0, -1):
            for pivot in range(i):
                compare = pivot + 1
                self.delay()
                if array[pivot] > array[compare]:
                    array[pivot], array[compare] = array[compare], array[pivot]
            self.fixbar(i)


    def selection_sort(self): # 선택 정렬
        global array
        global pivot
        global compare
        global compare_other
        global compare_list
        global fix

        for i in range(len(array) - 1):
            pivot = i
            for compare in range(i + 1, len(array)):
                self.delay()
                if array[compare] < array[pivot]:
                    pivot = compare
            array[i], array[pivot] = array[pivot], array[i]
            self.fixbar(i)


## ========================================================================== 정렬 알고리즘 끝 ========================================================================== ##

## ========================================================================== 탐색 알고리즘 ========================================================================== ##


    def linear_search(self):
        global array
        global pivot
        global search_value

        for pivot in array:
            self.delay()
            if pivot == search_value:
                return pivot



## ========================================================================== 탐색 알고리즘 끝 ========================================================================== ##





    def runSortFunc(self, name):
        self.sort_algorithms[name]()

    def runSearchFunc(self, name):
        global fix
        self.search_value = self.search_algorithms[name]()
        fix.append(self.search_value)
        self.delay()

    def delay(self): # 딜레이 넣기
        time.sleep(limit/1000)

    def fixbar(self, index): # fix된 막대 인덱스 추가
        fix.append(index)

# 전역 변수
array: list = []
pivot: int = -1
compare: int = -1
compare_other: int = -1
compare_list: list = []
fix: list = []
search_value: int

limit: int