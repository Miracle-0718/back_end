from PIL import Image
from PIL import ImageDraw
import numpy as np
import os
from cnstd import CnStd
from cnocr import CnOcr
import zhconv #繁简体转换库

# 使用现有的paddle检测模型
cn_std = CnStd(model_name='ch_PP-OCRv3_det')
cn_ocr = CnOcr(rec_model_name='chinese_cht_PP-OCRv3')
base_path = os.path.abspath(os.path.join(os.getcwd())) #以manage.py文件为标准

def img_detect(img_name):
    img = Image.open(base_path+'/img/unRecImg/'+img_name)
    box_infos = cn_std.detect(img)
    #绘制检测结果并保存
    for box_info in box_infos['detected_texts']:
        detect_box = box_info['box']
        draw = ImageDraw.Draw(img)  # 在上面画画
        rect = np.hstack((detect_box[2], detect_box[0]))
        draw.rectangle(rect, outline=(255, 0, 0))  # [左上角x，左上角y，右下角x，右下角y]，outline边框颜色
    save_fp = '/img/DetImg/'+img_name
    img.save(base_path+save_fp)
    return box_infos

def img_rec(img_name):
    box_infos = img_detect(img_name)
    text = []
    score = []
    for box_info in box_infos['detected_texts']:
        cropped_img = box_info['cropped_img']
        ocr_res = cn_ocr.ocr_for_single_line(cropped_img)
        text.append(ocr_res['text'])
        score.append(ocr_res['score'])

    text = '\n'.join(text) #list->string
    score = float(np.average(score)*100) #list->float
    return text,score

def convet_fan2jian(text):
    '''繁体字转简体字'''
    return zhconv.convert(text,'zh-cn')

if __name__ == "__main__":
    base_path = os.path.abspath(os.path.join(os.getcwd(), "../.."))
    img_detect('20230504184539.png')
    print("detect finish.")