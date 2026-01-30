"""
オセロゲームのユニットテスト
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from othello import OthelloGame


class TestOthelloGame:
    """OthelloGameクラスのテスト"""

    def setup_method(self):
        """各テストの前に実行"""
        self.game = OthelloGame()

    def test_initial_board_setup(self):
        """初期盤面が正しく配置されているか"""
        # 中央4マスの初期配置を確認
        assert self.game.board[3][3] == OthelloGame.WHITE
        assert self.game.board[3][4] == OthelloGame.BLACK
        assert self.game.board[4][3] == OthelloGame.BLACK
        assert self.game.board[4][4] == OthelloGame.WHITE

    def test_initial_player_is_black(self):
        """最初のプレイヤーが黒であるか"""
        assert self.game.current_player == OthelloGame.BLACK

    def test_initial_disc_count(self):
        """初期の石の数が正しいか"""
        black, white = self.game.count_discs()
        assert black == 2
        assert white == 2

    def test_is_valid_position(self):
        """座標の有効性チェック"""
        assert self.game.is_valid_position(0, 0) is True
        assert self.game.is_valid_position(7, 7) is True
        assert self.game.is_valid_position(-1, 0) is False
        assert self.game.is_valid_position(0, 8) is False
        assert self.game.is_valid_position(8, 8) is False

    def test_valid_moves_for_black_at_start(self):
        """黒の初期有効手が正しいか"""
        valid_moves = self.game.get_valid_moves(OthelloGame.BLACK)
        expected_moves = [(2, 3), (3, 2), (4, 5), (5, 4)]
        assert sorted(valid_moves) == sorted(expected_moves)

    def test_place_disc(self):
        """石を置いて反転が正しく行われるか"""
        # 黒が(2,3)に置く
        result = self.game.place_disc(2, 3)
        assert result is True
        assert self.game.board[2][3] == OthelloGame.BLACK
        assert self.game.board[3][3] == OthelloGame.BLACK  # 反転された

    def test_invalid_move_returns_false(self):
        """無効な手がFalseを返すか"""
        result = self.game.place_disc(0, 0)
        assert result is False

    def test_switch_player(self):
        """プレイヤー交代が正しく行われるか"""
        assert self.game.current_player == OthelloGame.BLACK
        self.game.switch_player()
        assert self.game.current_player == OthelloGame.WHITE
        self.game.switch_player()
        assert self.game.current_player == OthelloGame.BLACK

    def test_reset_game(self):
        """ゲームリセットが正しく行われるか"""
        # 何か手を打つ
        self.game.place_disc(2, 3)
        self.game.switch_player()

        # リセット
        self.game.reset()

        # 初期状態に戻っているか確認
        assert self.game.current_player == OthelloGame.BLACK
        black, white = self.game.count_discs()
        assert black == 2
        assert white == 2

    def test_game_not_over_at_start(self):
        """ゲーム開始時は終了していないか"""
        assert self.game.is_game_over() is False

    def test_get_flippable_discs_empty_cell(self):
        """空でないセルには石を置けない"""
        flippable = self.game.get_flippable_discs(3, 3, OthelloGame.BLACK)
        assert flippable == []

    def test_get_winner_returns_none_on_tie(self):
        """引き分け時はNoneを返す"""
        # 初期状態は2-2で引き分け
        winner = self.game.get_winner()
        assert winner is None

    def test_get_winner_black_wins(self):
        """黒が勝っている場合"""
        self.game.place_disc(2, 3)  # 黒が置く
        winner = self.game.get_winner()
        assert winner == OthelloGame.BLACK


class TestOthelloGameEdgeCases:
    """エッジケースのテスト"""

    def setup_method(self):
        self.game = OthelloGame()

    def test_diagonal_flip(self):
        """斜め方向の反転が正しいか"""
        # 斜めのテストケースを設定
        self.game.board = [[OthelloGame.EMPTY] * 8 for _ in range(8)]
        self.game.board[2][2] = OthelloGame.BLACK
        self.game.board[3][3] = OthelloGame.WHITE
        self.game.board[4][4] = OthelloGame.WHITE
        self.game.current_player = OthelloGame.BLACK

        flippable = self.game.get_flippable_discs(5, 5, OthelloGame.BLACK)
        assert (3, 3) in flippable
        assert (4, 4) in flippable

    def test_multiple_direction_flip(self):
        """複数方向の反転が正しいか"""
        self.game.board = [[OthelloGame.EMPTY] * 8 for _ in range(8)]
        # 縦方向の挟み込み配置
        self.game.board[2][3] = OthelloGame.BLACK
        self.game.board[3][3] = OthelloGame.WHITE
        self.game.current_player = OthelloGame.BLACK

        flippable = self.game.get_flippable_discs(4, 3, OthelloGame.BLACK)
        # この配置では(3,3)が反転可能
        assert (3, 3) in flippable


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
