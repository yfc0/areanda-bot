"""
Adds async context to a Python logger.
"""
import functools
import inspect
import logging
from contextvars import ContextVar
from typing import Any, Callable

_EXTRA_TYPE = dict[str, Any]
_EXTRA_VAR = ContextVar("extra", default=dict())


class Logger:
    """
    Wrapper for a python :py:class:`logging.Logger`.

    This wrapper reads the current local context and emits
    them for each log message.
    """

    _original_get = None

    def __init__(self, name: str | None = None):
        self.base_logger = self.__class__._original_get(name)

    @classmethod
    def setup(cls):
        cls._original_get = logging.getLogger
        logging.getLogger = cls

    @classmethod
    def extra(cls):
        return _EXTRA_VAR.get()

    def _msg(self, func: Callable, msg, *args, **kwargs):
        """Log with our extra values,"""
        extra = self.extra() | kwargs.pop("extra", {})
        # Because we wrap a logging.Logger instance through 2 layers
        # of redirection, we need to add 2 to the logger's stacklevel
        # so we correctly log the logging statement's line number and function name
        original_stacklevel = kwargs.pop("stacklevel", 1)
        stacklevel = original_stacklevel + 2
        return func(msg, *args, extra=extra, stacklevel=stacklevel, **kwargs)

    def __getattr__(self, item):
        attr = getattr(self.base_logger, item)
        if item in ("debug", "info", "warning", "error", "exception", "critical"):

            def _log(*args, **kwargs):
                self._msg(attr, *args, **kwargs)

            return _log
        return attr


class log_extra:
    def __init__(self, extra=None, attr_to_label: dict[str, str] = None, *_, **kwargs):
        self.new_extra = (extra or {}) | kwargs
        self.attr_to_label = attr_to_label
        self._token = None

    def __enter__(self):
        self._token = _EXTRA_VAR.set(_EXTRA_VAR.get() | self.new_extra)

    def __exit__(self, *args, **kwds):
        try:
            _EXTRA_VAR.reset(self._token)
        except Exception:
            logging.exception("_EXTRA_VAR exception")
            pass

    def __call__(self, f: Callable | type):
        if inspect.isclass(f):
            # TODO: doesn't work?
            for attr in f.__dict__:  # there's propably a better way to do this
                _method = getattr(f, attr)
                if attr != "__init__" and callable(_method):
                    setattr(f, attr, log_extra(self.new_extra, self.attr_to_label)(_method))
            return f
        elif inspect.iscoroutinefunction(f):

            @functools.wraps(f)
            async def actual_decorator(*args, **kwargs):
                if self.attr_to_label:
                    for attr, label in self.attr_to_label.items():
                        self.new_extra[label] = getattr(args[0], attr)
                with log_extra(self.new_extra):
                    return await f(*args, **kwargs)

        else:

            @functools.wraps(f)
            def actual_decorator(*args, **kwargs):
                if self.attr_to_label:
                    for attr, label in self.attr_to_label.items():
                        self.new_extra[label] = getattr(args[0], attr)
                with log_extra(self.new_extra):
                    return f(*args, **kwargs)

        return actual_decorator
