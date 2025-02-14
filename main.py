import numpy as np
from time import time
from Levenshtein import distance
from scipy.spatial.distance import cosine, euclidean, jaccard
from pprint import pprint

# Classe para processar palavras
class processar_palavra():
    def __init__(self, palavra):
        self.palavra = palavra
        self.tamanho = len(palavra)
        self.letras = set(palavra)

    def Att_palavra(self, palavra):
        self.palavra = palavra
        self.tamanho = len(palavra)
        self.letras = set(palavra)

    def Ajustar_Tam(self, palavra2) -> str:
        palavra1 = self.palavra
        tam_p1, tam_p2 = len(palavra1), len(palavra2)
        if tam_p1 > tam_p2:
            palavra2 = palavra2.ljust(tam_p1)
        elif tam_p2 > tam_p1:
            palavra1 = palavra1.ljust(tam_p2)
        else: 
            return palavra1, palavra2
        return palavra1, palavra2

    def filtrar_dados(self, prefixos, dados) -> list:
        palavra = self.palavra
        palavras1 = [plvr for plvr in dados
                        if len(plvr) <= (len(palavra)+2) and
                        len(plvr) > (len(palavra)-2) and 
                        len(set(plvr).intersection(set(palavra))) >= 2]

        palavras = [plvr for plvr in palavras1 for prf in prefixos if prf in plvr]
        return palavras

    @staticmethod
    def Converter_palavras(palavra) -> np.array:
        p_convertida = np.array([0 if c == ' ' else ord(c) for c in palavra])
        return p_convertida

    def Distancia_Levenshtein(self, palavra2) -> int:
        distancia = distance(self.palavra, palavra2)
        return distancia

    def Distancia_Euclidiana(self, palavra2) -> int:
        palavra1, palavra2 = self.Ajustar_Tam(palavra2)

        plvr1 = self.Converter_palavras(palavra1)
        plvr2 = self.Converter_palavras(palavra2)
        
        distancia = euclidean(plvr1, plvr2)
        return distancia

    def Distancia_Cosseno(self, palavra2) -> int:
        palavra1, palavra2 = self.Ajustar_Tam( palavra2)
        
        plvr1 = self.Converter_palavras(palavra1)
        plvr2 = self.Converter_palavras(palavra2)

        distancia = cosine(plvr1, plvr2)
        return distancia

    def Distancia_jaccad(self, palavra2) -> int:
        # encontrar a interseção e união
        plv1, plv2 = set(self.palavra), set(palavra2)
        intersecao = plv1.intersection(plv2)
        uniao = plv1.union(plv2)

        # determinando o numerador e denominador
        numerador = abs(len(intersecao))
        denominador = abs(len(uniao))

        # calculando a distancia jaccad
        dist = 1 - (numerador / denominador)
        return dist

    def Gerar_prefixos(self, n) -> list:
        palavra = self.palavra
        return [palavra[i:i + n] for i in range(self.tamanho - n + 1)]

    def Palavras_proximas(self, palavra2, distancia, lista, limite=5) -> list:
        """Adiciona uma palavra à lista se for única e mantém no máximo 'limite' elementos."""
        if distancia == 1:
            dist = self.Distancia_Levenshtein(palavra2)
        elif distancia == 2:
            dist = self.Distancia_Euclidiana(palavra2)
        elif distancia == 3:
            dist = self.Distancia_Cosseno(palavra2)
        elif distancia == 4:
            dist = self.Distancia_jaccad(palavra2)
        else:
            return """Opção de distância invalida:
                    Selecione entre:
                    [1] Distâcia de Edição 
                    [2] Distância Euclidiana
                    [3] Distância Cosseno
                    [4] Distância Jaccad"""

        # Criar estrutura de dicionário
        dados = {"Palavra": palavra2, "Distância": float(dist)}

        # Verificar se a palavra já existe na lista (independente da distância)
        palavras_existentes = {item["Palavra"] for item in lista}
        
        if palavra2 not in palavras_existentes:
            # Se a lista ainda tem espaço, adiciona a nova palavra
            if len(lista) < limite:
                lista.append(dados)
            else:
                # Encontrar a palavra com a maior distância na lista
                maior_dist = max(lista, key=lambda x: x["Distância"])
                
                # Substituir a de maior distância se a nova for melhor
                if dist < maior_dist["Distância"]:
                    lista.remove(maior_dist)
                    lista.append(dados)

        # Ordenar a lista pela distância para manter organização
        lista.sort(key=lambda x: x["Distância"])
        return lista

    def __repr__(self):
        return str({'Palavra': self.palavra, 'Tamanho': self.tamanho, 'Letras': self.letras})

def read_txt(caminho) -> list:
    with open(caminho, 'r', encoding='utf-8') as file:
        arquivo = [palavra.strip() for palavra in file]
    return arquivo

def main(palavra, distancia=1):
    caminho = "data/raw/palavras-br.txt"
    palavras = read_txt(caminho)

    tam = len(palavra) // 2
    p = processar_palavra(palavra)    

    prefixos = p.Gerar_prefixos(tam)
    palavras2 = p.filtrar_dados(prefixos, palavras)

    lista = []

    for plvr in palavras2:
        p.Palavras_proximas(plvr, distancia, lista)

    pprint(lista)

if '__main__' == __name__:
    """
    Opções de Distância disponiveis:
    [1] Distâcia de Edição 
    [2] Distância Euclidiana
    [3] Distância Cosseno
    [4] Distância Jaccard
    """
    inicio = time()
    palavras = ['condiaco', 'roblema', 'caus', 'facinado', 'modestis', 'perutava', 'estaquem', 'ignoraia', 'rsfriado', 'sevulo']

    for palavra in palavras:
        for distancia in range(1,5):
            print(f'Palavra teste {palavra}')
            # print(distancia)
            main(palavra ,distancia)

    fim  = time()
    print("Tempo de execução: ",fim - inicio)

    # Execução 0.5735607147216797 -> sem lib
    # Execução 0.5646066665649414 -> com lib