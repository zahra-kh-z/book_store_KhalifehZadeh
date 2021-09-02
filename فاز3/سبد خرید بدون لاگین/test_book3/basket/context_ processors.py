from .basket import Basket

"""
A context processor is a Python function that takes the request object as an
argument and returns a dictionary that gets added to the request context. 
Context processors come in handy when you need to make something available globally to all templates.
With it, you will be able to access the cart in any template.
"""


def basket(request):
    return {'basket': Basket(request)}
