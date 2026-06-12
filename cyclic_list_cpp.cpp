// cyclic_list_cpp.cpp
// Компиляция через Developer Command Prompt:
// cl /LD /EHsc /O2 cyclic_list_cpp.cpp /Fe:cyclic_list_cpp.dll

#ifdef _WIN32
    #define EXPORT __declspec(dllexport)
#else
    #define EXPORT __attribute__((visibility("default")))
#endif

#include <cstdlib>

struct Node {
    int data;
    Node* next;
};

struct CyclicList {
    Node* tail;
    int size;
};

extern "C" {

EXPORT CyclicList* create_list() {
    CyclicList* list = new CyclicList();
    list->tail = nullptr;
    list->size = 0;
    return list;
}

EXPORT int add_to_head(CyclicList* list, int value) {
    Node* node = new Node();
    node->data = value;
    if (list->tail == nullptr) {
        list->tail = node;
        node->next = node;
    } else {
        node->next = list->tail->next;
        list->tail->next = node;
    }
    list->size++;
    return 0;
}

EXPORT int add_to_tail(CyclicList* list, int value) {
    Node* node = new Node();
    node->data = value;
    if (list->tail == nullptr) {
        list->tail = node;
        node->next = node;
    } else {
        node->next = list->tail->next;
        list->tail->next = node;
        list->tail = node;
    }
    list->size++;
    return 0;
}

EXPORT int delete_head(CyclicList* list) {
    if (list->tail == nullptr) return -1;
    if (list->size == 1) {
        delete list->tail;
        list->tail = nullptr;
    } else {
        Node* head = list->tail->next;
        list->tail->next = head->next;
        delete head;
    }
    list->size--;
    return 0;
}

EXPORT int delete_by_value(CyclicList* list, int value) {
    if (list->tail == nullptr) return -1;
    Node* curr = list->tail->next;
    Node* prev = list->tail;
    for (int i = 0; i < list->size; i++) {
        if (curr->data == value) {
            if (list->size == 1) {
                delete curr;
                list->tail = nullptr;
            } else if (curr == list->tail) {
                prev->next = curr->next;
                list->tail = prev;
                delete curr;
            } else {
                prev->next = curr->next;
                delete curr;
            }
            list->size--;
            return 0;
        }
        prev = curr;
        curr = curr->next;
    }
    return -2;
}

EXPORT int search_value(CyclicList* list, int value) {
    if (list->tail == nullptr) return -1;
    Node* curr = list->tail->next;
    for (int i = 0; i < list->size; i++) {
        if (curr->data == value) return i;
        curr = curr->next;
    }
    return -2;
}

EXPORT int get_size(CyclicList* list) {
    return list->size;
}

EXPORT void get_elements(CyclicList* list, int* arr) {
    if (list->tail == nullptr) return;
    Node* curr = list->tail->next;
    for (int i = 0; i < list->size; i++) {
        arr[i] = curr->data;
        curr = curr->next;
    }
}

EXPORT void clear_list(CyclicList* list) {
    if (list->tail == nullptr) return;
    Node* curr = list->tail->next;
    int n = list->size;
    for (int i = 0; i < n; i++) {
        Node* tmp = curr;
        curr = curr->next;
        delete tmp;
    }
    list->tail = nullptr;
    list->size = 0;
}

EXPORT void destroy_list(CyclicList* list) {
    clear_list(list);
    delete list;
}

} // extern "C"