import os
import sys
root = os.path.dirname(__file__)
icon = os.path.join(root, 'icon-tt.ico')

# def resource_path(): # 파일과 리소스의 경로 찾기
#     relative_path = 'uieffect.ui'
#     # 리소스가 내부이면 파일 경로를, 외부이면 sys._MEIPASS를 base_path에 할당
#     base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
#     return os.path.join(base_path, relative_path) # 파일의 총 경로를 반환