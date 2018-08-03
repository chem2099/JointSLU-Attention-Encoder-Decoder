# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence


'''
编码器, 其中 input_dim 是字典中词的总数.
'''
class Encoder(nn.Module):

	def __init__(self, input_dim, embedding_dim, hidden_dim, 
				 num_layers=1, bidirectional=False):
		
		super(Encoder, self).__init__()

		self.input_dim = input_dim
		self.embedding_dim = embedding_dim
		self.hidden_dim = hidden_dim
		self.num_layers = num_layers
		self.bidirectional = bidirectional

		# 如果使用双向 LSTM, 那么预设 hidden 应该除 2,
		# 否则计算量会因为 2 倍隐层而增大许多喔！
		if bidirectional:
			self.hidden_dim //= 2

		# 词嵌入矩阵, 注意是线性的.
		self.embedding = nn.Embedding(self.input_dim, self.embedding_dim)
		self.lstm = nn.LSTM(self.embedding_dim, self.hidden_dim, 
			                num_layers=self.num_layers, batch_first=True, 
			                bidirectional=self.bidirectional)

	'''
	注意, 当使用 batch 时, x 作为输入张量 (batch, sent_len, word_len) 应该
	使得 sent_len 均相同, 不足的地方用 index=0 填充. 且要求样例根据句子长短
	从大到小, 从上往下排序. 并给定一个尺度为 (batch_size, 1) 表示各个句子长度
	的向量 seq_lens.

		input: (batch_size, sentence_length, embedding_length)
		output: (batch_size, sentence_length, hidden_length)
 	'''
	def forward(self, x, seq_lens):
		# 得到连续词向量.
		embedded_x = self.embedding(x)

		# batch 打包和解包.
		packed_input = pack_padded_sequence(embedded_x, seq_lens, batch_first=True)
		lstm_out, (h_last, c_last) = self.lstm(packed_input, None)
		padded_output, _ = pad_packed_sequence(lstm_out)

		# 使用 batch_first.
		return padded_output.transpose(0, 1)













class Decoder(nn.Module):

	def __init__(self):
		pass

	def forward(self, x):
		pass
