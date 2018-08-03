# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from utils.dictionary import *
from utils.model import *

import torch
from torch.autograd import Variable


if __name__ == "__main__":
	data = Dataset(random_state=20)
	data.quick_build()

	word_dict, label_dict, intent_dict = data.get_alphabets()
	sent_batch, label_batch, seq_lens, _ = data.get_batch()

	encoder = Encoder(len(word_dict), 64, 500, 3, True)

	sent_var = Variable(torch.LongTensor(sent_batch))
	label_var = Variable(torch.LongTensor(label_batch))

	print(label_var.size())

	print(encoder(sent_var, seq_lens).size())
