#%% [markdown]
# 1. We are seeking a formula that will be generalized to multiple cases instead of one specific task.
# 2. The whole process is inefficient with huge uncertainty. And we are impossible tp be aware of the ranges of coefficients before training the model. 
# 3. Yeah, 2nd would be better. Since the directions were hard-coded, disadvantages might be it will be hard to make it work in high-dimension feature space. 
# 4. Gradient is an ideal way to determine the direction in which the coefficients should be updated. 
#    It provide a direction where the loss will decrease fastest with respect ot coefficients, so-called steepest descent.
# 5. Suppose we have a known loss function, gradient refer to the derivative of loss w.r.t parameters and descent refer to the loss will decrease in a steepest descent direction.
# 6. The 3rd method is adaptive and generalized to more types of tasks compared to the previous 2 methods.
# 7. The essence of ML is optimization. We simply setup a objective (loss function) and samples (training data) and let the function converge to get the optimized parameters.