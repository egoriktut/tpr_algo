import tracemalloc
import time


def solve_hurwitz(game_matrix, optimistic_criteria):
    start_time = time.time()
    tracemalloc.start()
    opt_strategy = 0
    max_k = 0
    for i in range(len(game_matrix)):
        k = optimistic_criteria * max(game_matrix[i]) + (1 - optimistic_criteria) * min(game_matrix[i])
        if k > max_k:
            opt_strategy = i
            max_k = k
        print(k)
    return [
        f"Оптимальное решение: {max_k}",
        f"Оптимальная стратегия: {opt_strategy + 1}",
        f"Память: {int(tracemalloc.get_tracemalloc_memory() / 1024)} КБ ", 
        f"Время: {round((time.time() - start_time) * 1_000_000, 4)} нс ", 
    ]

