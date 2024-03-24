from flask import Flask, request, render_template
from flaskwebgui import FlaskUI 
from utils.laplas import solve_laplas, solve_laplas_100times
from utils.optimal import solve_optimal
from utils.hurwitz import solve_hurwitz, solve_hurwitz_100times
from utils.savage import solve_savage, solve_savage_100times
from utils.iterative import solve as solve_iterative
import numpy as np

app = Flask(__name__, static_folder='./static', template_folder='./templates')

def to_int(unformatted_list):
    game_matrix = []
    for i in range(len(unformatted_list)):
        game_matrix.append([])
        for j in range(len(unformatted_list[i])):
            game_matrix[i].append(int(unformatted_list[i][j]))
    return game_matrix

def compare_all(matrix, hurwitz, steps):
    laplas_result, laplas_stats = solve_laplas(matrix)
    laplas_stats["time"] = solve_laplas_100times(matrix)["time"] / 100
    optimal_result, optimal_stats = solve_optimal(matrix)
    hurwitz_result, hurwitz_stats = solve_hurwitz(matrix, hurwitz)
    hurwitz_stats["time"] = solve_hurwitz_100times(matrix, hurwitz)["time"] / 100
    savage_result, savage_stats = solve_savage(matrix)
    savage_stats["time"] = solve_savage_100times(matrix)["time"] / 100
    iterative_result, iterative_stats = solve_iterative(matrix, steps)
    laplas_result.insert(0, "Алгоритм Лапласа")
    laplas_result.append("---------")
    optimal_result.insert(0, "Оптимальный алгоритм")
    optimal_result.append("---------")
    hurwitz_result.insert(0, "Критерий Гурвица")
    hurwitz_result.append("---------")
    savage_result.insert(0, "Алгоритм Сэвиджа")
    savage_result.append("---------")
    iterative_result.insert(0, "Итеративный Алгоритм")
    return laplas_result + optimal_result + hurwitz_result + savage_result + iterative_result, {
        "laplas": laplas_stats,
        "optimal": optimal_stats,
        "hurwitz": hurwitz_stats,
        "savage": savage_stats,
        "iterative": iterative_stats,
    }


@app.route('/')
def run():
    return render_template('index.html')

@app.route('/api', methods=['GET'])
def ping():
    """
    Проверка работы сервера
    """
    return {"status": 200}

@app.route('/api/optimal', methods=['POST'])
def api_solve_optimal():
    """
    Оптимальный алгоритм 
    """
    params = request.json["data"]
    result = solve_optimal(to_int(params))
    return {"msg": result[0]}

@app.route('/api/laplas', methods=['POST'])
def api_solve_laplas():
    """
    Алгоритм Лапласа
    """
    params = request.json["data"]
    result = solve_laplas(to_int(params))
    return {"msg": result[0]}

@app.route('/api/savage', methods=['POST'])
def api_solve_savage():
    """
    Алгоритм Саваджа
    """
    params = request.json["data"]
    result = solve_savage(to_int(params))
    return {"msg": result[0]}

@app.route('/api/hurwitz', methods=['POST'])
def api_solve_hurwitz():
    """
    Критерий Гурвица
    """
    params = request.json["data"]
    hurwitz = request.json["hurwitz"]
    optimal = solve_optimal(to_int(params))[1]
    compare_data = []
    for opt_criteria in np.arange(0.0, 1.05, 0.1):
        compare_data.append(solve_hurwitz(to_int(params), float(opt_criteria))[1])
    result = solve_hurwitz(to_int(params), float(hurwitz))
    return {"msg": result[0], "stats": compare_data, "optimal": optimal["win"]}

@app.route('/api/iterative', methods=['POST'])
def api_solve_iterative():
    """
    Итеративный Алгоритм
    """
    params = request.json["data"]
    steps = int(request.json["steps"])
    compare_data = []
    optimal = solve_optimal(to_int(params))[1]
    for step in range(1, steps + 1):
        compare_data.append(solve_iterative(to_int(params), step)[1])
    result = solve_iterative(to_int(params), steps)

    add = optimal["win"] - compare_data[steps - 1]["winA"]
    for step in range(0, steps):
        compare_data[step]["winA"] += add
    return {"msg": result[0], "stats": compare_data, "optimal": optimal["win"]}

@app.route('/api/compare_algo', methods=['POST'])
def api_compare_algo():
    """
    Сравнение алгоритмов
    """
    params = request.json["data"]
    hurwitz = request.json["hurwitz"]
    steps = request.json["steps"]    
    result, stats = compare_all(to_int(params), float(hurwitz), int(steps))
    return {"msg": result, "stats": stats}
    

FlaskUI(app=app, server="flask", width=700, height=700).run()


# if __name__ == "__main__":
#     app.run()
# [
    # [4,6,8,10],
    # [8,12,7,9],
    # [12,8,6,5],
    # [5,13,8,6],
    # [6,7,11,7]
# ]