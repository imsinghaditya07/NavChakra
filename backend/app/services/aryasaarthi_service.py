"""
Backward compatibility proxy module.
Re-exports everything from kisaansarthi.
"""
from backend.app.services.kisaansarthi import *
import backend.app.services.kisaansarthi as _kisaansarthi

# Forward module-level getattr
def __getattr__(name):
    return getattr(_kisaansarthi, name)
