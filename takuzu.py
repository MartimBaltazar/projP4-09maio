# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 31:
# 99280 Martim Baltazar
# 99344 Vasco Simões
from sys import stdin

import sys

from numpy import append
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    def __init__(self,board,lst):
        self.board_str = board
        self.board_lst = lst 

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return board.board_lst[row][col]
        pass

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        if (row+1 == len(board.board_lst)):
            vertical_below = None
        else:
            vertical_below = int(board.board_lst[row+1][col])
            
        if (row != 0):
            vertical_above = int(board.board_lst[row-1][col])
        else: 
            vertical_above = None
        return (vertical_below,vertical_above)
        pass

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if (col+1 == len(board.board_lst)):
            column_right = None
        else:
            column_right = int(board.board_lst[row][col+1])
            
        if (col != 0):
            column_left = int(board.board_lst[row][col-1])
        else: 
            column_left = None
        return (column_left,column_right)
        pass

    def possible_actions(self, row: int, col:int,number:int) -> [(int,int,int)]:
        """Decide se uma ação é válida num determinado board"""
        
        # Verifica se horizontais sao iguais
        if (self.adjacent_horizontal_numbers(row,col) == (number,number)):
            print("pass Linhas:",(row,col,number))
            return None

        # Verifica se verticais sao iguais
        if (self.adjacent_vertical_numbers(row,col) == (number,number)):
            print("pass Coluna:",(row,col,number))
            return None

        # Verifica duas filas para cima
        if (row > 2):
            if (number == int(self.get_number(row-1,col)) 
            and number == int(self.get_number(row-2,col))):
                print("row,col: ",row,col)
                print((row,col,number))
                return None

        # Verifica duas filas para baixo
        if (row <= len(self.board_lst)-2):
            if (number == int(self.get_number(row+1,col)) 
            and number == int(self.get_number(row+2,col))):
                print("row,col: ",row,col)
                print((row,col,number))
                return None
        
        # Verifica duas colunas à esquerda
        if(col > 2):
            if (number == int(self.get_number(row,col-1)) 
            and number == int(self.get_number(row,col-2))):
                print("row,col: ",row,col)
                print((row,col,number))
                return None

        # Verifica duas colunas à direita
        if (col <= len(self.board_lst)-2):
            if (number == int(self.get_number(row,col+1)) 
            and number == int(self.get_number(row,col+2))):
                print("row,col: ",row,col)
                print((row,col,number))
                return None

        n = len(board.board_lst)
        #print("N: ",n)
        if (n % 2) == 0:
            lim = n // 2
        else:
            lim = (n // 2) + 1

        # Verificar se pode "number" na linha
        counter = 0
        for a in range(0,n):
            if board.board_lst[row][a] == str(number):
                counter += 1
        if (counter >= lim):
            return None

        # Verificar se pode "number" na coluna
        counter = 0
        for a in range(0,n):
            if board.board_lst[a][col] == str(number):
                counter += 1
        if (counter >= lim):
            return None

        return (row,col,number)  
    pass

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 takuzu.py < input_T01

            > from sys import stdin
            > stdin.readline()
        """
        board_list =[]
        boardstate = Board('',board_list)
        number = int(stdin.readline())
        number1 = number
        
        while (number1 != 0):
            line = stdin.readline()
            line_split = line.split("   ")
            print(line_split)
            board_list.append(line_split)
            number1 -= 1
            
        
        for a in range(0,number):
            for b in range(0,number):
                if 0 <= b < (number-1):
                    boardstate.board_str = boardstate.board_str +  board_list[a][b] + ' '          
                else:
                    boardstate.board_str = boardstate.board_str + board_list[a][b]
        return boardstate
        pass
    def __str__ (self):
        return str(self.board_str)

    # TODO: outros metodos da classe


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.board = board
        # TODO

        pass

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        actions = []
        size = len(state.board.board_lst)
        for a in range(0,size):
            for b in range(0,size):

                if state.board.get_number(a,b) == "2" or state.board.board_lst[a][b] == "2\n":
                    if (state.board.possible_actions(a,b,0)) != None:
                        actions.append(state.board.possible_actions(a,b,0))
                    if (state.board.possible_actions(a,b,1)) != None:
                        actions.append(state.board.possible_actions(a,b,1))
                    #actions.append(state.board.row_actions(a,b,0))
                    #actions.append(state.board.row_actions(a,b,1))
                    #actions.append((a,b,0))
                    #actions.append((a,b,1))
        # TODO

        print(actions)
        pass

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    
    board = Board.parse_instance_from_stdin() 
    print("Initial:\n", board, sep="")

    problem = Takuzu(board)
    print(board.adjacent_vertical_numbers(3, 3))
    initial_state = TakuzuState(board)
    problem.actions(initial_state)
    # Mostrar valor na posição (2, 2):
    #print(initial_state.board.get_number(2, 2)) 
    
    #print(board.adjacent_horizontal_numbers(3, 3))
    #print(board.adjacent_vertical_numbers(1, 1))
    #print(board.adjacent_horizontal_numbers(1, 1))

    pass
