#%% [markdown]
# 1. 机器学习主要用在什么特点的常见情况下。
# * 难以设定合适的规则来解决问题，待解决的问题存在某个潜在pattern可以作为参考。
# * 能收集到足够大的相关数据。

#%% [markdown]
# 2. 提出3个你认为使用了机器学习方法的场景
# * 自动翻译软件

#%% [markdown]
# 3. 提出3个你认为可以使用机器学习但还没有使用机器学习的场景。

#%% [markdown]
# 4. 什么是“模型”？ 为什么说“All models are wrong, but some useful”。
# * 模型是一种对现实问题抽象化的方式
# * 不存在适用于一切场景的模型，在某场景的下表现良好的模型在更换场景后也许会表现不佳，特定场景下应当专门训练适用模型。
 
#%% [markdown]
# 5. classification 和 Regression 主要针对什么？有什么区别？
# * classification 和 Regression是监督学习任务中的两种经典模式。
# * classification面向分类(离散)问题，模型输出一般为离散值来表示类别。Regression面向预测问题，模型输出一般为一个Scala。

#%% [markdown]
# 5. precision， recall，f1, auc 分别是什么意思？ 假设一个城市有 10000 人，有 30 个犯罪分子，
# 警察抓到了 35 个人，其中 20 个是犯罪分子，请问这个警察的 precision, recall, f1,auc 分别是什么？
# * Precision: $\frac{TP}{TP+FP}$，即真实的正例占所有预测正例的比例。
# * Recall: $\frac{TP}{TP + FN}$，即预测出的正例占所有正例比例。
# * AUC: ROC-AUC, ROC曲线与坐标轴形成的面积，其中坐标轴分别为TPR和FPR，在这里面积越大说明TPR在尽可能接近1，FPR在接近0。
# 
# * Precision: $\frac{20}{35}=\frac{4}{7}$
# * Recall: $\frac{20}{30}=\frac{2}{3}$
# * AUC: 在这里ROC曲线上只有一个点： 
#   * 即$TPR = Recall=\frac{2}{3}$
#   * $FPR = \frac{35-20}{35-20 + 10000-30} = \frac{15}{9975}=\frac{1}{665}$
#   * $ROC-AUC = \frac{1661}{1995}$


#%% [markdown]
# 6. 请提出两种场景，在第一种场景下，对模型的评估很注重precision,第二种很注重recall。
# * 重视Precision的时候一般是犯错成本比较高，例如虚假账户检测，目的是为降低服务运营成本，但若错将用户归为虚假账户而删除会引发一系列服务稳定问题，所以要求选择时不可错选。
# * 重视Recall的时候一般是遗漏成本较高，在疾病诊断中，遗漏一例潜在病毒携带者将会引发更大危机，所以倾向模型尽可能将所有正例找出来。

#%% [markdown]
# 7. 什么是Overfitting，什么是underfitting
# * Overfitting: 模型对训练集中特征拟合过深而造成在测试集上泛华能力下降。
# * Underfitting: 模型应为缺少特征或拟合不充分而在训练集上达不到理想的拟合程度。


#%% [markdown]
# 8. Lazy-learning, lazy在哪里？

#%% [markdown]
# 9. Median, mode, mean 分别是什么？有什么意义？
# Mean: 平均数, 反映样本中数据平均水平。
# Median: 中位数，反应样本中处于大小中间位置的数。
# Mode: 众数，样本中数量最多的样本点。
#

#%% [markdown]
# 10. Outliers 是什么？如何定义？

#%% [markdown]
# 11. Bias和Variance有什么关系?他们之间为什么是一种tradeoff的
# 根据Bias-Variance Decomposition, 模型的残差（error）可由Bias和Variance构成，其中Bias指的是模型对样本预测的偏差，Variance指的是模型的自身的方差。
# 一般当我们通过添加参数等使模型对样本的偏差降低时，也代表着模型的方差在增大，同样会使得残差变大。而当通过降低参数个数来减小模型方差时，有可能会导致模型对样本
# 解释性弱而使结果产生偏差。

#%% [markdown]
# 12. Train, Validation, test 数据集之间是什么关系？为什么要这么划分?

#%% [markdown]
# 13. Supervised Learning 中的supervise体现在什么地方。

#%% [markdown]
# 14. Linear Regression中什么是线性关系？
# Linear Regression中因变量$y$与要求的$\beta$满足线性关系。

#%% [markdown]
# 15. Linear Regression 中，Loss函数是怎么定义的？为什么要写成这样？什么是凸函数？优化中有什么意义？
# * Loss函数为squared error, $loss = \frac{1}{N}\sum_{i=1}^N(y_i-\hat{y}_i)^2$。
# * 根据linear regression定义, 目的是找一条曲线来使尽可能使所有$(y_i-\hat{y}_i)$最小，
#    而采用平方形式可以保证当函数收敛到最小值时，梯度会适应性地变小从而更易收敛，而且该形式也为凸函数所以一定存在最小值。
# * 凸函数$f(x)$满足 $f(\alpha x+(1-\alpha)y) \leq \alpha f(x) + (1-\alpha)f(y)\ \forall x,y \in Def(f)$.
# * 根据定义，凸函数存在理论最小值可以保证loss function收敛从而获得最优模型。

#%% [markdown]
# 16.简述Gradient Descent的过程，以 $y = -10 * x^2 + 3x + 4 $ 为例，从一个任一点 $ x = 10 $ 开始，如果根据 Gradient Descent 找到最值。 

#%% [markdown]
# 17. 一般在机器学习数量时，会做一个预处理（Normalization）， 简述 Normalization 的过程，以及数据经过 Normalization之后的平均值和标准差的情况。

#%% [markdown]
# 18. Logistic Regression 中的Logistic是什么曲线，被用在什么地方？

#%% [markdown]
# 19. Logistic Regression的Loss函数Cross-entropy是怎样的形式？有什么意义？