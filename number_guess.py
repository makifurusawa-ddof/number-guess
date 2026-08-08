"""数当てゲーム（1〜100）。

- 1〜100のランダムな整数を出題し、大小のヒントを頼りに正解を当てるCLIゲーム。
- 入力は空入力・非整数・範囲外を検証し、無効な入力は試行回数にカウントしない。
- 正解時は試行回数を表示し、続けるかどうか(y/n)を尋ねる。
- 'q' または 'quit' でいつでも中断でき、その際は正解の数字を告知して終了する。
"""

import random

MIN_NUMBER = 1
MAX_NUMBER = 100
QUIT_COMMANDS = ("q", "quit")


def read_guess() -> int | str:
    """ユーザーに数字の入力を求める。'QUIT'を返す場合は中断要求。"""
    while True:
        # Ctrl+C(KeyboardInterrupt) / Ctrl+D等(EOFError)はqと同様に中断扱いにする
        try:
            raw = input(f"{MIN_NUMBER}〜{MAX_NUMBER}の数を入力してください（q で終了）: ").strip()
        except (KeyboardInterrupt, EOFError):
            print()  # 中断時にプロンプト行を改行して見た目を整える
            return "QUIT"

        # 途中離脱コマンド
        if raw.lower() in QUIT_COMMANDS:
            return "QUIT"

        # 空入力チェック
        if raw == "":
            print("⚠ 入力が空です。数字を入力してください。")
            continue

        # 非整数チェック
        try:
            value = int(raw)
        except ValueError:
            print("⚠ 整数を入力してください。")
            continue

        # 範囲外チェック
        if value < MIN_NUMBER or value > MAX_NUMBER:
            print(f"⚠ {MIN_NUMBER}〜{MAX_NUMBER}の範囲で入力してください。")
            continue

        return value


def play_round(secret: int) -> tuple[bool, int]:
    """1ゲーム分の入力ループ。戻り値: (途中離脱したか, 試行回数)。"""
    attempts = 0
    while True:
        guess = read_guess()

        if guess == "QUIT":
            return True, attempts

        attempts += 1

        # 大小判定の分岐
        if guess < secret:
            print("もっと大きい数です。")
        elif guess > secret:
            print("もっと小さい数です。")
        else:
            print("正解です！")
            print(f"試行回数: {attempts} 回")
            return False, attempts


def ask_play_again() -> bool:
    """続けて遊ぶかどうかをy/nで確認する。"""
    while True:
        raw = input("続けて遊びますか？ (y/n): ").strip().lower()
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("⚠ y または n を入力してください。")


def main() -> None:
    while True:
        secret = random.randint(MIN_NUMBER, MAX_NUMBER)
        quit_requested, _attempts = play_round(secret)

        # 途中離脱: 正解を告知して終了
        if quit_requested:
            print(f"ゲームを終了します。正解は {secret} でした。")
            break

        # 正解後: 続行確認
        if not ask_play_again():
            print("プレイしてくれてありがとうございました！")
            break


if __name__ == "__main__":
    main()
