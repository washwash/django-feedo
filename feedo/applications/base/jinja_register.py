registered_jinja_functions = {}


def function(*args, **kwargs):
    if kwargs:
        name = kwargs.get('name')
    else:
        name = args[0].__name__

    def register(f):
        registered_jinja_functions[name] = f
        return f

    if kwargs:
        return register
    else:
        return register(args[0])
