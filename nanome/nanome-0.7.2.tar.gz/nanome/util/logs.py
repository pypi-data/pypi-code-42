import sys
import functools
if sys.version_info >= (3, 0):
    from ._logs_3 import _print
else:
    from ._logs_2 import _print

class Logs(object):
    _is_windows_cmd = False
    _print_type = {
        'debug': {'color': '\x1b[0m', 'msg': ''},
        'warning': {'color': '\x1b[33m', 'msg': 'Warning: '},
        'error': {'color': '\x1b[91m', 'msg': 'Error: '}
    }
    _closing = '\x1b[0m'
    __verbose = None

    @classmethod
    def _set_verbose(cls, value):
        cls.__verbose = value

    @classmethod
    def _is_verbose(cls):
        return cls.__verbose

    @classmethod
    def _print(cls, col_type, *args):
        _print(cls, col_type, args)

    @classmethod
    def error(cls, *args):
        """
        | Prints an error

        :param args: Variable length argument list
        :type args: Anything printable
        """
        cls._print(cls._print_type['error'], *args)

    @classmethod
    def warning(cls, *args):
        """
        | Prints a warning

        :param args: Variable length argument list
        :type args: Anything printable
        """
        cls._print(cls._print_type['warning'], *args)

    @classmethod
    def message(cls, *args):
        """
        | Prints a message

        :param args: Variable length argument list
        :type args: Anything printable
        """
        cls._print(cls._print_type['debug'], *args)

    @classmethod
    def debug(cls, *args):
        """
        | Prints a debug message
        | Prints only if plugin started in verbose mode (with -v argument)

        :param args: Variable length argument list
        :type args: Anything printable
        """
        if cls.__verbose == None:
            Logs.warning("Debug used before plugin start.")
            cls._print(cls._print_type['debug'], *args)
        elif cls.__verbose == True:
            cls._print(cls._print_type['debug'], *args)

    @classmethod
    def _init(cls):
        if sys.platform == 'win32' and sys.stdout.isatty():
            cls._is_windows_cmd = True

    @staticmethod
    def deprecated (new_func = None, msg = ""):
        def deprecated_decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if not wrapper.used:
                    warning = "Function " + func.__name__ + " is deprecated. "
                    if (new_func != None):
                        warning += "Try using " + new_func + " instead. "
                    warning += msg
                    Logs.warning(warning)
                    wrapper.used = True
                return func(*args, **kwargs)
            wrapper.used = False            
            return wrapper
        return deprecated_decorator

Logs._init()