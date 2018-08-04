# 使用加 Attention 机制的 Encoder-Decoder 模型实现 JointSLU
该仓库的代码复现了论文 **Attention-Based Recurrent Neural Network Models for Joint Intent Detection and Slot Filling** 中提到的
Attention-based RNN 模型。代码运行的环境是：Win10 + Pytorch 0.1 + Python 3.6。


在 Win10 中如果 Pytorch 和 Python 的版本和要求不一样，可以通过 Anaconda 配置安装一个新环境。命令可以如下：

    conda create -n NewEnv python=3.6
    conda activate NewEnv
    pip install -upgrade pip
    conda install --offline pytorch-0.2.1-py36he6bf560_0.2.1cu80.tar.bz2
    
注意，参数 offline 说明你必须先预下载官方包到本地。当然你也可以通过 pip 直接在线安装，不过需要以管理员模式运行命令
行 cmd。本仓库的代码不具备很高的可复用性，但是可以根据命令行参数，按照要求的格式，选择预备好的训练集，测试集和
全集(即训练集+测试集)，调节模型的参数以 demo 论文中提到模型的效果。

## 仓库结构
文件 .gitignore 和 .editorconfig 均是用来配置仓库环境的，可以忽略。而三个大文件夹：
> + **data** 包括了训练数据，测试数据，全集数据的默认储存地址(当命令行参数未给出时)。
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
