import pandas as pd
import numpy as np
# write your code here
user_input = input('provide the game state')
# user_input = 'O_OXXO_XX'
user_input = list(user_input)


def print_game(user_input):
    print('---------')
    for i in range(0, len(user_input), 3):
        print(f'| {user_input[i]} {user_input[i + 1]} {user_input[i + 2]} |')
    print('---------')


print_game(user_input)

df = pd.DataFrame.from_records(np.array(user_input).reshape(3, 3))

teams = ['X', 'O']


def check_for_win(df: pd.DataFrame, candidate_team):
    other_team = [t for t in teams if t != candidate_team][0]
    df = df.replace([candidate_team, other_team, '_'], [True, False, False])
    row_win = df.all(axis='columns').any()
    col_win = df.all(axis='index').any()
    diag_win_1 = np.diag(df).all()  # candidate wins on diag from top left to bottom right?
    diag_win_2 = np.diag(df[reversed(df.columns)]).all()  # candidate wins on diag from top right to bottom left?
    win = row_win or col_win or diag_win_1 or diag_win_2
    return win


x_win = check_for_win(df, 'X')
o_win = check_for_win(df, 'O')
n_plays_per_team = pd.Series(user_input).replace('_', None).value_counts()

if (x_win and o_win) or max(n_plays_per_team) - min(n_plays_per_team) not in (0, 1):
    print('Impossible')
elif x_win:
    print('X wins')
elif o_win:
    print('O wins')
elif '_' not in user_input:
    print('Draw')
elif '_' in user_input:
    print('Game not finished')
else:
    raise RuntimeError('unsure how to interpret game state.')
