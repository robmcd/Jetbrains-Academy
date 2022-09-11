import pandas as pd
import numpy as np

TEAMS = ['X', 'O']


def print_game(df_field: pd.DataFrame):
    print('---------')
    for index, values in df_field.iterrows():
        print(f'| {" ".join([v for v in values])} |')
    print('---------')


def check_for_win(df: pd.DataFrame, candidate_team):
    other_team = [t for t in TEAMS if t != candidate_team][0]
    df = df.replace([candidate_team, other_team, '_'], [True, False, False])
    row_win = df.all(axis='columns').any()
    col_win = df.all(axis='index').any()
    diag_win_1 = np.diag(df).all()  # candidate wins on diag from top left to bottom right?
    diag_win_2 = np.diag(df[reversed(df.columns)]).all()  # candidate wins on diag from top right to bottom left?
    win = row_win or col_win or diag_win_1 or diag_win_2
    return win


def is_game_over(df_field: pd.DataFrame) -> bool:
    """

    :param df_field:
    :return: whether or not the game is over
    """
    x_win = check_for_win(df_field, 'X')
    o_win = check_for_win(df_field, 'O')
    n_plays_per_team = pd.Series(df_field.to_numpy().flatten()).replace('_', None).value_counts()
    is_fresh_game = True if len(n_plays_per_team) == 0 else False
    is_game_over = True

    if is_fresh_game:
        is_game_over = False
    else:
        if (x_win and o_win) or max(n_plays_per_team) - min(n_plays_per_team) not in (0, 1):
            print('Impossible')
        elif x_win:
            print('X wins')
        elif o_win:
            print('O wins')
        elif '_' not in df_field.to_numpy():
            print('Draw')
        elif '_' in df_field.to_numpy():
            is_game_over = False
        else:
            raise RuntimeError('unsure how to interpret game state.')
    return is_game_over


def get_next_move():
    """

    :return: tuple representing row, col co-ords.
    """
    while True:
        user_move = input('Input your move')
        try:
            row, col = user_move.strip().replace(',', ' ').split(maxsplit=1)
        except ValueError:
            continue

        try:
            row, col = int(row) - 1, int(col) - 1
        except ValueError:
            print('You should enter numbers!')
            continue

        if max(row, col) > 2 or min(row, col) < 0:
            print('Coordinates should be from 1 to 3!')
            continue

        if df_field.loc[row, col] != '_':
            print('This cell is occupied! Choose another one!')
            continue

        return row, col


field = list('_' * 9)

global df_field
df_field = pd.DataFrame.from_records(np.array(field).reshape(3, 3))
print_game(df_field)
player = 'X'

while not is_game_over(df_field):
    row, col = get_next_move()
    df_field.loc[row, col] = player
    print_game(df_field)
    player = [t for t in TEAMS if t != player][0]


# eval_game_status(df_field)
