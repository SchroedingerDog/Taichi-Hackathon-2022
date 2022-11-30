# Taichi Hackathon 2022 项目设计

## 团队名：
民以观音土为天
## 项目名：
《马尔科夫链蒙特卡洛法对氢原子波函数采样生成电子云图像》
## 项目介绍：
&emsp;&emsp;对于高维参数的样本点进行采样，普通的接受-拒绝采样法效率是很低的。而类氢原子的电子云分布就是一个由空间波函数决定的三维参数抽样点。  

$$\begin{aligned} (r, \theta, \phi) &\sim \mathcal{J} \vert {\Psi_{nlm}} \vert ^2 \\ 
\mathcal{J} &= r^2\sin{\theta} \end{aligned}$$  

三维波函数![Wave function 3D illustration](/pic/eigenstate_4_3_1.png)
&emsp;&emsp;MCMC是一种自适应建议分布的重要性采样过程，建议分布在每抽样出一个点后都会自适应改变，每一步的接受与拒绝都会影响下一步的采样  

![MCMC and Adaptive Proposals](/pic/ImportanceAndMCMC.png)
马尔科夫链达到稳态分布即是目标分布。
![Markov chain Monte Carlo sampling using random walk](/pic/MarkovChainAndRandomWalk.png)