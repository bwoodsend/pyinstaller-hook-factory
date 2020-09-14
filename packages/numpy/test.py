import numpy as np

np.random.seed(0)

M = np.eye(5) + np.random.uniform(-.5, .5)
assert np.allclose(np.linalg.inv(M) @ M, np.eye(5))
eigen_values, eigen_vectors = np.linalg.eigh(M)
assert np.allclose(M @ eigen_vectors, eigen_vectors * eigen_values)

x, y = np.arange(5), [5, 2, 1, 2, 5]
poly = np.polynomial.Polynomial.fit(x, y, 2)
assert np.allclose(poly.coef, [1, 0, 4])
assert np.allclose(poly(x), y)

print("ok")
