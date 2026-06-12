// cyclic_list_stl.cpp
// Компиляция через Developer Command Prompt:
// cl /LD /EHsc /O2 cyclic_list_stl.cpp /Fe:cyclic_list_stl.dll

#include <vector>
#include <algorithm>

#ifdef _WIN32
    #define EXPORT __declspec(dllexport)
#else
    #define EXPORT __attribute__((visibility("default")))
#endif

// Структура: симулируем циклический список через std::vector
// head_index указывает на "голову" (первый элемент)
struct STLCyclicList {
    std::vector<int> data;
    // vector хранит элементы в порядке от head до tail
    // data[0] = head, data[size-1] = tail
};

extern "C" {

EXPORT STLCyclicList* stl_create_list() {
    return new STLCyclicList();
}

EXPORT int stl_add_to_head(STLCyclicList* list, int value) {
    list->data.insert(list->data.begin(), value);
    return 0;
}

EXPORT int stl_add_to_tail(STLCyclicList* list, int value) {
    list->data.push_back(value);
    return 0;
}

EXPORT int stl_delete_head(STLCyclicList* list) {
    if (list->data.empty()) return -1;
    list->data.erase(list->data.begin());
    return 0;
}

EXPORT int stl_delete_by_value(STLCyclicList* list, int value) {
    if (list->data.empty()) return -1;
    auto it = std::find(list->data.begin(), list->data.end(), value);
    if (it == list->data.end()) return -2;
    list->data.erase(it);
    return 0;
}

EXPORT int stl_search_value(STLCyclicList* list, int value) {
    if (list->data.empty()) return -1;
    auto it = std::find(list->data.begin(), list->data.end(), value);
    if (it == list->data.end()) return -2;
    return (int)std::distance(list->data.begin(), it);
}

EXPORT int stl_get_size(STLCyclicList* list) {
    return (int)list->data.size();
}

EXPORT int stl_get_elements(STLCyclicList* list, int* arr) {
    int n = (int)list->data.size();
    for (int i = 0; i < n; i++) {
        arr[i] = list->data[i];
    }
    return n;
}

EXPORT void stl_clear_list(STLCyclicList* list) {
    list->data.clear();
}

EXPORT void stl_destroy_list(STLCyclicList* list) {
    delete list;
}

} // extern "C"