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

    mem_prog = int(tracemalloc.get_tracemalloc_memory() / 1024)
    time_prog = round((time.time() - start_time) * 1_000_000, 4)
    return [
        f"Оптимальное решение: {max_k}",
        f"Оптимальная стратегия: {opt_strategy + 1}",
        f"Память: {mem_prog} КБ ", 
        f"Время: {time_prog} нс "
    ], {"time": time_prog, "mem": mem_prog, "win": max_k}

def solve_hurwitz_100times(game_matrix, optimistic_criteria):
    start_time = time.time()
    for i in range(100):
        solve_hurwitz(game_matrix, optimistic_criteria)
    
    return {"time": round((time.time() - start_time) * 1_000_000, 4)}

