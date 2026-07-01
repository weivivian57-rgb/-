import tkinter as tk
from tkinter import ttk, messagebox
import random
import csv
import time
import os
import statistics
from collections import deque

# =========================
# UI 主题颜色与全局常量
# =========================
PRIMARY = "#2F6AFF"
PRIMARY_HOVER = "#1A56FF"
BG = "#F6F8FF"
CARD = "#FFFFFF"

def init_style():
    style = ttk.Style()
    style.theme_use("clam")
    
    # ---------------- Notebook 选项卡终极扁平化优化 ----------------
    style.configure(
        "TNotebook",
        background="white",  
        borderwidth=0
    )
    style.configure(
        "TNotebook.Tab",
        font=("微软雅黑", 14, "bold"),
        padding=(50, 15),       # 加宽点击区域
        background="white",
        foreground="#333333",
        borderwidth=1,
        bordercolor="#E0E4EA",  # 扁平化浅灰边框
        lightcolor="white",     # 抹除 3D 高光
        darkcolor="white",      # 抹除 3D 阴影
        focuscolor=""           # 抹除点击时的虚线焦点框
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", "#EBEEFF")],       # 选中的背景色
        foreground=[("selected", "#2F6AFF")],       # 选中的文字颜色
        lightcolor=[("selected", "#EBEEFF")],       # 保持选中时无高光
        darkcolor=[("selected", "#EBEEFF")],
        expand=[("selected", [0, 0, 0, 0])]         # 核心关键：禁止选中时Tab变大，解决文字跳动问题
    )
    # ---------------------------------------------------------------

    # Frame
    style.configure(
        "Card.TFrame",
        background=CARD
    )
    
    # Label
    style.configure(
        "Title.TLabel",
        background=BG,
        font=("微软雅黑", 18, "bold"),
        foreground="#222"
    )
    style.configure(
        "SubTitle.TLabel",
        background=CARD,
        font=("微软雅黑", 12, "bold")
    )
    style.configure(
        "Normal.TLabel",
        background=CARD,
        font=("微软雅黑", 10)
    )
    
    # Entry
    style.configure(
        "TEntry",
        padding=8
    )
    
    # Button
    style.configure(
        "Primary.TButton",
        font=("微软雅黑", 10),
        padding=10
    )
    style.map(
        "Primary.TButton",
        background=[
            ("active", PRIMARY_HOVER),
            ("!disabled", PRIMARY)
        ],
        foreground=[
            ("!disabled", "white")
        ]
    )
    
    style.configure(
        "White.TButton",
        background="white",
        foreground=PRIMARY,
        bordercolor=PRIMARY,
        padding=10
    )
    style.map(
        "White.TButton",
        background=[
            ("active", "#EEF2FF")
        ]
    )
    
    # TreeView
    style.configure(
        "Treeview",
        rowheight=28,
        font=("微软雅黑", 10),
        borderwidth=0
    )
    style.configure(
        "Treeview.Heading",
        font=("微软雅黑", 10, "bold"),
        background=BG,
        borderwidth=0
    )
    style.map("Treeview", background=[("selected", PRIMARY)])
    
    return style

# =========================
# 1. 日志记录器 (Logger)
# =========================
class Logger:
    def __init__(self, text_widget):
        self.text = text_widget
    def log(self, msg):
        t = time.strftime("%H:%M:%S")
        self.text.insert(tk.END, f"[{t}] {msg}\n")
        self.text.see(tk.END)

# =========================
# 2. 底层数据结构定义
# =========================
class SqList:
    def __init__(self): self.data = []
    def insert(self, index, value):
        if index < 0 or index > len(self.data): raise IndexError("越界")
        self.data.insert(index, value)
    def delete(self, index):
        if index < 0 or index >= len(self.data): raise IndexError("越界")
        return self.data.pop(index)
    def clear(self): self.data.clear()

class Stack:
    def __init__(self): self.data = []
    def push(self, value): self.data.append(value)
    def pop(self):
        if not self.data: raise IndexError("空")
        return self.data.pop()
    def clear(self): self.data.clear()

class Queue:
    def __init__(self): self.data = deque()
    def enqueue(self, value): self.data.append(value)
    def dequeue(self):
        if not self.data: raise IndexError("空")
        return self.data.popleft()
    def clear(self): self.data.clear()

# =========================
# 3. 括号匹配算法
# =========================
def check_bracket(s):
    pairs = {')': '(', ']': '[', '}': '{', '>': '<', '）': '（', '】': '【', '」': '「', '》': '《'}
    stack = []
    has_bracket = False
    for i, ch in enumerate(s):
        if ch in pairs.values():
            stack.append((ch, i))
            has_bracket = True
        elif ch in pairs:
            has_bracket = True
            if not stack: return False, i
            top_char, top_idx = stack.pop()
            if top_char != pairs[ch]: return False, i
    if stack: return False, stack[-1][1]
    if not has_bracket: return False, -99 
    return True, -1

# =========================
# 4. 排序算法（生成器）
# =========================
class Sorter:
    def __init__(self, data):
        self.data = data
        self.cmp = 0
        self.swap = 0
    def bubble(self):
        a = self.data
        n = len(a)
        for i in range(n):
            for j in range(n - i - 1):
                self.cmp += 1
                if a[j] > a[j + 1]:
                    a[j], a[j + 1] = a[j + 1], a[j]
                    self.swap += 1
                    yield a.copy()
    def selection(self):
        a = self.data
        n = len(a)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                self.cmp += 1
                if a[j] < a[min_idx]: min_idx = j
            if min_idx != i:
                a[i], a[min_idx] = a[min_idx], a[i]
                self.swap += 1
                yield a.copy()
    def quick(self):
        a = self.data
        def q(l, r):
            if l >= r: return
            pivot = a[l]
            i, j = l, r
            while i < j:
                while i < j and a[j] >= pivot:
                    self.cmp += 1; j -= 1
                while i < j and a[i] <= pivot:
                    self.cmp += 1; i += 1
                if i < j:
                    a[i], a[j] = a[j], a[i]
                    self.swap += 1
                    yield a.copy()
            a[l], a[i] = a[i], a[l]
            self.swap += 1
            yield a.copy()
            yield from q(l, i - 1)
            yield from q(i + 1, r)
        yield from q(0, len(a) - 1)

# =========================
# 5. 主程序 GUI 界面
# =========================
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("数据结构与算法综合实验")
        self.root.geometry("1200x966")
        self.root.configure(bg="white")
        
        # 初始化统一样式
        init_style()

        self.sl = SqList()
        self.st = Stack()
        self.qu = Queue()
        self.data = []
        self.generator = None
        self.raw = []

        self.build_layout()

    def create_card_listbox(self, parent):
        """带有亮灰色边框的扁平Listbox，解决点击时边框消失跳动问题"""
        lb = tk.Listbox(
            parent, 
            relief="flat", 
            font=("微软雅黑", 11), 
            bg=CARD, 
            fg="#333",
            highlightbackground="#D9D9D9",   # 失去焦点时的边框色
            highlightcolor="#D9D9D9",        # 获得焦点(被点击)时的边框色保持不变
            highlightthickness=1,            # 强制维持1像素粗细，避免跳动
            selectbackground=PRIMARY, 
            exportselection=False
        )
        return lb

    def build_layout(self):
        # 整体布局容器，预留四周 Padding
        main_wrapper = tk.Frame(self.root, bg="white")
        main_wrapper.pack(fill=tk.BOTH, expand=True, padx=50, pady=(24, 24))

        # --- 1. 顶部选项卡 Notebook ---
        self.nb = ttk.Notebook(main_wrapper, style="TNotebook")
        self.nb.pack(fill=tk.BOTH, expand=True)
        
        # 初始化 Tab 容器 (背景使用统一样式)
        self.frame_tab1 = tk.Frame(self.nb, bg=BG)
        self.frame_tab2 = tk.Frame(self.nb, bg=BG)
        self.frame_tab3 = tk.Frame(self.nb, bg=BG)
        
        self.nb.add(self.frame_tab1, text="数据结构")
        self.nb.add(self.frame_tab2, text="排序算法演示")
        self.nb.add(self.frame_tab3, text="数据清洗与预处理")

        self.build_tab1()
        self.build_tab2()
        self.build_tab3()

        # --- 2. 底部系统日志区 (Logger) ---
        self.logger_frame = ttk.Frame(main_wrapper, style="Card.TFrame", padding=15)
        self.logger_frame.pack(fill=tk.X, pady=(24, 0))
        
        ttk.Label(self.logger_frame, text="系统运行日志", style="SubTitle.TLabel").pack(anchor="w", pady=(0, 10))
        
        self.log = tk.Text(self.logger_frame, height=8, bg="#F7F7F7", fg="#333333", bd=0, relief="flat", font=("Consolas", 10))
        self.log.pack(fill=tk.X)
        self.logger = Logger(self.log)


    # ================= 构建 TAB 1: 数据结构 =================
    def build_tab1(self):
        top_cols = tk.Frame(self.frame_tab1, bg=BG)
        top_cols.pack(fill=tk.BOTH, expand=True, pady=20, padx=20)
        top_cols.columnconfigure((0, 1, 2), weight=1, uniform="col")

        # --- 线性表 ---
        c1 = ttk.Frame(top_cols, style="Card.TFrame", padding=18)
        c1.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ttk.Label(c1, text="🗂️ 线性表(SqList)", style="SubTitle.TLabel").pack(anchor="w", pady=(0, 10))
        ttk.Label(c1, text="展示框", style="Normal.TLabel").pack(anchor="w")
        self.lb1 = self.create_card_listbox(c1)
        self.lb1.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        ttk.Label(c1, text="输入数值", style="Normal.TLabel").pack(anchor="w")
        self.e_val = ttk.Entry(c1, style="TEntry")
        self.e_val.pack(fill=tk.X, pady=(3, 10))
        
        ttk.Label(c1, text="索引位置", style="Normal.TLabel").pack(anchor="w")
        self.e_idx = ttk.Entry(c1, style="TEntry")
        self.e_idx.pack(fill=tk.X, pady=(3, 15))
        
        btn_f1 = ttk.Frame(c1, style="Card.TFrame")
        btn_f1.pack(fill=tk.X)
        btn_f1.columnconfigure((0, 1), weight=1, uniform="b")
        
        ttk.Button(btn_f1, text="展示动态遍历", style="Primary.TButton", width=16, command=self.sq_traverse).grid(row=0, column=0, sticky="ew", padx=(0, 5), pady=5)
        ttk.Button(btn_f1, text="插入元素", style="Primary.TButton", width=16, command=self.sq_ins).grid(row=0, column=1, sticky="ew", padx=(5, 0), pady=5)
        ttk.Button(btn_f1, text="清空重置", style="White.TButton", width=16, command=self.sq_clear).grid(row=1, column=0, sticky="ew", padx=(0, 5), pady=5)
        ttk.Button(btn_f1, text="删除(指定)选项", style="White.TButton", width=16, command=self.sq_del).grid(row=1, column=1, sticky="ew", padx=(5, 0), pady=5)

        # --- 栈 ---
        c2 = ttk.Frame(top_cols, style="Card.TFrame", padding=18)
        c2.grid(row=0, column=1, sticky="nsew", padx=10)
        
        ttk.Label(c2, text="📚 栈(Stack)", style="SubTitle.TLabel").pack(anchor="w", pady=(0, 10))
        ttk.Label(c2, text="展示框", style="Normal.TLabel").pack(anchor="w")
        self.lb2 = self.create_card_listbox(c2)
        self.lb2.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        ttk.Label(c2, text="输入数值", style="Normal.TLabel").pack(anchor="w")
        self.e_stack_val = ttk.Entry(c2, style="TEntry")
        self.e_stack_val.pack(fill=tk.X, pady=(3, 15))
        
        btn_f2 = ttk.Frame(c2, style="Card.TFrame")
        btn_f2.pack(fill=tk.X)
        btn_f2.columnconfigure((0, 1), weight=1, uniform="b")
        ttk.Button(btn_f2, text="入栈(Push)", style="Primary.TButton", width=16, command=self.push).grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ttk.Button(btn_f2, text="出栈(Pop)", style="White.TButton", width=16, command=self.pop).grid(row=0, column=1, sticky="ew", padx=(5, 0))

        # --- 队列 ---
        c3 = ttk.Frame(top_cols, style="Card.TFrame", padding=18)
        c3.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
        
        ttk.Label(c3, text="👥 队列(Queue)", style="SubTitle.TLabel").pack(anchor="w", pady=(0, 10))
        ttk.Label(c3, text="展示框", style="Normal.TLabel").pack(anchor="w")
        self.lb3 = self.create_card_listbox(c3)
        self.lb3.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        ttk.Label(c3, text="输入数值", style="Normal.TLabel").pack(anchor="w")
        self.e_queue_val = ttk.Entry(c3, style="TEntry")
        self.e_queue_val.pack(fill=tk.X, pady=(3, 15))
        
        btn_f3 = ttk.Frame(c3, style="Card.TFrame")
        btn_f3.pack(fill=tk.X)
        btn_f3.columnconfigure((0, 1), weight=1, uniform="b")
        ttk.Button(btn_f3, text="入队(Enqueue)", style="Primary.TButton", width=16, command=self.enq).grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ttk.Button(btn_f3, text="出队(Dequeue)", style="White.TButton", width=16, command=self.deq).grid(row=0, column=1, sticky="ew", padx=(5, 0))

        # --- 括号匹配验证 ---
        c_bottom = ttk.Frame(self.frame_tab1, style="Card.TFrame", padding=18)
        c_bottom.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        ttk.Label(c_bottom, text="➿ 括号匹配验证", style="SubTitle.TLabel").pack(anchor="w", pady=(0, 10))
        
        bk_inner = ttk.Frame(c_bottom, style="Card.TFrame")
        bk_inner.pack(fill=tk.X)
        
        ttk.Label(bk_inner, text="输入含有括号的字符串：", style="Normal.TLabel").pack(side=tk.LEFT)
        self.b = ttk.Entry(bk_inner, style="TEntry")
        self.b.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 20))
        
        ttk.Button(bk_inner, text="检 测", style="Primary.TButton", width=16, command=self.check).pack(side=tk.LEFT)

    # ================= 构建 TAB 2: 排序算法 =================
    def build_tab2(self):
        c_main = ttk.Frame(self.frame_tab2, style="Card.TFrame", padding=18)
        c_main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        ttk.Label(c_main, text="📊 排序展示", style="Title.TLabel", background=CARD).pack(anchor="w", pady=(0, 15))

        top_bar = ttk.Frame(c_main, style="Card.TFrame")
        top_bar.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Button(top_bar, text="生成随机数据", style="Primary.TButton", width=16, command=self.gen).pack(side=tk.LEFT)
        
        ttk.Button(top_bar, text="快速排序", style="White.TButton", width=16, command=lambda: self.start("q")).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(top_bar, text="选择排序", style="White.TButton", width=16, command=lambda: self.start("s")).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(top_bar, text="冒泡排序", style="White.TButton", width=16, command=lambda: self.start("b")).pack(side=tk.RIGHT)

        self.canvas = tk.Canvas(
            c_main, width=1050, height=460, bg="white", 
            highlightbackground="#D9D9D9", highlightthickness=1
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

    # ================= 构建 TAB 3: 数据清洗 =================
    def build_tab3(self):
        c_main = ttk.Frame(self.frame_tab3, style="Card.TFrame", padding=18)
        c_main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        top_bar = ttk.Frame(c_main, style="Card.TFrame")
        top_bar.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Button(top_bar, text="生成传感器脏数据", style="Primary.TButton", width=20, command=self.gen_and_save_data).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(top_bar, text="一键执行清洗", style="Primary.TButton", width=20, command=self.clean_sort_and_save).pack(side=tk.LEFT)

        # 统计条展示
        stats_bar = tk.Frame(c_main, bg=BG, padx=15, pady=12)
        stats_bar.pack(fill=tk.X, pady=(0, 15))
        tk.Label(stats_bar, text="清洗后统计：", font=("微软雅黑", 11, "bold"), bg=BG, fg="#333").pack(side=tk.LEFT, padx=(0,20))
        
        self.lbl_mean = self.create_stat_item(stats_bar, "均值")
        self.lbl_median = self.create_stat_item(stats_bar, "中位数")
        self.lbl_std = self.create_stat_item(stats_bar, "标准差")
        self.lbl_max = self.create_stat_item(stats_bar, "最大值")
        self.lbl_min = self.create_stat_item(stats_bar, "最小值")

        # 数据表格区域
        table_area = ttk.Frame(c_main, style="Card.TFrame")
        table_area.pack(fill=tk.BOTH, expand=True)
        table_area.columnconfigure((0,1), weight=1, uniform="t")

        # 原始数据区
        f_raw = ttk.Frame(table_area, style="Card.TFrame")
        f_raw.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        ttk.Label(f_raw, text="💽 原始数据", style="SubTitle.TLabel").pack(anchor="w", pady=(0, 10))
        
        raw_border = tk.Frame(f_raw, bg="#D9D9D9", padx=1, pady=1)
        raw_border.pack(fill=tk.BOTH, expand=True)
        cols = ("ID", "Temperature", "Humidity", "Pressure", "Label")
        self.t1 = ttk.Treeview(raw_border, columns=cols, show="headings")
        for c in cols: 
            self.t1.heading(c, text=c)
            self.t1.column(c, width=60, anchor="center")
        self.t1.pack(fill=tk.BOTH, expand=True)

        # 清洗后数据区
        f_clean = ttk.Frame(table_area, style="Card.TFrame")
        f_clean.grid(row=0, column=1, sticky="nsew", padx=(15, 0))
        ttk.Label(f_clean, text="📦 清洗后数据", style="SubTitle.TLabel").pack(anchor="w", pady=(0, 10))
        
        cln_border = tk.Frame(f_clean, bg="#D9D9D9", padx=1, pady=1)
        cln_border.pack(fill=tk.BOTH, expand=True)
        self.t2 = ttk.Treeview(cln_border, columns=cols, show="headings")
        for c in cols: 
            self.t2.heading(c, text=c)
            self.t2.column(c, width=60, anchor="center")
        self.t2.pack(fill=tk.BOTH, expand=True)

    def create_stat_item(self, parent, title):
        f = tk.Frame(parent, bg=BG)
        f.pack(side=tk.LEFT, padx=15)
        tk.Label(f, text=f"{title}：", font=("微软雅黑", 10), bg=BG,fg="#333333").pack(side=tk.LEFT)
        val_lbl = tk.Label(f, text="           ", font=("微软雅黑", 11, "underline"), bg=BG, fg=PRIMARY)
        val_lbl.pack(side=tk.LEFT)
        return val_lbl

    # ================= 业务逻辑绑定部分 =================
    def sq_ins(self):
        try:
            val = int(self.e_val.get()) 
            idx_str = self.e_idx.get()  
            idx = int(idx_str) if idx_str else len(self.sl.data)
            self.sl.insert(idx, val) 
            self.lb1.delete(0, tk.END)
            for item in self.sl.data: self.lb1.insert(tk.END, item)
            self.logger.log(f"线性表: 在索引 {idx} 成功插入 {val}")
            self.e_val.delete(0, tk.END)
            self.e_idx.delete(0, tk.END)
        except ValueError: messagebox.showerror("错误", "数值或索引必须为整数！")
        except IndexError: messagebox.showerror("越界", f"插入位置越界！当前范围: 0 ~ {len(self.sl.data)}")

    def sq_del(self):
        selected_indices = self.lb1.curselection()
        try:
            if selected_indices: idx = selected_indices[0]
            else:
                idx_str = self.e_idx.get()
                if not idx_str:
                    messagebox.showwarning("提示", "请先点击列表项，或输入索引！")
                    return
                idx = int(idx_str)
            val = self.sl.delete(idx)
            self.lb1.delete(0, tk.END)
            for item in self.sl.data: self.lb1.insert(tk.END, item)
            self.logger.log(f"线性表: 删除了索引[{idx}] 的元素: {val}")
            self.e_idx.delete(0, tk.END)
            self.lb1.selection_clear(0, tk.END)
        except ValueError: messagebox.showerror("错误", "必须填写整数！")
        except IndexError: messagebox.showerror("越界", "删除失败：越界或表空！")

    def sq_traverse(self):
        if not self.sl.data:
            messagebox.showinfo("提示", "当前为空表！")
            return
        self.logger.log("====== 开始遍历线性表 ======")
        def visit(index):
            if index < len(self.sl.data):
                self.lb1.selection_clear(0, tk.END)
                self.lb1.selection_set(index)
                self.lb1.see(index)
                self.logger.log(f"访问索引[{index}] -> 值: {self.sl.data[index]}")
                self.root.after(600, visit, index + 1)
            else:
                self.lb1.selection_clear(0, tk.END)
                self.logger.log("====== 遍历结束 ======")
        visit(0)

    def sq_clear(self):
        self.sl.clear()
        self.lb1.delete(0, tk.END)
        self.logger.log("线性表: 已清空")

    def push(self):
        try:
            v = int(self.e_stack_val.get())
            self.st.push(v)
            self.lb2.insert(0, v) 
            self.logger.log(f"栈: {v} 入栈")
            self.e_stack_val.delete(0, tk.END)
        except ValueError: messagebox.showerror("错误", "必须输入整数")

    def pop(self):
        try:
            val = self.st.pop()
            self.lb2.delete(0)
            self.logger.log(f"栈: {val} 出栈")
        except IndexError: messagebox.showerror("错误", "栈空！")

    def enq(self):
        try:
            v = int(self.e_queue_val.get())
            self.qu.enqueue(v)
            self.lb3.insert(tk.END, v)
            self.logger.log(f"队列: {v} 入队")
            self.e_queue_val.delete(0, tk.END)
        except ValueError: messagebox.showerror("错误", "必须输入整数")

    def deq(self):
        try:
            val = self.qu.dequeue()
            self.lb3.delete(0)
            self.logger.log(f"队列: {val} 出队")
        except IndexError: messagebox.showerror("错误", "队列空！")

    def check(self):
        test_str = self.b.get()
        if not test_str: return
        is_ok, err_pos = check_bracket(test_str)
        if err_pos == -99:
            self.logger.log("括号匹配: 字符串中不包含支持的括号")
            messagebox.showinfo("检测", "未检测到括号")
        elif is_ok:
            self.logger.log(f"括号匹配: '{test_str}' 匹配正确")
            messagebox.showinfo("检测", "匹配通过 ✓")
        else:
            self.logger.log(f"括号匹配: 定位在索引 {err_pos} 有误")
            messagebox.showerror("检测", f"匹配失败 ✗ (错在第 {err_pos + 1} 个字符)")

    def gen(self):
        self.data = [random.randint(1, 100) for _ in range(100)]
        self.draw(self.data)
        self.logger.log("排序模块: 成功生成数据")

    def draw(self, arr):
        self.canvas.delete("all")
        if not arr: return
        w_cv = self.canvas.winfo_width() if self.canvas.winfo_width() > 1 else 1050
        h_cv = self.canvas.winfo_height() if self.canvas.winfo_height() > 1 else 460
        w = w_cv / len(arr)
        m = max(arr)
        for i, v in enumerate(arr):
            h = (v / m) * (h_cv - 20) 
            self.canvas.create_rectangle(i*w, h_cv-h, (i+1)*w, h_cv, fill=PRIMARY, outline=CARD)

    def start(self, mode):
        if not self.data: return
        self.s = Sorter(self.data.copy())
        if mode == "b": self.generator = self.s.bubble()
        elif mode == "s": self.generator = self.s.selection()
        else: self.generator = self.s.quick()
        self.run_animation()

    def run_animation(self):
        try:
            current_arr = next(self.generator)
            self.draw(current_arr)
            self.root.after(10, self.run_animation)
        except StopIteration:
            self.logger.log(f"排序完成！共比较: {self.s.cmp} 次, 交换: {self.s.swap} 次")

    def gen_and_save_data(self):
        raw_data = []
        for i in range(200):
            raw_data.append([i, random.uniform(15, 35), random.uniform(30, 80), random.uniform(980, 1030), random.choice(["A", "B", "C"])])
        for _ in range(10): raw_data[random.randint(0, 199)][1] = "" 
        for _ in range(5):
            idx = random.randint(0, 199)
            if raw_data[idx][1] != "": raw_data[idx][1] = 150.0 
        
        with open("raw_data.csv", "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerows([["ID", "Temperature", "Humidity", "Pressure", "Label"]] + raw_data)

        self.t1.delete(*self.t1.get_children())
        for row in raw_data:
            self.t1.insert("", tk.END, values=[f"{x:.2f}" if isinstance(x, float) else x for x in row]) 
        self.logger.log("已生成200条含缺失和异常的数据至 raw_data.csv")

    def clean_sort_and_save(self):
        if not os.path.exists("raw_data.csv"):
            messagebox.showerror("错误", "请先生成数据！")
            return
            
        with open("raw_data.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            data_from_file = list(reader)

        valid_data = []
        for row in data_from_file:
            if row[1] == "": continue 
            valid_data.append([int(row[0]), float(row[1]), float(row[2]), float(row[3]), row[4]])

        temps = [r[1] for r in valid_data]
        mean_t, std_t = statistics.mean(temps), statistics.stdev(temps)
        
        for row in valid_data:
            if abs(row[1] - mean_t) > (2 * std_t): row[1] = mean_t 

        valid_data.sort(key=lambda x: x[1])

        with open("cleaned_sorted_data.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for row in valid_data:
                writer.writerow([row[0], f"{row[1]:.2f}", f"{row[2]:.2f}", f"{row[3]:.2f}", row[4]])

        self.t2.delete(*self.t2.get_children())
        for row in valid_data:
            self.t2.insert("", tk.END, values=[f"{x:.2f}" if isinstance(x, float) else x for x in row])
        self.logger.log("清洗排序完成，结果存至 cleaned_sorted_data.csv")

        # 同步更新统计面板
        f_temps = [row[1] for row in valid_data]
        self.lbl_mean.config(text=f"{statistics.mean(f_temps):.2f}")
        self.lbl_median.config(text=f"{statistics.median(f_temps):.2f}")
        self.lbl_std.config(text=f"{statistics.stdev(f_temps):.2f}")
        self.lbl_max.config(text=f"{max(f_temps):.2f}")
        self.lbl_min.config(text=f"{min(f_temps):.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()