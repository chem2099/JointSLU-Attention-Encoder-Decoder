# -*- coding: utf-8 -*-
from __future__ import unicode_literals

'''
储存以单词 word 或标注 slot 或目的 intent
的字典. 支持添加, 查询等操作.
'''
class Alphabet(object):

	def __init__(self, name="new_alphabet"):

		self.name = name

		# 储存所有单词的列表.
		self.word_list = []
		# 映射 : word -> index.
		self.word2index = {}
		# 映射 : index -> word.
		self.index2word = {}

	'''
	添加单个单词或者一个列表的单词.
	'''
	def add_words(self, elems):
		if isinstance(elems, list):
			for elem in elems:
				self.add_words(elem)
		elif isinstance(elems, str):
			# 注意字典中的元素不能重复加入, 重复者被忽略.
			if elems not in self.word_list:
				self.word2index[elems] = len(self.word_list)
				self.index2word[self.word2index[elems]] = elems
				self.word_list.append(elems)
		else:
			raise Exception("加入元素必须是字符串或者字符串的列表.")

	'''
	返回所有单词的列表.
	'''
	def get_words(self):
		return self.word_list

	'''
	返回两个字典:
		1, word2index: word -> index
		2, index2word: index -> word
	'''
	def get_dicts(self):
		return self.word2index, self.index2word

	'''
	查询单个单词或者一个列表的单词.
	'''
	def indexs(self, words):
		if isinstance(words, list):
			ret_list = []
			for word in words:
				ret_list.append(self.indexs(word))

			return ret_list
		elif isinstance(words, str):
			if words not in self.word2index.keys():
				raise Exception("查询元素不在字典中.")
			else:
				return self.word2index[words]
		# 否则都不是抛出错误.
		else:
			raise Exception("查询元素必须是字符串或者字符串的列表.")

	'''
	查询单个序号对应的单词或者一个列表的序列.
	'''
	def words(self, idxs):
		if isinstance(idxs, list):
			ret_list = []
			for index in idxs:
				ret_list.append(self.words(index))

			return ret_list
		elif isinstance(idxs, int):
			return self.index2word[idxs]
		else:
			raise Exception("查询元素必须是整形 Int 或者整形的列表.")

	'''
	返回字典的名字, 它与保存数据的路径有关.
	'''
	def get_name(self):
		return self.name

	'''
	将数据保存到指定路径下, 有默认值.
	'''
	def save(self, file_dir='../save/alphabets/'):
		self.write_list(self.word_list, file_dir + self.name + '-word_list.txt')
		self.write_dict(self.word2index, file_dir + self.name + '-word2index.txt')
		self.write_dict(self.index2word, file_dir + self.name + '-index2word.txt')

	'''
	加载已缓存在硬盘上的数据到对象.
	'''
	def load(self, file_dir='../save/alphabets/'):
		self.word_list = self.read_list(file_dir + self.name + '-word_list.txt')
		self.word2index = self.read_dict(file_dir + self.name + '-word2index.txt')
		self.index2word = self.read_dict(file_dir + self.name + '-index2word.txt')

	'''
	相当于 Java 中对象 Object 的 toString 方法.
	'''
	def __str__(self):
		return "元素字典 " + self.name + " 包含以下元素: \n" + str(self.word_list) +\
			   "\n\n其中映射 元素 -> 序号 如下: \n" + str(self.word2index) +\
			   "\n\n其中映射 序列 -> 元素 如下: \n" + str(self.index2word) + '\n'

	'''
	读写文件的辅助函数.
	'''
	def write_list(self, w_list, file_path):
		with open(file_path, 'w') as fr:
			for word in w_list:
				fr.write(word + '\n')

	'''
	读写文件的辅助函数.
	'''
	def read_list(self, file_path):
		ret_list = []
		with open(file_path, 'r') as fr:
			for line in fr.readlines():
				ret_list.append(line.strip())

		return ret_list

	'''
	读写文件的辅助函数.
	'''
	def write_dict(self, dictionary, file_path):
		with open(file_path, 'w') as fr:
			for pair in dictionary.items():
				fr.write(str(pair[0]) + '\t' + str(pair[1]) + '\n')

	'''
	读写文件的辅助函数.
	'''
	def read_dict(self, file_path):
		ret_dict = {}
		with open(file_path, 'r') as fr:
			for line in fr.readlines():
				items = line.strip().split()
				try:
					ret_dict[int(items[0])] = items[1]
				except Exception :
					ret_dict[items[0]] = int(items[1])

		return ret_dict


'''
读取原始数据, 其数据格式要求文件中每行格式:

	BOS word1 word2 ... wordn EOS tag1 tag2 ... tagn intent

'''
def read_data(file_path):
	sentence_list = []
	labels_list = []
	intent_list = []

	with open(file_path, 'r') as fr:
		for line in fr.readlines():
			items = line.strip().split('EOS')

			sentence_list.append(items[0].split()[1:-1])
			labels_list.append(items[1].split()[:-1])
			intent_list.append(items[1].split()[-1])

	return sentence_list, labels_list, intent_list


'''
搭建 word, label 和 intent 的字典.
'''
def build_alphabets(sentence_list, labels_list, intent_list, name='atis', save=True):
	word_dict = Alphabet(name + '-word')
	label_dict = Alphabet(name + '-label')
	intent_dict = Alphabet(name + '-intent')

	for sentence in sentence_list:
		word_dict.add_words(sentence)
	for labels in labels_list:
		label_dict.add_words(labels)
	intent_dict.add_words(intent_list)

	word_dict.save()
	label_dict.save()
	intent_dict.save()

	return word_dict, label_dict, intent_dict

'''
构建数据集, 将列表中的字符串均换成对应的序号. 这个方法连同以上均是
普适的, 可用来构建训练集, 测试集.
'''
def build_dataset(sentence_list, labels_list, intent_list, 
				  word_dict, label_dict, intent_dict):
	sentence_list_ = []
	labels_list_ = []

	for sentence in sentence_list:
		sentence_list_.append(word_dict.indexs(sentence))
	for labels in labels_list:
		labels_list_.append(label_dict.indexs(labels))
	intent_list_ = intent_dict.indexs(intent_list)

	return sentence_list_, labels_list_, intent_list_


if __name__ == "__main__":
	a, b, c = read_data('../data/atis.all.txt')
	a_dict, b_dict, c_dict = build_alphabets(a, b, c)
	print(build_dataset(a, b, c, a_dict, b_dict, c_dict)[2])













