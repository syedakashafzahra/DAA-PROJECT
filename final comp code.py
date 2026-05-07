import tkinter as tk
from tkinter import messagebox
import random
import math


# ── Colours ──────────────────────────────────────────────────────────────────
BG_DARK      = "#0f0f1a"
BG_CARD      = "#1a1a2e"
BG_PANEL     = "#16213e"
ACCENT_BLUE  = "#0f3460"
ACCENT_CYAN  = "#00d4ff"
ACCENT_GREEN = "#00ff88"
ACCENT_RED   = "#ff4757"
ACCENT_GOLD  = "#ffd700"
ACCENT_PURPLE= "#7c3aed"
TEXT_MAIN    = "#e8e8f0"
TEXT_DIM     = "#8888aa"
COIN_DEFAULT = "#1e3a5f"
COIN_HOVER   = "#2a4f7f"
COIN_WRONG   = "#4a1528"
COIN_RIGHT   = "#0a3d2e"


class FakeCoinGame:
    def __init__(self, n=12, g=10):
        self.n          = n
        self.g          = g
        self.fake_index = random.randint(0, n - 1)
        self.fake_type  = random.choice(["lighter", "heavier"])
        self.coins      = []
        self.steps      = 0
        self.weigh_log  = []
        for i in range(n):
            if i == self.fake_index:
                self.coins.append(g - 2 if self.fake_type == "lighter" else g + 2)
            else:
                self.coins.append(g)

    def weigh(self, start, end):
        self.steps += 1
        total    = sum(self.coins[start:end + 1])
        expected = (end - start + 1) * self.g
        self.weigh_log.append({
            "step": self.steps,
            "range": f"[{start}..{end}]",
            "actual": total,
            "expected": expected,
            "match": total == expected,
        })
        return total


class GameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Fake Coin Detector — DAA Assignment #4")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(True, True)

        self.show_weights = False
        self.game         = None
        self.attempts     = 0
        self.max_attempts = 6
        self.game_over    = False

        self.show_start_menu()

    # ── helpers ──────────────────────────────────────────────────────────────
    def clear_screen(self):
        for w in self.root.winfo_children():
            w.destroy()

    def _btn(self, parent, text, cmd, bg, fg=TEXT_MAIN,
             font=("Segoe UI", 11, "bold"), pady=8, padx=20):
        return tk.Button(
            parent, text=text, command=cmd,
            bg=bg, fg=fg,
            activebackground=ACCENT_CYAN, activeforeground=BG_DARK,
            font=font, pady=pady, padx=padx,
            relief="flat", bd=0, cursor="hand2"
        )

    # ════════════════════════════════════════════════════════════════════════
    # START MENU
    # ════════════════════════════════════════════════════════════════════════
    def show_start_menu(self):
        self.clear_screen()
        self.root.geometry("980x700")
        self.root.minsize(820, 600)

        # Header
        hdr = tk.Frame(self.root, bg=ACCENT_BLUE)
        hdr.pack(fill="x")
        tk.Label(hdr, text="FAKE COIN DETECTOR",
                 font=("Segoe UI", 28, "bold"),
                 fg=ACCENT_CYAN, bg=ACCENT_BLUE).pack(pady=(18, 2))
        tk.Label(hdr, text="Design & Analysis of Algorithms  •  Puzzle #53",
                 font=("Segoe UI", 10), fg=TEXT_DIM, bg=ACCENT_BLUE).pack(pady=(0, 14))

        # Two-column body using grid
        body = tk.Frame(self.root, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=30, pady=16)
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        # LEFT card
        left = tk.Frame(body, bg=BG_CARD, padx=20, pady=16)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        tk.Label(left, text="HOW TO PLAY",
                 font=("Segoe UI", 14, "bold"),
                 fg=ACCENT_CYAN, bg=BG_CARD).pack(anchor="w")
        tk.Frame(left, bg=ACCENT_BLUE, height=2).pack(fill="x", pady=(4, 12))

        rules = [
            ("🪙", "12 coins — one is FAKE (heavier or lighter)"),
            ("⚖",  "Spring scale returns the exact total weight"),
            ("🎯", "You have 6 attempts to click the correct fake coin"),
            ("🔎", "Use binary search logic to narrow it down"),
            ("💡", "'Show Solution' animates the O(log n) algorithm"),
            ("📊", "Watch the Efficiency Panel for live stats"),
        ]
        for icon, txt in rules:
            row = tk.Frame(left, bg=BG_CARD)
            row.pack(anchor="w", fill="x", pady=4)
            tk.Label(row, text=icon, font=("Segoe UI", 13),
                     fg=ACCENT_GOLD, bg=BG_CARD, width=3).pack(side="left")
            tk.Label(row, text=txt, font=("Segoe UI", 11),
                     fg=TEXT_MAIN, bg=BG_CARD,
                     wraplength=300, justify="left").pack(side="left", padx=4)

        # RIGHT card — complexity table using grid (no place(), no clipping)
        right = tk.Frame(body, bg=BG_CARD, padx=20, pady=16)
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        tk.Label(right, text="ALGORITHM COMPLEXITY",
                 font=("Segoe UI", 14, "bold"),
                 fg=ACCENT_CYAN, bg=BG_CARD).pack(anchor="w")
        tk.Frame(right, bg=ACCENT_BLUE, height=2).pack(fill="x", pady=(4, 14))

        # Table frame — grid layout, guaranteed no clipping
        tbl = tk.Frame(right, bg=BG_CARD)
        tbl.pack(fill="x")

        headers    = ["Method",         "Worst",    "Best",     "Avg"]
        hdr_colors = [TEXT_DIM,         ACCENT_GOLD, ACCENT_GREEN, ACCENT_CYAN]
        col_widths = [15,               10,          10,          10]

        # Header row
        for c, (h, col, w) in enumerate(zip(headers, hdr_colors, col_widths)):
            tk.Label(tbl, text=h,
                     font=("Consolas", 10, "bold"),
                     fg=col, bg=BG_CARD,
                     width=w, anchor="w"
                     ).grid(row=0, column=c, padx=6, pady=(0, 4), sticky="w")

        # Thin divider
        tk.Frame(tbl, bg=ACCENT_BLUE, height=1
                 ).grid(row=1, column=0, columnspan=4, sticky="ew",
                        padx=4, pady=(0, 6))

        # Data rows
        rows_data = [
            ("Brute Force",   "O(n)",     "Ω(1)",  "Θ(n)"),
            ("Binary Search", "O(log n)", "Ω(1)",  "Θ(log n)"),
        ]
        row_bgs   = [BG_PANEL, ACCENT_BLUE]
        val_colors = [ACCENT_CYAN, ACCENT_RED, ACCENT_GREEN, ACCENT_GOLD]

        for r, row_vals in enumerate(rows_data):
            bg = row_bgs[r]
            rf = tk.Frame(tbl, bg=bg, pady=6)
            rf.grid(row=r + 2, column=0, columnspan=4,
                    sticky="ew", padx=2, pady=3)
            for c, (val, vc, w) in enumerate(zip(row_vals, val_colors, col_widths)):
                tk.Label(rf, text=val,
                         font=("Consolas", 11, "bold"),
                         fg=vc, bg=bg,
                         width=w, anchor="w"
                         ).grid(row=0, column=c, padx=6, sticky="w")

        n = 12
        max_b  = math.ceil(math.log2(n))
        saving = round((1 - max_b / n) * 100)
        tk.Label(right,
                 text=(f"\nFor n={n}:  Binary Search  ≤ {max_b} weighings\n"
                       f"vs up to {n} for Brute Force  →  {saving}% fewer ops"),
                 font=("Consolas", 10), fg=ACCENT_GREEN,
                 bg=BG_CARD, justify="left").pack(anchor="w", pady=(10, 0))

        # Bottom buttons
        btns = tk.Frame(self.root, bg=BG_DARK)
        btns.pack(pady=18)

        self._btn(btns, "▶   START GAME", self.start_game,
                  ACCENT_CYAN, fg=BG_DARK,
                  font=("Segoe UI", 13, "bold"), pady=10, padx=40
                  ).pack(side="left", padx=12)

        self._btn(btns, "✕   EXIT", self.root.destroy,
                  ACCENT_RED, font=("Segoe UI", 12, "bold"),
                  pady=10, padx=28
                  ).pack(side="left", padx=12)

    # ════════════════════════════════════════════════════════════════════════
    # GAME SCREEN
    # ════════════════════════════════════════════════════════════════════════
    def start_game(self):
        self.clear_screen()
        self.root.geometry("1050x720")
        self.root.minsize(900, 640)
        self.game         = FakeCoinGame()
        self.attempts     = 0
        self.game_over    = False
        self.show_weights = False
        self._build_game_ui()

    def _build_game_ui(self):
        # Top bar
        top = tk.Frame(self.root, bg=ACCENT_BLUE, height=52)
        top.pack(fill="x")
        top.pack_propagate(False)

        tk.Label(top, text="FAKE COIN DETECTOR",
                 font=("Segoe UI", 14, "bold"),
                 fg=ACCENT_CYAN, bg=ACCENT_BLUE).pack(side="left", padx=20)

        self.status_var = tk.StringVar(value="Attempts: 0/6   |   Weighings: 0")
        tk.Label(top, textvariable=self.status_var,
                 font=("Consolas", 11, "bold"),
                 fg=TEXT_MAIN, bg=ACCENT_BLUE).pack(side="right", padx=20)

        # Main area
        main = tk.Frame(self.root, bg=BG_DARK)
        main.pack(fill="both", expand=True, padx=16, pady=10)
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, minsize=280)
        main.rowconfigure(0, weight=1)

        left_col = tk.Frame(main, bg=BG_DARK)
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        right_col = tk.Frame(main, bg=BG_DARK, width=280)
        right_col.grid(row=0, column=1, sticky="nsew")
        right_col.grid_propagate(False)

        # Result label
        self.result_var = tk.StringVar(value="Click a coin to test it!")
        tk.Label(left_col, textvariable=self.result_var,
                 font=("Segoe UI", 12, "bold"),
                 fg=ACCENT_GOLD, bg=BG_DARK,
                 wraplength=580, justify="center").pack(pady=(4, 10))

        # Coin grid
        coin_outer = tk.Frame(left_col, bg=BG_DARK)
        coin_outer.pack()
        self.buttons = []
        for i in range(self.game.n):
            btn = tk.Button(
                coin_outer, text=f"🪙\n{i}",
                width=8, height=3,
                bg=COIN_DEFAULT, fg=ACCENT_CYAN,
                activebackground=COIN_HOVER,
                font=("Segoe UI", 10, "bold"),
                relief="flat", bd=0, cursor="hand2",
                command=lambda idx=i: self.check_coin(idx)
            )
            btn.grid(row=i // 4, column=i % 4, padx=7, pady=7)
            self.buttons.append(btn)

        # Search visualiser bar
        viz_card = tk.Frame(left_col, bg=BG_CARD, padx=14, pady=10)
        viz_card.pack(fill="x", pady=(16, 0))
        tk.Label(viz_card, text="Binary Search Active Window",
                 font=("Segoe UI", 10, "bold"),
                 fg=ACCENT_CYAN, bg=BG_CARD).pack(anchor="w")
        self.viz_canvas = tk.Canvas(viz_card, height=40, bg=BG_CARD,
                                    highlightthickness=0)
        self.viz_canvas.pack(fill="x", pady=(6, 0))
        self.viz_canvas.bind("<Configure>",
                             lambda e: self._draw_viz(0, self.game.n - 1, -1))
        self._draw_viz(0, self.game.n - 1, -1)

        self._build_right_panel(right_col)

    def _build_right_panel(self, parent):
        # Controls
        ctrl = tk.Frame(parent, bg=BG_CARD, padx=14, pady=12)
        ctrl.pack(fill="x")
        tk.Label(ctrl, text="CONTROLS",
                 font=("Segoe UI", 9, "bold"),
                 fg=TEXT_DIM, bg=BG_CARD).pack(anchor="w", pady=(0, 6))

        for txt, bg, cmd in [
            ("💡  Show Solution",  ACCENT_PURPLE, self.show_solution),
            ("👁  Reveal Coin",    "#92400e",     self.reveal_fake),
            ("⚖  Toggle Weights", ACCENT_BLUE,   self.toggle_weights),
            ("🔄  Restart",        "#065f46",     self.restart_game),
            ("🏠  Main Menu",      "#374151",     self.show_start_menu),
        ]:
            tk.Button(ctrl, text=txt, command=cmd,
                      bg=bg, fg=TEXT_MAIN,
                      activebackground=ACCENT_CYAN, activeforeground=BG_DARK,
                      font=("Segoe UI", 10, "bold"),
                      relief="flat", bd=0, cursor="hand2",
                      width=24, pady=7
                      ).pack(fill="x", pady=3)

        # Efficiency panel
        eff = tk.Frame(parent, bg=BG_CARD, padx=14, pady=12)
        eff.pack(fill="both", expand=True, pady=(10, 0))
        tk.Label(eff, text="EFFICIENCY PANEL",
                 font=("Segoe UI", 10, "bold"),
                 fg=ACCENT_CYAN, bg=BG_CARD).pack(anchor="w")
        tk.Frame(eff, bg=ACCENT_BLUE, height=1).pack(fill="x", pady=(4, 8))

        self.eff_vars = {}
        for lbl, val in [
            ("n  (total coins)",    str(self.game.n)),
            ("Algo Weighings",      "0"),
            ("Max Binary log2(n)",  str(math.ceil(math.log2(self.game.n)))),
            ("Brute Force Max",     str(self.game.n)),
            ("Weighings Saved",     "—"),
            ("Speed-up Ratio",      "—"),
        ]:
            row = tk.Frame(eff, bg=BG_CARD)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=lbl,
                     font=("Consolas", 9), fg=TEXT_DIM,
                     bg=BG_CARD, anchor="w", width=20).pack(side="left")
            v = tk.StringVar(value=val)
            self.eff_vars[lbl] = v
            tk.Label(row, textvariable=v,
                     font=("Consolas", 10, "bold"),
                     fg=ACCENT_GOLD, bg=BG_CARD).pack(side="right")

        tk.Label(eff, text="WEIGH LOG",
                 font=("Segoe UI", 9, "bold"),
                 fg=ACCENT_CYAN, bg=BG_CARD).pack(anchor="w", pady=(12, 4))

        log_box = tk.Frame(eff, bg=BG_PANEL)
        log_box.pack(fill="both", expand=True)
        self.log_text = tk.Text(log_box, bg=BG_PANEL, fg=ACCENT_GREEN,
                                font=("Consolas", 8), relief="flat",
                                state="disabled")
        sb = tk.Scrollbar(log_box, command=self.log_text.yview,
                          bg=BG_PANEL, troughcolor=BG_DARK)
        self.log_text.config(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.log_text.pack(fill="both", expand=True, padx=4, pady=4)
        self._refresh_log()

    # ── canvas visualiser ─────────────────────────────────────────────────────
    def _draw_viz(self, low, high, mid):
        c = self.viz_canvas
        c.update_idletasks()
        c.delete("all")
        n    = self.game.n
        W    = c.winfo_width() or 600
        cell = W / n
        for i in range(n):
            x1 = i * cell + 2
            x2 = (i + 1) * cell - 2
            if i == mid:
                fill, fc = ACCENT_GOLD, BG_DARK
            elif low <= i <= high:
                fill, fc = ACCENT_BLUE, ACCENT_CYAN
            else:
                fill, fc = "#111122", TEXT_DIM
            c.create_rectangle(x1, 4, x2, 36, fill=fill, outline="")
            c.create_text((x1 + x2) / 2, 20, text=str(i),
                          fill=fc, font=("Consolas", 8))

    # ── status helpers ────────────────────────────────────────────────────────
    def _update_efficiency(self):
        steps = self.game.steps
        n     = self.game.n
        if steps > 0:
            self.eff_vars["Algo Weighings"].set(str(steps))
            self.eff_vars["Weighings Saved"].set(str(n - steps))
            self.eff_vars["Speed-up Ratio"].set(f"{n / steps:.1f}x")
        else:
            self.eff_vars["Algo Weighings"].set("0")
            self.eff_vars["Weighings Saved"].set("—")
            self.eff_vars["Speed-up Ratio"].set("—")

    def _refresh_log(self):
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        if not self.game.weigh_log:
            self.log_text.insert("end", "No weighings yet…\n")
        else:
            for e in self.game.weigh_log:
                sym  = "✓" if e["match"] else "✗"
                self.log_text.insert(
                    "end",
                    f"Step {e['step']}  {e['range']}\n"
                    f"  got={e['actual']}  exp={e['expected']}  {sym}\n"
                )
        self.log_text.config(state="disabled")
        self.log_text.see("end")

    def _update_status(self):
        self.status_var.set(
            f"Attempts: {self.attempts}/{self.max_attempts}   |   "
            f"Weighings: {self.game.steps}"
        )
        self._update_efficiency()
        self._refresh_log()

    # ── game logic ────────────────────────────────────────────────────────────
    def check_coin(self, index):
        if self.game_over:
            return
        self.attempts += 1
        btn = self.buttons[index]
        if index == self.game.fake_index:
            btn.config(bg=COIN_RIGHT, fg=ACCENT_GREEN)
            self.result_var.set(
                f"Correct!  Coin {index} is fake ({self.game.fake_type})"
                f" — found in {self.attempts} attempt(s)!"
            )
            messagebox.showinfo("Winner!",
                f"You found the fake coin!\n\n"
                f"Your attempts : {self.attempts}\n"
                f"Binary search max : {math.ceil(math.log2(self.game.n))} weighings",
                parent=self.root)
            self.game_over = True
            self._disable_all()
        else:
            btn.config(bg=COIN_WRONG, fg=ACCENT_RED)
            rem = self.max_attempts - self.attempts
            self.result_var.set(f"Wrong coin!  {rem} attempt(s) remaining.")
            if self.attempts >= self.max_attempts:
                messagebox.showerror("Game Over",
                    "No attempts left!\nRevealing the fake coin…",
                    parent=self.root)
                self.reveal_fake()
                self.game_over = True
                self._disable_all()
        self._update_status()

    def _disable_all(self):
        for b in self.buttons:
            b.config(state="disabled")

    def show_solution(self):
        self.game.steps    = 0
        self.game.weigh_log = []
        self._solve_step(0, self.game.n - 1, delay=0)

    def _solve_step(self, low, high, delay):
        if low == high:
            self.root.after(delay, lambda: self._solve_done(low))
            return
        mid = (low + high) // 2

        def step():
            self._draw_viz(low, high, mid)
            actual = self.game.weigh(low, mid)
            exp    = (mid - low + 1) * self.game.g
            self._update_status()
            if actual == exp:
                self._solve_step(mid + 1, high, 450)
            else:
                self._solve_step(low,     mid,  450)

        self.root.after(delay, step)

    def _solve_done(self, index):
        self._draw_viz(index, index, index)
        self.buttons[index].config(bg=COIN_RIGHT, fg=ACCENT_GREEN)
        self.result_var.set(
            f"Binary Search found Coin {index}  ({self.game.fake_type})"
            f"  |  {self.game.steps} weighing(s)  vs  {self.game.n} brute-force max"
        )
        self._update_status()
        self.game_over = True
        self._disable_all()

    def reveal_fake(self):
        idx = self.game.fake_index
        self.buttons[idx].config(bg=COIN_RIGHT, fg=ACCENT_GREEN)
        self.result_var.set(f"Fake Coin: {idx}  ({self.game.fake_type})")

    def toggle_weights(self):
        self.show_weights = not self.show_weights
        for i, btn in enumerate(self.buttons):
            if self.show_weights:
                w  = self.game.coins[i]
                fg = ACCENT_RED if w != self.game.g else ACCENT_CYAN
                btn.config(text=f"w={w}\n{i}", fg=fg)
            else:
                btn.config(text=f"🪙\n{i}", fg=ACCENT_CYAN)

    def restart_game(self):
        self.start_game()


if __name__ == "__main__":
    root = tk.Tk()
    GameUI(root)
    root.mainloop()
