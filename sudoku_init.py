WIDTH = 9
HEIGHT = 9
class Sudoku:
    
    def __init__(self, structure_file):
        self.width = WIDTH
        self.height = HEIGHT
        with open(structure_file, 'r') as f:
            lines = f.readlines()
            self.structure = []
            for line in lines:
                row = []
                for i in range(self.width):
                    if line[i] != '0':
                        row.append(int(line[i]))
                    else:
                        row.append(None)
                self.structure.append(row)

        # self.variables = ()
        # for i in range(WIDTH):
        #     for j in range(HEIGHT):
        #         if self.structure[i][j] is None:
        #             self.variables

    def neighbors(self, cell):
        x, y = cell
        res = set()
        for i in range(9):
            if i == y:
                continue
            if self.structure[x][i] is None:
                res.add((x,i))

        for j in range(9):
            if x == j:
                continue
            if self.structure[j][y] is None:
                res.add((j, y))
            
        for i in range((x//3)*3, (x//3)+3):
            for j in range((y//3)*3, (y//3)+3):
                if i==x and j == y:
                    continue
                if self.structure[i][j] is None:
                    res.add((i, j))

        return res    
    

    def is_neighbor(self, cell1, cell2):
        x1, y1 = cell1
        x2, y2 = cell2
        if x1 == x2 or y1== y2 or (x1//3==x2//3 and y1//3==y2//3):
            return True