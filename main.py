import tkinter as tk
from tkinter import messagebox
from cyclic_list import CyclicList

# Пытаемся импортировать C++ Dynamic модуль
try:
    from cyclic_list_cpp import CyclicListCPP
    CPP_AVAILABLE = True
    CPP_ERROR = ""
except Exception as e:
    CPP_AVAILABLE = False
    CPP_ERROR = str(e)

# Пытаемся импортировать C++ STL модуль
try:
    from cyclic_list_stl import CyclicListSTL
    STL_AVAILABLE = True
    STL_ERROR = ""
except Exception as e:
    STL_AVAILABLE = False
    STL_ERROR = str(e)


# Константы для выбора модулей
MODULE_PYTHON = 0
MODULE_CPP    = 1
MODULE_STL    = 2


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cyclic Singly Linked List")
        self.geometry("900x640")
        self.resizable(False, False)
        self.configure(bg="#1e1e2e")

        # Инициализация структур данных
        self.py_list  = CyclicList()
        self.cpp_list = CyclicListCPP() if CPP_AVAILABLE else None
        self.stl_list = CyclicListSTL() if STL_AVAILABLE else None

        # Переменная для хранения текущего режима
        self.module_var = tk.IntVar(value=MODULE_PYTHON)

        self._build_ui()
        self._update_canvas()

    def get_list(self):
        """Возвращает активный объект списка в зависимости от выбора"""
        m = self.module_var.get()
        if m == MODULE_CPP and self.cpp_list:
            return self.cpp_list
        if m == MODULE_STL and self.stl_list:
            return self.stl_list
        return self.py_list

    # ─────────────────── ПОСТРОЕНИЕ ИНТЕРФЕЙСА ───────────────────
    def _build_ui(self):
        # Заголовок
        tk.Label(self,
                 text="Cyclic Singly Linked List",
                 font=("Consolas", 18, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4"
                 ).pack(pady=8)

        # Переключатель модуля
        frame_switch = tk.Frame(self, bg="#1e1e2e")
        frame_switch.pack()

        tk.Label(frame_switch,
                 text="Module:",
                 bg="#1e1e2e", fg="#a6adc8",
                 font=("Consolas", 11)
                 ).pack(side=tk.LEFT, padx=5)

        # Радиокнопка Python
        tk.Radiobutton(frame_switch, text="Python", variable=self.module_var, value=MODULE_PYTHON,
                       bg="#1e1e2e", fg="#a6e3a1", selectcolor="#313244", activebackground="#1e1e2e",
                       font=("Consolas", 11), command=self._switch_module).pack(side=tk.LEFT, padx=5)

        # Радиокнопка C++ Dynamic
        if CPP_AVAILABLE:
            tk.Radiobutton(frame_switch, text="C++ Dynamic", variable=self.module_var, value=MODULE_CPP,
                           bg="#1e1e2e", fg="#89b4fa", selectcolor="#313244", activebackground="#1e1e2e",
                           font=("Consolas", 11), command=self._switch_module).pack(side=tk.LEFT, padx=5)
        else:
            tk.Label(frame_switch, text="C++ Dynamic (N/A)", bg="#1e1e2e", fg="#585b70", font=("Consolas", 11)).pack(side=tk.LEFT, padx=5)

        # Радиокнопка C++ STL
        if STL_AVAILABLE:
            tk.Radiobutton(frame_switch, text="C++ STL", variable=self.module_var, value=MODULE_STL,
                           bg="#1e1e2e", fg="#cba6f7", selectcolor="#313244", activebackground="#1e1e2e",
                           font=("Consolas", 11), command=self._switch_module).pack(side=tk.LEFT, padx=5)
        else:
            tk.Label(frame_switch, text="C++ STL (N/A)", bg="#1e1e2e", fg="#585b70", font=("Consolas", 11)).pack(side=tk.LEFT, padx=5)

        # Текстовая метка активного модуля
        self.module_label = tk.Label(self, text="Active: Python module", bg="#1e1e2e", fg="#a6e3a1", font=("Consolas", 10))
        self.module_label.pack()

        # Поле визуализации
        self.canvas = tk.Canvas(self, width=860, height=200, bg="#181825", highlightthickness=0)
        self.canvas.pack(pady=8, padx=20)

        # Панель управления (ввод и кнопки)
        frame_ctrl = tk.Frame(self, bg="#1e1e2e")
        frame_ctrl.pack(pady=5)

        tk.Label(frame_ctrl, text="Value:", bg="#1e1e2e", fg="#a6adc8", font=("Consolas", 12)).grid(row=0, column=0, padx=5)

        self.entry = tk.Entry(frame_ctrl, width=12, font=("Consolas", 14), bg="#313244", fg="#cdd6f4",
                              insertbackground="white", relief=tk.FLAT)
        self.entry.grid(row=0, column=1, padx=5)

        # Кнопки операций
        buttons = [
            ("Add Head",  "#a6e3a1", self.op_add_head),
            ("Add Tail",  "#89b4fa", self.op_add_tail),
            ("Del Head",  "#f38ba8", self.op_del_head),
            ("Del Value", "#fab387", self.op_del_value),
            ("Search",    "#f9e2af", self.op_search),
            ("Clear",     "#cba6f7", self.op_clear),
        ]
        for i, (text, color, cmd) in enumerate(buttons):
            tk.Button(frame_ctrl, text=text, font=("Consolas", 11, "bold"), bg=color, fg="#1e1e2e",
                      relief=tk.FLAT, width=9, command=cmd).grid(row=0, column=i + 2, padx=4)

        # Лог событий
        tk.Label(self, text="Log:", bg="#1e1e2e", fg="#a6adc8", font=("Consolas", 11)).pack(anchor="w", padx=25)
        self.log = tk.Text(self, height=7, width=100, bg="#181825", fg="#a6e3a1", font=("Consolas", 11),
                           relief=tk.FLAT, state=tk.DISABLED)
        self.log.pack(padx=20, pady=5)

    # ─────────────────── ПЕРЕКЛЮЧЕНИЕ ───────────────────
    def _switch_module(self):
        m = self.module_var.get()
        if m == MODULE_CPP:
            self.module_label.config(text="Active: C++ Dynamic module", fg="#89b4fa")
            self._log("--- Switched to C++ Dynamic module ---")
        elif m == MODULE_STL:
            self.module_label.config(text="Active: C++ STL module", fg="#cba6f7")
            self._log("--- Switched to C++ STL module ---")
        else:
            self.module_label.config(text="Active: Python module", fg="#a6e3a1")
            self._log("--- Switched to Python module ---")
        self._update_canvas()

    # ─────────────────── ОБРАБОТКА ДАННЫХ ───────────────────
    def _get_value(self):
        """Получает число из поля ввода с защитой от ошибок и переполнения"""
        val = self.entry.get().strip()
        if not val:
            raise ValueError("Enter a value!")
        if not val.lstrip('-').isdigit():
            raise ValueError("Value must be an integer!")
        
        num = int(val)
        # Ограничение для 32-битного знакового целого (стандарт int в C++)
        if num < -2147483648 or num > 2147483647:
            raise ValueError("Overflow! Keep value between -2.1b and 2.1b")
        
        return num

    def op_add_head(self):
        try:
            val = self._get_value()
            msg = self.get_list().add_to_head(val)
            self._log(msg)
            self._update_canvas()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def op_add_tail(self):
        try:
            val = self._get_value()
            msg = self.get_list().add_to_tail(val)
            self._log(msg)
            self._update_canvas()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def op_del_head(self):
        try:
            msg = self.get_list().delete_head()
            self._log(msg)
            self._update_canvas()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def op_del_value(self):
        try:
            val = self._get_value()
            msg = self.get_list().delete_by_value(val)
            self._log(msg)
            self._update_canvas()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def op_search(self):
        try:
            val = self._get_value()
            msg = self.get_list().search(val)
            self._log(msg)
            self._highlight_search(val)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def op_clear(self):
        msg = self.get_list().clear()
        self._log(msg)
        self._update_canvas()

    # ─────────────────── ВИЗУАЛИЗАЦИЯ ───────────────────
    def _update_canvas(self, highlight=None):
        self.canvas.delete("all")
        elements = self.get_list().get_elements()
        canvas_w, canvas_h = 860, 200
        node_h = 40

        if not elements:
            self.canvas.create_text(canvas_w // 2, 100, text="List is empty", fill="#585b70", font=("Consolas", 16))
            return

        n = len(elements)
        # Настройка размеров в зависимости от кол-ва элементов
        if n <= 5: gap, padding, font_size = 35, 16, 13
        elif n <= 10: gap, padding, font_size = 15, 10, 11
        else: gap, padding, font_size = 5, 5, 9

        def node_width(val):
            return max(35, len(str(val)) * font_size + padding * 2)

        total_w = sum(node_width(v) for v in elements) + gap * (n - 1)
        start_x = max(10, (canvas_w - total_w) // 2)
        y = 70
        
        # Отрисовка
        curr_x = start_x
        positions = []
        
        m = self.module_var.get()
        color_head = "#cba6f7" if m == MODULE_STL else "#a6e3a1"
        color_node = "#b4a7e3" if m == MODULE_STL else "#89b4fa"

        for i, val in enumerate(elements):
            nw = node_width(val)
            positions.append((curr_x, y, nw))

            # Цвет блока
            color = "#f9e2af" if (highlight is not None and val == highlight) else (color_head if i == 0 else ("#f38ba8" if i == n-1 else color_node))

            self.canvas.create_rectangle(curr_x, y, curr_x + nw, y + node_h, fill=color, outline="#cdd6f4", width=2)
            self.canvas.create_text(curr_x + nw // 2, y + node_h // 2, text=str(val), font=("Consolas", font_size, "bold"), fill="#1e1e2e")

            # Стрелка к следующему
            if i < n - 1:
                self.canvas.create_line(curr_x + nw, y + node_h // 2, curr_x + nw + gap, y + node_h // 2, arrow=tk.LAST, fill="#cdd6f4", width=2)
            
            # Подписи HEAD/TAIL
            if i == 0: self.canvas.create_text(curr_x + nw // 2, y - 15, text="HEAD", fill=color_head, font=("Consolas", 8, "bold"))
            if i == n - 1: self.canvas.create_text(curr_x + nw // 2, y - 15, text="TAIL", fill="#f38ba8", font=("Consolas", 8, "bold"))

            curr_x += nw + gap

        # Циклическая стрелка
        if n > 1:
            lx, ly, lnw = positions[-1]
            fx, fy, fnw = positions[0]
            self.canvas.create_line(lx + lnw, ly + node_h // 2, lx + lnw + 15, ly + node_h // 2, 
                                    lx + lnw + 15, ly + node_h + 30, fx + fnw // 2, ly + node_h + 30, 
                                    fx + fnw // 2, fy + node_h, arrow=tk.LAST, fill="#cba6f7", width=2, smooth=True)

        self.canvas.create_text(canvas_w - 10, 10, text=f"Size: {n}", fill="#a6adc8", font=("Consolas", 10), anchor="ne")

    def _highlight_search(self, value):
        self._update_canvas(highlight=value)

    def _log(self, message):
        self.log.configure(state=tk.NORMAL)
        self.log.insert(tk.END, f">>> {message}\n")
        self.log.see(tk.END)
        self.log.configure(state=tk.DISABLED)


if __name__ == "__main__":
    app = App()
    app.mainloop()