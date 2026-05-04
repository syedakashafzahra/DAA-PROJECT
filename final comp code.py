import tkinter as tk
from tkinter import messagebox
import random


class FakeCoinGame:
    def __init__(self, n=12, g=10):
        self.n = n
        self.g = g

        self.coins = []
        self.fake_index = random.randint(0, n - 1)
        self.fake_type = random.choice(["lighter", "heavier"])

        for i in range(n):
            if i == self.fake_index:
                if self.fake_type == "lighter":
                    self.coins.append(g - 2)
                else:
                    self.coins.append(g + 2)
            else:
                self.coins.append(g)

        self.steps = 0

   
    def weigh(self, start, end):
        self.steps += 1
        return sum(self.coins[start:end + 1])

   
    def binary_search_fake(self, low, high):
        if low == high:
            return low

        mid = (low + high) // 2

        expected = (mid - low + 1) * self.g
        actual = self.weigh(low, mid)

        if actual == expected:
            return self.binary_search_fake(mid + 1, high)
        else:
            return self.binary_search_fake(low, mid)



class GameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Coin Clash: Spot the Fake!")
        self.root.geometry("480x650")
        self.root.configure(bg="#cdb4db")

        self.show_weights = False
        self.show_start_menu()

   
    def show_start_menu(self):
        self.clear_screen()

        tk.Label(
            self.root,
            text="Coin Clash: Spot the Fake!",
            font=("Arial", 20, "bold"),
            fg="#3d2c5a",
            bg="#cdb4db"
        ).pack(pady=15)

        tk.Label(
            self.root,
            text="🪙 Welcome Challenger!",
            font=("Arial", 16, "bold"),
            fg="#5a3e7b",
            bg="#cdb4db"
        ).pack(pady=5)

      
        rules_frame = tk.Frame(self.root, bg="#bde0fe", padx=10, pady=10)
        rules_frame.pack(pady=10)

        tk.Label(
            rules_frame,
            text="📜 GAME RULES",
            font=("Arial", 13, "bold"),
            fg="#1d3557",
            bg="#bde0fe"
        ).pack()

        tk.Label(
            rules_frame,
            text=(
                "• One coin is fake (heavier or lighter)\n"
                "• You have 6 attempts\n"
                "• Click coins to find fake one\n"
                "• Use binary search logic"
            ),
            font=("Arial", 11),
            fg="#1d3557",
            bg="#bde0fe",
            justify="left"
        ).pack()

        tk.Button(
            self.root,
            text="▶ Start Game",
            font=("Arial", 14, "bold"),
            bg="#ffafcc",
            fg="#3d2c5a",
            width=18,
            command=self.start_game
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="❌ Exit",
            font=("Arial", 14, "bold"),
            bg="#ff6b6b",
            fg="white",
            width=18,
            command=self.root.quit
        ).pack(pady=5)

    
    def start_game(self):
        self.clear_screen()

        self.game = FakeCoinGame()
        self.attempts = 0
        self.max_attempts = 6
        self.game_over = False

        tk.Label(
            self.root,
            text="🪙 Find the Fake Coin!",
            font=("Arial", 18, "bold"),
            fg="#3d2c5a",
            bg="#cdb4db"
        ).pack(pady=10)

        self.status = tk.Label(
            self.root,
            text="Attempts: 0/6 | Weighings: 0",
            font=("Arial", 12),
            fg="#2b2d42",
            bg="#cdb4db"
        )
        self.status.pack()

        self.result = tk.Label(
            self.root,
            text="",
            font=("Arial", 12, "bold"),
            fg="#3d2c5a",
            bg="#cdb4db"
        )
        self.result.pack(pady=10)

        self.frame = tk.Frame(self.root, bg="#cdb4db")
        self.frame.pack()

        self.buttons = []
        self.create_buttons()

        self.control_frame = tk.Frame(self.root, bg="#bde0fe", padx=15, pady=15)
        self.control_frame.pack(pady=20)

        tk.Button(
            self.control_frame,
            text="Show Solution",
            font=("Arial", 11, "bold"),
            bg="#90e0ef",
            command=self.show_solution
        ).grid(row=0, column=0, padx=10, pady=6)

        tk.Button(
            self.control_frame,
            text="Reveal Coin",
            font=("Arial", 11, "bold"),
            bg="#ffd6a5",
            command=self.reveal_fake
        ).grid(row=0, column=1, padx=10, pady=6)

        tk.Button(
            self.control_frame,
            text="Restart",
            font=("Arial", 11, "bold"),
            bg="#b8f2e6",
            command=self.restart_game
        ).grid(row=1, column=0, padx=10, pady=6)

        tk.Button(
            self.control_frame,
            text="🏠 Menu",
            font=("Arial", 11, "bold"),
            bg="#ffc8dd",
            command=self.show_start_menu
        ).grid(row=1, column=1, padx=10, pady=6)

        tk.Button(
            self.control_frame,
            text="Show Weights",
            font=("Arial", 11, "bold"),
            bg="#caffbf",
            command=self.toggle_weights
        ).grid(row=2, column=0, columnspan=2, pady=6)

    def create_buttons(self):
        for i in range(self.game.n):
            btn = tk.Button(
                self.frame,
                text=f"🪙 {i}",
                width=8,
                height=2,
                bg="#a2d2ff",
                fg="#1d3557",
                command=lambda i=i: self.check_coin(i)
            )

            btn.grid(row=i // 4, column=i % 4, padx=6, pady=6)
            self.buttons.append(btn)

   
    def toggle_weights(self):
        self.show_weights = not self.show_weights

        for i, btn in enumerate(self.buttons):
            if self.show_weights:
                btn.config(text=f"{i}\n({self.game.coins[i]})")
            else:
                btn.config(text=f"🪙 {i}")

  
    def update_status(self):
        self.status.config(
            text=f"Attempts: {self.attempts}/{self.max_attempts} | Weighings: {self.game.steps}"
        )

    def check_coin(self, index):
        if self.game_over:
            return

        self.attempts += 1
        btn = self.buttons[index]

        if index == self.game.fake_index:
            btn.config(bg="#80ed99", state="disabled")
            self.result.config(
                text=f"🎉 Fake Coin Found! ({self.game.fake_type})",
                fg="#2d6a4f"
            )
            messagebox.showinfo("Winner!", "You found the fake coin!")
            self.game_over = True
            self.disable_all()

        else:
            btn.config(bg="#ffadad", state="disabled")
            self.result.config(text="❌ Wrong coin!", fg="#c1121f")

            if self.attempts >= self.max_attempts:
                messagebox.showerror("Game Over", "No attempts left!")
                self.reveal_fake()
                self.game_over = True
                self.disable_all()

        self.update_status()

  
    def disable_all(self):
        for b in self.buttons:
            b.config(state="disabled")

 
    def show_solution(self):
        self.game.steps = 0

        index = self.game.binary_search_fake(0, self.game.n - 1)

        self.update_status()  

        self.result.config(
            text=f"🔎 Fake Coin: {index} | Type: {self.game.fake_type}",
            fg="#3d2c5a"
        )

        self.game_over = True
        self.disable_all()

    
    def reveal_fake(self):
        self.buttons[self.game.fake_index].config(bg="#80ed99")
        self.result.config(
            text=f"💡 Fake coin: {self.game.fake_index} ({self.game.fake_type})",
            fg="#3d2c5a"
        )

    def restart_game(self):
        self.start_game()

    def clear_screen(self):
        for w in self.root.winfo_children():
            w.destroy()


root = tk.Tk()
app = GameUI(root)
root.mainloop()