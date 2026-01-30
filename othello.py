#!/usr/bin/env python3
"""
オセロ（リバーシ）ゲーム
tkinterを使用したGUIアプリケーション
"""

import tkinter as tk
from tkinter import messagebox
from typing import Optional


class OthelloGame:
    """オセロゲームのロジックを管理するクラス"""

    EMPTY = 0
    BLACK = 1
    WHITE = 2
    BOARD_SIZE = 8

    DIRECTIONS = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    def __init__(self):
        self.board: list[list[int]] = []
        self.current_player: int = self.BLACK
        self.reset()

    def reset(self) -> None:
        """ゲームを初期状態にリセット"""
        self.board = [[self.EMPTY] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
        center = self.BOARD_SIZE // 2
        self.board[center - 1][center - 1] = self.WHITE
        self.board[center - 1][center] = self.BLACK
        self.board[center][center - 1] = self.BLACK
        self.board[center][center] = self.WHITE
        self.current_player = self.BLACK

    def is_valid_position(self, row: int, col: int) -> bool:
        """座標がボード内かどうかを確認"""
        return 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE

    def get_flippable_discs(self, row: int, col: int, player: int) -> list[tuple[int, int]]:
        """指定位置に石を置いた場合に裏返せる石のリストを返す"""
        if self.board[row][col] != self.EMPTY:
            return []

        opponent = self.WHITE if player == self.BLACK else self.BLACK
        flippable = []

        for dr, dc in self.DIRECTIONS:
            r, c = row + dr, col + dc
            temp_flippable = []

            while self.is_valid_position(r, c) and self.board[r][c] == opponent:
                temp_flippable.append((r, c))
                r += dr
                c += dc

            if temp_flippable and self.is_valid_position(r, c) and self.board[r][c] == player:
                flippable.extend(temp_flippable)

        return flippable

    def is_valid_move(self, row: int, col: int, player: int) -> bool:
        """指定位置が有効な手かどうかを確認"""
        return len(self.get_flippable_discs(row, col, player)) > 0

    def get_valid_moves(self, player: int) -> list[tuple[int, int]]:
        """指定プレイヤーの有効な手のリストを返す"""
        valid_moves = []
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self.is_valid_move(row, col, player):
                    valid_moves.append((row, col))
        return valid_moves

    def place_disc(self, row: int, col: int) -> bool:
        """石を置いて裏返す処理を実行"""
        flippable = self.get_flippable_discs(row, col, self.current_player)
        if not flippable:
            return False

        self.board[row][col] = self.current_player
        for r, c in flippable:
            self.board[r][c] = self.current_player

        return True

    def switch_player(self) -> None:
        """プレイヤーを交代"""
        self.current_player = self.WHITE if self.current_player == self.BLACK else self.BLACK

    def count_discs(self) -> tuple[int, int]:
        """黒と白の石の数を返す"""
        black_count = sum(row.count(self.BLACK) for row in self.board)
        white_count = sum(row.count(self.WHITE) for row in self.board)
        return black_count, white_count

    def is_game_over(self) -> bool:
        """ゲーム終了かどうかを確認"""
        return (not self.get_valid_moves(self.BLACK) and
                not self.get_valid_moves(self.WHITE))

    def get_winner(self) -> Optional[int]:
        """勝者を返す（引き分けの場合はNone）"""
        black_count, white_count = self.count_discs()
        if black_count > white_count:
            return self.BLACK
        elif white_count > black_count:
            return self.WHITE
        return None


class OthelloGUI:
    """オセロゲームのGUIを管理するクラス"""

    CELL_SIZE = 60
    DISC_PADDING = 5
    BOARD_COLOR = "#008000"
    LINE_COLOR = "#000000"
    BLACK_COLOR = "#000000"
    WHITE_COLOR = "#FFFFFF"
    VALID_MOVE_COLOR = "#90EE90"

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("オセロ")
        self.root.resizable(False, False)

        self.game = OthelloGame()
        self.setup_ui()
        self.draw_board()

    def setup_ui(self) -> None:
        """UIコンポーネントを設定"""
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)

        # 情報表示フレーム
        info_frame = tk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(0, 10))

        self.turn_label = tk.Label(
            info_frame,
            text="",
            font=("Helvetica", 14, "bold")
        )
        self.turn_label.pack(side=tk.LEFT)

        self.score_label = tk.Label(
            info_frame,
            text="",
            font=("Helvetica", 14)
        )
        self.score_label.pack(side=tk.RIGHT)

        # ゲームボード（Canvas）
        canvas_size = self.CELL_SIZE * OthelloGame.BOARD_SIZE
        self.canvas = tk.Canvas(
            main_frame,
            width=canvas_size,
            height=canvas_size,
            bg=self.BOARD_COLOR,
            highlightthickness=2,
            highlightbackground=self.LINE_COLOR
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # ボタンフレーム
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        self.reset_button = tk.Button(
            button_frame,
            text="新しいゲーム",
            font=("Helvetica", 12),
            command=self.reset_game
        )
        self.reset_button.pack(side=tk.LEFT, expand=True)

        self.pass_button = tk.Button(
            button_frame,
            text="パス",
            font=("Helvetica", 12),
            command=self.pass_turn,
            state=tk.DISABLED
        )
        self.pass_button.pack(side=tk.RIGHT, expand=True)

    def draw_board(self) -> None:
        """ボード全体を描画"""
        self.canvas.delete("all")

        # グリッド線を描画
        for i in range(OthelloGame.BOARD_SIZE + 1):
            x = i * self.CELL_SIZE
            self.canvas.create_line(x, 0, x, self.CELL_SIZE * OthelloGame.BOARD_SIZE,
                                   fill=self.LINE_COLOR, width=1)
            self.canvas.create_line(0, x, self.CELL_SIZE * OthelloGame.BOARD_SIZE, x,
                                   fill=self.LINE_COLOR, width=1)

        # 有効な手を表示
        valid_moves = self.game.get_valid_moves(self.game.current_player)
        for row, col in valid_moves:
            x1 = col * self.CELL_SIZE + 2
            y1 = row * self.CELL_SIZE + 2
            x2 = (col + 1) * self.CELL_SIZE - 2
            y2 = (row + 1) * self.CELL_SIZE - 2
            self.canvas.create_rectangle(x1, y1, x2, y2,
                                        fill=self.VALID_MOVE_COLOR,
                                        outline="")

        # 石を描画
        for row in range(OthelloGame.BOARD_SIZE):
            for col in range(OthelloGame.BOARD_SIZE):
                if self.game.board[row][col] != OthelloGame.EMPTY:
                    self.draw_disc(row, col, self.game.board[row][col])

        # 情報ラベルを更新
        self.update_labels()

        # パスボタンの状態を更新
        self.update_pass_button()

    def draw_disc(self, row: int, col: int, player: int) -> None:
        """指定位置に石を描画"""
        x1 = col * self.CELL_SIZE + self.DISC_PADDING
        y1 = row * self.CELL_SIZE + self.DISC_PADDING
        x2 = (col + 1) * self.CELL_SIZE - self.DISC_PADDING
        y2 = (row + 1) * self.CELL_SIZE - self.DISC_PADDING

        color = self.BLACK_COLOR if player == OthelloGame.BLACK else self.WHITE_COLOR
        outline = self.WHITE_COLOR if player == OthelloGame.BLACK else self.BLACK_COLOR

        self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline=outline, width=2)

    def update_labels(self) -> None:
        """情報ラベルを更新"""
        player_name = "黒" if self.game.current_player == OthelloGame.BLACK else "白"
        self.turn_label.config(text=f"現在の手番: {player_name}")

        black_count, white_count = self.game.count_discs()
        self.score_label.config(text=f"黒: {black_count}  白: {white_count}")

    def update_pass_button(self) -> None:
        """パスボタンの状態を更新"""
        valid_moves = self.game.get_valid_moves(self.game.current_player)
        opponent = OthelloGame.WHITE if self.game.current_player == OthelloGame.BLACK else OthelloGame.BLACK
        opponent_moves = self.game.get_valid_moves(opponent)

        # 現在のプレイヤーに有効な手がなく、相手に有効な手がある場合のみパス可能
        if not valid_moves and opponent_moves:
            self.pass_button.config(state=tk.NORMAL)
        else:
            self.pass_button.config(state=tk.DISABLED)

    def on_canvas_click(self, event: tk.Event) -> None:
        """キャンバスクリック時の処理"""
        col = event.x // self.CELL_SIZE
        row = event.y // self.CELL_SIZE

        if not self.game.is_valid_position(row, col):
            return

        if self.game.place_disc(row, col):
            self.game.switch_player()
            self.draw_board()
            self.check_game_state()

    def pass_turn(self) -> None:
        """パスの処理"""
        self.game.switch_player()
        self.draw_board()
        self.check_game_state()

    def check_game_state(self) -> None:
        """ゲーム状態をチェック"""
        if self.game.is_game_over():
            self.show_result()

    def show_result(self) -> None:
        """ゲーム結果を表示"""
        black_count, white_count = self.game.count_discs()
        winner = self.game.get_winner()

        if winner == OthelloGame.BLACK:
            result = f"黒の勝利！\n黒: {black_count}  白: {white_count}"
        elif winner == OthelloGame.WHITE:
            result = f"白の勝利！\n黒: {black_count}  白: {white_count}"
        else:
            result = f"引き分け！\n黒: {black_count}  白: {white_count}"

        messagebox.showinfo("ゲーム終了", result)

    def reset_game(self) -> None:
        """ゲームをリセット"""
        self.game.reset()
        self.draw_board()


def main():
    """メイン関数"""
    root = tk.Tk()
    OthelloGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
