import ctypes
import os

class CyclicListSTL:
    def __init__(self):
        dll_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "cyclic_list_stl.dll"
        )
        self.lib = ctypes.CDLL(dll_path)
        self._setup()
        self.ptr = self.lib.stl_create_list()

    def _setup(self):
        self.lib.stl_create_list.restype        = ctypes.c_void_p

        self.lib.stl_add_to_head.argtypes       = [ctypes.c_void_p, ctypes.c_int]
        self.lib.stl_add_to_head.restype        = ctypes.c_int

        self.lib.stl_add_to_tail.argtypes       = [ctypes.c_void_p, ctypes.c_int]
        self.lib.stl_add_to_tail.restype        = ctypes.c_int

        self.lib.stl_delete_head.argtypes       = [ctypes.c_void_p]
        self.lib.stl_delete_head.restype        = ctypes.c_int

        self.lib.stl_delete_by_value.argtypes   = [ctypes.c_void_p, ctypes.c_int]
        self.lib.stl_delete_by_value.restype    = ctypes.c_int

        self.lib.stl_search_value.argtypes      = [ctypes.c_void_p, ctypes.c_int]
        self.lib.stl_search_value.restype       = ctypes.c_int

        self.lib.stl_get_size.argtypes          = [ctypes.c_void_p]
        self.lib.stl_get_size.restype           = ctypes.c_int

        self.lib.stl_get_elements.argtypes      = [ctypes.c_void_p,
                                                    ctypes.POINTER(ctypes.c_int)]
        self.lib.stl_get_elements.restype       = ctypes.c_int

        self.lib.stl_clear_list.argtypes        = [ctypes.c_void_p]
        self.lib.stl_clear_list.restype         = None

        self.lib.stl_destroy_list.argtypes      = [ctypes.c_void_p]
        self.lib.stl_destroy_list.restype       = None

    def add_to_head(self, value):
        self.lib.stl_add_to_head(self.ptr, value)
        return f"[C++ STL] Added {value} to head"

    def add_to_tail(self, value):
        self.lib.stl_add_to_tail(self.ptr, value)
        return f"[C++ STL] Added {value} to tail"

    def delete_head(self):
        res = self.lib.stl_delete_head(self.ptr)
        if res == -1:
            raise ValueError("List is empty!")
        return "[C++ STL] Deleted head"

    def delete_by_value(self, value):
        res = self.lib.stl_delete_by_value(self.ptr, value)
        if res == -1:
            raise ValueError("List is empty!")
        if res == -2:
            raise ValueError(f"Element {value} not found!")
        return f"[C++ STL] Deleted: {value}"

    def search(self, value):
        res = self.lib.stl_search_value(self.ptr, value)
        if res == -1:
            raise ValueError("List is empty!")
        if res == -2:
            raise ValueError(f"Element {value} not found!")
        return f"[C++ STL] Found {value} at position {res}"

    def get_elements(self):
        size = self.lib.stl_get_size(self.ptr)
        if size == 0:
            return []
        arr = (ctypes.c_int * size)()
        self.lib.stl_get_elements(self.ptr, arr)
        return list(arr)

    def clear(self):
        self.lib.stl_clear_list(self.ptr)
        return "[C++ STL] List cleared"

    def __del__(self):
        if hasattr(self, "ptr") and self.ptr:
            self.lib.stl_destroy_list(self.ptr)