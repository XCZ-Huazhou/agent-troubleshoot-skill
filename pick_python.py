#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""agent-troubleshoot · Python 解释器全盘智能扫描 + 点击式选择框

用法：
    python pick_python.py                     # 快速扫描（PATH/py启动器/conda）+ 弹窗点选
    python pick_python.py --deep              # 先快速扫描，再全盘深度扫描（不限时），然后弹窗
    python pick_python.py --deep --roots D:\\
    python pick_python.py --scan-only         # 只打印扫描结果（JSON），不弹窗

说明：
    - 仅用标准库（含 tkinter 图形界面），无需安装任何第三方库
    - 深度扫描会遍历本地固定磁盘查找 python.exe / pypy.exe，
      自动跳过 Windows、回收站、node_modules、.git 等无关目录，不限时直至扫完所有磁盘
    - 选中的解释器路径保存到本目录 .python_default.json，
      之后运行 diagnose.py 时优先使用该解释器
"""

import json
import os
import re
import shutil
import string
import subprocess
import sys
import time
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
SAVE_PATH = SKILL_DIR / ".python_default.json"

SKIP_DIRS = {
    "$recycle.bin", "system volume information", "windows", "winnt",
    "program files", "program files (x86)", "programdata",
    "node_modules", ".git", "__pycache__", "site-packages",
    "dist-packages", "$windows.~bt", "recovery", "onedrivetemp",
    "wutemp", "perflogs",
}


def _add(found, path, source):
    """登记一个候选解释器（绝对路径去重，跳过微软商店占位符）。"""
    if not path:
        return
    p = os.path.abspath(os.path.expandvars(path))
    if not os.path.isfile(p):
        return
    base = os.path.basename(p).lower()
    if ("python" not in base and "pypy" not in base) or not base.endswith(".exe"):
        return
    key = p.lower()
    if key in found:
        return
    if "windowsapps" in key:
        source += "（微软商店占位，慎选）"
    found[key] = {"path": p, "source": source}


def find_interpreters():
    """快速扫描：PATH / py 启动器 / conda / 当前解释器。返回 [{path, source}]。"""
    found = {}

    for name in ("python", "python3"):
        w = shutil.which(name)
        if w:
            _add(found, w, f"PATH 中的 {name}")

    py = shutil.which("py")
    if py:
        try:
            out = subprocess.run([py, "--list-paths"], capture_output=True,
                                 text=True, timeout=20)
            for line in (out.stdout or "").splitlines():
                m = re.search(r"[A-Za-z]:\\[^\s]*python\.exe", line, re.I)
                if m:
                    tag = line.strip().split()[0] if line.strip() else ""
                    _add(found, m.group(0), f"py 启动器 {tag}")
        except Exception:
            pass

    conda = shutil.which("conda")
    if conda:
        try:
            out = subprocess.run([conda, "info", "--json"], capture_output=True,
                                 text=True, timeout=30)
            info = json.loads(out.stdout or "{}")
            for env in info.get("envs", []):
                _add(found, os.path.join(env, "python.exe"), "conda 环境")
        except Exception:
            pass

    _add(found, sys.executable, "当前运行的 Python")
    return list(found.values())


def fixed_drives():
    """枚举本机所有固定盘符根目录（A-Z 中实际存在的）。"""
    roots = []
    for letter in string.ascii_uppercase:
        root = f"{letter}:\\"
        if os.path.isdir(root):
            roots.append(root)
    return roots


def deep_scan(candidates, roots=None):
    """全盘深度扫描：在给定根目录（默认全部固定磁盘）下查找解释器。

    - candidates 为快速扫描结果列表，深度扫描结果会合并后返回
    - 跳过 SKIP_DIRS 中的无关目录；不限时，直至扫完所有磁盘
    """
    if roots is None:
        roots = fixed_drives()

    found = {c["path"].lower(): dict(c) for c in candidates}

    checked = 0
    last_report = time.monotonic()
    for root in roots:
        for cur, dirs, files in os.walk(root, topdown=True, onerror=None):
            checked += 1
            now = time.monotonic()
            if now - last_report > 5:
                last_report = now
                print(f"[深度扫描] 已检查 {checked} 个目录… 当前：{cur}", flush=True)

            dirs[:] = [d for d in dirs if d.lower() not in SKIP_DIRS]
            low_dir = cur.lower().replace("/", "\\") + os.sep
            if low_dir.endswith("\\lib\\venv\\"):
                dirs[:] = []                       # venv 垫片目录，整个跳过
                continue

            exe_hits = []
            for f in files:
                low = f.lower()
                if not low.startswith("python") or not low.endswith(".exe"):
                    continue
                if low.startswith("pythonw"):      # 无窗口版，跳过
                    continue
                exe_hits.append(f)

            for f in exe_hits:
                src = "全盘扫描"
                if ".pixi" in low_dir:
                    src = "pixi 环境"
                elif "envs" in low_dir:
                    src = "环境目录"
                _add(found, os.path.join(cur, f), src)
        # end walk

    return list(found.values())


def save_choice(path, source):
    SAVE_PATH.write_text(
        json.dumps({"default_python": path, "source": source}, ensure_ascii=False, indent=2),
        encoding="utf-8")


def gui_pick(candidates):
    """弹出点击式选择框；返回选中项或 None（用户取消）。"""
    import tkinter as tk
    from tkinter import filedialog, messagebox

    picked = {"path": None, "source": "手动指定"}

    root = tk.Tk()
    root.title("agent-troubleshoot · 选择默认 Python 环境")
    root.attributes("-topmost", True)
    root.geometry("760x440")

    tk.Label(root, text="请点选一个 Python 环境作为本技能的默认解释器：",
             font=("Microsoft YaHei UI", 11, "bold")).pack(anchor="w", padx=12, pady=(12, 4))

    var = tk.StringVar(value=candidates[0]["path"] if candidates else "")
    box = tk.Listbox(root, font=("Consolas", 10), selectmode=tk.SINGLE,
                     activestyle="dotbox")
    for c in candidates:
        box.insert(tk.END, f"{c['path']}    [{c['source']}]")
    box.pack(fill="both", expand=True, padx=12, pady=4)
    if candidates:
        box.selection_set(0)

    def browse():
        f = filedialog.askopenfilename(title="选择其它 Python 解释器",
                                       filetypes=[("Python", "python*.exe"), ("所有文件", "*.*")])
        if f:
            box.insert(tk.END, f"{f}    [手动指定]")
            box.selection_clear(0, tk.END)
            box.selection_set(tk.END)

    def confirm():
        sel = box.curselection()
        if not sel:
            messagebox.showwarning("未选择", "请先在列表中点选一项。", parent=root)
            return
        entry = box.get(sel[0])
        picked["path"] = entry.split("    [")[0]
        picked["source"] = entry.split("    [")[1].rstrip("]") if "    [" in entry else "手动指定"
        root.destroy()

    btns = tk.Frame(root)
    btns.pack(fill="x", padx=12, pady=8)
    tk.Button(btns, text="浏览其它解释器…", command=browse).pack(side="left")
    tk.Button(btns, text="确定 ✔", width=12, bg="#2f7d32", fg="white",
              font=("Microsoft YaHei UI", 10, "bold"), command=confirm).pack(side="right")

    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()
    return picked


def main():
    argv = sys.argv[1:]
    scan_only = "--scan-only" in argv
    do_deep = "--deep" in argv
    roots = None
    extras = []

    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--roots" and i + 1 < len(argv):
            roots = [r for r in argv[i + 1].split(",") if r.strip()]
            i += 2
            continue
        if not a.startswith("--"):
            extras.append(a)
        i += 1

    candidates = find_interpreters()
    seen = {c["path"].lower() for c in candidates}

    if do_deep:
        candidates = deep_scan(candidates, roots=roots)
        seen = {c["path"].lower() for c in candidates}
        for extra in extras:
            p = os.path.abspath(os.path.expandvars(extra))
            if os.path.isfile(p) and p.lower() not in seen:
                candidates.append({"path": p, "source": "指定附加路径"})
                seen.add(p.lower())

    if scan_only or not candidates:
        print(json.dumps({"candidates": candidates}, ensure_ascii=False, indent=2))
        if not candidates:
            print("未扫描到任何解释器；可再次运行并用「浏览」按钮手动指定。")
        return

    picked = gui_pick(candidates)
    if picked and picked.get("path"):
        save_choice(picked["path"], picked["source"])
        print("已保存默认解释器：", picked["path"])
        print("配置文件：", SAVE_PATH)
    else:
        print("已取消，未做更改。")


if __name__ == "__main__":
    main()
