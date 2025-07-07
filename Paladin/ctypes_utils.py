import ctypes
import platform

import numpy as np

# FUNCTYPE
if platform.system() == 'Windows':
    FUNCTYPE = ctypes.WINFUNCTYPE
elif platform.system() == 'Linux':
    FUNCTYPE = ctypes.CFUNCTYPE
else:
    raise NotImplementedError(f'Unsupported platform: {platform.system()}')


# LoadLibrary
LoadLibraryEx = np.ctypeslib.load_library

if platform.system() == 'Windows':
    LoadLibrary = ctypes.windll.LoadLibrary
elif platform.system() == 'Linux':
    LoadLibrary = ctypes.cdll.LoadLibrary
else:
    raise NotImplementedError(f'Unsupported platform: {platform.system()}')
