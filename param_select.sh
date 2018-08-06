#!bin/bash

#python ./main.py -mse True

for optimizer in sgd adam adagrad;
do
	for batch in 8 16 32 64;
	do
		for lr in 0.1 0.005 0.01 0.05 0.1 0.5 1.0;
		do
			for epochs in 400 800 1600;
			do
				for worddim in 32 64 128;
				do
					for slotdim in 8 16 32 64;
					do
						for layers in 1 2 3;
						do
							for hidden in 64 128 256;
							do
								log_dir=./logs/batch_${batch}_lr_${lr}_worddim_${worddim}_slotdim_${slotdim}_layers_${layers}_hidden_${hidden}/
								mkdir -p ${log_dir}
								echo "训练参数: 优化算法 ${optimizer}"
								echo "          batch 尺寸 ${batch}"
								echo "          学习率 ${lr}"
								echo "          训练轮式 ${epochs}"
								echo "          词向量维度 ${worddim}"
								echo "          标注向量维度 ${slotdim}"
								echo "          Encoder 层数 ${layers}"
								echo "          LSTM 隐层数 ${layers}"
								echo ""
								CUDA_VISIBLE_DEVISES=3 python ./main.py -mse True -de ./data/atis.test.txt \
								-lr ${lr} \
								--num_epoch ${epochs} \
								-op ${optimizer} \
								-bs ${batch} \
								-we ${worddim} \
								-se ${slotdim} \
								-nl ${layers} \
								-hz ${hidden} &>${log_dir}/log.txt
							done
						done
					done
				done
			done
		done
	done
done
								
