from benchopt import BaseSolver
from benchopt import safe_import_context
from benchopt.utils.stream_redirection import SuppressStd

with safe_import_context() as import_ctx:
    import numpy as np
    from scipy.optimize.__nnls import nnls


class Solver(BaseSolver):
    name = 'scipy'

    install_cmd = 'conda'
    requirements = ['scipy']

    def set_objective(self, X, y, fit_intercept=False):
        self.X, self.y = X, y
        self.fit_intercept = fit_intercept

    def run(self, n_iter):
        m, n = self.X.shape

        w = np.zeros((n,))
        zz = np.zeros((m,))
        index = np.zeros((n,), dtype=int)

        out = SuppressStd()
        try:
            with out:
                self.w, _, _ = nnls(
                    self.X, m, n, self.y, w, zz, index, n_iter+1)
        except BaseException:
            print(out.output)
            raise

    def get_result(self):
        return self.w
