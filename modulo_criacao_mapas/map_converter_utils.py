from PIL import Image
import numpy as np

def retornaPrctCombust(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def converter_mapa(arquivo_entrada, arquivo_saida_base):
    """
    Converte um arquivo de imagem em três arquivos de mapa (.map, _fogo.map, _vento.map).
    arquivo_entrada: caminho do PNG de entrada
    arquivo_saida_base: caminho base para os arquivos de saída (sem extensão)
    """
    im = Image.open(arquivo_entrada)
    im2arr = np.array(im)

    # Mapa estático de distâncias
    with open(arquivo_saida_base + ".map", "w") as arq_out:
        for r in range(0, im2arr.shape[0]):
            for c in range(0, im2arr.shape[1]):
                if im2arr[r][c][0] == 0 and im2arr[r][c][1] == 0 and im2arr[r][c][2] == 0:
                    arq_out.write('1')
                elif im2arr[r][c][0] == 255 and im2arr[r][c][1] == 0 and im2arr[r][c][2] == 0:
                    arq_out.write('2')
                elif im2arr[r][c][0] == 255 and im2arr[r][c][1] == 255 and im2arr[r][c][2] == 255:
                    arq_out.write('0')
                elif im2arr[r][c][0] == 255 and im2arr[r][c][1] == 165 and im2arr[r][c][2] == 0:
                    arq_out.write('9')
                elif im2arr[r][c][0] == 255 and im2arr[r][c][1] == 166 and im2arr[r][c][2] == 0:
                    arq_out.write('9')
                elif im2arr[r][c][0] == 0 and im2arr[r][c][1] == 255 and im2arr[r][c][2] == 0:
                    arq_out.write('7')
                elif im2arr[r][c][0] == 0 and im2arr[r][c][1] == 0:
                    arq_out.write('0')
                else:
                    arq_out.write('8')
            arq_out.write('\n')

    # Mapa de fogo fixo
    with open(arquivo_saida_base + "_fogo.map", "w") as arq_out:
        for r in range(0, im2arr.shape[0]):
            for c in range(0, im2arr.shape[1]):
                if im2arr[r][c][0] == 0 and im2arr[r][c][1] == 0 and im2arr[r][c][2] == 0:
                    arq_out.write('0')
                elif im2arr[r][c][0] == 255 and im2arr[r][c][1] == 0 and im2arr[r][c][2] == 0:
                    arq_out.write('0')
                elif im2arr[r][c][0] == 255 and im2arr[r][c][1] == 255 and im2arr[r][c][2] == 255:
                    arq_out.write('1')
                elif im2arr[r][c][0] == 0 and im2arr[r][c][1] == 255 and im2arr[r][c][2] == 0:
                    arq_out.write('1')
                elif im2arr[r][c][0] == 0 and im2arr[r][c][1] == 0:
                    arq_out.write(str(int(retornaPrctCombust(im2arr[r][c][2], 1, 255, 0, 8))))
                else:
                    arq_out.write('1')
            arq_out.write('\n')

    # Mapa de vento fixo
    with open(arquivo_saida_base + "_vento.map", "w") as arq_out:
        for r in range(0, im2arr.shape[0]):
            for c in range(0, im2arr.shape[1]):
                if im2arr[r][c][0] == 0 and im2arr[r][c][1] == 0 and im2arr[r][c][2] == 0:
                    arq_out.write('0')
                elif im2arr[r][c][0] == 255 and im2arr[r][c][1] == 0 and im2arr[r][c][2] == 0:
                    arq_out.write('1')
                elif im2arr[r][c][0] == 255 and im2arr[r][c][1] == 255 and im2arr[r][c][2] == 255:
                    arq_out.write('1')
                else:
                    arq_out.write('1')
            arq_out.write('\n') 