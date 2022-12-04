from sympy import Symbol, lambdify, integrate, conjugate, pi, oo, sin, cos
from sympy.physics.hydrogen import R_nl, Psi_nlm
import numpy as np


class Shapes:
    """
    shape 1 -> prob_radius 氢原子径向波函数
    shape 2 -> hybird_wave 不稳定初始波形
    shape 3 -> multi_peaks 多峰分布
    shape 4 -> wavefunc_polar {r, theta}平面的氢原子波函数
    """

    @staticmethod
    def prob_radius(rd) -> float:
        n, l = 5, 0
        wf = lambdify("r", R_nl(n, l, "r"), "numpy")
        if rd < 0:
            return 0.0
        else:
            return rd**2 * wf(rd) ** 2

    @staticmethod
    def hybrid_wave(x):
        v, d, t = 0.8, 0.4, 0
        amp = (
            np.exp(-((x - 5.5 - v * t) ** 2) / d)
            + np.heaviside(x - 1 - v * t, 0.5) * np.heaviside(-(x - 2 - v * t), 0.5)
            + np.minimum(np.maximum(x - 3 - v * t, 0), np.maximum(-(x - 4 - v * t), 0))
        )
        return amp

    @staticmethod
    def multi_peaks(x):
        return np.exp(-(x**2) / 5) * (
            3 * np.cos(x) ** 2 * np.sin(4 * x) ** 2 + 2 * np.sin(6 + x) ** 2
        )

    @staticmethod
    def wavefunc_polar(rd, th) -> float:
        n, l, m = 2, 0, 0
        wf = lambdify(
            ["r", "phi", "theta"], Psi_nlm(n, l, m, "r", "phi", "theta"), "numpy"
        )
        print(wf(rd, 0, np.pi / 3))


if __name__ == "__main__":
    Shapes.wavefunc_polar(1, np.pi / 3)
