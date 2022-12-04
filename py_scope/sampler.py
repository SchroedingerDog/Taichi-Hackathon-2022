import numpy as np
from scipy.stats import norm, truncnorm
from sympy.physics.hydrogen import R_nl, Psi_nlm

# from sympy.abc import r, theta, phi
import matplotlib.pyplot as plt

plt.style.use(["ggplot", "notebook", "grid"])
# print(plt.style.available)


class AcceptanceRejection_1D:
    """
    --------------------------------------------
    Description:
        Rejection sampling algorithm for 1-d variables.

    --------------------------------------------
    Attributes:
        f:   callable -> The desired distribution.
        q:   callable -> The proposal distribution.
        rvs: callable -> Generate candidate random variables subject to q.
        m:   float    -> The magnification to q.
        N:   int      -> The times of sampling.
    """

    np.random.seed(0)  # 0表示种子只有一个，故每次随机值不再变化

    def __init__(
        self,
        desired: "callable",
        proposal: "callable",  # must be pdf
        candidates: "callable",
        magnify: float,  # m * q >= f
        shots: int,
    ):
        self.f = desired
        self.q = proposal
        self.rvs = candidates  # input an int number and return RandomVariables
        self.m = magnify
        self.N = shots

    @property
    def implement(self):
        X = self.rvs(self.N)  # generate q distribution candidate points
        F = self.f(X)
        Q = self.q(X)
        alpha = F / (self.m * Q)  # f ~ m*q likely
        U = np.random.rand(self.N)
        boolean = alpha >= U
        A = X[boolean]  # accepted
        R = X[~boolean]  # rejected
        beta = A.size / self.N  # acceptance rate

        # 以下参数是为了画出取舍示意图 #
        wrap = U * self.m * Q  # np.random.uniform(low=0, high=m*q(X), size=shots)
        wrap_A = wrap[boolean]
        wrap_B = wrap[~boolean]
        return A, R, beta, wrap_A, wrap_B

    def plot_comparison(self, x_min, x_max):
        xs = np.linspace(x_min, x_max, 1_000_000)
        acc, rej, rate, mq_acc, mq_rej = self.implement
        fig = plt.figure(figsize=(16, 8), num="f & m*q")
        fig.suptitle("Acceptance-Rejection Sampling")

        ax1 = plt.subplot(221)
        ax1.plot(xs, self.f(xs), label=r"$f$")
        ax1.plot(xs, self.q(xs), label=r"$q$")
        ax1.plot(xs, self.m * self.q(xs), label=r"$m \times q$")
        ax1.legend(loc="upper right", fontsize=8, ncol=2)

        ax2 = plt.subplot(222)
        ax2.plot(xs, self.f(xs), "k", label=r"$f$")
        ax2.plot(xs, self.m * self.q(xs), "g--", label=r"$m \times q$")
        ax2.scatter(acc, mq_acc, color="r", alpha=0.4, label="accept")
        ax2.scatter(rej, mq_rej, color="grey", alpha=0.2, label="reject")
        ax2.legend(loc="upper right", fontsize=8, ncol=2)

        ax3 = plt.subplot(212)
        ax3.hist(acc, bins=60, density=True, label=r"$sampled$")

        plt.tight_layout()
        plt.show()


class MetropolisHasting_1D:
    """
    --------------------------------------------
    Description:
        Metropolis Hasting algorithm for 1-d variables sampling.

    --------------------------------------------
    Attributes:
        f: callable -> The desired distribution.
        q: callable -> The transition pdf T(i, j).
        rvs: callable -> A random walker which generates a new candidate.
    """

    def __init__(
        self,
        desired: "callable",
        proposal: "callable",
        candidates: "callable",
        shots: int,
    ):
        self.f = desired
        self.q = proposal  # (un)symmetrical transition pdf q(x_i -> x_j)
        self.rvs = candidates  # input RandomVariable[i] return RandomVariable[j]
        self.N = shots

    def random_walk(self, x_now):
        """
        --------------------------------------------
        method-1: sample a candidate from the proposal distribution q .
                -> x_next = norm.rvs(loc=x_now, scale=1)

        --------------------------------------------
        method-2: movement .
                -> x_next = x_now + sigma * np.random.randn()
        """
        x_next = self.rvs(x_now)
        return x_next

    def implement(self, x_min, x_max):
        """
        --------------------------------------------
        method-1: 新建高维数组，逐元素修改
                -> chain = np.ndarray((self.N,), np.float64)

        --------------------------------------------
        method-2: 新建空数组，逐步扩增
                -> chain = [x_start]
        """
        num_accept = 0
        x_start = np.random.uniform(low=x_min, high=x_max)  # initialize x0
        chain = [x_start]
        for _ in range(self.N):
            x_now = chain[-1]
            x_next = self.random_walk(x_now)
            alpha = min(
                1,
                (self.f(x_next) * self.q(x_now, x_next))
                / (self.f(x_now) * self.q(x_next, x_now)),
            )  # calculate probability of accepting the new candidate
            if np.random.random() < alpha:  # 其实random必然小于1，所以alpha不需要取min
                chain.append(x_next)
                num_accept += 1
            else:
                chain.append(x_now)
        return chain, num_accept

    def plot_comparison(self, x_min, x_max):
        xs = np.linspace(x_min, x_max, self.N)
        samples, _ = self.implement(x_min, x_max)
        fig = plt.figure(figsize=(16, 8), num="MCMC sampler")
        fig.suptitle("Markov-Chain Monte Carlo Sampling")

        ax1 = plt.subplot(111)
        fs = [self.f(x) for x in xs]
        ax1.plot(xs, fs, label=r"$f$")
        ax1.hist(samples, bins=60, density=True, label=r"$sampled$")
        ax1.legend(loc="upper right", fontsize=8, ncol=2)

        plt.tight_layout()
        plt.show()
