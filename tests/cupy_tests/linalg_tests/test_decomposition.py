import unittest

import numpy

from cupy import cuda
from cupy import testing


@unittest.skipUnless(
    cuda.cusolver_enabled, 'Only cusolver in CUDA 8.0 is supported')
@testing.gpu
class TestCholeskyDecomposition(unittest.TestCase):

    _multiprocess_can_split_ = True

    @testing.for_dtypes([
        numpy.int32, numpy.int64, numpy.uint32, numpy.uint64,
        numpy.float32, numpy.float64])
    @testing.numpy_cupy_allclose(atol=1e-3)
    def check_L(self, array, xp, dtype):
        a = xp.asarray(array, dtype=dtype)
        return xp.linalg.cholesky(a)

    def test_decomposition(self):
        # A normal positive definite matrix
        A = numpy.random.randint(0, 100, size=(5, 5))
        A = numpy.dot(A, A.transpose())
        self.check_L(A)
        # np.linalg.cholesky only uses a lower triangle of an array
        self.check_L(numpy.array([[1, 2], [1, 9]]))


@unittest.skipUnless(
    cusolver_enabled, 'Only cusolver in CUDA 8.0 is supported')
@testing.gpu
class TestQRDecomposition(unittest.TestCase):

    _multiprocess_can_split_ = True

    @testing.for_float_dtypes(no_float16=True)
    @testing.numpy_cupy_allclose(atol=1e-5)
    def check_mode(self, array, xp, dtype, mode, index=None):
        a = xp.asarray(array, dtype=dtype)
        result = xp.linalg.qr(a, mode=mode)
        if type(result) == tuple:
            return result[index]
        else:
            return result

    def test_r_mode(self):
        self.check_mode(numpy.random.randn(2, 3), mode='r')
        self.check_mode(numpy.random.randn(3, 3), mode='r')
        self.check_mode(numpy.random.randn(4, 2), mode='r')

    def test_raw_mode(self):
        self.check_mode(numpy.random.randn(2, 4), mode='raw', index=0)
        self.check_mode(numpy.random.randn(1, 5), mode='raw', index=1)
        self.check_mode(numpy.random.randn(2, 3), mode='raw', index=0)
        self.check_mode(numpy.random.randn(4, 3), mode='raw', index=1)
        self.check_mode(numpy.random.randn(4, 5), mode='raw', index=0)
        self.check_mode(numpy.random.randn(3, 3), mode='raw', index=1)

    def test_complete_mode(self):
        self.check_mode(numpy.random.randn(2, 4), mode='complete', index=0)
        self.check_mode(numpy.random.randn(1, 5), mode='complete', index=1)
        self.check_mode(numpy.random.randn(2, 3), mode='complete', index=0)
        self.check_mode(numpy.random.randn(4, 3), mode='complete', index=1)
        self.check_mode(numpy.random.randn(4, 5), mode='complete', index=0)
        self.check_mode(numpy.random.randn(3, 3), mode='complete', index=1)

    def test_reduced_mode(self):
        self.check_mode(numpy.random.randn(2, 4), mode='reduced', index=0)
        self.check_mode(numpy.random.randn(1, 5), mode='reduced', index=1)
        self.check_mode(numpy.random.randn(2, 3), mode='reduced', index=0)
        self.check_mode(numpy.random.randn(4, 3), mode='reduced', index=1)
        self.check_mode(numpy.random.randn(4, 5), mode='reduced', index=0)
        self.check_mode(numpy.random.randn(3, 3), mode='reduced', index=1)
