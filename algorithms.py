import time

class MyAlgorithms():
    def __init__(self):
        self.sort_algorithms = {
            "버블 정렬":self.bubble_sort,
            "선택 정렬":self.selection_sort,
            "삽입 정렬":self.insertion_sort,
            "병합 정렬":self.merge_sort,
            "퀵 정렬":self.quick_sort,
            "힙 정렬":self.heap_sort,
        }
        self.search_algorithms = {
            "선형 탐색":self.linear_search,
            "이진 탐색":self.binary_search,
        }

## ========================================================================== 정렬 알고리즘 ========================================================================== ##
# 사용 가능한 전역 변수: array, pivot, compare, other_compare, compare_list, fix


    def bubble_sort(self, array): # 버블 정렬
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



    def selection_sort(self, array): # 선택 정렬
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



    def insertion_sort(self, array): # 삽입 정렬
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



    def merge_sort(self, array): # 병합 정렬
        n = len(array)
        step = 1
        while step < n:
            left = 0
            while left + step < n:
                mid = left + step
                right = min(left + 2 * step, n)
                self.merge_sort_recursive(array, left, mid, right)
                left += 2 * step
            step *= 2



    def merge_sort_recursive(self, array, left, mid, right): # 병합 정렬 재귀
        global compare_list
        global pivot
        global fix

        temp = []
        for i in range(left, right):
            compare_list.append(i)
        i, j = left, mid
        while i < mid and j < right:
            if array[i] <= array[j]:
                temp.append(array[i])
                i += 1
            else:
                temp.append(array[j])
                j += 1
        while i < mid:
            temp.append(array[i])
            i += 1
        while j < right:
            temp.append(array[j])
            j += 1
        for i in range(left, right):
            array[i] = temp[i - left]
            pivot = i
            self.delay()
            self.fixbar(i)

        if right - left < len(array) - 1:
            compare_list = []
            fix = []



    def quick_sort(self, array): # 퀵 정렬
        self.quick_sort_recursive(array, 0, len(array) - 1)

    def quick_sort_recursive(self, array, start, end): # 퀵 정렬 재귀
        global pivot
        global compare
        global compare_other

        if start == end :
            pivot = start
            self.delay()
            self.fixbar(start)
            return
        elif start >= end :
            return
        pivot = start
        compare = start
        compare_other = end
        
        while compare <= compare_other:
            while compare <= end and array[compare] <= array[pivot]:
                self.delay()
                compare += 1
            while compare_other > start and array[compare_other] >= array[pivot]:
                self.delay()
                compare_other -= 1
            if compare > compare_other:
                array[pivot], array[compare_other] = array[compare_other], array[pivot]
                self.fixbar(compare_other)
            else:
                array[compare_other], array[compare] = array[compare], array[compare_other]
        
        
        self.quick_sort_recursive(array, start, compare_other - 1)
        self.quick_sort_recursive(array, compare_other + 1, end)


    def heap_sort(self, array):
        global pivot
        global compare
        
        n = len(array)

        for i in range(n // 2 - 1, -1, -1):
            self.heap_sort_recursive(array, n, i)

        for compare in range(n - 1, 0, -1):
            pivot = 0
            array[0], array[compare] = array[compare], array[0]
            self.delay()
            self.fixbar(compare)
            self.heap_sort_recursive(array, compare, 0)
        
        self.fixbar(0)


    def heap_sort_recursive(self, array, n, i):
        global pivot
        global compare

        pivot = i
        compare = pivot
        left = 2 * pivot + 1
        right = 2 * pivot + 2
        
        if left < n and array[left] > array[compare]:
            compare = left
        
        if right < n and array[right] > array[compare]:
            compare = right
        
        if compare != pivot:
            array[pivot], array[compare] = array[compare], array[pivot]
            self.delay()
            self.heap_sort_recursive(array, n, compare)



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
        self.sort_algorithms[name](array)

    def runSearchFunc(self, name):
        global array
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