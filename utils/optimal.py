import numpy as np
from scipy import optimize
import copy
import tracemalloc
import time


def solve_optimal(Win_Lose_Matrix):
    tracemalloc.start()
    start_time = time.time()
    to_print = []
    to_print.append('Решение:')

    def make_ans_optimal(sol: dict):
        to_print.append('Переменные  Значения')
        for i in range(len(sol['x'])):
            to_print.append(f"y{i + 1:<8} = {sol['x'][i]:<25}")
        to_print.append(f"z{'':<8} = {sol['fun']:<25}")

    def find_mixed_strategy(straight_solution, reverse_solution):
        mixed_strategy_A = straight_solution.x
        mixed_strategy_B = reverse_solution.x
        price_A = 1 / straight_solution.fun
        price_B = 1 / reverse_solution.fun

        return mixed_strategy_A, mixed_strategy_B, price_A, price_B

    A_ub = copy.deepcopy(Win_Lose_Matrix)
    c = [-1] * len(A_ub[0])  # Функция цели
    b_ub = [1] * len(A_ub)  # '1'
    straight_sol = optimize.linprog(c=c, A_ub=A_ub, b_ub=b_ub, method='highs')
    make_ans_optimal(straight_sol)

    to_print.append("")

    c = [1] * len(A_ub)  # Функция цели
    b_ub = [-1] * len(A_ub[0])
    left_side = np.array(A_ub).T * -1
    reverse_sol = optimize.linprog(c=c, A_ub=left_side, b_ub=b_ub, method='highs')
    make_ans_optimal(reverse_sol)

    # Нахождение оптимальных смешанных стратегий и цен игры для обоих игроков
    mixed_strategy_A, mixed_strategy_B, price_A, price_B = find_mixed_strategy(straight_sol, reverse_sol)

    to_print.append(f"Оптимальная смешанная стратегия для игрока A: {' '.join(f'{val:.5f}' for val in mixed_strategy_A)}")
    to_print.append(f"Оптимальная смешанная стратегия для игрока B: {' '.join(f'{val:.5f}' for val in mixed_strategy_B)}")
    to_print.append(f"Средний выигрыш: {price_B:.5f}")

    mem_prog = int(tracemalloc.get_tracemalloc_memory() / 1024)
    time_prog = round((time.time() - start_time) * 1_000_000, 4)

    # print("\n".join(to_print))
    return [
        f"Оптимальное решение игрока А: {', '.join(map(lambda x: str(round(x, 5)), mixed_strategy_A))}",
        f"Оптимальное решение игрока В: {', '.join(map(lambda x: str(round(x, 5)), mixed_strategy_B))}",
        f"Оптимальное решение: {price_B:.5f}",
        f"Память: {mem_prog} КБ ", 
        f"Время: {time_prog} нс "
    ], {"time": time_prog, "mem": mem_prog, "win": price_B}
