# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 31:
# 99280 Martim Baltazar
# 99344 Vasco Simões
from copy import deepcopy
from sys import stdin

import sys

from numpy import append
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    depth_limited_search,
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

        self.num_pos_livres = 0
        self.coord_pos = {}
        
        self.livres_row = {}
        self.livres_col = {}

        self.adj_verticais = {}
        self.adj_horizontais = {}

        self.adj_cima = {}
        self.adj_baixo = {}
        self.adj_direita = {}
        self.adj_esquerda = {}

        self.row_values = {}
        self.col_values = {}

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board_lst[row][col]
        pass

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        if (row+1 == len(self.board_lst)):
            vertical_below = None
        else:
            vertical_below = int(self.board_lst[row+1][col])
            
        if (row != 0):
            vertical_above = int(self.board_lst[row-1][col])
        else: 
            vertical_above = None
        return (vertical_below,vertical_above)
        pass

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if (col+1 == len(self.board_lst)):
            column_right = None
        else:
            column_right = int(self.board_lst[row][col+1])
            
        if (col != 0):
            column_left = int(self.board_lst[row][col-1])
        else: 
            column_left = None
        return (column_left,column_right)
        pass

    def possible_actions(self, row: int, col:int,number:int) -> [(int,int,int)]:
        """Decide se uma ação é válida num determinado board"""
        
        # Verifica se horizontais sao iguais
        # #print("adj,hor:",self.adjacent_horizontal_numbers(row,col))
        if (self.adjacent_horizontal_numbers(row,col) == (number,number)):
            return None

        # Verifica se verticais sao iguais
        if (self.adjacent_vertical_numbers(row,col) == (number,number)):
            return None

        n = len(self.board_lst)
        var = 0
        lim = n // 2

        if (n % 2) != 0:
            var = -1
            lim+=1

        # Verifica duas filas para cima
        if (row >= 2):
            if (number == int(self.get_number(row-1,col)) 
            and number == int(self.get_number(row-2,col))):
                return None

        # Verifica duas filas para baixo
        if (row <= n-3):
            if (number == int(self.get_number(row+1,col)) 
            and number == int(self.get_number(row+2,col))):
                return None
        
        # Verifica duas colunas à esquerda
        if(col >= 2):
            if (number == int(self.get_number(row,col-1)) 
            and number == int(self.get_number(row,col-2))):         
                return None

        # Verifica duas colunas à direita
        if (col <= n-3):
            if (number == int(self.get_number(row,col+1)) 
            and number == int(self.get_number(row,col+2))):  
                return None

        
        # Verificar se pode "number" na linha
        counter = 1
        for a in range(0,n):
            if int(self.board_lst[row][a]) == number:
                if (a != col):
                    counter += 1
        if (counter > lim):
            return None

        # Verificar se pode "number" na coluna
        counter = 1
        for a in range(0,n):
            if int(self.board_lst[a][col]) == number:
                if (a != row):
                    counter += 1
        if (counter > lim):
            return None


        return (row,col,number)  
    pass

    def board_attibutes_setup(self):
        """Percorre o board e regista informações relevantes para a escolha
        das ações """

        n = len(self.board_lst)

        var = 0

        if (n % 2) != 0:
            var = -1
       
        for a in range(0,n):
            countZerosColuna = 0
            countUnsColuna = 0

            countZerosLinha = 0
            countUnsLinha = 0

            self.livres_row[a] = 0
            self.livres_col[a] = 0

            for b in range(0,n): 
                valor_pos = int(self.board_lst[a][b])
                valor_col = int(self.board_lst[b][a])

                if valor_pos == 2:

                    self.num_pos_livres +=1
                    self.coord_pos[(a,b)] = 1
                    self.livres_row[a]+=1

                    self.adj_verticais[(a,b)] = [self.adjacent_vertical_numbers(a,b)[0],self.adjacent_vertical_numbers(a,b)[1]]
                    self.adj_horizontais[(a,b)] = [self.adjacent_horizontal_numbers(a,b)[0],self.adjacent_horizontal_numbers(a,b)[1]]

                if valor_pos == 0:
                    countZerosLinha+=1
                if valor_pos == 1:
                    countUnsLinha+=1

                if valor_col == 0:
                    countZerosColuna+=1
                if valor_col == 1:
                    countUnsColuna+=1
                if valor_col == 2:
                    self.livres_col[a]+=1

                # Verifica duas filas para cima
                if (a >= 2) and valor_pos == 2:
                    self.adj_cima[(a,b)]=[int(self.get_number(a-1,b)),int(self.get_number(a-2,b))]

                # Verifica duas filas para baixo
                if (a <= n-3) and valor_pos == 2:
                    self.adj_baixo[(a,b)]=[int(self.get_number(a+1,b)),int(self.get_number(a+2,b))]

                # Verifica duas colunas à esquerda
                if(b >= 2) and valor_pos == 2:
                    self.adj_esquerda[(a,b)]=[int(self.get_number(a,b-1)),int(self.get_number(a,b-2))]

                # Verifica duas colunas à direita
                if (b <= n-3) and valor_pos == 2:
                    self.adj_direita[(a,b)]=[int(self.get_number(a,b+1)),int(self.get_number(a,b+2))]                

            self.row_values[a] = [countZerosLinha,countUnsLinha]
            self.col_values[a] = [countZerosColuna,countUnsColuna]
        return 0
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
        
        # #print(number1)

        while (number1 != 0):
            line = stdin.readline()
            line_split = line.split("\t")
            board_list.append((line_split))
            number1 -= 1
            
        
        for a in range(0,number):
            for b in range(0,number):
                if 0 <= b < (number-1):
                    boardstate.board_str = boardstate.board_str +  board_list[a][b] + '\t'          
                else:
                    boardstate.board_str = boardstate.board_str + board_list[a][b]
                board_list[a][b] = int(board_list[a][b])
        return boardstate
        pass
    def __str__ (self):
        return str(self.board_str)

    # TODO: outros metodos da classe


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.board = board
        self.initial = TakuzuState(board)
        # TODO

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        actions = []
        
        n = len(self.board.board_lst)
        lim = n // 2
        if (n % 2) != 0:
            lim +=1

        counter = 0
        for a in range(0,n):
            for b in range (0,n):
                if int(state.board.board_lst[a][b]) == 2:
                    counter+=1
                    self.board.coord_pos[(a,b)] = 1

         #print(counter)

        self.board.num_pos_livres = counter
         #print("pos livres: ",counter)

        while (counter > 0):
            good_action = False
            if (good_action == False):
                if (self.get_key(self.board.adj_horizontais,[0,0]) != None):
                    good_action = True

                    # Guardar a posicao no tabuleiro
                    pos = self.get_key(self.board.adj_horizontais,[0,0])
                    actions.append((pos[0],pos[1],1))
   
                    self.board.num_pos_livres-=1
                    # Coordenadas das posicoes livres
                    del self.board.coord_pos[pos]
                    self.board.row_values[pos[0]] = [self.board.row_values[pos[0]][0],self.board.row_values[pos[0]][1]+1]
                    self.board.col_values[pos[1]] = [self.board.col_values[pos[1]][0],self.board.col_values[pos[1]][1]+1]
                    adj_vert = self.board.adj_verticais[pos]
                    adj_hor = self.board.adj_horizontais[pos]

                    if pos in self.board.adj_cima:
                        adj_cima = self.board.adj_cima[pos]
                        
                    if pos in self.board.adj_baixo:
                        adj_baixa = self.board.adj_baixo[pos]
                    
                    if pos in self.board.adj_esquerda:
                        adj_esquerda = self.board.adj_esquerda[pos]
                    
                    if pos in self.board.adj_direita:
                        adj_direita = self.board.adj_direita[pos]

                    if (adj_vert[0]==2):
                        pos_vert = (pos[0]+1,pos[1])
                        if pos_vert in self.board.adj_verticais:
                            self.board.adj_verticais[pos_vert] = [self.board.adj_verticais[pos_vert][0],1]

                        if (pos_vert in self.board.adj_cima):
                            self.board.adj_cima[pos_vert] = [1,self.board.adj_cima[pos_vert][1]]

                    if (adj_vert[1]==2):
                        pos_vert = (pos[0]-1,pos[1])
                        self.board.adj_verticais[pos_vert] = [1,self.board.adj_verticais[pos_vert][1]]
                        if (pos_vert in self.board.adj_baixo):
                            self.board.adj_baixo[pos_vert] = [1,self.board.adj_baixo[pos_vert][1]]

                    if pos in self.board.adj_cima:
                        adj_cima = self.board.adj_cima[pos]
                        if(adj_cima[1]==2):
                            pos_cima = (pos[0]-2,pos[1])
                            if (pos_cima in self.board.adj_baixo):
                                self.board.adj_baixo[pos_cima] = [self.board.adj_baixo[pos_cima][0],1]

                    if pos in self.board.adj_baixo:
                        adj_baixo = self.board.adj_baixo[pos]
                        if (adj_baixo[1]==2):
                            pos_baixo = (pos[0]+2,pos[1])
                            if (pos_baixo in self.board.adj_cima):
                                self.board.adj_cima[pos_baixo] = [self.board.adj_cima[pos_baixo][0],1]

                    if pos in self.board.adj_esquerda:
                        adj_esquerda = self.board.adj_esquerda[pos]
                        if (adj_esquerda[1]==2):
                            pos_esquerda = (pos[0],pos[1]-2)
                            if (pos_esquerda in self.board.adj_direita):
                                self.board.adj_direita[pos_esquerda] = [self.board.adj_direita[pos_esquerda][0],1]

                    # Alterar, nas adj direiuta, as adjacentes da posicao a esquerda
                    if pos in self.board.adj_direita:
                        adj_direita = self.board.adj_direita[pos]
                        if (adj_direita[1]==2):
                            pos_direita = (pos[0],pos[1]+2)
                            if (pos_direita in self.board.adj_esquerda):
                                self.board.adj_esquerda[pos_direita] = [self.board.adj_esquerda[pos_direita][0],1]

                     #print("vert:",self.board.adj_verticais[pos])
                     #print("hori:",self.board.adj_horizontais[pos])
                    
                    del self.board.adj_verticais[pos]
                    del self.board.adj_horizontais[pos]

                    if pos in self.board.adj_cima:
                        del self.board.adj_cima[pos]

                    if pos in self.board.adj_baixo:
                        del self.board.adj_baixo[pos]

                    if pos in self.board.adj_esquerda:            
                        del self.board.adj_esquerda[pos]

                    if pos in self.board.adj_direita:
                        del self.board.adj_direita[pos]

                    counter-=1

                elif (self.get_key(self.board.adj_horizontais,[1,1]) != None):
                    good_action = True

                    # Guardar a posicao no tabuleiro
                    pos = self.get_key(self.board.adj_horizontais,[1,1])
                     #print(pos)
                    # (2,2)

                    # Adicionar jogada a lista actions
                    
                    #if pos == (4,10):
                        #exit()
                    actions.append((pos[0],pos[1],0))
                     #print(actions)

                    ## Atualizar as estruturas

                    # Numero de posicoes livres    
                    self.board.num_pos_livres-=1
                     #print("Num pos livres: ",self.board.num_pos_livres) 
                    
                    # Coordenadas das posicoes livres
                    del self.board.coord_pos[pos]
                     #print("Coordenadas pos livres: ",self.board.coord_pos,"\n")

                     #print("Zeros e Uns por linha:  ",self.board.row_values)
                     #print("Zeros e Uns por coluna: ",self.board.col_values,"\n")

                    # Valores de 0 e 1 na linha   =       # Zeros (+1)                          # Um
                    self.board.row_values[pos[0]] = [self.board.row_values[pos[0]][0]+1,self.board.row_values[pos[0]][1]]

                    # Valores de 0 e 1 na linha   =       # Zeros (+1)                          # Um
                    self.board.col_values[pos[1]] = [self.board.col_values[pos[1]][0]+1,self.board.col_values[pos[1]][1]]
                            
                     #print("Zeros e Uns por linha:  ",self.board.row_values)
                     #print("Zeros e Uns por coluna: ",self.board.col_values,"\n")
                    # Eliminar a pos escolhida da lista de adjacentes
                    
                    if pos in self.board.adj_verticais:
                        adj_vert = self.board.adj_verticais[pos]

                    adj_hor = self.board.adj_horizontais[pos]

                    if pos in self.board.adj_cima:
                        adj_cima = self.board.adj_cima[pos]
                        
                    if pos in self.board.adj_baixo:
                        adj_baixa = self.board.adj_baixo[pos]
                    
                    if pos in self.board.adj_esquerda:
                        adj_esquerda = self.board.adj_esquerda[pos]
                    
                    if pos in self.board.adj_direita:
                        adj_direita = self.board.adj_direita[pos]

                    # Alterar, nas adj verticais, as adjacentes da posicao abaixo
                    if (adj_vert[0]==2):
                        pos_vert = (pos[0]+1,pos[1])
                        if pos_vert in self.board.adj_verticais:
                            self.board.adj_verticais[pos_vert] = [self.board.adj_verticais[pos_vert][0],0]
                            if (pos_vert in self.board.adj_cima):
                                self.board.adj_cima[pos_vert] = [0,self.board.adj_cima[pos_vert][1]]
                    
                    # Alterar, nas adj verticais, as adjacentes da posicao acima
                    if (adj_vert[1]==2):
                        pos_vert = (pos[0]-1,pos[1])
                        if pos_vert in self.board.adj_verticais:
                            self.board.adj_verticais[pos_vert] = [0,self.board.adj_verticais[pos_vert][1]]
                            if (pos_vert in self.board.adj_baixo):
                                self.board.adj_baixo[pos_vert] = [0,self.board.adj_baixo[pos_vert][1]]

                    # Alterar, nas adj cima, as adjacentes da posicao abaixo
                    if pos in self.board.adj_cima:
                        adj_cima = self.board.adj_cima[pos]
                        if(adj_cima[1]==2):
                            pos_cima = (pos[0]-2,pos[1])
                            if (pos_cima in self.board.adj_baixo):
                                self.board.adj_baixo[pos_cima] = [self.board.adj_baixo[pos_cima][0],0]

                    # Alterar, nas adj vaixo, as adjacentes da posicao acima
                    if pos in self.board.adj_baixo:
                        adj_baixo = self.board.adj_baixo[pos]
                        if (adj_baixo[1]==2):
                            pos_baixo = (pos[0]+2,pos[1])
                            if (pos_baixo in self.board.adj_cima):
                                self.board.adj_cima[pos_baixo] = [self.board.adj_cima[pos_baixo][0],0]

                    # Alterar, nas adj esqeuerda, as adjacentes da posicao a direiuta
                    if pos in self.board.adj_esquerda:
                        adj_esquerda = self.board.adj_esquerda[pos]
                        if (adj_esquerda[1]==2):
                            pos_esquerda = (pos[0],pos[1]-2)
                            if (pos_esquerda in self.board.adj_direita):
                                self.board.adj_direita[pos_esquerda] = [self.board.adj_direita[pos_esquerda][0],0]


                    # Alterar, nas adj direiuta, as adjacentes da posicao a esquerda
                    if pos in self.board.adj_direita:
                        adj_direita = self.board.adj_direita[pos]
                        if (adj_direita[1]==2):
                            pos_direita = (pos[0],pos[1]+2)
                            if (pos_direita in self.board.adj_esquerda):
                                self.board.adj_esquerda[pos_direita] = [self.board.adj_esquerda[pos_direita][0],0]

                     #print("vert:",self.board.adj_verticais[pos])
                     #print("hori:",self.board.adj_horizontais[pos])
                    
                    del self.board.adj_verticais[pos]
                    del self.board.adj_horizontais[pos]

                    if pos in self.board.adj_cima:
                        del self.board.adj_cima[pos]

                    if pos in self.board.adj_baixo:
                        del self.board.adj_baixo[pos]

                    if pos in self.board.adj_esquerda:            
                        del self.board.adj_esquerda[pos]

                    if pos in self.board.adj_direita:
                        del self.board.adj_direita[pos]

                    counter-=1
                
                elif (self.get_key(self.board.adj_verticais,[0,0]) != None):
                    good_action = True

                    pos = self.get_key(self.board.adj_verticais,[0,0])

                    actions.append((pos[0],pos[1],1))
                    self.board.num_pos_livres-=1

                    del self.board.coord_pos[pos]
                    # Valores de 0 e 1 na linha   =       # Zeros                           # Um (+1)
                    self.board.row_values[pos[0]] = [self.board.row_values[pos[0]][0],self.board.row_values[pos[0]][1]+1]

                    # Valores de 0 e 1 na linha   =       # Zeros                           # Um (+1)
                    self.board.col_values[pos[1]] = [self.board.col_values[pos[1]][0],self.board.col_values[pos[1]][1]+1]
                            
                    adj_vert = self.board.adj_verticais[pos]
                    adj_hor = self.board.adj_horizontais[pos]

                    if pos in self.board.adj_cima:
                        adj_cima = self.board.adj_cima[pos]
                        
                    if pos in self.board.adj_baixo:
                        adj_baixa = self.board.adj_baixo[pos]
                    
                    if pos in self.board.adj_esquerda:
                        adj_esquerda = self.board.adj_esquerda[pos]
                    
                    if pos in self.board.adj_direita:
                        adj_direita = self.board.adj_direita[pos]

                    # Alterar, nas adj horizontais, as adjacentes da posicao abaixo
                    if (adj_hor[0]==2):
                        pos_hor = (pos[0],pos[1]-1)
                         #print(self.board.adj_horizontais[pos_hor])
                        self.board.adj_horizontais[pos_hor] = [self.board.adj_horizontais[pos_hor][0],1]
                        if (pos_hor in self.board.adj_direita):
                            self.board.adj_direita[pos_hor] = [1,self.board.adj_direita[pos_hor][1]]
                
                    # Alterar, nas adj verticais, as adjacentes da posicao acima
                    if (adj_hor[1]==2):
                        pos_hor = (pos[0],pos[1]+1)
                        self.board.adj_horizontais[pos_hor] = [1,self.board.adj_horizontais[pos_hor][1]]

                        if (pos_hor in self.board.adj_esquerda):
                            self.board.adj_esquerda[pos_hor] = [1,self.board.adj_esquerda[pos_hor][1]]
                    
                    # Alterar, nas adj cima, as adjacentes da posicao abaixo
                    if pos in self.board.adj_cima:
                        adj_cima = self.board.adj_cima[pos]
                        if(adj_cima[1]==2):
                            pos_cima = (pos[0]-2,pos[1])
                            if (pos_cima in self.board.adj_baixo):
                                self.board.adj_baixo[pos_cima] = [self.board.adj_baixo[pos_cima][0],1]

                    # Alterar, nas adj vaixo, as adjacentes da posicao acima
                    if pos in self.board.adj_baixo:
                        adj_baixo = self.board.adj_baixo[pos]
                        if (adj_baixo[1]==2):
                            pos_baixo = (pos[0]+2,pos[1])
                            if pos_baixo in self.board.adj_cima:
                                self.board.adj_cima[pos_baixo] = [self.board.adj_cima[pos_baixo][0],1]

                    # Alterar, nas adj esqeuerda, as adjacentes da posicao a direiuta
                    if pos in self.board.adj_esquerda:
                        adj_esquerda = self.board.adj_esquerda[pos]
                        if (adj_esquerda[1]==2):
                            pos_esquerda = (pos[0],pos[1]-2)
                            if pos_esquerda in self.board.adj_direita:
                                self.board.adj_direita[pos_esquerda] = [self.board.adj_direita[pos_esquerda][0],1]

                    # Alterar, nas adj direiuta, as adjacentes da posicao a esquerda
                    if pos in self.board.adj_direita:
                        adj_direita = self.board.adj_direita[pos]
                        if (adj_direita[1]==2):
                            pos_direita = (pos[0],pos[1]+2)
                            if pos_direita in self.board.adj_esquerda:
                                self.board.adj_esquerda[pos_direita] = [self.board.adj_esquerda[pos_direita][0],1]

                    del self.board.adj_verticais[pos]
                    del self.board.adj_horizontais[pos]

                    if pos in self.board.adj_cima:
                        del self.board.adj_cima[pos]

                    if pos in self.board.adj_baixo:
                        del self.board.adj_baixo[pos]

                    if pos in self.board.adj_esquerda:            
                        del self.board.adj_esquerda[pos]

                    if pos in self.board.adj_direita:
                        del self.board.adj_direita[pos]

                    counter-=1

                elif (self.get_key(self.board.adj_verticais,[1,1]) != None):
                    good_action = True

                    pos = self.get_key(self.board.adj_verticais,[1,1])
                    actions.append((pos[0],pos[1],0))
                    self.board.num_pos_livres-=1
                    del self.board.coord_pos[pos]
                    self.board.row_values[pos[0]] = [self.board.row_values[pos[0]][0]+1,self.board.row_values[pos[0]][1]]
                    self.board.col_values[pos[1]] = [self.board.col_values[pos[1]][0]+1,self.board.col_values[pos[1]][1]]
                            
                    adj_vert = self.board.adj_verticais[pos]
                    adj_hor = self.board.adj_horizontais[pos]

                    if pos in self.board.adj_cima:
                        adj_cima = self.board.adj_cima[pos]
                        
                    if pos in self.board.adj_baixo:
                        adj_baixa = self.board.adj_baixo[pos]
                    
                    if pos in self.board.adj_esquerda:
                        adj_esquerda = self.board.adj_esquerda[pos]
                    
                    if pos in self.board.adj_direita:
                        adj_direita = self.board.adj_direita[pos]

                    # Alterar, nas adj horizontais, as adjacentes da posicao abaixo
                    if (adj_hor[0]==2):
                        pos_hor = (pos[0],pos[1]-1)
                        if pos_hor in self.board.adj_horizontais:
                            self.board.adj_horizontais[pos_hor] = [self.board.adj_horizontais[pos_hor][0],0]
                            if (pos_hor in self.board.adj_direita):
                                self.board.adj_direita[pos_hor] = [0,self.board.adj_direita[pos_hor][1]]
                    
                    # Alterar, nas adj verticais, as adjacentes da posicao acima
                    if (adj_hor[1]==2):
                        pos_hor = (pos[0],pos[1]+1)
                        if pos_hor in self.board.adj_horizontais:
                            self.board.adj_horizontais[pos_hor] = [0,self.board.adj_horizontais[pos_hor][1]]
                            if (pos_hor in self.board.adj_esquerda):
                                self.board.adj_esquerda[pos_hor] = [0,self.board.adj_esquerda[pos_hor][1]]
                    
                    # Alterar, nas adj cima, as adjacentes da posicao abaixo
                    if pos in self.board.adj_cima:
                        adj_cima = self.board.adj_cima[pos]
                        if(adj_cima[1]==2):
                            pos_cima = (pos[0]-2,pos[1])
                            if (pos_cima in self.board.adj_baixo):
                                self.board.adj_baixo[pos_cima] = [self.board.adj_baixo[pos_cima][0],0]

                    # Alterar, nas adj vaixo, as adjacentes da posicao acima
                    if pos in self.board.adj_baixo:
                        adj_baixo = self.board.adj_baixo[pos]
                        if (adj_baixo[1]==2):
                            pos_baixo = (pos[0]+2,pos[1])
                            if pos_baixo in self.board.adj_cima:
                                self.board.adj_cima[pos_baixo] = [self.board.adj_cima[pos_baixo][0],0]

                    # Alterar, nas adj esqeuerda, as adjacentes da posicao a direiuta
                    if pos in self.board.adj_esquerda:
                        adj_esquerda = self.board.adj_esquerda[pos]
                        if (adj_esquerda[1]==2):
                            pos_esquerda = (pos[0],pos[1]-2)
                            if pos_esquerda in self.board.adj_direita:
                                self.board.adj_direita[pos_esquerda] = [self.board.adj_direita[pos_esquerda][0],0]

                    # Alterar, nas adj direiuta, as adjacentes da posicao a esquerda
                    if pos in self.board.adj_direita:
                        adj_direita = self.board.adj_direita[pos]
                        if (adj_direita[1]==2):
                            pos_direita = (pos[0],pos[1]+2)
                            if pos_direita in self.board.adj_esquerda:
                                self.board.adj_esquerda[pos_direita] = [self.board.adj_esquerda[pos_direita][0],0]

                     #print("vert:",self.board.adj_verticais[pos])
                     #print("hori:",self.board.adj_horizontais[pos])
                    
                    del self.board.adj_verticais[pos]
                    del self.board.adj_horizontais[pos]

                    if pos in self.board.adj_cima:
                        del self.board.adj_cima[pos]

                    if pos in self.board.adj_baixo:
                        del self.board.adj_baixo[pos]

                    if pos in self.board.adj_esquerda:            
                        del self.board.adj_esquerda[pos]

                    if pos in self.board.adj_direita:
                        del self.board.adj_direita[pos]

                    counter-=1

                elif (self.get_key(self.board.adj_cima,[0,0]) != None):
                    good_action = True

                    # Guardar a posicao no tabuleiro
                    pos = self.get_key(self.board.adj_cima,[0,0])
                     #print(pos)
                    # (2,2)

                    # Adicionar jogada a lista actions
 
                    actions.append((pos[0],pos[1],1))
                     #print(actions)

                    ## Atualizar as estruturas

                    # Numero de posicoes livres    
                    self.board.num_pos_livres-=1
                     #print("Num pos livres: ",self.board.num_pos_livres) 
                    
                    # Coordenadas das posicoes livres
                    del self.board.coord_pos[pos]
                    self.board.row_values[pos[0]] = [self.board.row_values[pos[0]][0],self.board.row_values[pos[0]][1]+1]

                    # Valores de 0 e 1 na linha   =       # Zeros                         # Um (+1) 
                    self.board.col_values[pos[1]] = [self.board.col_values[pos[1]][0],self.board.col_values[pos[1]][1]+1]
                            
                    if pos in self.board.adj_baixo:
                        adj_baixo = self.board.adj_baixo[pos]
                        if (adj_baixo[0]==2):
                            pos_baixo = (pos[0]+1,pos[1])
                            if pos_baixo in self.board.adj_verticais:
                                self.board.adj_verticais[pos_baixo] = [self.board.adj_verticais[pos_baixo][0],1]
                                if (pos_baixo in self.board.adj_cima):
                                    self.board.adj_cima[pos_baixo] = [1,self.board.adj_cima[pos_baixo][1]]
                
                    if pos in self.board.adj_baixo:
                        adj_baixo = self.board.adj_baixo[pos]
                        if (adj_baixo[1]==2):
                            pos_baixo = (pos[0]+2,pos[1])
                            if (pos_baixo in self.board.adj_cima):
                                self.board.adj_cima[pos_baixo] = [self.board.adj_cima[pos_baixo][0],1]

                    if pos in self.board.adj_horizontais:
                        adj_hor = self.board.adj_horizontais[pos]
                        if (adj_hor[1]==2):
                            pos_hor = (pos[0],pos[1]+1)
                            self.board.adj_horizontais[pos_hor] = [1,self.board.adj_horizontais[pos_hor][1]]
                            if (pos_hor in self.board.adj_esquerda):
                                self.board.adj_esquerda[pos_hor] = [1,self.board.adj_esquerda[pos_hor][1]]
                            
                    if pos in self.board.adj_horizontais:
                            adj_hor = self.board.adj_horizontais[pos]
                            if (adj_hor[0]==2):
                                pos_hor = (pos[0],pos[1]-1)
                                self.board.adj_horizontais[pos_hor] = [self.board.adj_horizontais[pos_hor][0],1]
                                if (pos_hor in self.board.adj_direita):
                                    self.board.adj_direita[pos_hor] = [1,self.board.adj_direita[pos_hor][1]]

                    if pos in self.board.adj_direita:
                        adj_direita = self.board.adj_direita[pos]
                        if (adj_direita[1]==2):
                            pos_direita = (pos[0],pos[1]+2)
                            if pos_direita in self.board.adj_esquerda:
                                self.board.adj_esquerda[pos_direita] = [self.board.adj_esquerda[pos_direita][0],1]

                    if pos in self.board.adj_esquerda:
                        adj_esquerda = self.board.adj_esquerda[pos]
                        if (adj_esquerda[1]==2):
                            pos_esquerda = (pos[0],pos[1]-2)
                            if pos_esquerda in self.board.adj_direita:
                                self.board.adj_direita[pos_esquerda] = [self.board.adj_direita[pos_esquerda][0],1]

                    # Porque foi preenchida
                    del self.board.adj_verticais[pos]
                    del self.board.adj_horizontais[pos]

                    if pos in self.board.adj_cima:
                        del self.board.adj_cima[pos]

                    if pos in self.board.adj_baixo:
                        del self.board.adj_baixo[pos]

                    if pos in self.board.adj_esquerda:            
                        del self.board.adj_esquerda[pos]

                    if pos in self.board.adj_direita:
                        del self.board.adj_direita[pos]

                    counter-=1
        
                elif (self.get_key(self.board.adj_cima,[1,1]) != None):
                    good_action = True

                    # Guardar a posicao no tabuleiro
                    pos = self.get_key(self.board.adj_cima,[1,1])
                     #print(pos)
                    # (2,2)

                    # Adicionar jogada a lista actions
 
                    actions.append((pos[0],pos[1],0))
                     #print(actions)

                    ## Atualizar as estruturas

                    # Numero de posicoes livres    
                    self.board.num_pos_livres-=1
                     #print("Num pos livres: ",self.board.num_pos_livres) 
                    
                    # Coordenadas das posicoes livres
                    del self.board.coord_pos[pos]
                     #print("Coordenadas pos livres: ",self.board.coord_pos,"\n")

                     #print("Zeros e Uns por linha:  ",self.board.row_values)
                     #print("Zeros e Uns por coluna: ",self.board.col_values,"\n")

                    # Valores de 0 e 1 na linha   =       # Zeros (+1)                          # Um 
                    self.board.row_values[pos[0]] = [self.board.row_values[pos[0]][0]+1,self.board.row_values[pos[0]][1]]

                    # Valores de 0 e 1 na linha   =       # Zeros (+1)                          # Um
                    self.board.col_values[pos[1]] = [self.board.col_values[pos[1]][0]+1,self.board.col_values[pos[1]][1]]
                            
                     #print("Zeros e Uns por linha:  ",self.board.row_values)
                     #print("Zeros e Uns por coluna: ",self.board.col_values,"\n")

                    if pos in self.board.adj_baixo:
                        adj_baixo = self.board.adj_baixo[pos]
                        if (adj_baixo[0]==2):
                            pos_baixo = (pos[0]+1,pos[1])
                            if pos_baixo in self.board.adj_verticais:
                                self.board.adj_verticais[pos_baixo] = [self.board.adj_verticais[pos_baixo][0],0]
                                if (pos_baixo in self.board.adj_cima):
                                    self.board.adj_cima[pos_baixo] = [0,self.board.adj_cima[pos_baixo][1]]
                
                    if pos in self.board.adj_baixo:
                        adj_baixo = self.board.adj_baixo[pos]
                        if (adj_baixo[1]==2):
                            pos_baixo = (pos[0]+2,pos[1])
                            if (pos_baixo in self.board.adj_cima):
                                self.board.adj_cima[pos_baixo] = [self.board.adj_cima[pos_baixo][0],0]

                    if pos in self.board.adj_horizontais:
                        adj_hor = self.board.adj_horizontais[pos]
                        if (adj_hor[1]==2):
                            pos_hor = (pos[0],pos[1]+1)
                            self.board.adj_horizontais[pos_hor] = [0,self.board.adj_horizontais[pos_hor][1]]
                            if (pos_hor in self.board.adj_esquerda):
                                self.board.adj_esquerda[pos_hor] = [0,self.board.adj_esquerda[pos_hor][1]]
                            
                    if pos in self.board.adj_horizontais:
                            adj_hor = self.board.adj_horizontais[pos]
                            if (adj_hor[0]==2):
                                pos_hor = (pos[0],pos[1]-1)
                                self.board.adj_horizontais[pos_hor] = [self.board.adj_horizontais[pos_hor][0],0]
                                if (pos_hor in self.board.adj_direita):
                                    self.board.adj_direita[pos_hor] = [0,self.board.adj_direita[pos_hor][1]]

                    if pos in self.board.adj_direita:
                        adj_direita = self.board.adj_direita[pos]
                        if (adj_direita[1]==2):
                            pos_direita = (pos[0],pos[1]+2)
                            if pos_direita in self.board.adj_esquerda:
                                self.board.adj_esquerda[pos_direita] = [self.board.adj_esquerda[pos_direita][0],0]

                    if pos in self.board.adj_esquerda:
                        adj_esquerda = self.board.adj_esquerda[pos]
                        if (adj_esquerda[1]==2):
                            pos_esquerda = (pos[0],pos[1]-2)
                            if pos_esquerda in self.board.adj_direita:
                                self.board.adj_direita[pos_esquerda] = [self.board.adj_direita[pos_esquerda][0],0]

                    # Porque foi preenchida
                    del self.board.adj_verticais[pos]
                    del self.board.adj_horizontais[pos]

                    if pos in self.board.adj_cima:
                        del self.board.adj_cima[pos]

                    if pos in self.board.adj_baixo:
                        del self.board.adj_baixo[pos]

                    if pos in self.board.adj_esquerda:            
                        del self.board.adj_esquerda[pos]

                    if pos in self.board.adj_direita:
                        del self.board.adj_direita[pos]

                    counter-=1
        
                elif (self.get_key(self.board.adj_baixo,[0,0]) != None):
                    good_action = True

                    # Guardar a posicao no tabuleiro
                    pos = self.get_key(self.board.adj_baixo,[0,0])
                     #print(pos)
                    # (2,2)

                    # Adicionar jogada a lista actions
 
                    actions.append((pos[0],pos[1],1))
                     #print(actions)

                    ## Atualizar as estruturas

                    # Numero de posicoes livres    
                    self.board.num_pos_livres-=1
                     #print("Num pos livres: ",self.board.num_pos_livres) 
                    
                    # Coordenadas das posicoes livres
                    del self.board.coord_pos[pos]
                     #print("Coordenadas pos livres: ",self.board.coord_pos,"\n")

                     #print("Zeros e Uns por linha:  ",self.board.row_values)
                     #print("Zeros e Uns por coluna: ",self.board.col_values,"\n")

                    # Valores de 0 e 1 na linha   =       # Zeros                           # Um (+1)
                    self.board.row_values[pos[0]] = [self.board.row_values[pos[0]][0],self.board.row_values[pos[0]][1]+1]

                    # Valores de 0 e 1 na linha   =       # Zeros                         # Um (+1) 
                    self.board.col_values[pos[1]] = [self.board.col_values[pos[1]][0],self.board.col_values[pos[1]][1]+1]
                            
                     #print("Zeros e Uns por linha:  ",self.board.row_values)
                     #print("Zeros e Uns por coluna: ",self.board.col_values,"\n")


                    if pos in self.board.adj_cima:
                        adj_cima = self.board.adj_cima[pos]
                        if (adj_cima[0]==2):
                            pos_cima = (pos[0]-1,pos[1])
                            if pos_cima in self.board.adj_verticais:
                                self.board.adj_verticais[pos_cima] = [1,self.board.adj_verticais[pos_cima][1]]
                                if (pos_cima in self.board.adj_baixo):
                                    self.board.adj_baixo[pos_cima] = [1,self.board.adj_baixo[pos_cima][1]]
                
                    if pos in self.board.adj_cima:
                        adj_cima = self.board.adj_cima[pos]
                        if (adj_cima[1]==2):
                            pos_cima = (pos[0]-2,pos[1])
                            if (pos_cima in self.board.adj_baixo):
                                self.board.adj_baixo[pos_cima] = [self.board.adj_baixo[pos_cima][0],1]

                    if pos in self.board.adj_horizontais:
                        adj_hor = self.board.adj_horizontais[pos]
                        if (adj_hor[1]==2):
                            pos_hor = (pos[0],pos[1]+1)
                            self.board.adj_horizontais[pos_hor] = [1,self.board.adj_horizontais[pos_hor][1]]
                            if (pos_hor in self.board.adj_esquerda):
                                self.board.adj_esquerda[pos_hor] = [1,self.board.adj_esquerda[pos_hor][1]]
                            
                    if pos in self.board.adj_horizontais:
                            adj_hor = self.board.adj_horizontais[pos]
                            if (adj_hor[0]==2):
                                pos_hor = (pos[0],pos[1]-1)
                                self.board.adj_horizontais[pos_hor] = [self.board.adj_horizontais[pos_hor][0],1]
                                if (pos_hor in self.board.adj_direita):
                                    self.board.adj_direita[pos_hor] = [1,self.board.adj_direita[pos_hor][1]]

                    if pos in self.board.adj_direita:
                        adj_direita = self.board.adj_direita[pos]
                        if (adj_direita[1]==2):
                            pos_direita = (pos[0],pos[1]+2)
                            if pos_direita in self.board.adj_esquerda:
                                self.board.adj_esquerda[pos_direita] = [self.board.adj_esquerda[pos_direita][0],1]

                    if pos in self.board.adj_esquerda:
                        adj_esquerda = self.board.adj_esquerda[pos]
                        if (adj_esquerda[1]==2):
                            pos_esquerda = (pos[0],pos[1]-2)
                            if pos_esquerda in self.board.adj_direita:
                                self.board.adj_direita[pos_esquerda] = [self.board.adj_direita[pos_esquerda][0],1]

                    # Porque foi preenchida
                    del self.board.adj_verticais[pos]
                    del self.board.adj_horizontais[pos]

                    if pos in self.board.adj_cima:
                        del self.board.adj_cima[pos]

                    if pos in self.board.adj_baixo:
                        del self.board.adj_baixo[pos]

                    if pos in self.board.adj_esquerda:            
                        del self.board.adj_esquerda[pos]

                    if pos in self.board.adj_direita:
                        del self.board.adj_direita[pos]

                    counter-=1

                elif (self.get_key(self.board.adj_baixo,[1,1]) != None):
                    good_action = True

                    # Guardar a posicao no tabuleiro
                    pos = self.get_key(self.board.adj_baixo,[1,1])
                     #print(pos)
                    # (2,2)

                    # Adicionar jogada a lista actions
 
                    actions.append((pos[0],pos[1],0))
                     #print(actions)

                    ## Atualizar as estruturas

                    # Numero de posicoes livres    
                    self.board.num_pos_livres-=1
                     #print("Num pos livres: ",self.board.num_pos_livres) 
                    
                    # Coordenadas das posicoes livres
                    del self.board.coord_pos[pos]
                     #print("Coordenadas pos livres: ",self.board.coord_pos,"\n")

                     #print("Zeros e Uns por linha:  ",self.board.row_values)
                     #print("Zeros e Uns por coluna: ",self.board.col_values,"\n")

                    # Valores de 0 e 1 na linha   =       # Zeros (+1)                          # Um 
                    self.board.row_values[pos[0]] = [self.board.row_values[pos[0]][0]+1,self.board.row_values[pos[0]][1]]

                    # Valores de 0 e 1 na linha   =       # Zeros (+1)                          # Um
                    self.board.col_values[pos[1]] = [self.board.col_values[pos[1]][0]+1,self.board.col_values[pos[1]][1]]
                            
                     #print("Zeros e Uns por linha:  ",self.board.row_values)
                     #print("Zeros e Uns por coluna: ",self.board.col_values,"\n")

                    if pos in self.board.adj_cima:
                        adj_cima = self.board.adj_cima[pos]
                        if (adj_cima[0]==2):
                            pos_cima = (pos[0]-1,pos[1])
                            if pos_cima in self.board.adj_verticais:
                                self.board.adj_verticais[pos_cima] = [0,self.board.adj_verticais[pos_cima][1]]
                                if (pos_cima in self.board.adj_baixo):
                                    self.board.adj_baixo[pos_cima] = [0,self.board.adj_baixo[pos_cima][1]]
                
                    if pos in self.board.adj_cima:
                        adj_cima = self.board.adj_cima[pos]
                        if (adj_cima[1]==2):
                            pos_cima = (pos[0]-2,pos[1])
                            if (pos_cima in self.board.adj_baixo):
                                self.board.adj_baixo[pos_cima] = [self.board.adj_baixo[pos_cima][0],0]

                    if pos in self.board.adj_horizontais:
                        adj_hor = self.board.adj_horizontais[pos]
                        if (adj_hor[1]==2):
                            pos_hor = (pos[0],pos[1]+1)
                            self.board.adj_horizontais[pos_hor] = [0,self.board.adj_horizontais[pos_hor][1]]
                            if (pos_hor in self.board.adj_esquerda):
                                self.board.adj_esquerda[pos_hor] = [0,self.board.adj_esquerda[pos_hor][1]]
                            
                    if pos in self.board.adj_horizontais:
                            adj_hor = self.board.adj_horizontais[pos]
                            if (adj_hor[0]==2):
                                pos_hor = (pos[0],pos[1]-1)
                                self.board.adj_horizontais[pos_hor] = [self.board.adj_horizontais[pos_hor][0],0]
                                if (pos_hor in self.board.adj_direita):
                                    self.board.adj_direita[pos_hor] = [0,self.board.adj_direita[pos_hor][1]]

                    if pos in self.board.adj_direita:
                        adj_direita = self.board.adj_direita[pos]
                        if (adj_direita[1]==2):
                            pos_direita = (pos[0],pos[1]+2)
                            if pos_direita in self.board.adj_esquerda:
                                self.board.adj_esquerda[pos_direita] = [self.board.adj_esquerda[pos_direita][0],0]

                    if pos in self.board.adj_esquerda:
                        adj_esquerda = self.board.adj_esquerda[pos]
                        if (adj_esquerda[1]==2):
                            pos_esquerda = (pos[0],pos[1]-2)
                            if pos_esquerda in self.board.adj_direita:
                                self.board.adj_direita[pos_esquerda] = [self.board.adj_direita[pos_esquerda][0],0]


                    # Porque foi preenchida
                    del self.board.adj_verticais[pos]
                    del self.board.adj_horizontais[pos]

                    if pos in self.board.adj_cima:
                        del self.board.adj_cima[pos]

                    if pos in self.board.adj_baixo:
                        del self.board.adj_baixo[pos]

                    if pos in self.board.adj_esquerda:            
                        del self.board.adj_esquerda[pos]

                    if pos in self.board.adj_direita:
                        del self.board.adj_direita[pos]

                    counter-=1

                elif (self.get_key(self.board.adj_esquerda,[0,0]) != None):
                    good_action = True

                    # Guardar a posicao no tabuleiro
                    pos = self.get_key(self.board.adj_esquerda,[0,0])
                     #print(pos)

                    # Adicionar jogada a lista actions
 
                    actions.append((pos[0],pos[1],1))
                     #print(actions)

                    ## Atualizar as estruturas

                    # Numero de posicoes livres    
                    self.board.num_pos_livres-=1
                     #print("Num pos livres: ",self.board.num_pos_livres) 
                    
                    # Coordenadas das posicoes livres
                    del self.board.coord_pos[pos]
                     #print("Coordenadas pos livres: ",self.board.coord_pos,"\n")

                     #print("Zeros e Uns por linha:  ",self.board.row_values)
                     #print("Zeros e Uns por coluna: ",self.board.col_values,"\n")

                         #print(self.board.row_values)
                         #print(self.board.col_values)


                    # Valores de 0 e 1 na linha   =       # Zeros                           # Um (+1)
                    self.board.row_values[pos[0]] = [self.board.row_values[pos[0]][0],self.board.row_values[pos[0]][1]+1]

                    # Valores de 0 e 1 na linha   =       # Zeros                         # Um (+1) 
                    self.board.col_values[pos[1]] = [self.board.col_values[pos[1]][0],self.board.col_values[pos[1]][1]+1]

                    #if pos == (1,6):
                        # #print("\n",self.board.row_values)
                        # #print(self.board.col_values)
                            
                     #print("Zeros e Uns por linha:  ",self.board.row_values)
                     #print("Zeros e Uns por coluna: ",self.board.col_values,"\n")

                    if pos in self.board.adj_horizontais:
                        adj_hor = self.board.adj_horizontais[pos]
                        if (adj_hor[1]==2):
                            pos_hor = (pos[0],pos[1]+1)
                            self.board.adj_horizontais[pos_hor] = [1,self.board.adj_horizontais[pos_hor][1]]
                            if (pos_hor in self.board.adj_esquerda):
                                self.board.adj_esquerda[pos_hor] = [1,self.board.adj_esquerda[pos_hor][1]]

                    if pos in self.board.adj_direita:
                        adj_direita = self.board.adj_direita[pos]
                        if (adj_direita[1]==2):
                            pos_direita = (pos[0],pos[1]+2)
                            if pos_direita in self.board.adj_esquerda:
                                self.board.adj_esquerda[pos_direita] = [self.board.adj_esquerda[pos_direita][0],1]

                    if pos in self.board.adj_cima:
                        adj_cima = self.board.adj_cima[pos]
                        if (adj_cima[0]==2):
                            pos_cima = (pos[0]-1,pos[1])
                            if pos_cima in self.board.adj_verticais:
                                self.board.adj_verticais[pos_cima] = [1,self.board.adj_verticais[pos_cima][1]]
                                if (pos_cima in self.board.adj_baixo):
                                    self.board.adj_baixo[pos_cima] = [1,self.board.adj_baixo[pos_cima][1]]
                
                    if pos in self.board.adj_cima:
                        adj_cima = self.board.adj_cima[pos]
                        if (adj_cima[1]==2):
                            pos_cima = (pos[0]-2,pos[1])
                            if (pos_cima in self.board.adj_baixo):
                                self.board.adj_baixo[pos_cima] = [self.board.adj_baixo[pos_cima][0],1]

                    if pos in self.board.adj_baixo:
                        adj_baixo = self.board.adj_baixo[pos]
                        if (adj_baixo[0]==2):
                            pos_baixo = (pos[0]+1,pos[1])
                            if pos_baixo in self.board.adj_verticais:
                                self.board.adj_verticais[pos_baixo] = [self.board.adj_verticais[pos_baixo][0],1]
                                if (pos_baixo in self.board.adj_cima):
                                    self.board.adj_cima[pos_baixo] = [1,self.board.adj_cima[pos_baixo][1]]
                
                    if pos in self.board.adj_baixo:
                        adj_baixo = self.board.adj_baixo[pos]
                        if (adj_baixo[1]==2):
                            pos_baixo = (pos[0]+2,pos[1])
                            if (pos_baixo in self.board.adj_cima):
                                self.board.adj_cima[pos_baixo] = [self.board.adj_cima[pos_baixo][0],1]

                    # Porque foi preenchida
                    del self.board.adj_verticais[pos]
                    del self.board.adj_horizontais[pos]

                    if pos in self.board.adj_cima:
                        del self.board.adj_cima[pos]

                    if pos in self.board.adj_baixo:
                        del self.board.adj_baixo[pos]

                    if pos in self.board.adj_esquerda:            
                        del self.board.adj_esquerda[pos]

                    if pos in self.board.adj_direita:
                        del self.board.adj_direita[pos]

                    counter-=1

                elif (self.get_key(self.board.adj_esquerda,[1,1]) != None):
                    good_action = True

                    # Guardar a posicao no tabuleiro
                    pos = self.get_key(self.board.adj_esquerda,[1,1])
                     #print(pos)
                    # (2,2)

                    # Adicionar jogada a lista actions
 
                    actions.append((pos[0],pos[1],0))
                     #print(actions)

                    ## Atualizar as estruturas

                    # Numero de posicoes livres    
                    self.board.num_pos_livres-=1
                     #print("Num pos livres: ",self.board.num_pos_livres) 
                    
                    # Coordenadas das posicoes livres
                    del self.board.coord_pos[pos]
                     #print("Coordenadas pos livres: ",self.board.coord_pos,"\n")

                     #print("Zeros e Uns por linha:  ",self.board.row_values)
                     #print("Zeros e Uns por coluna: ",self.board.col_values,"\n")

                    # Valores de 0 e 1 na linha   =       # Zeros (+1)                          # Um 
                    self.board.row_values[pos[0]] = [self.board.row_values[pos[0]][0]+1,self.board.row_values[pos[0]][1]]

                    # Valores de 0 e 1 na linha   =       # Zeros (+1)                          # Um
                    self.board.col_values[pos[1]] = [self.board.col_values[pos[1]][0]+1,self.board.col_values[pos[1]][1]]

                     #print("Zeros e Uns por linha:  ",self.board.row_values)
                     #print("Zeros e Uns por coluna: ",self.board.col_values,"\n")

                    if pos in self.board.adj_horizontais:
                        adj_hor = self.board.adj_horizontais[pos]
                        if (adj_hor[1]==2):
                            pos_hor = (pos[0],pos[1]+1)
                            self.board.adj_horizontais[pos_hor] = [0,self.board.adj_horizontais[pos_hor][1]]
                            if (pos_hor in self.board.adj_esquerda):
                                self.board.adj_esquerda[pos_hor] = [0,self.board.adj_esquerda[pos_hor][1]]

                    if pos in self.board.adj_direita:
                        adj_direita = self.board.adj_direita[pos]
                        if (adj_direita[1]==2):
                            pos_direita = (pos[0],pos[1]+2)
                            if pos_direita in self.board.adj_esquerda:
                                self.board.adj_esquerda[pos_direita] = [self.board.adj_esquerda[pos_direita][0],0]

                    if pos in self.board.adj_cima:
                        adj_cima = self.board.adj_cima[pos]
                        if (adj_cima[0]==2):
                            pos_cima = (pos[0]-1,pos[1])
                            if pos_cima in self.board.adj_verticais:
                                self.board.adj_verticais[pos_cima] = [0,self.board.adj_verticais[pos_cima][1]]
                                if (pos_cima in self.board.adj_baixo):
                                    self.board.adj_baixo[pos_cima] = [0,self.board.adj_baixo[pos_cima][1]]
                
                    if pos in self.board.adj_cima:
                        adj_cima = self.board.adj_cima[pos]
                        if (adj_cima[1]==2):
                            pos_cima = (pos[0]-2,pos[1])
                            if (pos_cima in self.board.adj_baixo):
                                self.board.adj_baixo[pos_cima] = [self.board.adj_baixo[pos_cima][0],0]

                    if pos in self.board.adj_baixo:
                        adj_baixo = self.board.adj_baixo[pos]
                        if (adj_baixo[0]==2):
                            pos_baixo = (pos[0]+1,pos[1])
                            if pos_baixo in self.board.adj_verticais:
                                self.board.adj_verticais[pos_baixo] = [self.board.adj_verticais[pos_baixo][0],0]
                                if (pos_baixo in self.board.adj_cima):
                                    self.board.adj_cima[pos_baixo] = [0,self.board.adj_cima[pos_baixo][1]]
                
                    if pos in self.board.adj_baixo:
                        adj_baixo = self.board.adj_baixo[pos]
                        if (adj_baixo[1]==2):
                            pos_baixo = (pos[0]+2,pos[1])
                            if (pos_baixo in self.board.adj_cima):
                                self.board.adj_cima[pos_baixo] = [self.board.adj_cima[pos_baixo][0],0]

                    # Porque foi preenchida
                    del self.board.adj_verticais[pos]
                    del self.board.adj_horizontais[pos]

                    if pos in self.board.adj_cima:
                        del self.board.adj_cima[pos]

                    if pos in self.board.adj_baixo:
                        del self.board.adj_baixo[pos]

                    if pos in self.board.adj_esquerda:            
                        del self.board.adj_esquerda[pos]

                    if pos in self.board.adj_direita:
                        del self.board.adj_direita[pos]

                    counter-=1

                elif (self.get_key(self.board.adj_direita,[0,0]) != None):
                    good_action = True

                    # Guardar a posicao no tabuleiro
                    pos = self.get_key(self.board.adj_direita,[0,0])
                     #print(pos)
                    # (2,2)

                    # Adicionar jogada a lista actions
                    actions.append((pos[0],pos[1],1))
                     #print(actions)

                    ## Atualizar as estruturas

                    # Numero de posicoes livres    
                    self.board.num_pos_livres-=1
                     #print("Num pos livres: ",self.board.num_pos_livres) 
                    
                    # Coordenadas das posicoes livres
                    del self.board.coord_pos[pos]
                     #print("Coordenadas pos livres: ",self.board.coord_pos,"\n")

                     #print("Zeros e Uns por linha:  ",self.board.row_values)
                     #print("Zeros e Uns por coluna: ",self.board.col_values,"\n")

                    # Valores de 0 e 1 na linha   =       # Zeros                           # Um (+1)
                    self.board.row_values[pos[0]] = [self.board.row_values[pos[0]][0],self.board.row_values[pos[0]][1]+1]

                    # Valores de 0 e 1 na linha   =       # Zeros                         # Um (+1) 
                    self.board.col_values[pos[1]] = [self.board.col_values[pos[1]][0],self.board.col_values[pos[1]][1]+1]
                            
                     #print("Zeros e Uns por linha:  ",self.board.row_values)
                     #print("Zeros e Uns por coluna: ",self.board.col_values,"\n")

                    if pos in self.board.adj_cima:
                        adj_cima = self.board.adj_cima[pos]
                        if (adj_cima[0]==2):
                            pos_cima = (pos[0]-1,pos[1])
                            if pos_cima in self.board.adj_verticais:
                                self.board.adj_verticais[pos_cima] = [1,self.board.adj_verticais[pos_cima][1]]
                                if (pos_cima in self.board.adj_baixo):
                                    self.board.adj_baixo[pos_cima] = [1,self.board.adj_baixo[pos_cima][1]]
                
                    if pos in self.board.adj_cima:
                        adj_cima = self.board.adj_cima[pos]
                        if (adj_cima[1]==2):
                            pos_cima = (pos[0]-2,pos[1])
                            if (pos_cima in self.board.adj_baixo):
                                self.board.adj_baixo[pos_cima] = [self.board.adj_baixo[pos_cima][0],1]

                    if pos in self.board.adj_baixo:
                        adj_baixo = self.board.adj_baixo[pos]
                        if (adj_baixo[0]==2):
                            pos_baixo = (pos[0]+1,pos[1])
                            if pos_baixo in self.board.adj_verticais:
                                self.board.adj_verticais[pos_baixo] = [self.board.adj_verticais[pos_baixo][0],1]
                                if (pos_baixo in self.board.adj_cima):
                                    self.board.adj_cima[pos_baixo] = [1,self.board.adj_cima[pos_baixo][1]]
                
                    if pos in self.board.adj_baixo:
                        adj_baixo = self.board.adj_baixo[pos]
                        if (adj_baixo[1]==2):
                            pos_baixo = (pos[0]+2,pos[1])
                            if (pos_baixo in self.board.adj_cima):
                                self.board.adj_cima[pos_baixo] = [self.board.adj_cima[pos_baixo][0],1]

                    if pos in self.board.adj_horizontais:
                            adj_hor = self.board.adj_horizontais[pos]
                            if (adj_hor[0]==2):
                                pos_hor = (pos[0],pos[1]-1)
                                self.board.adj_horizontais[pos_hor] = [self.board.adj_horizontais[pos_hor][0],1]
                                if (pos_hor in self.board.adj_direita):
                                    self.board.adj_direita[pos_hor] = [1,self.board.adj_direita[pos_hor][1]]

                    if pos in self.board.adj_esquerda:
                        adj_esquerda = self.board.adj_esquerda[pos]
                        if (adj_esquerda[1]==2):
                            pos_esquerda = (pos[0],pos[1]-2)
                            if pos_esquerda in self.board.adj_direita:
                                self.board.adj_direita[pos_esquerda] = [self.board.adj_direita[pos_esquerda][0],1]

                    # Porque foi preenchida
                    del self.board.adj_verticais[pos]
                    del self.board.adj_horizontais[pos]

                    if pos in self.board.adj_cima:
                        del self.board.adj_cima[pos]

                    if pos in self.board.adj_baixo:
                        del self.board.adj_baixo[pos]

                    if pos in self.board.adj_esquerda:            
                        del self.board.adj_esquerda[pos]

                    if pos in self.board.adj_direita:
                        del self.board.adj_direita[pos]

                    counter-=1

                elif (self.get_key(self.board.adj_direita,[1,1]) != None):
                    good_action = True

                    # Guardar a posicao no tabuleiro
                    pos = self.get_key(self.board.adj_direita,[1,1])
                     #print(pos)
                    # (2,2)

                    # Adicionar jogada a lista actions
                    actions.append((pos[0],pos[1],0))
                     #print(actions)

                    ## Atualizar as estruturas

                    # Numero de posicoes livres    
                    self.board.num_pos_livres-=1
                     #print("Num pos livres: ",self.board.num_pos_livres) 
                    
                    # Coordenadas das posicoes livres
                    del self.board.coord_pos[pos]
                     #print("Coordenadas pos livres: ",self.board.coord_pos,"\n")

                     #print("Zeros e Uns por linha:  ",self.board.row_values)
                     #print("Zeros e Uns por coluna: ",self.board.col_values,"\n")

                    # Valores de 0 e 1 na linha   =       # Zeros (+1)                          # Um 
                    self.board.row_values[pos[0]] = [self.board.row_values[pos[0]][0]+1,self.board.row_values[pos[0]][1]]

                    # Valores de 0 e 1 na linha   =       # Zeros (+1)                          # Um
                    self.board.col_values[pos[1]] = [self.board.col_values[pos[1]][0]+1,self.board.col_values[pos[1]][1]]
                            
                     #print("Zeros e Uns por linha:  ",self.board.row_values)
                     #print("Zeros e Uns por coluna: ",self.board.col_values,"\n")

                    if pos in self.board.adj_cima:
                        adj_cima = self.board.adj_cima[pos]
                        if (adj_cima[0]==2):
                            pos_cima = (pos[0]-1,pos[1])
                            if pos_cima in self.board.adj_verticais:
                                self.board.adj_verticais[pos_cima] = [0,self.board.adj_verticais[pos_cima][1]]
                                if (pos_cima in self.board.adj_baixo):
                                    self.board.adj_baixo[pos_cima] = [0,self.board.adj_baixo[pos_cima][1]]
                
                    if pos in self.board.adj_cima:
                        adj_cima = self.board.adj_cima[pos]
                        if (adj_cima[1]==2):
                            pos_cima = (pos[0]-2,pos[1])
                            if (pos_cima in self.board.adj_baixo):
                                self.board.adj_baixo[pos_cima] = [self.board.adj_baixo[pos_cima][0],0]

                    if pos in self.board.adj_baixo:
                        adj_baixo = self.board.adj_baixo[pos]
                        if (adj_baixo[0]==2):
                            pos_baixo = (pos[0]+1,pos[1])
                            if pos_baixo in self.board.adj_verticais:
                                self.board.adj_verticais[pos_baixo] = [self.board.adj_verticais[pos_baixo][0],0]
                                if (pos_baixo in self.board.adj_cima):
                                    self.board.adj_cima[pos_baixo] = [0,self.board.adj_cima[pos_baixo][1]]
                
                    if pos in self.board.adj_baixo:
                        adj_baixo = self.board.adj_baixo[pos]
                        if (adj_baixo[1]==2):
                            pos_baixo = (pos[0]+2,pos[1])
                            if (pos_baixo in self.board.adj_cima):
                                self.board.adj_cima[pos_baixo] = [self.board.adj_cima[pos_baixo][0],0]

                    if pos in self.board.adj_horizontais:
                            adj_hor = self.board.adj_horizontais[pos]
                            if (adj_hor[0]==2):
                                pos_hor = (pos[0],pos[1]-1)
                                self.board.adj_horizontais[pos_hor] = [self.board.adj_horizontais[pos_hor][0],0]
                                if (pos_hor in self.board.adj_direita):
                                    self.board.adj_direita[pos_hor] = [0,self.board.adj_direita[pos_hor][1]]

                    if pos in self.board.adj_esquerda:
                        adj_esquerda = self.board.adj_esquerda[pos]
                        if (adj_esquerda[1]==2):
                            pos_esquerda = (pos[0],pos[1]-2)
                            if pos_esquerda in self.board.adj_direita:
                                self.board.adj_direita[pos_esquerda] = [self.board.adj_direita[pos_esquerda][0],0]

                    # Porque foi preenchida
                    del self.board.adj_verticais[pos]
                    del self.board.adj_horizontais[pos]

                    if pos in self.board.adj_cima:
                        del self.board.adj_cima[pos]

                    if pos in self.board.adj_baixo:
                        del self.board.adj_baixo[pos]

                    if pos in self.board.adj_esquerda:            
                        del self.board.adj_esquerda[pos]

                    if pos in self.board.adj_direita:
                        del self.board.adj_direita[pos]

                    counter-=1
                
                else:
                     #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n")
                    for num_linha,valores_linha in self.board.row_values.items():
                        if (valores_linha[0] == lim) and (valores_linha[1] < lim):
                            posicao = []
                            for key in self.board.coord_pos:
                                if key[0] == num_linha:
                                    actions.append((key[0],key[1],1))
                                    posicao.append(key)
                                    self.board.num_pos_livres-=1
                                    counter-=1

                                    # Valores de 0 e 1 na linha   =       # Zeros                           # Um (+1)
                                    self.board.row_values[key[0]] = [self.board.row_values[key[0]][0],self.board.row_values[key[0]][1]+1]

                                    # Valores de 0 e 1 na linha   =       # Zeros                         # Um (+1) 
                                    self.board.col_values[key[1]] = [self.board.col_values[key[1]][0],self.board.col_values[key[1]][1]+1]
                                    
                                    # ATUALIZAR

                                    if key in self.board.adj_cima:
                                        adj_cima = self.board.adj_cima[key]
                                        if (adj_cima[0]==2):
                                            pos_cima = (key[0]-1,key[1])
                                            if pos_cima in self.board.adj_verticais:
                                                self.board.adj_verticais[pos_cima] = [1,self.board.adj_verticais[pos_cima][1]]
                                                if (pos_cima in self.board.adj_baixo):
                                                    self.board.adj_baixo[pos_cima] = [1,self.board.adj_baixo[pos_cima][1]]
                                
                                    if key in self.board.adj_cima:
                                        adj_cima = self.board.adj_cima[key]
                                        if (adj_cima[1]==2):
                                            pos_cima = (key[0]-2,key[1])
                                            if (pos_cima in self.board.adj_baixo):
                                                self.board.adj_baixo[pos_cima] = [self.board.adj_baixo[pos_cima][0],1]

                                    if key in self.board.adj_baixo:
                                        adj_baixo = self.board.adj_baixo[key]
                                        if (adj_baixo[0]==2):
                                            pos_baixo = (key[0]+1,key[1])
                                            if pos_baixo in self.board.adj_verticais:
                                                self.board.adj_verticais[pos_baixo] = [self.board.adj_verticais[pos_baixo][0],1]
                                                if (pos_baixo in self.board.adj_cima):
                                                    self.board.adj_cima[pos_baixo] = [1,self.board.adj_cima[pos_baixo][1]]
                                
                                    if key in self.board.adj_baixo:
                                        adj_baixo = self.board.adj_baixo[key]
                                        if (adj_baixo[1]==2):
                                            pos_baixo = (key[0]+2,key[1])
                                            if (pos_baixo in self.board.adj_cima):
                                                self.board.adj_cima[pos_baixo] = [self.board.adj_cima[pos_baixo][0],1]

                                    if key in self.board.adj_verticais:
                                        del self.board.adj_verticais[key]
                                                                    
                                    if key in self.board.adj_horizontais:
                                        del self.board.adj_horizontais[key]

                                    if key in self.board.adj_cima:
                                        del self.board.adj_cima[key]

                                    if key in self.board.adj_baixo:
                                        del self.board.adj_baixo[key]

                                    if key in self.board.adj_esquerda:            
                                        del self.board.adj_esquerda[key]

                                    if key in self.board.adj_direita:
                                        del self.board.adj_direita[key]


                            if (posicao != []):
                                good_action = True
                                for i in posicao:
                                    del self.board.coord_pos[i]


                        if (valores_linha[0] < lim) and (valores_linha[1] == lim):
                            posicao = []
                            for key in self.board.coord_pos:
                                if key[0] == num_linha:
                                    actions.append((key[0],key[1],0))
                                    posicao.append(key)
                                    self.board.num_pos_livres-=1
                                    counter-=1

                                    # Valores de 0 e 1 na linha   =       # Zeros (+1)                      # Um
                                    self.board.row_values[key[0]] = [self.board.row_values[key[0]][0]+1,self.board.row_values[key[0]][1]]

                                    # Valores de 0 e 1 na linha   =       # Zeros  (+1)                     # Um
                                    self.board.col_values[key[1]] = [self.board.col_values[key[1]][0]+1,self.board.col_values[key[1]][1]]

                                    # ATUALIZAR

                                    if key in self.board.adj_cima:
                                        adj_cima = self.board.adj_cima[key]
                                        if (adj_cima[0]==2):
                                            pos_cima = (key[0]-1,key[1])
                                            if pos_cima in self.board.adj_verticais:
                                                self.board.adj_verticais[pos_cima] = [0,self.board.adj_verticais[pos_cima][1]]
                                                if (pos_cima in self.board.adj_baixo):
                                                    self.board.adj_baixo[pos_cima] = [0,self.board.adj_baixo[pos_cima][1]]
                                
                                    if key in self.board.adj_cima:
                                        adj_cima = self.board.adj_cima[key]
                                        if (adj_cima[1]==2):
                                            pos_cima = (key[0]-2,key[1])
                                            if (pos_cima in self.board.adj_baixo):
                                                self.board.adj_baixo[pos_cima] = [self.board.adj_baixo[pos_cima][0],0]

                                    if key in self.board.adj_baixo:
                                        adj_baixo = self.board.adj_baixo[key]
                                        if (adj_baixo[0]==2):
                                            pos_baixo = (key[0]+1,key[1])
                                            if pos_baixo in self.board.adj_verticais:
                                                self.board.adj_verticais[pos_baixo] = [self.board.adj_verticais[pos_baixo][0],0]
                                                if (pos_baixo in self.board.adj_cima):
                                                    self.board.adj_cima[pos_baixo] = [0,self.board.adj_cima[pos_baixo][1]]
                                
                                    if key in self.board.adj_baixo:
                                        adj_baixo = self.board.adj_baixo[key]
                                        if (adj_baixo[1]==2):
                                            pos_baixo = (key[0]+2,key[1])
                                            if (pos_baixo in self.board.adj_cima):
                                                self.board.adj_cima[pos_baixo] = [self.board.adj_cima[pos_baixo][0],0]

                                    if key in self.board.adj_verticais:
                                        del self.board.adj_verticais[key]
                                                                    
                                    if key in self.board.adj_horizontais:
                                        del self.board.adj_horizontais[key]

                                    if key in self.board.adj_cima:
                                        del self.board.adj_cima[key]

                                    if key in self.board.adj_baixo:
                                        del self.board.adj_baixo[key]

                                    if key in self.board.adj_esquerda:            
                                        del self.board.adj_esquerda[key]

                                    if key in self.board.adj_direita:
                                        del self.board.adj_direita[key]


                            if (posicao != []):
                                good_action = True
                                for i in posicao:
                                    del self.board.coord_pos[i]

                    for num_coluna,valores_coluna in self.board.col_values.items():
                        if (valores_coluna[0] == lim) and (valores_coluna[1] < lim):
                            posicao = []
                            for key in self.board.coord_pos:
                                if key[1] == num_coluna:
                                    actions.append((key[0],key[1],1))
                                    posicao.append(key)
                                    self.board.num_pos_livres-=1
                                    counter-=1

                                    # Valores de 0 e 1 na linha   =       # Zeros                           # Um (+1)
                                    self.board.row_values[key[0]] = [self.board.row_values[key[0]][0],self.board.row_values[key[0]][1]+1]

                                    # Valores de 0 e 1 na linha   =       # Zeros                         # Um (+1) 
                                    self.board.col_values[key[1]] = [self.board.col_values[key[1]][0],self.board.col_values[key[1]][1]+1]


                                    # ATUALIZAR

                                    if key in self.board.adj_horizontais:
                                        adj_hor = self.board.adj_horizontais[key]
                                        if (adj_hor[1]==2):
                                            pos_hor = (key[0],key[1]+1)
                                            self.board.adj_horizontais[pos_hor] = [1,self.board.adj_horizontais[pos_hor][1]]
                                            if (pos_hor in self.board.adj_esquerda):
                                                self.board.adj_esquerda[pos_hor] = [1,self.board.adj_esquerda[pos_hor][1]]
                                            
                                    if key in self.board.adj_horizontais:
                                            adj_hor = self.board.adj_horizontais[key]
                                            if (adj_hor[0]==2):
                                                pos_hor = (key[0],key[1]-1)
                                                self.board.adj_horizontais[pos_hor] = [self.board.adj_horizontais[pos_hor][0],1]
                                                if (pos_hor in self.board.adj_direita):
                                                    self.board.adj_direita[pos_hor] = [1,self.board.adj_direita[pos_hor][1]]

                                    if key in self.board.adj_direita:
                                        adj_direita = self.board.adj_direita[key]
                                        if (adj_direita[1]==2):
                                            pos_direita = (key[0],key[1]+2)
                                            if pos_direita in self.board.adj_esquerda:
                                                self.board.adj_esquerda[pos_direita] = [self.board.adj_esquerda[pos_direita][0],1]

                                    if key in self.board.adj_esquerda:
                                        adj_esquerda = self.board.adj_esquerda[key]
                                        if (adj_esquerda[1]==2):
                                            pos_esquerda = (key[0],key[1]-2)
                                            if pos_esquerda in self.board.adj_direita:
                                                self.board.adj_direita[pos_esquerda] = [self.board.adj_direita[pos_esquerda][0],1]


                                    if key in self.board.adj_verticais:
                                        del self.board.adj_verticais[key]
                                                                    
                                    if key in self.board.adj_horizontais:
                                        del self.board.adj_horizontais[key]

                                    if key in self.board.adj_cima:
                                        del self.board.adj_cima[key]

                                    if key in self.board.adj_baixo:
                                        del self.board.adj_baixo[key]

                                    if key in self.board.adj_esquerda:            
                                        del self.board.adj_esquerda[key]

                                    if key in self.board.adj_direita:
                                        del self.board.adj_direita[key]


                            if (posicao != []):
                                good_action = True
                                for i in posicao:
                                    del self.board.coord_pos[i]

                        if (valores_coluna[0] < lim) and (valores_coluna[1] == lim):
                            posicao = []
                            for key in self.board.coord_pos:
                                if key[1] == num_coluna:
                                    actions.append((key[0],key[1],0))
                                    posicao.append(key)
                                    
                                    self.board.num_pos_livres-=1
                                    counter-=1

                                    # Valores de 0 e 1 na linha   =       # Zeros (+1)                      # Um
                                    self.board.row_values[key[0]] = [self.board.row_values[key[0]][0]+1,self.board.row_values[key[0]][1]]

                                    # Valores de 0 e 1 na linha   =       # Zeros  (+1)                     # Um
                                    self.board.col_values[key[1]] = [self.board.col_values[key[1]][0]+1,self.board.col_values[key[1]][1]]

                                    # ATUALIZAR
                                    
                                    if key in self.board.adj_horizontais:
                                        adj_hor = self.board.adj_horizontais[key]
                                        if (adj_hor[1]==2):
                                            pos_hor = (key[0],key[1]+1)
                                            self.board.adj_horizontais[pos_hor] = [0,self.board.adj_horizontais[pos_hor][1]]
                                            if (pos_hor in self.board.adj_esquerda):
                                                self.board.adj_esquerda[pos_hor] = [0,self.board.adj_esquerda[pos_hor][1]]
                                            
                                    if key in self.board.adj_horizontais:
                                            adj_hor = self.board.adj_horizontais[key]
                                            if (adj_hor[0]==2):
                                                pos_hor = (key[0],key[1]-1)
                                                self.board.adj_horizontais[pos_hor] = [self.board.adj_horizontais[pos_hor][0],0]
                                                if (pos_hor in self.board.adj_direita):
                                                    self.board.adj_direita[pos_hor] = [0,self.board.adj_direita[pos_hor][1]]

                                    if key in self.board.adj_direita:
                                        adj_direita = self.board.adj_direita[key]
                                         #print(adj_direita)
                                        if (adj_direita[1]==2):
                                            pos_direita = (key[0],key[1]+2)
                                             #print(pos_direita)
                                            if pos_direita in self.board.adj_esquerda:
                                                self.board.adj_esquerda[pos_direita] = [self.board.adj_esquerda[pos_direita][0],0]
                                    
                                    if key in self.board.adj_esquerda:
                                        adj_esquerda = self.board.adj_esquerda[key]
                                        if (adj_esquerda[1]==2):
                                            pos_esquerda = (key[0],key[1]-2)
                                            if pos_esquerda in self.board.adj_direita:
                                                self.board.adj_direita[pos_esquerda] = [self.board.adj_direita[pos_esquerda][0],0]

                                    if key in self.board.adj_verticais:
                                        del self.board.adj_verticais[key]
                                                                    
                                    if key in self.board.adj_horizontais:
                                        del self.board.adj_horizontais[key]

                                    if key in self.board.adj_cima:
                                        del self.board.adj_cima[key]

                                    if key in self.board.adj_baixo:
                                        del self.board.adj_baixo[key]

                                    if key in self.board.adj_esquerda:            
                                        del self.board.adj_esquerda[key]

                                    if key in self.board.adj_direita:
                                        del self.board.adj_direita[key]

                            if (posicao != []):
                                good_action = True
                                for i in posicao:
                                    del self.board.coord_pos[i]
                    
            # Talvez faça sentido peneirar as ERRADAS pelo possible action
            if (good_action == False):
                 #print("posicoes vazias: ",self.board.coord_pos,"\n")
                posicao = []
                 #print(self.board.coord_pos)
                #exit()
                for key in self.board.coord_pos:
                    #if (state.board.possible_actions(key[0],key[1],0) != None):
                    actions.append((key[0],key[1],0))

                    #if (state.board.possible_actions(key[0],key[1],1) != None):
                    actions.append((key[0],key[1],1))

                    #actions.append((key[0],key[1],0))
                    #actions.append((key[0],key[1],1))
                    posicao.append(key)
                    self.board.num_pos_livres-=1
                    counter-=1
                
                if (posicao != []):
                    for i in posicao:
                        del self.board.coord_pos[i]

        return actions
        pass
    
    def get_key(self,my_dict,val):
        for key, value in my_dict.items():
            if val == value:
                return key

    def old_actions(self, state: TakuzuState):
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
        # TODO
        # #print(actions)
        return actions
        pass

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        board = deepcopy(state.board)

         #print("\nantes:")
         #print(board.board_lst)
         #print((action[0],action[1],action[2]))
        board.board_lst[action[0]][action[1]] = action[2]
         #print("\ndepois:")
         #print(board.board_lst)

        size = len(board.board_lst)

        str_list = list(board.board_str)
        str_list[action[0]*2*size+action[1]*2] = str(action[2])
        new_board_str="".join(str_list)
        board.board_str = new_board_str

        state.board = board

        return TakuzuState(board)
        pass

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        size = len(state.board.board_lst)
         #print("BOARD_LIST(to_str): \n",state.board)
         #print("board string : \n",list(state.board.board_str))
         #print("BOARD_LIST: ",state.board.board_lst)

        col_list = []
        for a in range(0,size):
            col_list_aux = []
            for b in range(0,size):
                
                col_list_aux.append(state.board.board_lst[b][a])
                

                if int(state.board.board_lst[a][b]) == 2:
                     #print("POsicao Vazia\n")
                     #print(state.board,"\n")

                    return False
                
                if (state.board.possible_actions(a,b,int(state.board.board_lst[a][b])) == None):
                     #print("posicao:",a,b)
                     #print(state.board.board_lst,"\n")
                     #print(state.board)
                     #print("coord pos:\n",state.board.coord_pos)
                    #exit()
                     #print("PA: ",state.board.possible_actions(a,b,int(state.board.board_lst[a][b])))
                    return False

            col_list.append(col_list_aux)

         #print("COL LIST: ",col_list)

        dup_free = []
        dup_free_set = set()
        for x in col_list:
            if tuple(x) not in dup_free_set:
                dup_free.append(x)
                dup_free_set.add(tuple(x))
        if (len(dup_free) != len(col_list)):
            return False

        dup_free = []
        dup_free_set = set()
        for x in state.board.board_lst:
            if tuple(x) not in dup_free_set:
                dup_free.append(x)
                dup_free_set.add(tuple(x))
        if (len(dup_free) != len(state.board.board_lst)):
            return False
                
        return True
                
                        
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        n = len(self.board.board_lst)

        count = 0

        for a in range(0,n):
            for b in range(0,n):
                if self.board.adjacent_horizontal_numbers(a,b) in ((0,0),(1,1)):
                    count += 0
                if self.board.adjacent_vertical_numbers(a,b) in ((0,0),(1,1)):
                    count += 0
                if self.board.adjacent_horizontal_numbers(a,b) in ((0,1),(1,0)):
                    count += 2
                if self.board.adjacent_vertical_numbers(a,b) in ((0,1),(1,0)):
                    count += 2
                if self.board.adjacent_horizontal_numbers(a,b) in ((2,1),(1,2),(2,0),(0,2)):
                    count += 10
                if self.board.adjacent_vertical_numbers(a,b) in ((2,1),(1,2),(2,0),(0,2)):
                    count += 10
                if self.board.adjacent_horizontal_numbers(a,b) in ((None,1),(1,None),(None,0),(0,None)):
                    count += 20
                if self.board.adjacent_vertical_numbers(a,b) in ((None,1),(1,None),(None,0),(0,None)):
                    count += 20
                if self.board.adjacent_horizontal_numbers(a,b) in ((None,2),(2,None),(2,2)):
                    count += 50
                if self.board.adjacent_vertical_numbers(a,b) in ((None,2),(2,None),(2,2)):
                    count += 50
                if (int(self.board.board_lst[a][b]) == 2):
                    count +=5
        
        return count
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    
    #board = Board.parse_instance_from_stdin()
    #board.get_number(1,1)

    exemplo = 4

    if (exemplo == 1):
        board = Board.parse_instance_from_stdin()
         #print("Initial:\n", board, sep="")
        # Imprimir valores adjacentes
         #print(board.adjacent_vertical_numbers(3, 3))
         #print(board.adjacent_horizontal_numbers(3, 3))
         #print(board.adjacent_vertical_numbers(1, 1))
         #print(board.adjacent_horizontal_numbers(1, 1))
    
    if (exemplo == 2):
        board = Board.parse_instance_from_stdin()
         #print("Initial:\n", board, sep="")
        # Criar uma instância de Takuzu:
        problem = Takuzu(board)
        # Criar um estado com a configuração inicial:
        initial_state = TakuzuState(board)

        

        # Mostrar valor na posição (2, 2):
         #print(initial_state.board.get_number(2, 2))
        # Realizar acção de inserir o número 1 na posição linha 2 e coluna 2
        result_state = problem.result(initial_state, (2, 2, 1))
        # Mostrar valor na posição (2, 2):
         #print(result_state.board.get_number(2, 2))
    
    if (exemplo == 3):
        board = Board.parse_instance_from_stdin()
        # Criar uma instância de Takuzu:
        problem = Takuzu(board)
        # Criar um estado com a configuração inicial:
        s0 = TakuzuState(board)
         #print("Initial:\n", s0.board, sep="")
        # Aplicar as ações que resolvem a instância
        s1 = problem.result(s0, (0, 0, 0))
        s2 = problem.result(s1, (0, 2, 1))
        s3 = problem.result(s2, (1, 0, 1))
        s4 = problem.result(s3, (1, 1, 0))
        s5 = problem.result(s4, (1, 3, 1))
        s6 = problem.result(s5, (2, 0, 0))
        s7 = problem.result(s6, (2, 2, 1))
        s8 = problem.result(s7, (2, 3, 1))
        s9 = problem.result(s8, (3, 2, 0))
        # Verificar se foi atingida a solução
         #print("Is goal?", problem.goal_test(s9))
         #print("Solution:\n", s9.board, sep="")
    
    if (exemplo == 4):
        board = Board.parse_instance_from_stdin()

        board.board_attibutes_setup()

        # Criar uma instância de Takuzu:
        problem = Takuzu(board)

        # Obter o nó solução usando a procura em profundidade:
        goal_node = depth_first_tree_search(problem)
        
         #print(goal_node)
        # Verificar se foi atingida a solução
        # #print("Is goal?", problem.goal_test(goal_node.state))
        # #print("Solution:\n", goal_node.state.board, sep="")

        # #print(type(None))

        problem.goal_test(goal_node.state)
        print(goal_node.state.board, end="")

    pass
