# uiEffect
[imagaug](https://github.com/aleju/imgaug)를 활용한 GUI 이미지 증대 프로그램입니다.


## 의도
#### 시작(2022.04.14.-2022.04.26.)
* 회사에서 이미지 증대 효과 중 라벨링 회전 효과가 필요해 자체 개발

* 실제 사용하기는 CUI형식으로 사용했으나 상사가 이미지 회전을 직접 보고 싶어하셨기에 GUI 형식 추가 개발

* CUI형식으로 효과 추가, 이미지 저장등 구현했으나 GUI는 보여주기 식으로 라벨링 회전 목적으로 개발 


#### 정리(2022.04.01.-2023.04.12.)
* 퇴사 후 GUI형식으로 재개발(소스 정리)

* GUI 화면 재구성

* 저장 방식 추가(통합 저장, 개별 저장)


## 환경
* Pycharm
* Pychon
* PyQt5


## 오류 해결
* np.bool 오류
  * numpy 1.24.X 버전으로 업데이트 되면서 np.bool를 부분이 삭제되어 imgaug를 이용하기 위해서는 업데이터 전인 **numpy 1.23.5 이하 버전 사용**
