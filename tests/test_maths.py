from src.utils.maths import Gaussian
import unittest


class TestGaussian(unittest.TestCase):
    def test_gaussian_multiply_throws_type_error(self):
        # given
        x = Gaussian()
        y = 3

        # when, then
        with self.assertRaises(TypeError):
            x * y

    def test_gaussian_multiply(self):
        # given
        x = Gaussian(pi=3, tau=4)
        y = Gaussian(pi=5, tau=6)

        # when
        z = x * y

        # then
        self.assertEqual(z.tau, x.tau+y.tau)
        self.assertEqual(z.pi, x.pi+y.pi)

    def test_gaussian_divide(self):
        # given
        x = Gaussian(pi=4, tau=8)
        y = Gaussian(pi=2, tau=2)

        # when
        z = x / y

        # then
        self.assertEqual(z.tau, x.tau - y.tau)
        self.assertEqual(z.pi, x.pi - y.pi)

    def test_gaussian_divide_throws_type_error(self):
        # given
        x = Gaussian()
        y = 3

        # when, then
        with self.assertRaises(TypeError):
            x / y
