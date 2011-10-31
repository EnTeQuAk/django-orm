# -*- coding: utf-8 -*-

from django.db.models.expressions import F as BaseF

class F(BaseF):
    _invert = False

    def __invert__(self):
        self._invert = True
        return self

    def evaluate(self, evaluator, qn, connection):
        result = list(evaluator.evaluate_leaf(self, qn, connection))
        if self._invert:
            result[0] = "NOT %s" % result[0]
        return tuple(result)
