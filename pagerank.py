#!/usr/bin/env python
# PageRank (on memory)
# using power method

from numarray import *
from numarray.matrix import *
 
EPS = 1.0e-10

class PageRank():
    def __init__(self, adj_matrix):
        self._cnt = 0
        self._err = 0
        self._dim = adj_matrix[0].size()
        self._P = zeros( (self._dim, self._dim), Float64 )

        for i in range(self._dim):
            self._P[i,:] = adj_matrix[i] / (sum(adj_matrix[i]) * 1.0)

    def calc(self, curr, alpha):
        self._cnt = 0
        while 1:
            # iteration in power method
            self._cnt += 1
            prev = curr
            curr = alpha * dot(transpose(self._P), prev)
            curr += (1. - alpha) / (self._dim * 1.)
            self._err = self.diff(prev, curr)
            if (self._err < EPS): break
        return curr

    def diff(self, prev, curr):
        err = 0
        for i in range(self._dim):
            err += absolute(prev[i] - curr[i])
        return err


Adj = Matrix([array([0, 0, 1, 1]),
              array([0, 0, 1, 1]),
              array([1, 1, 0, 0]),
              array([0, 1, 1, 0])])

init = array([1/4., 1/4., 1/4., 1/4.])

pr = PageRank(Adj)
for alpha in [1.0, 0.8, 0.5, 0]:
    rank = pr.calc(init, alpha)
    print "###### alpha =", alpha
    print rank
    print "error:", pr._err
    print "iteration:", pr._cntarray([0, 0, 1, 1]),
