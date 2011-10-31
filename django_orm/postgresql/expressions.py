# -*- coding: utf-8 -*-

from django.db.models.expressions import F as BaseF

class F(BaseF):
    def __invert__(self):
        self._invert = True
        return self

    def evaluate(self, evaluator, qn, connection):
        result = evaluator.evaluate_leaf(self, qn, connection)
        if self._invert and len(result) == 2 and connection.vendor == 'postgresql':
            result = list(result)
            result[0] = "NOT %s" % result[0]
            result = tuple(result)

        return result
