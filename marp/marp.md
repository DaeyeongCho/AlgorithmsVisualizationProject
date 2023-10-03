---
marp: true
paginate: true
footer: 컴퓨터공학과 20학번 조대영
---

# 컴퓨터종합설계 3주차

컴퓨터공학전공 2020215730 조대영

---

<!-- _header: 목차-->

# 목차

* ### 코멘트 반영(개발)
* ### 개발 진척사항
* ### 코멘트 반영(논문) + 논문 진척사항

---

<!-- _header: 코멘트 반영(개발)-->

# 코멘트 반영(개발)

## 코멘트: 다양한 기능 추가

### 고려 사항

**정렬 알고리즘:** 내림차순 정렬

**탐색 알고리즘:** 여러번 탐색

**공통:** 피벗-컴페어 값 표시, 비교 위치 및 횟수 표시, 다중 리스트-트리 구조의 경우 다른 방법으로 표현, 소스코드 보기, 알고리즘 설명, 복잡도 표시

**기타:** 전체/창 모드, fps 설정, 캡쳐, 소스코드 입력 기능

**핵심 기능 구현이 우선이므로 실제 기능 적용은 1차 제출 이후 진행 예정**

---

<!-- _header: 개발 진척사항-->

# 개발 진척사항

Preview

<p align="center">
    <img src="./old_ui_scr.png" align="center" width="40%">
    <img src="./arrow.png" align="center" width="10%">
    <img src="./ui_scr.png" align="center" width="40%">
</p>

---

<!-- _header: 개발 진척사항-->

## 개발 내용

**3주차 목표(지난주):** 각종 핵심 위젯들의 기능 구현, 알고리즘 최소 1가지 이상 구현, 제공 기능 확실하게 정립

* **그래프 라이브러리 변경**

* 실시간 그래프 구현

* 타이머 구현

* 실행 시 옵션 값 적용되도록 구현

* 실행 시 State 창에 각종 정보 표현

* 알고리즘 이식 시 코드 수정 정도의 차이 줄임

* 버블 정렬 구현

---

<!-- _header: 개발 진척사항-->

### 그래프 라이브러리 변경
#### matplotlib -> PyQtGraph

<p align="center">
    <img src="./matplot_logo.png" align="center" width="15%">
    <img src="./arrow.png" align="center" width="10%">
    <img src="./pyqtgraph.png" align="center" width="15%">
</p>

* **원인:** 그래프는 사용 모니터의 초당 프레임(FPS) 속도에 맞게 그래프가 전환 되어야 함.<br>(초당 60회, 120회, 144회 등)

* **matplotlob 문제점:** 느린 전환 속도 (초당 10회 수준)<br>정적인 그래프 작성에 중점을 둔 라이브러리이기 때문

* **PyQtGraph:** 실시간 차트에 적합하게 설계된 라이브러리<br>모니터의 프레임 속도를 충분히 따라 감.

---

<!-- _header: 개발 진척사항-->

### 실시간 그래프 구현

![height:300px](./graph.png)
![height:70px](./value.png)

전역 변수인 array, compare, pivot, fixed 값에 따라 그래프 및 색상 표현
해당 값에 따라 그래프에 실시간으로 반영 됨
array: 회색, pivot: 빨강, compare: 파랑, fixed: 노랑

---

<!-- _header: 개발 진척사항-->

### 타이머 구현

![height:300px](./timestamp.png)

1ms 단위로 실행되는 타이머 구현
진행 시간 등에 사용

---

<!-- _header: 개발 진척사항-->

### 실행 시 옵션 값 적용되도록 구현

![height:200px](./option.png)
![height:70px](./number.png)

옵션 입력 값에 따라 실행 시 반영 됨

데이터 크기 100 지정 시 그래프에도 100개의 막대 반영

속도, 섞는 횟수 등도 반영

---

<!-- _header: 개발 진척사항-->

### 실행 시 State 창에 정보 표현

<p align="center">
    <img src="./notstart.png" align="center" width="12%">
    <img src="./arrow.png" align="center" width="10%">
    <img src="./started.png" align="center" width="20%">
</p>

실행 버튼 클릭 시 state 창에 표현 됨.
진행 시간은 실시간으로 변경 됨

---

<!-- _header: 개발 진척사항-->

### 알고리즘 이식 시 수정 정도의 차이 줄임

**프로토타입**

<p align="center">
    <img src="./before.png" align="center" width="40%">
    <img src="./arrow.png" align="center" width="10%">
    <img src="./oldafter.png" align="center" width="40%">
</p>

거의 다른 코드가 되었음.

---

<!-- _header: 개발 진척사항-->

**현재 프로그램**

<p align="center">
    <img src="./before.png" align="center" width="40%">
    <img src="./arrow.png" align="center" width="10%">
    <img src="./newafter.png" align="center" width="40%">
</p>

delay() 함수 2개, fixbar() 함수 1개 추가가 전부

---

<!-- _header: 개발 진척사항-->

### 버블 정렬 구현

<p align="center">
    <img src="./bubble1.png" align="center" width="30%">
    <img src="./bubble2.png" align="center" width="30%">
    <img src="./bubble3.png" align="center" width="30%">
</p>


---

<!-- _header: 개발 진척사항-->

### self 평가

* matplotlib 라이브러리에서 상당한 시간 소요

* 핵심 기능들 조금씩은 구현, 버블 정렬 구현, 제공 기능 정립 실패

* 핵심 기능들의 일부분씩은 모두 구현해 보았으므로 앞으로는 비교적 빠르게 진행될 것으로 예상

* 이번주 목표에서 달성하지 못한 제공 기능을 정립하고 로그 기능, 메뉴바와 대화상자 등 추가적인 기능 구현 필요

---


<!-- _header: 논문 진척사항-->

# 코멘트 반영(논문) + 논문 진척사항

## 코멘트

* 두서 정리<br>->수필 형식이 아닌 논문 형식에 적합한 문법과 단어로 논문 전반을 수정함.

* 문단, 단락 정리<br>->단락마다 첫 문장 띄워쓰기, 단락 간 한 줄 띄우기 등

* 연구 내용 및 방법 서술

---

<!-- _header: 논문 진척사항-->

## 지난주 목표 및 진척사항

**3주차 목표:** 두서가 없더라도 핵심 내용을 포함하는 것을 목표로 논문의 모든 목차 내용 작성

* '실험 및 결과 분석'과 '요약'을 제외한 모든 목차 어느정도 작성

* 두서 및 문단-단락 정리

* 표, 그림 추가


---

<!-- _header: 논문 진척사항-->

# 논문 진척사항

<p align="center">
    <img src="./n1.jpg" align="center" width="22%">
    <img src="./n2.jpg" align="center" width="22%">
    <img src="./n3.jpg" align="center" width="22%">
    <img src="./n4.jpg" align="center" width="22%">
</p>

---

<!-- _header: 논문 진척사항-->

<p align="center">
  <img src="./n5.jpg" align="center" width="22%">
  <img src="./n6.jpg" align="center" width="22%">
  <img src="./n7.jpg" align="center" width="22%">
  <img src="./n8.jpg" align="center" width="22%">
</p>

---

<!-- _header: 논문 진척사항-->

### 두서 및 단락 정리 서론 예시

<p align="center">
  <img src="./nex.png" align="center" width="50%">
</p>

---

<!-- _header: 논문 진척사항-->

### 그림, uml, 캡쳐본 추가

<p align="center">
  <img src="./class_uml.jpg" align="center" width="40%">
  <img src="./ui_uml.jpg" align="center" width="40%">
</p>

---

# 감사합니다.