# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from utils.dictionary import *
from utils.model import *
from utils.process import *



if __name__ == "__main__":
	data = Dataset(random_state=20)
	data.quick_build()
	word_dict, label_dict, intent_dict = data.get_alphabets()

	encoder = Encoder(len(word_dict), 200, 128, 1, True)
	decoder = Decoder(128, 12, len(label_dict), len(intent_dict))

	train(encoder, decoder, data,"adagrad",
		  32, 1e-1,
		  800, 1, 30, 10,
		  './save/model/', None)