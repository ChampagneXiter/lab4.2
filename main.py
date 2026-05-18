import tkinter as tk
from tkinter import messagebox
from cyclic_list import CyclicList

try:
    from cyclic_list_cpp import CyclicListCPP
    CPP_AVAILABLE = True
except Exception as e:
    CPP_AVAILABLE = False
    CPP_ERROR = str(e)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cyclic Singly Linked List")
        self.geometry("900x620")
        self.resizable(False, False)
        self.configure(bg="#1e1e2e")

        self.py_list  = CyclicList()
        self.cpp_list = CyclicListCPP() if CPP_AVAILABLE else None
        self.use_cpp  = tk.BooleanVar(value=False)

        self._build_ui()
        self._update_canvas()

    def get_list(self):
        if self.use_cpp.get() and self.cpp_list:
            return self.cpp_list
        return self.py_list

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

        tk.Radiobutton(frame_switch,
                       text="Python",
                       variable=self.use_cpp,
                       value=False,
                       bg="#1e1e2e", fg="#a6e3a1",
                       selectcolor="#313244",
                       activebackground="#1e1e2e",
                       font=("Consolas", 11),
                       command=self._switch_module
                       ).pack(side=tk.LEFT, padx=5)

        if CPP_AVAILABLE:
            tk.Radiobutton(frame_switch,
                           text="C++",
                           variable=self.use_cpp,
                           value=True,
                           bg="#1e1e2e", fg="#89b4fa",
                           selectcolor="#313244",
                           activebackground="#1e1e2e",
                           font=("Consolas", 11),
                           command=self._switch_module
                           ).pack(side=tk.LEFT, padx=5)
        else:
            tk.Label(frame_switch,
                     text="C++ (DLL not found)",
                     bg="#1e1e2e", fg="#585b70",
                     font=("Consolas", 11)
                     ).pack(side=tk.LEFT, padx=5)

        # Статус модуля
        self.module_label = tk.Label(self,
                                     text="Active: Python module",
                                     bg="#1e1e2e", fg="#a6e3a1",
                                     font=("Consolas", 10))
        self.module_label.pack()

        # Canvas
        self.canvas = tk.Canvas(self,
                                width=860, height=200,
                                bg="#181825",
                                highlightthickness=0)
        self.canvas.pack(pady=8, padx=20)

        # Панель кнопок
        frame_ctrl = tk.Frame(self, bg="#1e1e2e")
        frame_ctrl.pack(pady=5)

        tk.Label(frame_ctrl,
                 text="Value:",
                 bg="#1e1e2e", fg="#a6adc8",
                 font=("Consolas", 12)
                 ).grid(row=0, column=0, padx=5)

        self.entry = tk.Entry(frame_ctrl,
                              width=8,
                              font=("Consolas", 14),
                              bg="#313244", fg="#cdd6f4",
                              insertbackground="white",
                              relief=tk.FLAT)
        self.entry.grid(row=0, column=1, padx=5)

        buttons = [
            ("Add Head",  "#a6e3a1", self.op_add_head),
            ("Add Tail",  "#89b4fa", self.op_add_tail),
            ("Del Head",  "#f38ba8", self.op_del_head),
            ("Del Value", "#fab387", self.op_del_value),
            ("Search",    "#f9e2af", self.op_search),
            ("Clear",     "#cba6f7", self.op_clear),
        ]
        for i, (text, color, cmd) in enumerate(buttons):
            tk.Button(frame_ctrl,
                      text=text,
                      font=("Consolas", 11, "bold"),
                      bg=color, fg="#1e1e2e",
                      relief=tk.FLAT,
                      width=9,
                      command=cmd
                      ).grid(row=0, column=i + 2, padx=4)

        # Лог
        tk.Label(self,
                 text="Log:",
                 bg="#1e1e2e", fg="#a6adc8",
                 font=("Consolas", 11)
                 ).pack(anchor="w", padx=25)

        self.log = tk.Text(self,
                           height=7, width=100,
                           bg="#181825", fg="#a6e3a1",
                           font=("Consolas", 11),
                           relief=tk.FLAT,
                           state=tk.DISABLED)
        self.log.pack(padx=20, pady=5)

    # ─────────────────── ПЕРЕКЛЮЧАТЕЛЬ ───────────────────
    def _switch_module(self):
        if self.use_cpp.get():
            self.module_label.config(
                text="Active: C++ module",
                fg="#89b4fa")
            self._log("--- Switched to C++ module ---")
        else:
            self.module_label.config(
                text="Active: Python module",
                fg="#a6e3a1")
            self._log("--- Switched to Python module ---")
        self._update_canvas()

    # ─────────────────── ОПЕРАЦИИ ───────────────────
    def _get_value(self):
        val = self.entry.get().strip()
        if not val:
            raise ValueError("Enter a value!")
        if not val.lstrip('-').isdigit():
            raise ValueError("Value must be an integer!")
        return int(val)

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
        canvas_w = 860
        node_h   = 40

        if not elements:
            self.canvas.create_text(
                canvas_w // 2, 100,
                text="List is empty",
                fill="#585b70",
                font=("Consolas", 16))
            return

        n = len(elements)

        if n <= 4:
            gap, padding, font_size = 35, 16, 13
        elif n <= 7:
            gap, padding, font_size = 22, 12, 11
        elif n <= 10:
            gap, padding, font_size = 12, 8, 10
        else:
            gap, padding, font_size = 6, 5, 8

        def node_width(val):
            return max(32, len(str(val)) * font_size + padding * 2)

        total = sum(node_width(v) for v in elements) + gap * (n - 1)

        if total > canvas_w - 20:
            ratio = (canvas_w - 20) / total
            gap       = max(3, int(gap * ratio))
            padding   = max(2, int(padding * ratio))
            font_size = max(7, int(font_size * ratio))

            def node_width(val):
                return max(24, len(str(val)) * font_size + padding * 2)

            total = sum(node_width(v) for v in elements) + gap * (n - 1)

        start_x = max(5, (canvas_w - total) // 2)
        y = 70
        positions = []
        x = start_x

        for i, val in enumerate(elements):
            nw = node_width(val)
            positions.append((x, y, nw))

            if highlight is not None and val == highlight:
                color = "#f9e2af"
            elif i == 0:
                color = "#a6e3a1"
            elif i == len(elements) - 1:
                color = "#f38ba8"
            else:
                color = "#89b4fa"

            self.canvas.create_rectangle(
                x, y, x + nw, y + node_h,
                fill=color, outline="#cdd6f4", width=2)

            self.canvas.create_text(
                x + nw // 2, y + node_h // 2,
                text=str(val),
                font=("Consolas", font_size, "bold"),
                fill="#1e1e2e",
                width=nw - 4)

            if i < len(elements) - 1:
                self.canvas.create_line(
                    x + nw, y + node_h // 2,
                    x + nw + gap, y + node_h // 2,
                    arrow=tk.LAST, fill="#cdd6f4", width=2)

            if font_size >= 8:
                if i == 0:
                    self.canvas.create_text(
                        x + nw // 2, y - 15,
                        text="HEAD", fill="#a6e3a1",
                        font=("Consolas", 8, "bold"))
                if i == len(elements) - 1:
                    self.canvas.create_text(
                        x + nw // 2, y - 15,
                        text="TAIL", fill="#f38ba8",
                        font=("Consolas", 8, "bold"))

            x += nw + gap

        if len(elements) > 1:
            lx, ly, lnw = positions[-1]
            fx, fy, fnw = positions[0]
            self.canvas.create_line(
                lx + lnw,      ly + node_h // 2,
                lx + lnw + 12, ly + node_h // 2,
                lx + lnw + 12, ly + node_h + 28,
                fx + fnw // 2, ly + node_h + 28,
                fx + fnw // 2, fy + node_h,
                arrow=tk.LAST, fill="#cba6f7",
                width=2, smooth=True)

        self.canvas.create_text(
            canvas_w - 5, 5,
            text=f"Size: {n}",
            fill="#a6adc8",
            font=("Consolas", 9),
            anchor="ne")

    def _highlight_search(self, value):
        self._update_canvas(highlight=value)

    # ─────────────────── ЛОГ ───────────────────
    def _log(self, message):
        self.log.configure(state=tk.NORMAL)
        self.log.insert(tk.END, f">>> {message}\n")
        self.log.see(tk.END)
        self.log.configure(state=tk.DISABLED)


if __name__ == "__main__":
    app = App()
    app.mainloop()