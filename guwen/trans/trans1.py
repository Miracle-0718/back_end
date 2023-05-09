import os
import torch
import torch.nn as nn
import re

from trans.infer_config import  config
from trans.net import zh_tokenizer,TranslationModel,PositionalEncoding

device = config['device']
max_length = config['max_length']
gu_vocab_file = config['gu_vocab_file']
xian_vocab_file = config['xian_vocab_file']
model_path = config['model_path']

def translate(model,src_vocab,tgt_vocab,src: str):
    """
    :param src_vocab: 源语言词典
    :param tgt_vocab: 目标语言词典
    :param src: 源句子
    :return: 翻译后的句子
    """

    # 将与原句子分词后，通过词典转为index，然后增加<bos>和<eos>
    src = torch.tensor([0] + src_vocab(zh_tokenizer(src)) + [1]).unsqueeze(0).to(device)
    # 首次tgt为<bos>
    tgt = torch.tensor([[0]]).to(device)
    # 一个一个词预测，直到预测为<eos>，或者达到句子最大长度
    for i in range(max_length):
        # 进行transformer计算
        out = model(src, tgt)
        # 预测结果，因为只需要看最后一个词，所以取`out[:, -1]`
        predict = model.predictor(out[:, -1])
        # 找出最大值的index
        y = torch.argmax(predict, dim=1)
        # 和之前的预测结果拼接到一起
        tgt = torch.concat([tgt, y.unsqueeze(0)], dim=1)
        # 如果为<eos>，说明预测结束，跳出循环
        if y == 1:
            break
    # 将预测tokens拼起来
    tgt = ''.join(tgt_vocab.lookup_tokens(tgt.squeeze().tolist())).replace("<s>", "").replace("</s>", "")
    return tgt

def adjust_sentence(sentence,max_length = max_length-2):
    '''
    长句子调整算法，分割满足模型识别长度需求的多个子句
    :param sentence: str sentences
    :return: list of sentences (len <=maxlength 要去掉开始和结束符)
    '''
    subs = re.split("[，。；：]", sentence) #先根据标点符号分隔成子句
    new_subs = []
    i = 0
    while i < len(subs):
        # 如果是没有标点符号的单个长子句
        if len(subs[i]) > max_length:
            templist = re.findall(r'.{'+str(max_length)+'}', subs[i]) #至极按照模型最大长度分割
            new_subs.extend(templist)
            if len(subs[i]) > len(templist)*max_length: #剩余字符也加入
                new_subs.append(subs[i][len(templist)*max_length:])
        # 子句等于最大长度则不用处理
        elif len(subs[i]) == max_length:
            new_subs.append(subs[i])
        # 对于短子句：在保证不超过最大长度的条件下尽量拼接
        else:
            temp = subs[i]
            for j in range(i+1,len(subs)):
                if len(temp)+len(subs[j])+1 <= max_length:
                    temp += '，'+ subs[j]
                    i += 1
                else:
                    break
            new_subs.append(temp)
        i += 1
    return new_subs

def text_trans(text):
    '''
    :param text: str sentence join with '\n'
    :return: list result_list
    '''
    sentences = text.split('\n')
    #load model
    if os.path.exists(gu_vocab_file):
        gu_vocab = torch.load(gu_vocab_file, map_location="cpu")
    if os.path.exists(xian_vocab_file):
        xian_vocab = torch.load(xian_vocab_file, map_location="cpu")
    model = torch.load(model_path,map_location=torch.device('cpu'))
    model = model.eval()

    #translate sent by sent
    results = []
    for sentence in sentences:
        if len(sentence) <= max_length-2:
            results.append(translate(model, gu_vocab, xian_vocab, sentence))
        else:
            results.extend([translate(model, gu_vocab, xian_vocab, sub_sent)
                            for sub_sent in adjust_sentence(sentence)])
    return results

if __name__ == "__main__":
    test_text = '哈哈哈哈\n121231asjgfkagfakasdh\n政通人和，百废待兴，欲重修岳阳，增其旧制'
    print(text_trans(test_text))

