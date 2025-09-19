from sudoku_init import Sudoku
import copy
from collections import deque

class Sudoku_Solve:
    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku
        self.height = self.sudoku.height
        self.width = self.sudoku.width
        self.domains = {
            (i, j): set(range(1, 10)) if sudoku.structure[i][j] is None else {sudoku.structure[i][j]}
            for i in range(9) for j in range(9)
        }
        

    def enforce_node_consistency(self):
        for var in self.domains:
            if len(self.domains[var]) == 1:
                value = next(iter(self.domains[var]))
                for neighbor in self.sudoku.neighbors(var):
                    if value in self.domains[neighbor]:
                        self.domains[neighbor].discard(value)

    def con_cho(self):
        print("Con cho Huy")

    def con_lon(self):
        print("Con lon Hung")

    def propagate_constraints(self):
        change = True
        while change:
            change = False
            for unit_type in [self.get_all_boxs, self.get_all_cols, self.get_all_rows]:
                for units in unit_type():
                    count = {k: set() for k in range(1, 10)}
                    for cell in units:
                        if cell in self.domains:
                            for val in self.domains[cell]:
                                count[val].add(cell)

                    for k in count:
                        if len(count[k]) == 1:
                            x, y = next(iter(count[k]))
                            if len(self.domains[(x, y)]) > 1:
                                self.sudoku.structure[x][y] = k
                                # self.update_domain((x, y), k)
                                self.assign((x,y), k)
                                change = True

    def assign(self, cell, value):
        self.sudoku.structure[cell[0]][cell[1]] = value
        self.domains[cell] = {value}
        for neighbor in self.sudoku.neighbors(cell):
            self.domains[neighbor].discard(value)


    def get_all_rows(self):
        return [[(i, j) for j in range(9)] for i in range(9)]
    
    def get_all_cols(self):
        return [[(i, j) for i in range(9)] for j in range(9)]
    
    def get_all_boxs(self):
        return[[(t, s) for t in range(i*3, i*3+3) for s in range(j*3, j*3+3)]
               for i in range(3) for j in range(3)]
    

    def update_domain(self, cell, value):
        x, y = cell
        neighbors = self.sudoku.neighbors(cell)
        self.domains[cell] = {value}
        for neighbor in neighbors:
            if value in self.domains[neighbor]:
                self.domains[neighbor].discard(value)


    
    def is_complete(self):

        for unit_type in [self.get_all_boxs, self.get_all_cols, self.get_all_rows]:
            for units in unit_type():
                count = set()
                for cell in units:
                    if len(self.domains[cell]) != 1:
                        return False
                    count.add(next(iter(self.domains[cell])))
                if len(count) < 9:
                    return False
                
        return True 
    

    def revise(self, xi, xj):
        revised = False
        to_remove = set()
        for x in self.domains[xi]:
            # Nếu không có giá trị y nào khác x trong xj thỏa mãn ràng buộc, loại bỏ x
            if not any(x != y for y in self.domains[xj]):
                to_remove.add(x)
                revised = True
        if revised:
            self.domains[xi] -= to_remove
        return revised
    
    def ac3(self):
        queue = deque()
        for xi in self.domains:
            for xj in self.sudoku.neighbors(xi):
                queue.append((xi, xj))

        while queue:
            xi, xj = queue.popleft()
            if self.revise(xi, xj):
                if len(self.domains[xi]) == 0:
                    return False
                for xk in self.sudoku.neighbors(xi):
                    if xk != xj:
                        queue.append((xk, xi))
        return True


    def is_complete1(self, assignment):
        return len(assignment) == self.height*self.width
    
    def order_domains_value(self, cell, assignment):
        def number_conflicts(value):
            count = 0
            for neighbor in self.sudoku.neighbors(cell):
                if neighbor in assignment:
                    continue
                if value in self.domains[neighbor]:
                    count+=1
            return count
        return sorted(self.domains[cell], key=number_conflicts)
    
    def select_unassigned_variable(self, assignment):
        unassigned = [x for x in self.domains if x not in assignment]
        return min(
            unassigned,
            key= lambda var: (
                len(self.domains[var]),
                len(self.sudoku.neighbors(var))
            )
        )
    
    def consistent(self, assignment):
        for cell1 in assignment:
            for cell2 in assignment:
                if cell1 == cell2:
                    continue
                if self.sudoku.is_neighbor(cell1, cell2):
                    if assignment[cell1] == assignment[cell2]:
                        return False
                    
        return True
    
    def inferences(self, cell, value):
        self.domains[cell] = {value}
        x, y = cell
        self.sudoku.structure[x][y] = value
        for neighbor in self.sudoku.neighbors(cell):
            if value in self.domains[neighbor]:
                self.domains[neighbor].remove(value)

    def backtrack(self, assignment):
        if self.is_complete1(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        list_val = self.order_domains_value(var, assignment)
        tmp_domains = copy.deepcopy(self.domains)
        for value in list_val:
            assignment[var] = value
            if self.consistent(assignment):  # kiểm tra sau khi gán
                self.inferences(var, value)
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            # backtrack
            self.domains = copy.deepcopy(tmp_domains)
            self.sudoku.structure[var[0]][var[1]] = None
            del assignment[var]
        return None

    def solve1(self):
        self.enforce_node_consistency()
        # self.ac3()
        assignment = {}
        for cell in self.domains:
            if len(self.domains[cell]) == 1:
                assignment[cell] = next(iter(self.domains[cell]))

        return self.backtrack(assignment)

        



    def solve(self):
        self.enforce_node_consistency()
        self.propagate_constraints()
        return self.is_complete()

    def print_board(self):
        for i in range(9):
            row = [str(next(iter(self.domains[(i, j)])) if len(self.domains[(i, j)]) == 1 else '.') for j in range(9)]
            print(' '.join(row))

    def print(self, assignment):
        for i in range(9):
            row = []
            for j in range(9):
                row.append(assignment[(i, j)])
            print(row)
    
    


def main():
    import sys
    if len(sys.argv) != 2:
        sys.exit('miss structure file')
    sudoku = Sudoku(sys.argv[1])
    creator = Sudoku_Solve(sudoku)
    res = creator.solve1()
    if res != None:
        creator.print(res)

        # creator.print_board()
    else:
        print('No solution')



if __name__ == '__main__':
    main()