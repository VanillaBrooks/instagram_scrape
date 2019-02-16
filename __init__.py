from py._native import ffi, lib
from . import _native


def test():
		return _native.lib.cosine_sim(["234"],['234234'], 5)
