# 使用加 Attention 机制的 Encoder-Decoder 模型实现 JointSLU
该仓库的代码复现了论文 **Attention-Based Recurrent Neural Network Models for Joint Intent Detection and Slot Filling** 中提到的
Attention-based RNN 模型。代码运行的环境是：Win10 + Pytorch 0.1 + Python 3.6。

注意仓库中的 bash 脚本文件 param_select.sh, 它可用于在服务器中 GridSearch 最佳超参数组合组合之用。与之对应的是
win10 版本中没有的命令行参数 model_selection，它在脚本执行 main.py 时被设置为 True，停止在训练过程中输出各个步
骤的时间开销以及每间隔步的测试集(test)评分。但保留了每间隔步的 batch 损失以及最终开发集(dev)的评分。

使用默认数据集 atis.--.txt 的同学在选参数时可以参照我在服务器上的调参结果 server_result.txt。

## 仓库结构
文件 .gitignore 和 .editorconfig 均是用来配置仓库环境的，可以忽略。而三个大文件夹：
> + **data** 包括了训练数据、测试数据、全集数据、开发数据的默认储存地址(当命令行参数未给出时)。
> + **save** 包括了训练模型过程中保存的模型、预测数据以及 word, slot, intent 的信息。
> + **utils** 包含了本次复现需要的所有辅助代码，例如模型 model.py、训练 process.py。


而源码文件 main.py 是主程序的入口；demo.txt 包含了默认所有命令行参数时打印的输出信息(一次训练时间很长)。

## 使用说明
如果只是想看一个简单的 demo，只需 Win + R 键入 cmd 打开仓库目录下的命令行，然后输入：

    python main.py # 注意环境, 否则需要先 activate.
 
如果想调节网络参数，导入自己的数据集等，可以通过输入命令行参数即可。关于参数的具体信息可以通过命令：

    python main.py -h
    
查看。需要注意两点，一方面注意 -h 打印的提示信息，复现模型的泛化效果对参数的设定十分敏感。例如虽然支持 GPU + C-
UDA 加速，但 batch 最好不要太大。太大的 batch 会拖慢训练速度，降低泛化能力，甚至会爆掉 PC 的内存。因此，你不应该
偏离默认参数太远。另一方面，代码中有丰富的中文注释，方便您查看或者修改其中的设定，如输出延时等。

## 格式控制
复用此代码，格式是很重要的。虽然很多错误都有中文提示，下面就几个重要的格式说明一下。

##### 导入数据集
默认的数据集在相对目录 “./data/” 下。其中包含三个文件 train.txt、test.txt、dev.txt、all.txt。后者即简单的将前
三者 “拼” 起来。文件中每一行代表一个样例，依次包括句子、标注序列 slot 和目的标记 label。例如：
	
		BOS fly from boston to New York EOS O O B.City O B.City I.City Flight_Fly
		
其中，BOS 和 EOS 是占位符，且 BOS 对应了开头一个标注 O。而最后的 Flight_Fly 是目的标记，其余不言自明。因此，我们
事实上需要 word、slot 和 label 三个字典。而每轮训练后，在相对地址 “./save/alphabets” 中记录了这些字典的信息。

##### 输出预测文件
执行 main.py 除了训练模型，还有预测给定数据到文件。默认时，是输出测试集的 **n_best** 预测到目录 "./save/prediction" 中
去。比较麻烦的是，如果想导入自己的求测数据，你需要查看函数 predict 的 API 并修改 main.py 的主程序代码。

## 信息反馈
由于编写仓促，许多地方必有所不足、纰漏。还望您及时 pull request，或者联系我的邮箱：
		
		liyangming98@gmail.com

最后，开源精神万岁，非常感谢学长 @yizhen 一直以来的帮助。
