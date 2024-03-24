import os
import numpy as np
import tracemalloc
import time 

CURRENT_DIRECTORY = os.getcwd()

class Iterative:
    def __init__(self, Matrix, vector, steps):
        self.Matrix = Matrix
        self.vector = vector
        self.answer = []
        self.steps = steps
        self.max_k0 = 0
        self.max_k1 = 0

    def find_solution_A(self):
        sol = np.linalg.solve(self.Matrix, self.vector)
        v1 = 0
        iter = 1
        for i in sol:
            v1 += i * sum(self.Matrix[iter-1]) / len(self.Matrix[iter - 1])
            self.answer.append(f"Стратегия А{iter}: {str(round(v1*i, 2))}") 
            iter += 1

        self.max_k0 = round(v1, 2)
        self.answer.append(f"Оптимальное решение: {self.max_k0}")


    def find_solution_B(self):
        matrix = np.array(self.Matrix)
        sol = np.linalg.solve(matrix.transpose(), self.vector)
        v1 = 0
        iter = 1
        for i in sol:
            v1 += i * sum(self.Matrix[iter-1]) / len(self.Matrix[iter - 1])
            self.answer.append(f"Стратегия B{iter}: {str(round(v1*i, 2))}")
            iter += 1
            
        self.max_k1 = round(v1, 2)
        self.answer.append(f"Оптимальное решение: {self.max_k1}")
    
    def sum_two_rows(self, row, row_letter):
        for i in range(len(row)):
            row[i] += row_letter[i]
        return row

    def find_big_big_table(self):
        matrix_B = self.Matrix
        matrix = np.array(self.Matrix)
        matrix_A = matrix.transpose().tolist()
        
        row_B = [0, 0, 0]
        row_A = [0, 0, 0]

        step_B = 1
        step_A = matrix_B[step_B].index(min(matrix_B[step_B]))
        
        row_B = self.sum_two_rows(row_B, matrix_B[step_B])
        row_A = self.sum_two_rows(row_A, matrix_A[step_A])
        
        
        
        for i in range(self.steps):
            v_ = round(row_B[step_A]/(i+1), 2)
            step_B = row_A.index(max(row_A))
            row_B = self.sum_two_rows(row_B, matrix_B[step_B])
            _v = round(row_A[step_B]/(i+1), 2)
            v = round((v_+_v)/2, 2)
            step_A = row_B.index(min(row_B))
            row_A = self.sum_two_rows(row_A, matrix_A[step_A])  
        print(row_A)
        print(row_B)
        print(v)
        self.max_k0 = v
    


def solve(game_matrix, steps):


    start_time = time.time()
    tracemalloc.start()
    a = Iterative(game_matrix[:-1], game_matrix[-1], steps)      
    a.find_solution_A()
    a.find_solution_B()

    a.find_big_big_table()
    print(a.answer)
    mem_prog = int(tracemalloc.get_tracemalloc_memory() / 1024)
    time_prog = round((time.time() - start_time) * 1_000_000, 4)
    a.answer.append(f"Память: {mem_prog} КБ ")
    a.answer.append(f"Время: {time_prog} нс ")
    return a.answer, {"mem": mem_prog, "time": time_prog, "winA": a.max_k0, "winB": a.max_k1}

Matrix = [[4,6,8,10],
              [8,12,7,9],
              [12,8,6,5],
              [5,13,8,6], [6,7,11,7]]

solve(Matrix, 5)

"""
f"Макс: {max(F)}", 
        f"Мин: {min(F)}", 
        f"Оптимальное решение: {sum(F) / len(F)}", 
        f"Оптимальная стратегия: {opt_strategy + 1}",
        f"Память: {mem_prog} КБ ", 
        f"Время: {time_prog} нс "
"""

