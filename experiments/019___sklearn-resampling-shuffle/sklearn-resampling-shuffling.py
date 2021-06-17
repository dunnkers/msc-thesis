import numpy as np
from fseval.pipeline.resample import Resample

r = Resample(name="bootstrap", replace=True, sample_size=1.00)
X = r.transform(np.array([[1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3]]))
print(X)


"""
Conclusion:

sklearn.preprocessing.resample does not shuffle the **features**: only the rows.

"""
