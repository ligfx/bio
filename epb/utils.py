import inspect

def require_kw(kwargs, key):
	try:
		return kwargs[key]
	except KeyError:
		raise TypeError("%s() requires '%s' keyword argument" % (inspect.stack()[1][3], key))