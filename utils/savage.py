import tracemalloc
import time

def solve_savage(game_matrix):
    start_time = time.time()
    tracemalloc.start()
    risk_matrix = []
    rotated = list(zip(*game_matrix[::-1]))

    for i in range(len(rotated)):
        maxim = max(rotated[i])
        risk_matrix.append([])

        for j in range(len(rotated[i])):
            risk_matrix[i].append(maxim - rotated[i][j])
    risk_matrix = list(reversed(list(zip(*risk_matrix))))

    print(risk_matrix)

    opt_strategy = 0
    for i in range(len(risk_matrix)):
        print(risk_matrix[i], min(risk_matrix[i]), min(risk_matrix[opt_strategy]))
        if min(risk_matrix[i]) > min(risk_matrix[opt_strategy]):
            opt_strategy = i

    return [
        f"Оптимальная стратегия: {opt_strategy + 1}",
        f"Память: {int(tracemalloc.get_tracemalloc_memory() / 1024)} КБ ", 
        f"Время: {round((time.time() - start_time) * 1_000_000, 4)} нс ", 
    ]




game_matrix = [
    [4, 6, 8, 10],
    [8, 12, 7, 9],
    [12, 8, 6, 5],
    [5, 13, 8, 6],
    [6, 7, 11, 7],
]

print(solve_savage(game_matrix))