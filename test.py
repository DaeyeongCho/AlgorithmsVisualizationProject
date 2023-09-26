import matplotlib.pyplot as plt

class BarChart:
    def __init__(self):
        self.fig, self.ax = plt.subplots()

    def plot(self, categories, values, new_order):
        # 막대 그래프 그리기
        self.ax.bar(categories, values)

        # x 축 레이블 교환
        self.ax.set_xticks(categories)
        self.ax.set_xticklabels(new_order)

        # 그래프 제목 및 레이블 추가 (선택 사항)
        self.ax.set_title('막대 그래프 위치 교환 예제')
        self.ax.set_xlabel('카테고리')
        self.ax.set_ylabel('값')

        # 그래프 표시
        plt.show()

# 데이터 설정
categories = ['A', 'B', 'C', 'D']
values = [10, 15, 7, 12]

# 새로운 순서 정의
new_order = ['D', 'C', 'B', 'A']

# BarChart 클래스 인스턴스 생성 및 그래프 플롯
bar_chart = BarChart()
bar_chart.plot(categories, values, new_order)
