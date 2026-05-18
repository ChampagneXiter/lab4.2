# ============================================================
# Обёртка для C++ модуля через ctypes
# ============================================================

import ctypes
import os

class CyclicListCPP:
    def __init__(self):
        dll_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "cyclic_list_cpp.dll"
        )
        self.lib = ctypes.CDLL(dll_path)
        self._setup()
        self.ptr = self.lib.create_list()

    def _setup(self):
        self.lib.create_list.restype       = ctypes.c_void_p
        self.lib.add_to_head.argtypes      = [ctypes.c_void_p, ctypes.c_int]
        self.lib.add_to_head.restype       = ctypes.c_int
        self.lib.add_to_tail.argtypes      = [ctypes.c_void_p, ctypes.c_int]
        self.lib.add_to_tail.restype       = ctypes.c_int
        self.lib.delete_head.argtypes      = [ctypes.c_void_p]
        self.lib.delete_head.restype       = ctypes.c_int
        self.lib.delete_by_value.argtypes  = [ctypes.c_void_p, ctypes.c_int]
        self.lib.delete_by_value.restype   = ctypes.c_int
        self.lib.search_value.argtypes     = [ctypes.c_void_p, ctypes.c_int]
        self.lib.search_value.restype      = ctypes.c_int
        self.lib.get_size.argtypes         = [ctypes.c_void_p]
        self.lib.get_size.restype          = ctypes.c_int
        self.lib.get_elements.argtypes     = [ctypes.c_void_p,
                                              ctypes.POINTER(ctypes.c_int)]
        self.lib.clear_list.argtypes       = [ctypes.c_void_p]
        self.lib.destroy_list.argtypes     = [ctypes.c_void_p]

    def add_to_head(self, value):
        self.lib.add_to_head(self.ptr, value)
        return f"[C++] Added {value} to head"

    def add_to_tail(self, value):
        self.lib.add_to_tail(self.ptr, value)
        return f"[C++] Added {value} to tail"

    def delete_head(self):
        res = self.lib.delete_head(self.ptr)
        if res == -1:
            raise ValueError("List is empty!")
        return "[C++] Deleted head"

    def delete_by_value(self, value):
        res = self.lib.delete_by_value(self.ptr, value)
        if res == -1:
            raise ValueError("List is empty!")
        if res == -2:
            raise ValueError(f"Element {value} not found!")
        return f"[C++] Deleted: {value}"

    def search(self, value):
        res = self.lib.search_value(self.ptr, value)
        if res == -1:
            raise ValueError("List is empty!")
        if res == -2:
            raise ValueError(f"Element {value} not found!")
        return f"[C++] Found {value} at position {res}"

    def get_elements(self):
        size = self.lib.get_size(self.ptr)
        if size == 0:
            return []
        arr = (ctypes.c_int * size)()
        self.lib.get_elements(self.ptr, arr)
        return list(arr)

    def clear(self):
        self.lib.clear_list(self.ptr)
        return "[C++] List cleared"

    def __del__(self):
        if hasattr(self, "ptr") and self.ptr:
            self.lib.destroy_list(self.ptr)