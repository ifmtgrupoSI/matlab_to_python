import numpy as np
from scipy import spatial
import matplotlib.pylab as plt

LINE_START = 10000
LINE_END = 39999
COLUMN = 2


'''
Função utilizada para recortar uma determinada coluna de um arquivo.
ARGUMENTOS => O primeiro argumento é o nome do arquivo,
              o segundo, o indice da coluna (contando a partir de 0). 
RETORNO => A função retorna uma lista que contem os valores (convertido para float) da respectiva coluna.

!!! extraordinariamente, a função trabalha somente com as linhas delimitadas por LINE_START e LINE_END.
'''
###############
def CutColumn(name_file, column):
    column_list = []
    line_number = 0
    with open(name_file, 'r') as file:
        for line in file:             
            line_number += 1
            if line_number < LINE_START:
                continue
            if line_number > LINE_END:
                break
            column_list.append(float(line.split()[column].replace(',', '.')))
    file.close()
    return column_list
###############


###############
def format_coord(x, y):
    col = int(x + 0.5)
    row = int(y + 0.5)
    if col >= 0 and col < numcols and row >= 0 and row < numrows:
        z = H1[row, col]
        return 'x=%1.4f, y=%1.4f, z=%1.4f' % (x, y, z)
    else:
        return 'x=%1.4f, y=%1.4f' % (x, y)
###############

file_no_damage = 'Imp_b_1Sensor1_3.lvm'
file_damage = []
file_damage.append('Imp_d1_1_1Sensor1_1.lvm')
file_damage.append('Imp_d1_1_1Sensor1_2.lvm')
file_damage.append('Imp_d1_1_1Sensor1_3.lvm')
file_damage.append('Imp_d1_1_1Sensor1_4.lvm')
file_damage.append('Imp_d1_1_1Sensor1_5.lvm')
file_damage.append('Imp_d1_1_1Sensor1_6.lvm')
file_damage.append('Imp_d1_1_1Sensor1_7.lvm')
file_damage.append('Imp_d1_1_1Sensor1_8.lvm')
file_damage.append('Imp_d1_1_1Sensor1_9.lvm')
file_damage.append('Imp_d1_1_1Sensor1_10.lvm')

#Cria a matriz com os valores da placa integra 
column_list = CutColumn(file_no_damage, COLUMN)
matriz_no_damage = np.reshape(column_list, (3000,10),order='F')

#Cria a matriz da placa com dano e em seguida a imagem para cada arquivo da placa com dano
for current_file_name in file_damage:
    print('Generating image from file', current_file_name)
    column_list = CutColumn(current_file_name, COLUMN)                       
    matriz_damage = np.reshape(column_list, (3000,10),order='F')             
    matriz_final = np.hstack((matriz_no_damage, matriz_damage))          

    A_1 = spatial.distance.pdist(matriz_final.transpose(),'minkowski') 
    Z_1 = spatial.distance.squareform(A_1)    
    size = 1
    for dim in np.shape(Z_1):
        size *= dim
    aux = np.reshape(Z_1, (size,1))
    H1 = Z_1/max(aux)                         

    fig, ax = plt.subplots()
    ax.imshow(H1, interpolation='nearest')
    numrows, numcols = H1.shape
        
    ax.format_coord = format_coord
    plt.savefig(str(current_file_name).replace('lvm','png'))
    plt.close()