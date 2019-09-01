import simpleeval
import operator as op
import random
import funcy
from .errors import Stop

def evaluate(expression, variables):
    names = {
        **simpleeval.DEFAULT_NAMES,
        'data': variables,
    }
    def update(x, y):
        op.setitem(variables, x, y)
        return ''
        
    functions = dict(
        **simpleeval.DEFAULT_FUNCTIONS,
        update=update,
        print=print,
        choice=random.choice,
        stop=funcy.raiser(Stop),
    )
    evaluator_class = simpleeval.EvalWithCompoundTypes(
        names=names, functions=functions)
    try:
        res = evaluator_class.eval(expression)
        # print(res)
        return res
    except Exception as e:
        raise e from None
