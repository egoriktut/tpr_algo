import tracemalloc
import time

def solve_laplas(game_matrix):
    start_time = time.time()
    tracemalloc.start()
    F = list()
    opt_strategy = 0
    for i in range(len(game_matrix)):
        Fsum = 0
        for j in range(len(game_matrix[i])):
            Fsum += game_matrix[i][j]
        
        F.append(Fsum / len(game_matrix[i]))
        if (Fsum > F[opt_strategy]):
            opt_strategy = i
    mem_prog = int(tracemalloc.get_tracemalloc_memory() / 1024)
    time_prog = round((time.time() - start_time) * 1_000_000, 4)
    return [
        f"Макс: {max(F)}", 
        f"Мин: {min(F)}", 
        f"Оптимальное решение: {sum(F) / len(F)}", 
        f"Оптимальная стратегия: {opt_strategy + 1}",
        f"Память: {mem_prog} КБ ", 
        f"Время: {time_prog} нс "
    ], {"time": time_prog, "mem": mem_prog}

