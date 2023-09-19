import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# 초기화 함수: 막대 그래프 초기 설정
def init():
    global bars
    x = np.arange(len(data))
    bars = ax.bar(x, data, color='blue')
    return bars

# 업데이트 함수: 막대 그래프를 시간에 따라 업데이트
def update(frame):
    global data, bars
    data = np.random.randint(1, 10, len(data))  # 랜덤한 데이터 생성
    for bar, h in zip(bars, data):
        bar.set_height(h)  # 막대 높이 업데이트
    return bars

# 초기 데이터
num_bars = 100
data = np.random.randint(1, 10, num_bars)

# Figure 생성
fig, ax = plt.subplots()

# 초기 막대 그래프 생성
bars = init()

# FuncAnimation 객체 생성
ani = FuncAnimation(fig, update, init_func=init, blit=True, interval=1)  # 1밀리초(0.001초) 간격으로 업데이트

# 애니메이션 재생
plt.show()
