from flask import Flask, request, render_template
from flaskwebgui import FlaskUI 
from utils.laplas import solve_laplas
from utils.optimal import solve_optimal
from utils.hurwitz import solve_hurwitz
from utils.savage import solve_savage

app = Flask(__name__, static_folder='./static', template_folder='./templates')

def to_int(unformatted_list):
    game_matrix = []
    for i in range(len(unformatted_list)):
        game_matrix.append([])
        for j in range(len(unformatted_list[i])):
            game_matrix[i].append(int(unformatted_list[i][j]))
    return game_matrix

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
    return {"msg": result}

@app.route('/api/laplas', methods=['POST'])
def api_solve_laplas():
    """
    Алгоритм Лапласа
    """
    params = request.json["data"]
    result = solve_laplas(to_int(params))
    return {"msg": result}

@app.route('/api/savage', methods=['POST'])
def api_solve_savage():
    """
    Алгоритм Саваджа
    """
    params = request.json["data"]
    result = solve_savage(to_int(params))
    return {"msg": result}

@app.route('/api/hurwitz', methods=['POST'])
def api_solve_hurwitz():
    """
    Критерий Гурвица
    """
    params = request.json["data"]
    hurwitz = request.json["hurwitz"]
    result = solve_hurwitz(to_int(params), float(hurwitz))
    return {"msg": result}
    

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