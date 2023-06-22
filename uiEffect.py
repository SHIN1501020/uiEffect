import sys
import os
import imageio.v2 as imageio
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5 import QtGui
#import imgaug as ia
import imgaug.augmenters as iaa
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
import resources
import cv2

def resource_path(relative_path): # 파일과 리소스의 경로 찾기
    # 리소스가 내부이면 파일 경로를, 외부이면 sys._MEIPASS를 base_path에 할당
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path) # 파일의 총 경로를 반환

form = resource_path('uieffect.ui')
# form = resources.resource_path()
form_class = uic.loadUiType(form)[0]

class WindowClass(QMainWindow, form_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.center()

        #비활성화
        self.setEnabledWidget(False)
        # self.gb_effect.setEnabled(False) #효과 그룹
        # self.btn_exec.setEnabled(False) #실행버튼
        # self.progressBar.setEnabled(False) #진행바
        # self.btn_path_save.setEnabled(False) #저장위치 변경 버튼
        # self.lb_path_folder.setEnabled(False) #현재 폴더 위치 표시창
        # self.lb_path_save.setEnabled(False)#저장 폴더 위치 표시창
        # self.lb_dir.setEnabled(False)
        # self.lb_save.setEnabled(False)

        #변수 선언
        self.list_image = list()
        self.list_image_path = list()
        self.tb_list.setColumnWidth(0, 970)

        #버튼 설정
        self.btn_open.clicked.connect(self.openDirDialog)
        self.btn_path_save.clicked.connect(self.openSaveDirDialog)
        self.btn_exec.clicked.connect(self.saveEffectedImage)
        self.cbb_temperature.currentIndexChanged.connect(self.changeComboBoxTemperature)

        #효과 버튼 설정
        self.cb_rotation.pressed.connect(self.showEffectImage) #체크 박스 누를 때
        self.cb_rotation.released.connect(self.showImage) #체크 박스 뗄 때 원본 이미지 라벨선 지우기
        self.cb_rain.clicked.connect(self.showEffectImage) #비
        self.cb_snow.clicked.connect(self.showEffectImage) #눈
        self.cb_fog.clicked.connect(self.showEffectImage) #안개
        self.cb_frost.clicked.connect(self.showEffectImage)
        self.cb_spatter.clicked.connect(self.showEffectImage)
        self.cb_temperature.clicked.connect(self.showEffectImage)
        self.cb_motionBlur.clicked.connect(self.showEffectImage)
        self.cb_defocusBlur.clicked.connect(self.showEffectImage)
        self.cb_zoomBlur.clicked.connect(self.showEffectImage)
        self.cb_contrast.clicked.connect(self.showEffectImage)
        self.cb_jpegCompression.clicked.connect(self.showEffectImage)
        self.cb_pixelate.clicked.connect(self.showEffectImage)
        self.cb_gaussianNoise.clicked.connect(self.showEffectImage)

        #효과 값 설정
        self.sb_rotation.valueChanged.connect(self.showEffectImage)
        self.sb_rain_size.valueChanged.connect(self.showEffectImage)
        self.sb_rain_speed.valueChanged.connect(self.showEffectImage)
        self.sb_snow_size.valueChanged.connect(self.showEffectImage)
        self.sb_snow_speed.valueChanged.connect(self.showEffectImage)
        self.sb_fog_value.valueChanged.connect(self.showEffectImage)
        self.sb_frost_value.valueChanged.connect(self.showEffectImage)
        self.sb_spatter_value.valueChanged.connect(self.showEffectImage)
        self.sb_temperature_value.valueChanged.connect(self.showEffectImage)
        self.sb_motionBlur_value.valueChanged.connect(self.showEffectImage)
        self.sb_defocusBlur_value.valueChanged.connect(self.showEffectImage)
        self.sb_zoomBlur_value.valueChanged.connect(self.showEffectImage)
        self.sb_contrast_value.valueChanged.connect(self.showEffectImage)
        self.sb_jpegCompression_value.valueChanged.connect(self.showEffectImage)
        self.sb_pixelate_value.valueChanged.connect(self.showEffectImage)
        self.sb_gaussianNoise_value.valueChanged.connect(self.showEffectImage)

        #이미지 미리보기
        self.tb_list.cellClicked.connect(self.showImage)
        self.tb_list.currentCellChanged.connect(self.showImage)



    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def openDirDialog(self): #이미지가 있는 폴더 열기
        dir_name = QFileDialog.getExistingDirectory(self, self.tr("이미지 파일이 있는 폴더를 지정해주세요."), "./", QFileDialog.ShowDirsOnly)

        if(dir_name):
            list_file = os.listdir(dir_name)  # 폴더 위치에 있는 모든 파일
            #저장파일 위치 잡기
            self.lb_path_folder.setText(dir_name)
            self.lb_path_save.setText(dir_name+'/'+'aug')
            #리스트 초기화
            self.list_image = []
            self.list_image_path = []

            for file in list_file:
                if file.endswith(".jpg") or file.endswith(".JPG") or file.endswith(".png") or file.endswith(".PNG"):

                    self.list_image.append(file)
                    self.list_image_path.append(dir_name + '/' + file)

            #이미지 파일 있을 때만 활성화
            if len(self.list_image) > 0:
                self.tb_list.setRowCount(len(self.list_image))

                for count, file in enumerate(self.list_image):
                    self.tb_list.setItem(count, 0, QTableWidgetItem(file))

                self.setEnabledWidget(True)
                #self.tb_list.resizeColumnsToContents()#테이블 열 너비 맞추기

            else:
                #이미지 미리보기 지우기
                self.lb_orign_image.setText("원본 이미지")
                self.lb_aug_imgae.setText("효과 적용 이미지")
                # 테이블 비우기
                self.tb_list.clearContents()
                self.tb_list.setRowCount(0)
                self.setEnabledWidget(False)

                self.openDirMsgBox()


        else:
            QMessageBox.about(self, 'Warning', '폴더가 선택되지 않았습니다.')

    def setEnabledWidget(self, bool):
        self.f_save.setEnabled(bool) #저장 형식
        self.tb_list.setEnabled(bool)  # 파일 목록 리스트 활성화
        self.lb_path_folder.setEnabled(bool)  # 파일 위치 활성화
        self.lb_path_save.setEnabled(bool)  # 저장 파일 위치 활성화
        self.gb_effect.setEnabled(bool)  # 옵션 그룹창 활성화
        self.btn_exec.setEnabled(bool)  # 실행버튼 활성화
        self.progressBar.setEnabled(bool)  # 진행바 활성화
        self.btn_path_save.setEnabled(bool)  # 저장위치 변경 버튼
        self.lb_path_folder.setEnabled(bool)  # 현재 폴더 위치 표시창
        self.lb_path_save.setEnabled(bool)  # 저장 폴더 위치 표시창
        self.lb_dir.setEnabled(bool)
        self.lb_save.setEnabled(bool)


    def openSaveDirDialog(self): #증대 이미지를 저장할 폴더 지정
        dir_name = QFileDialog.getExistingDirectory(self, self.tr("증대 이미지를 저장할 폴더를 지정해주세요."), "./",QFileDialog.ShowDirsOnly)
        if(dir_name):
            self.lb_path_save.setText(dir_name)
        else:
            QMessageBox.about(self, 'Warning', '폴더가 선택되지 않았습니다.')


    def createFolder(self, directory): #새폴더 만들기
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print('Error: Createing directory.' + directory)


    def saveEffectedImage(self): #실행 버튼
        save_dir_path = self.lb_path_save.text()
        self.createFolder(save_dir_path)

        self.progressBar.setValue(0)
        total_size = len(self.list_image_path)

        for count, path in enumerate(self.list_image_path):
            #원본 이미지 가져오기
            image = imageio.imread(path)
            image_aug = image
            w = image.shape[1]
            h = image.shape[0]

            #이미지 파일 이름
            save_file_name = os.path.basename(path)
            point_ext = save_file_name.rfind('.')
            save_file_name = save_file_name[:point_ext] #확장자 제거한 이미지 파일 이름

            #원본 라벨 가져오기
            point_ext = path.rfind('.') + 1 #ext 위치 찾기
            yolo_label_path = path[:point_ext] + "txt" #같은 위치에 있는 txt 라벨 파일 값 가져오기

            if os.path.isfile(yolo_label_path):
                yolo = self.copyYoloLabel(yolo_label_path)
            else:
                yolo = self.emptyYoloLabel()

            if self.cb_each_save.isChecked():
                #효과 적용
                if (image.shape[0] >= 32) & (image.shape[1] >= 32):
                    if self.cb_rotation.isChecked():
                        image_aug, bbs, bbs_aug, label_id = self.toRotation(image, yolo, self.sb_rotation.value())
                        yolo = self.convertYoloLabel(label_id, bbs_aug, w, h)
                        _save_file_name = save_file_name + '_rotation({0})'.format(self.sb_rotation.value())
                        save_image_file_path, save_label_file_path = self.saveFileNames(save_dir_path, _save_file_name)
                        self.saveImageLabel(save_image_file_path, image_aug, yolo_label_path, save_label_file_path, yolo)

                    if self.cb_rain.isChecked():
                        image_aug = self.toRain(image, self.sb_rain_size.value(), self.sb_rain_speed.value())
                        _save_file_name = save_file_name + '_rain(s{0}s{1})'.format(int(self.sb_rain_size.value()*100), int(self.sb_rain_speed.value()*100))
                        save_image_file_path, save_label_file_path = self.saveFileNames(save_dir_path, _save_file_name)
                        self.saveImageLabel(save_image_file_path, image_aug, yolo_label_path, save_label_file_path, yolo)

                    if self.cb_snow.isChecked():
                        image_aug = self.toSnow(image, self.sb_snow_size.value(), self.sb_snow_speed.value())
                        _save_file_name = save_file_name + '_snow(s{0}s{1})'.format(int(self.sb_snow_size.value()*100), int(self.sb_snow_speed.value()*100))
                        save_image_file_path, save_label_file_path = self.saveFileNames(save_dir_path, _save_file_name)
                        self.saveImageLabel(save_image_file_path, image_aug, yolo_label_path, save_label_file_path, yolo)

                    if self.cb_fog.isChecked():
                        image_aug = self.toFog(image, self.sb_fog_value.value())
                        _save_file_name = save_file_name + '_fog({0})'.format(self.sb_fog_value.value())
                        save_image_file_path, save_label_file_path = self.saveFileNames(save_dir_path, _save_file_name)
                        self.saveImageLabel(save_image_file_path, image_aug, yolo_label_path, save_label_file_path, yolo)

                    if self.cb_frost.isChecked():
                        image_aug = self.toFrost(image, self.sb_frost_value.value())
                        _save_file_name = save_file_name + '_frost({0})'.format(self.sb_frost_value.value())
                        save_image_file_path, save_label_file_path = self.saveFileNames(save_dir_path, _save_file_name)
                        self.saveImageLabel(save_image_file_path, image_aug, yolo_label_path, save_label_file_path, yolo)

                    if self.cb_spatter.isChecked():
                        image_aug = self.toSpatter(image, self.sb_spatter_value.value())
                        _save_file_name = save_file_name + '_spatter({0})'.format(self.sb_spatter_value.value())
                        save_image_file_path, save_label_file_path = self.saveFileNames(save_dir_path, _save_file_name)
                        self.saveImageLabel(save_image_file_path, image_aug, yolo_label_path, save_label_file_path, yolo)

                    if self.cb_contrast.isChecked():
                        image_aug = self.toContrast(image, self.sb_contrast_value.value())
                        _save_file_name = save_file_name + '_contrast({0})'.format(self.sb_contrast_value.value())
                        save_image_file_path, save_label_file_path = self.saveFileNames(save_dir_path, _save_file_name)
                        self.saveImageLabel(save_image_file_path, image_aug, yolo_label_path, save_label_file_path, yolo)

                    if self.cb_temperature.isChecked():
                        image_aug = self.toTemperature(image, self.sb_temperature_value.value())
                        _save_file_name = save_file_name + '_temperature({0})'.format(self.sb_temperature_value.value())
                        save_image_file_path, save_label_file_path = self.saveFileNames(save_dir_path, _save_file_name)
                        self.saveImageLabel(save_image_file_path, image_aug, yolo_label_path, save_label_file_path, yolo)

                    if self.cb_motionBlur.isChecked():
                        image_aug = self.toMotionBlur(image, self.sb_motionBlur_value.value())
                        _save_file_name = save_file_name + '_motionBlur({0})'.format(self.sb_motionBlur_value.value())
                        save_image_file_path, save_label_file_path = self.saveFileNames(save_dir_path, _save_file_name)
                        self.saveImageLabel(save_image_file_path, image_aug, yolo_label_path, save_label_file_path, yolo)

                    if self.cb_defocusBlur.isChecked():
                        image_aug = self.toDefocusBlur(image, self.sb_defocusBlur_value.value())
                        _save_file_name = save_file_name + '_defocusBlur({0})'.format(self.sb_defocusBlur_value.value())
                        save_image_file_path, save_label_file_path = self.saveFileNames(save_dir_path, _save_file_name)
                        self.saveImageLabel(save_image_file_path, image_aug, yolo_label_path, save_label_file_path, yolo)

                    if self.cb_zoomBlur.isChecked():
                        image_aug = self.toZoomBlur(image, self.sb_zoomBlur_value.value())
                        _save_file_name = save_file_name + '_zoomBlur({0})'.format(self.sb_zoomBlur_value.value())
                        save_image_file_path, save_label_file_path = self.saveFileNames(save_dir_path, _save_file_name)
                        self.saveImageLabel(save_image_file_path, image_aug, yolo_label_path, save_label_file_path, yolo)

                    if self.cb_jpegCompression.isChecked():
                        image_aug = self.toJpegCompression(image, self.sb_jpegCompression_value.value())
                        _save_file_name = save_file_name + '_jpegCompression({0})'.format(self.sb_jpegCompression_value.value())
                        save_image_file_path, save_label_file_path = self.saveFileNames(save_dir_path, _save_file_name)
                        self.saveImageLabel(save_image_file_path, image_aug, yolo_label_path, save_label_file_path, yolo)

                    if self.cb_pixelate.isChecked():
                        image_aug = self.toPixelate(image, self.sb_pixelate_value.value())
                        _save_file_name = save_file_name + '_pixelate({0})'.format(self.sb_pixelate_value.value())
                        save_image_file_path, save_label_file_path = self.saveFileNames(save_dir_path, _save_file_name)
                        self.saveImageLabel(save_image_file_path, image_aug, yolo_label_path, save_label_file_path, yolo)

                    if self.cb_gaussianNoise.isChecked():
                        image_aug = self.toGaussianNoise(image, self.sb_gaussianNoise_value.value())
                        _save_file_name = save_file_name + '_gaussianNoise({0})'.format(self.sb_gaussianNoise_value.value())
                        save_image_file_path, save_label_file_path = self.saveFileNames(save_dir_path, _save_file_name)
                        self.saveImageLabel(save_image_file_path, image_aug, yolo_label_path, save_label_file_path, yolo)


            if self.cb_unite_save.isChecked():
                #효과 적용
                if (image.shape[0] >= 32) & (image.shape[1] >= 32):
                    if self.cb_rotation.isChecked():
                        image_aug, bbs, bbs_aug, label_id = self.toRotation(image_aug, yolo, self.sb_rotation.value())
                        yolo = self.convertYoloLabel(label_id, bbs_aug, w, h)
                        save_file_name += '_rotation({0})'.format(self.sb_rotation.value())

                    if self.cb_rain.isChecked():
                        image_aug = self.toRain(image_aug, self.sb_rain_size.value(), self.sb_rain_speed.value())
                        save_file_name += '_rain(s{0}s{1})'.format(int(self.sb_rain_size.value()*100), int(self.sb_rain_speed.value()*100))

                    if self.cb_snow.isChecked():
                        image_aug = self.toSnow(image_aug, self.sb_snow_size.value(), self.sb_snow_speed.value())
                        save_file_name += '_snow(s{0}s{1})'.format(int(self.sb_snow_size.value()*100), int(self.sb_snow_speed.value()*100))

                    if self.cb_fog.isChecked():
                        image_aug = self.toFog(image_aug, self.sb_fog_value.value())
                        save_file_name += '_fog({0})'.format(self.sb_fog_value.value())

                    if self.cb_frost.isChecked():
                        image_aug = self.toFrost(image_aug, self.sb_frost_value.value())
                        save_file_name += '_frost({0})'.format(self.sb_frost_value.value())

                    if self.cb_spatter.isChecked():
                        image_aug = self.toSpatter(image_aug, self.sb_spatter_value.value())
                        save_file_name += '_spatter({0})'.format(self.sb_spatter_value.value())

                    if self.cb_contrast.isChecked():
                        image_aug = self.toContrast(image_aug, self.sb_contrast_value.value())
                        save_file_name += '_contrast({0})'.format(self.sb_contrast_value.value())

                    if self.cb_temperature.isChecked():
                        image_aug = self.toTemperature(image_aug, self.sb_temperature_value.value())
                        save_file_name += '_temperature({0})'.format(self.sb_temperature_value.value())

                    if self.cb_motionBlur.isChecked():
                        image_aug = self.toMotionBlur(image_aug, self.sb_motionBlur_value.value())
                        save_file_name += '_motionBlur({0})'.format(self.sb_motionBlur_value.value())

                    if self.cb_defocusBlur.isChecked():
                        image_aug = self.toDefocusBlur(image_aug, self.sb_defocusBlur_value.value())
                        save_file_name += '_defocusBlur({0})'.format(self.sb_defocusBlur_value.value())

                    if self.cb_zoomBlur.isChecked():
                        image_aug = self.toZoomBlur(image_aug, self.sb_zoomBlur_value.value())
                        save_file_name += '_zoomBlur({0})'.format(self.sb_zoomBlur_value.value())

                    if self.cb_jpegCompression.isChecked():
                        image_aug = self.toJpegCompression(image_aug, self.sb_jpegCompression_value.value())
                        save_file_name += '_jpegCompression({0})'.format(self.sb_jpegCompression_value.value())

                    if self.cb_pixelate.isChecked():
                        image_aug = self.toPixelate(image_aug, self.sb_pixelate_value.value())
                        save_file_name += '_pixelate({0})'.format(self.sb_pixelate_value.value())

                    if self.cb_gaussianNoise.isChecked():
                        image_aug = self.toGaussianNoise(image_aug, self.sb_gaussianNoise_value.value())
                        save_file_name += '_gaussianNoise({0})'.format(self.sb_gaussianNoise_value.value())


                #효과 적용된 이미지 파일 저장
                    save_image_file_path = save_dir_path + '/' + save_file_name + '.jpg'
                    imageio.imwrite(save_image_file_path, image_aug)

                #효과 적용된 라벨 파일 저장
                    if os.path.isfile(yolo_label_path): #원본 라벨 파일이 있을 때만 저장
                        save_label_file_path = save_dir_path + '/' + save_file_name + '.txt'
                        with open(save_label_file_path, 'w') as f:
                            for count in range(len(yolo)):
                                data = "{0} {1:0.4f} {2:0.4f} {3:0.4f} {4:0.4f}\n".format(yolo[count]['id'], yolo[count]['x'],
                                                                                      yolo[count]['y'], yolo[count]['w'],
                                                                                      yolo[count]['h'])
                                f.write(data)
                        f.close()


            pBar = int(((count+1)/total_size) * 100)
            self.progressBar.setValue(pBar)

        self.progressBarMsgBox()
        self.progressBar.setValue(0)


    def saveFileNames(self, dir_path, file_name):
        save_image_path = dir_path + '/' + file_name + '.jpg'
        save_label_path = dir_path + '/' + file_name + '.txt'
        return save_image_path, save_label_path

    def saveImageLabel(self, image_save_path, image, label_path, label_save_path, yolo):
        imageio.imwrite(image_save_path, image)
        # 효과 적용된 라벨 파일 저장
        if os.path.isfile(label_path):  # 원본 라벨 파일이 있을 때만 저장
            with open(label_save_path, 'w') as f:
                for count in range(len(yolo)):
                    data = "{0} {1:0.4f} {2:0.4f} {3:0.4f} {4:0.4f}\n".format(yolo[count]['id'], yolo[count]['x'],
                                                                              yolo[count]['y'], yolo[count]['w'],
                                                                              yolo[count]['h'])
                    f.write(data)
            f.close()

    def progressBarMsgBox(self):
        msg = QMessageBox()
        msg.setWindowTitle("이미지 증대 실행")
        msg.setText("이미지 증대가 완료 됐습니다.")
        msg.exec_()

    def openDirMsgBox(self):
        msg = QMessageBox()
        msg.setWindowTitle("폴더 열기")
        msg.setText("이미지 파일이 없는 폴더입니다.")
        msg.exec_()


    def resizeingImage(self, image_path):
        image = imageio.imread(image_path)
        # 이미지 크기 변환
        h, w = image.shape[:2]

        if w > h:
            scaled_w = 481
            scaled_h = int(h / (w / scaled_w))
        else:
            scaled_h = 389
            scaled_w = int(w / (h / scaled_h))

        resized_image = cv2.resize(image, (scaled_w, scaled_h))
        return resized_image


    def showImage(self): #원본 이미지 미리보기
        #셀이 선택 되어있으면 보여주기
        selectedCheck = self.tb_list.selectedRanges()
        if selectedCheck:
            count_row = self.tb_list.currentRow() #선택된 이미지
            #pixmap = QPixmap(self.list_image_path[count_row])
            image_path = self.list_image_path[count_row]
            image = self.resizeingImage(image_path)
            self.showQPixamp(self.lb_orign_image, image) #원본이미지 미리보기
            self.showEffectImage()  #효과 적용된 이미지 미리보기
            # #scaled_pixmap = pixmap.scaledToWidth(398)
            # #수정
            # w = pixmap.size().width()
            # h = pixmap.size().height()
            # if w > h:
            #     scaled_pixmap = pixmap.scaledToWidth(481)
            # else:
            #     scaled_pixmap = pixmap.scaledToHeight(389)
            # self.lb_orign_image.setPixmap(QPixmap(scaled_pixmap))#원본 이미지 보기
            # self.showEffectImage()#효과 적용된 이미지 미리보기


    def showEffectImage(self): #효과 적용된 이미지 미리보기
        # 셀이 선택 되어있으면 보여주기
        selectedCheck = self.tb_list.selectedRanges()
        if selectedCheck:
            count_row = self.tb_list.currentRow()
            image_path = self.list_image_path[count_row]  #이미지 경로
            image = self.resizeingImage(image_path)
            image_aug = image

            if(image.shape[0] >= 32) & (image.shape[1] >= 32):
                #회전 효과
                if self.cb_rotation.isChecked():
                    point_ext = image_path.rfind('.') + 1 #확장자 위치 찾기
                    yolo_label_path = image_path[:point_ext] + "txt" #yolo label txt

                    if os.path.isfile(yolo_label_path): #파일 있는지 확인 없으면 빈파일 생성? 빈파일 없어야 라벨 없는걸 확인할 수 있지 않을까
                        yolo = self.copyYoloLabel(yolo_label_path) #yolo label 값 저장
                    else:
                        yolo = self.emptyYoloLabel()

                    image_aug, bbs, bbs_aug, label_id = self.toRotation(image_aug, yolo, self.sb_rotation.value()) #회전

                    image, image_aug = self.drawRotaion(image, image_aug, bbs, bbs_aug) #라벨 회전 그리기
                    #pixmap = self.convertQpixmap(image) #원본이미지 화면 출력 형태로 변환
                    #self.lb_orign_image.setPixmap(pixmap) #라벨 위치 그려진 원본이미지
                    self.showQPixamp(self.lb_orign_image, image)

                if self.cb_rain.isChecked():
                    image_aug = self.toRain(image_aug, self.sb_rain_size.value(), self.sb_rain_speed.value())

                if self.cb_snow.isChecked():
                    image_aug = self.toSnow(image_aug, self.sb_snow_size.value(), self.sb_snow_speed.value())

                if self.cb_fog.isChecked():
                    image_aug = self.toFog(image_aug, self.sb_fog_value.value())

                if self.cb_frost.isChecked():
                    image_aug = self.toFrost(image_aug, self.sb_frost_value.value())

                if self.cb_spatter.isChecked():
                    image_aug = self.toSpatter(image_aug, self.sb_spatter_value.value())

                if self.cb_contrast.isChecked():
                    image_aug = self.toContrast(image_aug, self.sb_contrast_value.value())

                if self.cb_temperature.isChecked():
                    image_aug = self.toTemperature(image_aug, self.sb_temperature_value.value())

                if self.cb_motionBlur.isChecked():
                    image_aug = self.toMotionBlur(image_aug, self.sb_motionBlur_value.value())

                if self.cb_defocusBlur.isChecked():
                    image_aug = self.toDefocusBlur(image_aug, self.sb_defocusBlur_value.value())

                if self.cb_zoomBlur.isChecked():
                    image_aug = self.toZoomBlur(image_aug, self.sb_zoomBlur_value.value())

                if self.cb_jpegCompression.isChecked():
                    image_aug = self.toJpegCompression(image_aug, self.sb_jpegCompression_value.value())

                if self.cb_pixelate.isChecked():
                    image_aug = self.toPixelate(image_aug, self.sb_pixelate_value.value())

                if self.cb_gaussianNoise.isChecked():
                    image_aug = self.toGaussianNoise(image_aug, self.sb_gaussianNoise_value.value())


                #효과 적용된 이미지 미리보기
                self.showQPixamp(self.lb_aug_imgae, image_aug)
                self.show

    def showQPixamp(self, display, image): #화면에 표시 가능한 형식으로 변환/출력
        pixmap = self.convertQpixmap(image) #화면 출력 형태로 변환
        display.setPixmap(pixmap)
        # w = pixmap.size().width()
        # h = pixmap.size().height()
        # if w > h:
        #     scaled_pixmap = pixmap.scaledToWidth(481)
        # else:
        #     scaled_pixmap = pixmap.scaledToHeight(389)
        # display.setPixmap(scaled_pixmap) #라벨 위치에 그림 출력

    def emptyYoloLabel(self): #빈 라벨 회전만 하는 용도
        yolo = list()
        yolo.append(dict())
        yolo[0]['id'] = int(0)
        yolo[0]['x'] = float(0)
        yolo[0]['y'] = float(0)
        yolo[0]['w'] = float(0)
        yolo[0]['h'] = float(0)
        return yolo

    def copyYoloLabel(self, path): #라벨 리스트에 저장
        yolo = list()
        with open(path, 'r') as f:
            lines = f.readlines()
            for count_lines, line in enumerate(lines):
                line_split = line.split()
                yolo.append(dict())
                yolo[count_lines]['id'] = int(line_split[0])
                yolo[count_lines]['x'] = float(line_split[1])
                yolo[count_lines]['y'] = float(line_split[2])
                yolo[count_lines]['w'] = float(line_split[3])
                yolo[count_lines]['h'] = float(line_split[4])
        return yolo


    def convertPoint(self, yolo, w, h):
        label_point = list() #좌표 값
        label_id = list() #클래스 id
        for count in range(len(yolo)):
            label_id.append(yolo[count]['id'])
            W = yolo[count]['w'] * w
            H = yolo[count]['h'] * h
            x1 = ((yolo[count]['x'] * w * 2) - W) / 2
            x2 = x1 + W
            y1 = ((yolo[count]['y'] * h * 2) - H) / 2
            y2 = y1 + H
            label_point.append(BoundingBox(x1=x1, x2=x2, y1=y1, y2=y2))
        return label_point, label_id


    def convertYoloLabel(self, label_id, bbs, w, h):
        yolo = list()
        for count, box in enumerate(bbs.remove_out_of_image().clip_out_of_image()):
            yolo.append(dict())
            yolo[count]['id'] = label_id[count]
            yolo[count]['x'] = box.center_x / w
            yolo[count]['y'] = box.center_y / h
            yolo[count]['w'] = box.width / w
            yolo[count]['h'] = box.height / h
        return yolo


    def toRotation(self, image, yolo, angle):
        w = image.shape[1]  # 전체 이미지 너비
        h = image.shape[0]  # 전체 이미지 높이
        #회전
        bbs_list, label_id = self.convertPoint(yolo, w, h)
        bbs = BoundingBoxesOnImage(bbs_list, shape=image.shape)
        image_aug, bbs_aug = iaa.Affine(rotate=angle)(image=image, bounding_boxes=bbs) #회전 함수
        #선 그리는 함수 따로 빼기
        return image_aug, bbs, bbs_aug, label_id

    def toRain(self, image, size, speed):
        image_aug = iaa.Rain(drop_size=size, speed=speed)(image=image)
        return image_aug

    def toSnow(self, image, size, speed):
        image_aug = iaa.Snowflakes(flake_size=size, speed=speed)(image=image)
        return image_aug

    def toFog(self, image, severity):
        image_aug = iaa.imgcorruptlike.Fog(severity=severity)(image=image)
        return image_aug

    def toFrost(self, image, severity):
        image_aug = iaa.imgcorruptlike.Frost(severity=severity)(image=image)
        return image_aug

    def toSpatter(self, image, severity):
        image_aug = iaa.imgcorruptlike.Spatter(severity=severity)(image=image)
        return image_aug

    def toContrast(self, image, severity):
        image_aug = iaa.imgcorruptlike.Contrast(severity=severity)(image=image)
        return image_aug

    def toTemperature(self, image, severity):
        image_aug = iaa.ChangeColorTemperature(severity)(image=image)
        return image_aug

    def toMotionBlur(self, image, severity):
        image_aug = iaa.imgcorruptlike.MotionBlur(severity=severity)(image=image)
        return image_aug

    def toDefocusBlur(self, image, severity):
        image_aug = iaa.imgcorruptlike.DefocusBlur(severity=severity)(image=image)
        return image_aug

    def toZoomBlur(self, image, severity):
        image_aug = iaa.imgcorruptlike.ZoomBlur(severity=severity)(image=image)
        return image_aug

    def toJpegCompression(self, image, severity):
        image_aug = iaa.imgcorruptlike.JpegCompression(severity=severity)(image=image)
        return image_aug

    def toPixelate(self, image, severity):
        image_aug = iaa.imgcorruptlike.Pixelate(severity=severity)(image=image)
        return image_aug

    def toGaussianNoise(self, image, severity):
        image_aug = iaa.imgcorruptlike.GaussianNoise(severity=severity)(image=image)
        return image_aug


    def drawRotaion(self, image, image_aug, bbs, bbs_aug):
        # w = image.shape[1]  # 전체 이미지 너비
        # h = image.shape[0]  # 전체 이미지 높이
        #line_size = int(((h / w) * 398) * 0.025)  # 선 두께
        line_size = int(2)  # 선 두께
        # if w > h:
        #     line_size = int(w * 0.007)
        # else:
        #     line_size = int(h * 0.007)
        image = bbs.draw_on_image(image, size=line_size, color=[0, 0, 255])
        image_aug = bbs_aug.draw_on_image(image_aug, size=line_size, color=[0, 0, 255])

        return image, image_aug

    def changeComboBoxTemperature(self):
        color_tone = self.cbb_temperature.currentText()
        if color_tone == "red":
            self.sb_temperature_value.setRange(1000, 4000)
            self.sb_temperature_value.setValue(4000)
            self.sb_temperature_value.setSingleStep(100)

        elif color_tone == "blue":
            self.sb_temperature_value.setRange(10000, 40000)
            self.sb_temperature_value.setValue(10000)
            self.sb_temperature_value.setSingleStep(1000)


    def convertQpixmap(self, image): #Qpixmap으로 변환(미리보기)
        h , w , c = image.shape
        qImg = QtGui.QImage(image.data, w, h, w * c, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        return pixmap



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(resources.icon))
    myWindow = WindowClass()

    myWindow.show()

    app.exec_()


