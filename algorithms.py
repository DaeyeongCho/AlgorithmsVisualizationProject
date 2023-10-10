import time

class MyAlgorithms():
    def __init__(self):
        self.sort_algorithms = {
            "버블 정렬":self.bubble_sort,
            "선택 정렬":self.selection_sort,
            "삽입 정렬":self.insertion_sort,
            "병합 정렬":self.merge_sort,
        }
        self.search_algorithms = {
            "선형 탐색":self.linear_search,
            "이진 탐색":self.binary_search,
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
        global fix

        for i in range(len(array) - 1):
            pivot = i
            for compare in range(i + 1, len(array)):
                self.delay()
                if array[compare] < array[pivot]:
                    pivot = compare
            array[i], array[pivot] = array[pivot], array[i]
            self.fixbar(i)


    def insertion_sort(self):
        global array
        global pivot
        global compare

        self.fixbar(0)
        for end in range(1, len(array)):
            for pivot in range(end, 0, -1):
                compare = pivot - 1
                self.delay()
                if array[compare] > array[pivot]:
                    array[compare], array[pivot] = array[pivot], array[compare]
            self.fixbar(end)


    def merge_sort(self, arr = None):
        global array

        if arr is None:
            arr = array


        if len(arr) < 2:
            return arr

        mid = len(arr) // 2
        low_arr = self.merge_sort(arr[:mid])
        high_arr = self.merge_sort(arr[mid:])

        merged_arr = []
        l = h = 0
        while l < len(low_arr) and h < len(high_arr):
            if low_arr[l] < high_arr[h]:
                merged_arr.append(low_arr[l])
                l += 1
            else:
                merged_arr.append(high_arr[h])
                h += 1
        merged_arr += low_arr[l:]
        merged_arr += high_arr[h:]
        return merged_arr


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


    def binary_search(self):
        global array
        global pivot
        global compare
        global compare_other
        global search_value

        compare = 0
        compare_other = len(array) - 1

        while compare <= compare_other:
            pivot = (compare + compare_other) // 2
            
            self.delay()

            if array[pivot] == search_value:
                return pivot
            elif array[pivot] < search_value:
                compare = pivot + 1
            else:
                compare_other = pivot -1

        return None



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