#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iD01t Academy - Python Exercises Book 2 · Edition #2
Premium 2025 Dark Suite · One file · Desktop GUI

This single script packages a clean dark UI and twelve polished mini apps.
It auto-installs required dependencies at first run, uses icon.ico from the same
folder for the window and header, persists data to ./data, and exports all data
to a ZIP on demand.

Author: Guillaume Lessard, iD01t Productions
Version: 1.5.2.0
"""

import os, sys, json, subprocess, importlib, datetime, csv, zipfile, webbrowser, traceback, random
from pathlib import Path
from typing import Any, Dict, List

# --------------------------- dependency bootstrap ----------------------------
REQUIRED = [
    "ttkbootstrap",      # optional theme engine, app runs fine without it
    "requests",          # http client
    "beautifulsoup4",    # html parsing
    "matplotlib",        # charts
    "Pillow",            # icon fallback
]

def _pip_install(pkg: str) -> None:
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet", pkg],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception as e:
        print(f"[warn] pip could not install {pkg}: {e}")

def _ensure_deps() -> None:
    for pkg in REQUIRED:
        mod = pkg.split("[")[0].replace("-", "_")
        try:
            importlib.import_module(mod)
        except Exception:
            _pip_install(pkg)

_ensure_deps()

# ------------------------------ safe imports ---------------------------------
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

try:
    import ttkbootstrap as tb
    from ttkbootstrap.constants import *
    _HAS_TTKB = True
except Exception:
    tb = None
    _HAS_TTKB = False

try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.pyplot as plt
    _HAS_MPL = True
except Exception:
    _HAS_MPL = False

try:
    import requests
    from bs4 import BeautifulSoup
    _HAS_WEB = True
except Exception:
    _HAS_WEB = False

try:
    from PIL import Image, ImageTk
    _HAS_PIL = True
except Exception:
    _HAS_PIL = False

# ------------------------------- app constants --------------------------------
APP_NAME = "iD01t Academy - Python Exercises Book 2 · Edition #2"
APP_VERSION = "1.5.2.0"
ORG = "iD01t Productions"
HOMEPAGE = "https://id01t.store"

def resource_path(rel: str) -> Path:
    base = getattr(sys, "_MEIPASS", None)
    return (Path(base) / rel) if base else (Path(__file__).resolve().parent / rel)

ICON_PATH = resource_path("icon.ico")
DATA_DIR = resource_path("data")
DATA_DIR.mkdir(exist_ok=True)

# ------------------------------- helpers --------------------------------------
def set_app_icon(win: tk.Misc) -> None:
    try:
        if ICON_PATH.exists():
            try:
                win.iconbitmap(ICON_PATH)
                return
            except Exception:
                pass
        if _HAS_PIL and ICON_PATH.exists():
            img = Image.open(ICON_PATH)
            win.iconphoto(True, ImageTk.PhotoImage(img))
    except Exception:
        pass

def open_url(url: str) -> None:
    try:
        webbrowser.open_new_tab(url)
    except Exception:
        pass

def safe_load_json(path: Path, default: Any) -> Any:
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        traceback.print_exc()
    return default

def safe_save_json(path: Path, data: Any) -> bool:
    try:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return True
    except Exception as e:
        messagebox.showerror("Save failed", f"Could not save {path.name}\n{e}")
        return False

def export_zip_all() -> None:
    fp = filedialog.asksaveasfilename(
        title="Export all data",
        defaultextension=".zip",
        initialfile="iD01t_Academy_Data.zip",
        filetypes=[("ZIP", "*.zip")],
    )
    if not fp:
        return
    try:
        with zipfile.ZipFile(fp, "w", compression=zipfile.ZIP_DEFLATED) as z:
            for p in DATA_DIR.rglob("*"):
                if p.is_file():
                    z.write(p, p.relative_to(DATA_DIR.parent))
        messagebox.showinfo("Export complete", "Data exported successfully")
    except Exception as e:
        messagebox.showerror("Export failed", str(e))

# ------------------------------- styling --------------------------------------
def apply_2025_dark_style(root: tk.Tk) -> None:
    if _HAS_TTKB:
        # modern dark theme
        tb.Style(theme="darkly")
        return
    # fallback theme for pure ttk
    style = ttk.Style()
    for theme in ("clam", "alt", "default"):
        try:
            style.theme_use(theme)
            break
        except Exception:
            continue
    bg = "#111318"
    surface = "#161a22"
    text = "#e6e6e6"
    sub = "#9aa4b2"
    accent = "#4f8cff"
    danger = "#ff4f6d"
    style.configure(".", background=bg, foreground=text, fieldbackground=surface)
    style.configure("TFrame", background=bg)
    style.configure("TLabel", background=bg, foreground=text)
    style.configure("Header.TLabel", font=("Segoe UI Semibold", 13))
    style.configure("Sub.TLabel", foreground=sub)
    style.configure("TNotebook", background=bg, tabmargins=[6, 4, 6, 0])
    style.configure("TNotebook.Tab", background=surface, foreground=text, padding=[12, 6])
    style.map("TNotebook.Tab", background=[("selected", accent)], foreground=[("selected", "#0b1220")])
    style.configure("TButton", padding=6)
    style.map("TButton", background=[("active", accent)], foreground=[("active", "#0b1220")])
    style.configure("Accent.TButton", background=accent, foreground="#0b1220", padding=6)
    style.configure("Danger.TButton", background=danger, foreground="#0b1220", padding=6)
    style.configure("Treeview", background=surface, fieldbackground=surface, foreground=text, rowheight=24)
    style.configure("TEntry", fieldbackground=surface)
    style.configure("TCombobox", fieldbackground=surface)

def section(parent: tk.Widget, title: str, subtitle: str = "") -> ttk.Frame:
    frm = ttk.Frame(parent, padding=(10, 8))
    frm.pack(fill="x")
    ttk.Label(frm, text=title, style="Header.TLabel").pack(anchor="w")
    if subtitle:
        ttk.Label(frm, text=subtitle, style="Sub.TLabel").pack(anchor="w")
    return frm

class CodeViewer(tk.Toplevel):
    def __init__(self, master, code: str, title: str):
        super().__init__(master)
        self.title(title)
        set_app_icon(self)
        self.geometry("980x640")
        self.minsize(700, 400)
        txt = scrolledtext.ScrolledText(self, wrap="none", font=("Consolas", 10))
        txt.pack(fill="both", expand=True)
        txt.insert("1.0", code)
        txt.configure(state="disabled")

def view_source(master, cls) -> None:
    import inspect
    try:
        code = inspect.getsource(cls)
    except Exception as e:
        code = f"# Source not available: {e}"
    CodeViewer(master, code, f"{cls.__name__} source")

# ------------------------------- mini apps ------------------------------------
class ExpenseTracker(ttk.Frame):
    FILE = DATA_DIR / "expenses.json"
    def __init__(self, master):
        super().__init__(master, padding=10)
        self.data: List[Dict[str, Any]] = safe_load_json(self.FILE, [])
        head = section(self, "Expense Tracker", "Add entries and review summaries")
        grid = ttk.Frame(head); grid.pack(fill="x", pady=6)
        self.amount = tk.StringVar()
        self.category = tk.StringVar()
        self.date = tk.StringVar(value=str(datetime.date.today()))
        ttk.Label(grid, text="Amount").grid(row=0, column=0, sticky="w")
        ttk.Entry(grid, textvariable=self.amount, width=10).grid(row=0, column=1, padx=6)
        ttk.Label(grid, text="Category").grid(row=0, column=2, sticky="w")
        ttk.Entry(grid, textvariable=self.category, width=16).grid(row=0, column=3, padx=6)
        ttk.Label(grid, text="Date YYYY-MM-DD").grid(row=0, column=4, sticky="w")
        ttk.Entry(grid, textvariable=self.date, width=12).grid(row=0, column=5, padx=6)
        ttk.Button(grid, text="Add", command=self.add, style="Accent.TButton").grid(row=0, column=6, padx=6)
        ttk.Button(grid, text="Export CSV", command=self.export_csv).grid(row=0, column=7, padx=6)
        self.table = ttk.Treeview(self, columns=("date","cat","amt"), show="headings", height=10)
        self.table.pack(fill="both", expand=True, pady=8)
        for k, w in [("date", 140), ("cat", 180), ("amt", 120)]:
            self.table.heading(k, text=k.title()); self.table.column(k, width=w, anchor="w")
        bar = ttk.Frame(self); bar.pack(fill="x")
        ttk.Button(bar, text="Summary", command=self.show_summary).pack(side="left")
        if _HAS_MPL:
            ttk.Button(bar, text="Bar Chart", command=self.show_chart).pack(side="left", padx=6)
        ttk.Button(bar, text="View Tab Code", command=lambda: view_source(self, ExpenseTracker)).pack(side="right")
        self.refresh()
    def add(self):
        try:
            amt = float(self.amount.get().strip())
            cat = self.category.get().strip() or "General"
            dt = datetime.datetime.strptime(self.date.get().strip(), "%Y-%m-%d").date().isoformat()
            self.data.append({"amount": amt, "category": cat, "date": dt})
            safe_save_json(self.FILE, self.data)
            self.amount.set(""); self.category.set("")
            self.refresh()
        except Exception as e:
            messagebox.showerror("Invalid input", str(e))
    def refresh(self):
        for i in self.table.get_children(): self.table.delete(i)
        for r in self.data:
            self.table.insert("", "end", values=(r["date"], r["category"], f"{r['amount']:.2f}"))
    def show_summary(self):
        if not self.data:
            messagebox.showinfo("Summary", "No data yet")
            return
        cats: Dict[str, float] = {}
        for r in self.data:
            cats[r["category"]] = cats.get(r["category"], 0.0) + float(r["amount"])
        lines = [f"{k}: {v:.2f}" for k, v in sorted(cats.items())]
        messagebox.showinfo("Category totals", "\n".join(lines))
    def show_chart(self):
        cats: Dict[str, float] = {}
        for r in self.data:
            cats[r["category"]] = cats.get(r["category"], 0.0) + float(r["amount"])
        if not cats:
            messagebox.showinfo("Chart", "No data to chart")
            return
        win = tk.Toplevel(self); win.title("Expenses by category"); set_app_icon(win); win.geometry("720x460")
        fig, ax = plt.subplots()
        ax.bar(list(cats.keys()), list(cats.values()))
        ax.set_ylabel("Amount"); ax.set_title("Expenses by category"); ax.tick_params(axis="x", rotation=30)
        canvas = FigureCanvasTkAgg(fig, master=win); canvas.draw(); canvas.get_tk_widget().pack(fill="both", expand=True)
    def export_csv(self):
        fp = filedialog.asksaveasfilename(title="Export CSV", defaultextension=".csv", initialfile="expenses.csv")
        if not fp:
            return
        with open(fp, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["date", "category", "amount"])
            for r in self.data: w.writerow([r["date"], r["category"], r["amount"]])
        messagebox.showinfo("Export complete", "CSV saved")

class MiniAdventure(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        section(self, "Adventure", "Small branching story")
        self.out = scrolledtext.ScrolledText(self, height=18, wrap="word", font=("Segoe UI", 10))
        self.out.pack(fill="both", expand=True)
        bar = ttk.Frame(self); bar.pack(pady=6, fill="x")
        self.state = 0
        ttk.Button(bar, text="Start", command=self.start, style="Accent.TButton").pack(side="left")
        ttk.Button(bar, text="Choice A", command=lambda: self.choice("A")).pack(side="left", padx=6)
        ttk.Button(bar, text="Choice B", command=lambda: self.choice("B")).pack(side="left")
        ttk.Button(bar, text="View Tab Code", command=lambda: view_source(self, MiniAdventure)).pack(side="right")
    def write(self, s): self.out.insert("end", s + "\n"); self.out.see("end")
    def start(self): self.out.delete("1.0", "end"); self.write("You stand before a silent cave. Enter or walk the forest?"); self.state = 1
    def choice(self, c):
        if self.state == 0: self.start(); return
        if self.state == 1:
            if c == "A": self.write("You enter the cave. A faint glow ahead. Continue or retreat?"); self.state = 2
            else: self.write("You walk the forest path and find a river. Cross or follow?"); self.state = 3
        elif self.state == 2:
            if c == "A": self.write("You find crystals and a map. Victory."); self.state = 0
            else: self.write("You trip on a rock and crawl back to safety. The end."); self.state = 0
        elif self.state == 3:
            if c == "A": self.write("You cross safely, discovering an abandoned camp. The end."); self.state = 0
            else: self.write("Following the river leads you home. The end."); self.state = 0

class PasswordVault(ttk.Frame):
    FILE = DATA_DIR / "passwords.json"
    def __init__(self, master):
        super().__init__(master, padding=10)
        self.data: Dict[str, str] = safe_load_json(self.FILE, {})
        section(self, "Password Vault", "Educational example, not for real secrets")
        grid = ttk.Frame(self); grid.pack(pady=6)
        self.site = tk.StringVar(); self.pw = tk.StringVar()
        ttk.Label(grid, text="Site").grid(row=0, column=0, sticky="w")
        ttk.Entry(grid, textvariable=self.site, width=24).grid(row=0, column=1, padx=6)
        ttk.Label(grid, text="Password").grid(row=1, column=0, sticky="w")
        ttk.Entry(grid, textvariable=self.pw, width=24, show="*").grid(row=1, column=1, padx=6)
        ttk.Button(grid, text="Save", command=self.save_pw, style="Accent.TButton").grid(row=2, column=0, pady=6)
        ttk.Button(grid, text="Show", command=self.show_pw).grid(row=2, column=1, pady=6)
        self.list = tk.Listbox(self, height=8); self.list.pack(fill="x")
        ttk.Label(self, text="This is a demo, use a real password manager for production").pack(anchor="w", pady=(4, 0))
        ttk.Button(self, text="View Tab Code", command=lambda: view_source(self, PasswordVault)).pack(anchor="e", pady=6)
        self.refresh_list()
    @staticmethod
    def _enc(s: str, k: int = 3) -> str:
        return "".join(chr((ord(ch) + k) % 65535) for ch in s)
    @staticmethod
    def _dec(s: str, k: int = 3) -> str:
        return "".join(chr((ord(ch) - k) % 65535) for ch in s)
    def save_pw(self):
        site = self.site.get().strip(); pw = self.pw.get()
        if not site or not pw:
            messagebox.showerror("Missing", "Fill both fields")
            return
        self.data[site] = self._enc(pw)
        safe_save_json(self.FILE, self.data)
        self.pw.set("")
        self.refresh_list()
    def show_pw(self):
        sel = self.list.curselection()
        if not sel: return
        site = self.list.get(sel[0])
        messagebox.showinfo("Password", f"{site}: {self._dec(self.data.get(site, '?'))}")
    def refresh_list(self):
        self.list.delete(0, "end")
        for s in sorted(self.data.keys()):
            self.list.insert("end", s)

class TodoApp(ttk.Frame):
    FILE = DATA_DIR / "tasks.json"
    def __init__(self, master):
        super().__init__(master, padding=10)
        self.data: List[str] = safe_load_json(self.FILE, [])
        section(self, "To Do", "Quick task list")
        row = ttk.Frame(self); row.pack(fill="x", pady=6)
        self.entry = ttk.Entry(row); self.entry.pack(side="left", fill="x", expand=True); self.entry.bind("<Return>", lambda e: self.add())
        ttk.Button(row, text="Add", command=self.add, style="Accent.TButton").pack(side="left", padx=6)
        self.list = tk.Listbox(self, height=12); self.list.pack(fill="both", expand=True)
        bar = ttk.Frame(self); bar.pack(pady=6, fill="x")
        ttk.Button(bar, text="Remove selected", command=self.remove, style="Danger.TButton").pack(side="left")
        ttk.Button(bar, text="View Tab Code", command=lambda: view_source(self, TodoApp)).pack(side="right")
        self.refresh()
    def add(self):
        t = self.entry.get().strip()
        if not t: return
        self.data.append(t); safe_save_json(self.FILE, self.data); self.entry.delete(0, "end"); self.refresh()
    def remove(self):
        sel = self.list.curselection()
        if not sel: return
        self.data.pop(sel[0]); safe_save_json(self.FILE, self.data); self.refresh()
    def refresh(self):
        self.list.delete(0, "end")
        for t in self.data: self.list.insert("end", t)

class WebScraper(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        section(self, "Web Scraper", "Fetch page title and first links")
        row = ttk.Frame(self); row.pack(fill="x", pady=6)
        self.url = tk.StringVar(value="https://example.com")
        ttk.Label(row, text="URL").pack(side="left")
        ttk.Entry(row, textvariable=self.url).pack(side="left", fill="x", expand=True, padx=6)
        ttk.Button(row, text="Fetch", command=self.fetch, style="Accent.TButton").pack(side="left")
        self.out = scrolledtext.ScrolledText(self, height=18); self.out.pack(fill="both", expand=True, pady=6)
        ttk.Button(self, text="View Tab Code", command=lambda: view_source(self, WebScraper)).pack(anchor="e")
    def fetch(self):
        if not _HAS_WEB:
            messagebox.showerror("Missing", "requests and bs4 required"); return
        url = self.url.get().strip()
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            title = soup.title.text.strip() if soup.title else "(no title)"
            self.out.delete("1.0", "end")
            self.out.insert("end", f"Title: {title}\n\nLinks:\n")
            for i, a in enumerate(soup.find_all("a", href=True)[:20], 1):
                label = a.get_text(" ").strip().replace("\n", " ")
                self.out.insert("end", f"{i:02d}. {label[:60]} -> {a['href']}\n")
        except Exception as e:
            messagebox.showerror("Fetch failed", str(e))

class UnitConverter(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        section(self, "Unit Converter", "Length, weight, temperature")
        grid = ttk.Frame(self); grid.pack(pady=6)
        self.inp = tk.StringVar(); self.mode = tk.StringVar(value="cm->inch"); self.out = tk.StringVar()
        opts = ["cm->inch", "inch->cm", "kg->lb", "lb->kg", "C->F", "F->C"]
        ttk.Entry(grid, textvariable=self.inp, width=12).grid(row=0, column=0, padx=6)
        ttk.Combobox(grid, values=opts, textvariable=self.mode, width=10, state="readonly").grid(row=0, column=1, padx=6)
        ttk.Button(grid, text="Convert", command=self.convert, style="Accent.TButton").grid(row=0, column=2, padx=6)
        ttk.Label(grid, textvariable=self.out, font=("Segoe UI", 11, "bold")).grid(row=0, column=3, padx=10)
        ttk.Button(self, text="View Tab Code", command=lambda: view_source(self, UnitConverter)).pack(anchor="e", pady=6)
    def convert(self):
        try:
            v = float(self.inp.get())
            m = self.mode.get()
            res = {
                "cm->inch": v / 2.54,
                "inch->cm": v * 2.54,
                "kg->lb": v * 2.20462,
                "lb->kg": v / 2.20462,
                "C->F": v * 9 / 5 + 32,
                "F->C": (v - 32) * 5 / 9,
            }[m]
            self.out.set(f"{res:.3f}")
        except Exception:
            self.out.set("Invalid")

class QuizGame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        section(self, "Quiz", "Five quick questions")
        self.qs = [
            ("Which keyword defines a function in Python?", ["def", "fun", "func"], 0),
            ("What does len([1,2,3]) return?", ["2", "3", "4"], 1),
            ("Which type is immutable?", ["list", "dict", "tuple"], 2),
            ("What opens a file for reading text?", ["open(path,'r')", "read(path)", "file.read()"], 0),
            ("Which library plots charts?", ["matplotlib", "bs4", "ttkbootstrap"], 0),
        ]
        self.idx = 0; self.score = 0
        self.qvar = tk.StringVar(); self.sel = tk.IntVar(value=-1)
        ttk.Label(self, textvariable=self.qvar, wraplength=700).pack(anchor="w", pady=6)
        self.opts = []
        for i in range(3):
            rb = ttk.Radiobutton(self, text="", value=i, variable=self.sel)
            rb.pack(anchor="w"); self.opts.append(rb)
        bar = ttk.Frame(self); bar.pack(fill="x", pady=6)
        ttk.Button(bar, text="Submit", command=self.submit, style="Accent.TButton").pack(side="left")
        self.status = ttk.Label(bar, text="Score: 0/0"); self.status.pack(side="left", padx=12)
        ttk.Button(bar, text="View Tab Code", command=lambda: view_source(self, QuizGame)).pack(side="right")
        self.load_q()
    def load_q(self):
        if self.idx >= len(self.qs):
            messagebox.showinfo("Quiz done", f"Final score {self.score}/{len(self.qs)}")
            self.idx = 0; self.score = 0
        q, ans, _ = self.qs[self.idx]
        self.qvar.set(q)
        for i, rb in enumerate(self.opts): rb.config(text=ans[i])
        self.sel.set(-1); self.status.config(text=f"Score: {self.score}/{self.idx}")
    def submit(self):
        if self.sel.get() == -1: return
        correct = self.qs[self.idx][2]
        if self.sel.get() == correct: self.score += 1
        self.idx += 1; self.load_q()

class WeatherMini(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        section(self, "Weather", "Open Meteo, no key required")
        row = ttk.Frame(self); row.pack(fill="x", pady=6)
        self.lat = tk.DoubleVar(value=45.5); self.lon = tk.DoubleVar(value=-73.6)
        ttk.Label(row, text="Latitude").pack(side="left")
        ttk.Entry(row, textvariable=self.lat, width=8).pack(side="left", padx=6)
        ttk.Label(row, text="Longitude").pack(side="left")
        ttk.Entry(row, textvariable=self.lon, width=8).pack(side="left", padx=6)
        ttk.Button(row, text="Fetch", command=self.fetch, style="Accent.TButton").pack(side="left")
        self.out = scrolledtext.ScrolledText(self, height=12); self.out.pack(fill="both", expand=True, pady=6)
        ttk.Button(self, text="View Tab Code", command=lambda: view_source(self, WeatherMini)).pack(anchor="e")
    def fetch(self):
        if not _HAS_WEB:
            messagebox.showerror("Missing", "requests required"); return
        url = f"https://api.open-meteo.com/v1/forecast?latitude={self.lat.get():.3f}&longitude={self.lon.get():.3f}&current_weather=true"
        try:
            r = requests.get(url, timeout=10)
            cw = r.json().get("current_weather", {})
            self.out.delete("1.0", "end")
            for k in ["temperature", "windspeed", "winddirection", "time"]:
                if k in cw: self.out.insert("end", f"{k}: {cw[k]}\n")
        except Exception as e:
            messagebox.showerror("Fetch failed", str(e))

class Plotter(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        section(self, "Plotter", "Plot comma separated values")
        row = ttk.Frame(self); row.pack(fill="x", pady=6)
        self.vals = tk.StringVar(value="1,2,3,4,3,2,1")
        ttk.Label(row, text="Values").pack(side="left")
        ttk.Entry(row, textvariable=self.vals).pack(side="left", fill="x", expand=True, padx=6)
        ttk.Button(row, text="Plot", command=self.plot, style="Accent.TButton").pack(side="left")
        ttk.Button(self, text="View Tab Code", command=lambda: view_source(self, Plotter)).pack(anchor="e", pady=6)
    def plot(self):
        if not _HAS_MPL:
            messagebox.showerror("Missing", "matplotlib required"); return
        try:
            nums = [float(x.strip()) for x in self.vals.get().split(",") if x.strip()]
            win = tk.Toplevel(self); win.title("Plot"); set_app_icon(win); win.geometry("720x460")
            fig, ax = plt.subplots()
            ax.plot(nums, marker="o"); ax.set_title("Values plot"); ax.set_xlabel("Index"); ax.set_ylabel("Value")
            canvas = FigureCanvasTkAgg(fig, master=win); canvas.draw(); canvas.get_tk_widget().pack(fill="both", expand=True)
        except Exception as e:
            messagebox.showerror("Plot failed", str(e))

class Reminders(ttk.Frame):
    FILE = DATA_DIR / "reminders.json"
    def __init__(self, master):
        super().__init__(master, padding=10)
        self.data: List[Dict[str, Any]] = safe_load_json(self.FILE, [])
        section(self, "Reminders", "Dated notes")
        grid = ttk.Frame(self); grid.pack(pady=6)
        self.msg = tk.StringVar(); self.date = tk.StringVar(value=str(datetime.date.today()))
        ttk.Entry(grid, textvariable=self.msg, width=40).grid(row=0, column=0, padx=6)
        ttk.Entry(grid, textvariable=self.date, width=12).grid(row=0, column=1, padx=6)
        ttk.Button(grid, text="Add", command=self.add, style="Accent.TButton").grid(row=0, column=2, padx=6)
        self.list = tk.Listbox(self, height=10); self.list.pack(fill="both", expand=True, pady=6)
        bar = ttk.Frame(self); bar.pack(fill="x")
        ttk.Button(bar, text="Remove selected", command=self.remove, style="Danger.TButton").pack(side="left")
        ttk.Button(bar, text="View Tab Code", command=lambda: view_source(self, Reminders)).pack(side="right")
        self.refresh()
    def add(self):
        try:
            d = datetime.datetime.strptime(self.date.get().strip(), "%Y-%m-%d").date().isoformat()
            msg = self.msg.get().strip()
            if not msg: raise ValueError("Message required")
            self.data.append({"date": d, "message": msg}); safe_save_json(self.FILE, self.data); self.msg.set(""); self.refresh()
        except Exception as e:
            messagebox.showerror("Invalid", str(e))
    def remove(self):
        sel = self.list.curselection()
        if not sel: return
        self.data.pop(sel[0]); safe_save_json(self.FILE, self.data); self.refresh()
    def refresh(self):
        self.list.delete(0, "end")
        today = datetime.date.today()
        for r in sorted(self.data, key=lambda x: x["date"]):
            d = datetime.date.fromisoformat(r["date"])
            status = "Today" if d == today else "Future" if d > today else "Past"
            self.list.insert("end", f"{status} | {r['date']} | {r['message']}")

class TextTools(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        section(self, "Text Tools", "Word count and frequency")
        self.inp = scrolledtext.ScrolledText(self, height=12)
        self.inp.pack(fill="both", expand=True)
        row = ttk.Frame(self); row.pack(fill="x", pady=6)
        ttk.Button(row, text="Analyze", command=self.analyze, style="Accent.TButton").pack(side="left")
        ttk.Button(row, text="View Tab Code", command=lambda: view_source(self, TextTools)).pack(side="right")
        self.out = scrolledtext.ScrolledText(self, height=10)
        self.out.pack(fill="both", expand=True, pady=6)
    def analyze(self):
        text = self.inp.get("1.0", "end").strip()
        words = [w.strip(".,;:!?()[]{}\"'").lower() for w in text.split()]
        freq: Dict[str, int] = {}
        for w in words:
            if w: freq[w] = freq.get(w, 0) + 1
        lines = [f"{w}: {c}" for w, c in sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:50]]
        self.out.delete("1.0", "end")
        self.out.insert("end", f"Words: {len(words)}\nUnique: {len(freq)}\n\nTop:\n" + "\n".join(lines))

class TimerTool(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        section(self, "Timer", "Simple countdown")
        row = ttk.Frame(self); row.pack(pady=6)
        self.sec = tk.IntVar(value=10)
        ttk.Label(row, text="Seconds").pack(side="left")
        ttk.Entry(row, textvariable=self.sec, width=6).pack(side="left", padx=6)
        ttk.Button(row, text="Start", command=self.start, style="Accent.TButton").pack(side="left")
        self.lbl = ttk.Label(self, text="Ready"); self.lbl.pack(pady=10)
        ttk.Button(self, text="View Tab Code", command=lambda: view_source(self, TimerTool)).pack(anchor="e")
    def start(self):
        try:
            n = int(self.sec.get())
            self._tick(n)
        except Exception:
            self.lbl.config(text="Invalid number")
    def _tick(self, n: int):
        self.lbl.config(text=f"{n}s remaining" if n > 0 else "Done")
        if n > 0:
            self.after(1000, lambda: self._tick(n - 1))

# ------------------------------- main window ----------------------------------
class MainApp(tb.Window if _HAS_TTKB else tk.Tk):
    def __init__(self):
        if _HAS_TTKB:
            super().__init__(themename="darkly")
        else:
            super().__init__()
        self.title(f"{APP_NAME} · v{APP_VERSION}")
        set_app_icon(self)
        self.geometry("1200x780")
        self.minsize(960, 640)
        apply_2025_dark_style(self)

        # header
        top = ttk.Frame(self, padding=(12, 8)); top.pack(fill="x")
        # small icon at left
        try:
            if _HAS_PIL and ICON_PATH.exists():
                img = Image.open(ICON_PATH).resize((20, 20))
                tkimg = ImageTk.PhotoImage(img)
                ico = ttk.Label(top, image=tkimg); ico.image = tkimg; ico.pack(side="left", padx=(0, 8))
        except Exception:
            pass
        ttk.Label(top, text=APP_NAME, style="Header.TLabel").pack(side="left")
        ttk.Button(top, text="Export All Data", command=export_zip_all).pack(side="right")
        ttk.Button(top, text="Help", command=lambda: open_url(HOMEPAGE)).pack(side="right", padx=6)
        ttk.Button(top, text="About", command=self.show_about).pack(side="right")

        # tabs
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=10, pady=10)

        tabs = [
            ("Expenses", ExpenseTracker),
            ("Adventure", MiniAdventure),
            ("Passwords", PasswordVault),
            ("To Do", TodoApp),
            ("Scraper", WebScraper),
            ("Converter", UnitConverter),
            ("Quiz", QuizGame),
            ("Weather", WeatherMini),
            ("Plotter", Plotter),
            ("Reminders", Reminders),
            ("Text Tools", TextTools),
            ("Timer", TimerTool),
        ]
        for name, cls in tabs:
            try:
                tab = cls(self.nb)
                self.nb.add(tab, text=name)
            except Exception as e:
                err = ttk.Frame(self.nb, padding=10)
                ttk.Label(err, text=f"Failed to load {name}: {e}").pack(anchor="w")
                self.nb.add(err, text=name)

    def show_about(self):
        messagebox.showinfo(
            "About",
            f"{APP_NAME}\nVersion {APP_VERSION}\n{ORG}\nicon.ico is used if present next to the app\nNo data leaves your computer",
        )

# ---------------------------------- run ---------------------------------------
if __name__ == "__main__":
    try:
        app = MainApp()
        app.mainloop()
    except Exception as e:
        traceback.print_exc()
        # tk may not be fully initialized if the error occurs early
        try:
            messagebox.showerror("Fatal error", str(e))
        except Exception:
            print(f"Fatal error: {e}")
