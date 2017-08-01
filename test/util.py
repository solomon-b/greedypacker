import sys
import contextlib

@contextlib.contextmanager
def stdout_redirect(stringIO):
    sys.stdout = stringIO
    try:
        yield stringIO
    finally:
        sys.stdout = sys.__stdout__
        stringIO.seek(0)
