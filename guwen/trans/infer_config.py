import torch
import os
from pathlib import Path

data_path = Path(os.path.dirname(os.path.abspath(__file__))) / 'data' #获取当前文件所在文件夹的绝对路径/data

config = {
    'device': torch.device('cuda:0' if torch.cuda.is_available() else 'cpu'),
    # 定义句子最大长度，如果句子不够这个长度，则填充，若超出该长度，则裁剪
    'max_length': 20,

    # 模型目录，训练好的模型会放在该目录下
    'model_path' : data_path / 'model_87000.pt',

    # 字典数据文件路径
    'gu_vocab_file' : data_path / 'vocab_gu.pt',
    'xian_vocab_file' : data_path / 'vocab_xian.pt',

    'max_length' : 20,

    #句子总数量
    'row_count' : 967255,
}