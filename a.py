class Solution:
    def isValidSudoku(self, board: list[list[str]]) -> bool:

        for i in range(9):
            mp = []
            for j in range(9):
                if board[i][j].isdigit():
                    if board[i][j] in mp:
                        return False
                    mp.append(board[i][j])
            del mp
            mp = []
            for j in range(9):
                if board[j][i].isdigit():
                    if board[j][i] in mp:
                        return False    
                    mp.append(board[j][i])
            del mp


        for i in range(0,3):
            for j in range(0,3):
                mp=[]
                for a in range(i*3,i*3+3):
                    for b in range(j*3,j*3+3):
                        if board[a][b].isdigit():
                            if board[a][b] in mp:
                                return False
                            mp.append(board[a][b])
                del mp

        return True
        

print(Solution().isValidSudoku([["5","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]))