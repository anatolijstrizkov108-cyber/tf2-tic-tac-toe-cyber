# -*- coding: utf-8 -*-
import random
import os
import time

# ---- неоновая палитра ----
NEON_PINK   = "\033[95m"
NEON_CYAN   = "\033[96m"
NEON_YELLOW = "\033[93m"
RED_TEAM    = "\033[91m"   # RED
BLU_TEAM    = "\033[94m"   # BLU
DIM         = "\033[90m"
BOLD        = "\033[1m"
RESET       = "\033[0m"

WIN_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)

# ---- «травма тим»-реплики ----
TAUNTS_WIN = [
    "MEDIC! ...а, не, это я тебя подлатал. GG.",
    "КРИТ! КРИТ! КРИТ!",
    "Ты как диспенсер — стоишь и ничего не делаешь.",
]
TAUNTS_LOSE = [
    "Я ТЕБЯ ПОДЛАТАЛ... но не помогло.",
    "Похоже, тебе нужен MEDIC. Срочно.",
    "Intel потерян. Команда в ярости.",
]
TAUNTS_DRAW = [
    "Ничья. Как две команды на 2fort.",
    "Все живы, никто не победил. Классика.",
    "Обе команды отступили на базу. Реванш?",
]


def wipe():
    os.system("cls" if os.name == "nt" else "clear")


def glitch(text, color=NEON_CYAN):
    """Псевдо-глитч: неоновый текст с рамкой."""
    bar = "▓▒░" * 12
    print(f"{color}{bar}{RESET}")
    print(f"{color}{BOLD}{text.center(36)}{RESET}")
    print(f"{color}{bar}{RESET}")


class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.field = [" "] * 9
        self.winner = None

    @property
    def free_cells(self):
        return [i for i, v in enumerate(self.field) if v == " "]

    def full(self):
        return " " not in self.field

    # ---------- киберпанк-отрисовка ----------
    def paint(self):
        def c(sym):
            if sym == "X":
                return f"{RED_TEAM}{BOLD}{sym}{RESET}"   # RED team
            if sym == "O":
                return f"{BLU_TEAM}{BOLD}{sym}{RESET}"   # BLU team
            return f"{DIM}·{RESET}"

        f = self.field
        print(f"\n{DIM}  ┌──── СЕТКА // GRID ────┐{RESET}")
        print(f"{NEON_CYAN}     1   2   3{RESET}")
        print(f"{NEON_PINK}   ╔═══╦═══╦═══╗{RESET}")
        print(f"{NEON_PINK}   ║{RESET} {c(f[0])} {NEON_PINK}║{RESET} {c(f[1])} {NEON_PINK}║{RESET} {c(f[2])} {NEON_PINK}║{RESET}")
        print(f"{NEON_PINK}   ╠═══╬═══╬═══╣{RESET}")
        print(f"{NEON_PINK}   ║{RESET} {c(f[3])} {NEON_PINK}║{RESET} {c(f[4])} {NEON_PINK}║{RESET} {c(f[5])} {NEON_PINK}║{RESET}")
        print(f"{NEON_PINK}   ╠═══╬═══╬═══╣{RESET}")
        print(f"{NEON_PINK}   ║{RESET} {c(f[6])} {NEON_PINK}║{RESET} {c(f[7])} {NEON_PINK}║{RESET} {c(f[8])} {NEON_PINK}║{RESET}")
        print(f"{NEON_PINK}   ╚═══╩═══╩═══╝{RESET}")
        print(f"{DIM}  └──── SECTOR 9 ────┘{RESET}\n")

    # ---------- логика ----------
    def find_winner(self):
        for a, b, d in WIN_LINES:
            if self.field[a] != " " and self.field[a] == self.field[b] == self.field[d]:
                self.winner = self.field[a]
                return self.winner
        return None

    def minimax(self, ai_turn, alpha=float("-inf"), beta=float("inf")):
        w = self.find_winner()
        if w == "O":
            return 10, None
        if w == "X":
            return -10, None
        if self.full():
            return 0, None

        cells = self.free_cells

        if ai_turn:
            score, pick = float("-inf"), None
            for cell in cells:
                self.field[cell] = "O"
                val, _ = self.minimax(False, alpha, beta)
                self.field[cell] = " "
                if val > score:
                    score, pick = val, cell
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return score, pick

        score, pick = float("inf"), None
        for cell in cells:
            self.field[cell] = "X"
            val, _ = self.minimax(True, alpha, beta)
            self.field[cell] = " "
            if val < score:
                score, pick = val, cell
            beta = min(beta, score)
            if beta <= alpha:
                break
        return score, pick

    def ai_turn(self):
        if not self.free_cells:
            return None
        _, cell = self.minimax(True)
        if cell is not None:
            self.field[cell] = "O"
        return cell

    def human_turn(self, cell):
        if cell in range(9) and self.field[cell] == " ":
            self.field[cell] = "X"
            return True
        return False


def ask_again():
    while True:
        ans = input(f"\n{NEON_YELLOW}>> Ещё раунд? (д/н): {RESET}").strip().lower()
        if ans in ("д", "да", "y", "yes"):
            return True
        if ans in ("н", "нет", "n", "no"):
            return False
        print(f"{RED_TEAM}Введи 'д' или 'н'!{RESET}")


def main():
    stats = {"X": 0, "O": 0, "draw": 0}
    game = Game()

    wipe()
    glitch("КРЕСТИКИ-НОЛИКИ // CYBER", NEON_PINK)
    glitch("TF2 EDITION  —  TRAUMA TEAM", NEON_CYAN)
    print(f"\n{RED_TEAM}Ты — RED (X){RESET}   {BLU_TEAM}Компьютер — BLU (O){RESET}")
    print(f"{DIM}Жребий решит, кто начнёт мясорубку.{RESET}\n")
    input(f"{NEON_YELLOW}>> ENTER, чтобы зайти на сервер...{RESET}")

    while True:
        wipe()
        game.reset()
        human = random.choice([True, False])
        if human:
            glitch(">> RED ГОТОВ. ВПЕРЁД!", RED_TEAM)
        else:
            glitch(">> BLU ЗАХВАТИЛ ИНИЦИАТИВУ!", BLU_TEAM)

        over = False
        while not over:
            print(f"{DIM}{'─' * 40}{RESET}")
            print(f"  {RED_TEAM}RED (X): {stats['X']}{RESET}  |  {BLU_TEAM}BLU (O): {stats['O']}{RESET}  |  {DIM}Ничьи: {stats['draw']}{RESET}")
            print(f"{DIM}{'─' * 40}{RESET}")
            game.paint()

            if human:
                print(f"{NEON_YELLOW}>> Твой ход (1–9) или 'q' для выхода:{RESET}")
                raw = input(f"{RED_TEAM}RED>{RESET} ")
                if raw.strip().lower() == "q":
                    print(f"\n{NEON_PINK}👋 Отключаемся от сервера...{RESET}")
                    return
                try:
                    cell = int(raw) - 1
                except ValueError:
                    print(f"{RED_TEAM}❌ Не число. Повтори.{RESET}")
                    input(f"{DIM}ENTER...{RESET}")
                    continue
                if game.human_turn(cell):
                    human = False
                else:
                    print(f"{RED_TEAM}❌ Занято или вне зоны!{RESET}")
                    input(f"{DIM}ENTER...{RESET}")
                    continue
            else:
                print(f"{BLU_TEAM}>> BLU взводит турель...{RESET}")
                time.sleep(0.4)
                cell = game.ai_turn()
                if cell is not None:
                    print(f"{BLU_TEAM}💻 BLU ударил по сектору {cell + 1}{RESET}")
                human = True

            w = game.find_winner()
            if w:
                wipe()
                game.paint()
                if w == "X":
                    glitch(">>> RED TEAM ПОБЕДИЛА! <<<", RED_TEAM)
                    print(f"{NEON_CYAN}💬 {random.choice(TAUNTS_WIN)}{RESET}")
                    stats["X"] += 1
                else:
                    glitch(">>> BLU TEAM ПОБЕДИЛА! <<<", BLU_TEAM)
                    print(f"{RED_TEAM}💬 {random.choice(TAUNTS_LOSE)}{RESET}")
                    stats["O"] += 1
                over = True
            elif game.full():
                wipe()
                game.paint()
                glitch(">>> НИЧЬЯ // STALEMATE <<<", NEON_YELLOW)
                print(f"{NEON_CYAN}💬 {random.choice(TAUNTS_DRAW)}{RESET}")
                stats["draw"] += 1
                over = True

        if not ask_again():
            print(f"\n{NEON_PINK}👋 Спасибо за игру! MEDIC уходит в отпуск.{RESET}")
            return
        print(f"\n{NEON_CYAN}🔄 Новая мясорубка!{RESET}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{NEON_PINK}👋 Сервер отключён. До встречи!{RESET}")
    except Exception as exc:
        print(f"\n{RED_TEAM}❌ Сбой системы: {exc}{RESET}")
        input(f"\n{DIM}ENTER для выхода...{RESET}")
