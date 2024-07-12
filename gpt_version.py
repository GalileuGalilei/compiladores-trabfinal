class GramaticaRegular:
    def __init__(self, arquivo_gramatica):
        self.simbolo_inicial = ''
        self.terminais = set()
        self.nao_terminais = set()
        self.regras = {}
        self.ler_gramatica(arquivo_gramatica)
        self.verificar_gramatica_linear_a_direita()

    def ler_gramatica(self, arquivo_gramatica):
        with open(arquivo_gramatica, 'r') as file:
            linhas = file.readlines()
            self.simbolo_inicial = linhas[0].strip()
            self.terminais = set(linhas[1].strip().split())
            self.nao_terminais = set(linhas[2].strip().split())
            for linha in linhas[3:]:
                esquerda, direita = linha.split('->')
                esquerda = esquerda.strip()
                direitas = [prod.strip() for prod in direita.split('|')]
                if esquerda not in self.regras:
                    self.regras[esquerda] = []
                self.regras[esquerda].extend(direitas)

    def verificar_gramatica_linear_a_direita(self):
        for cabeca, producoes in self.regras.items():
            for producao in producoes:
                if producao != 'ε' and not (producao[-1] in self.nao_terminais or producao[-1] in self.terminais):
                    raise ValueError("A gramática não é linear à direita")

    def pertence_gramatica(self, palavra):
        return self.analise_bottom_up(palavra)

    def analise_bottom_up(self, palavra):
        n = len(palavra)
        tabela = [set() for _ in range(n + 1)]
        tabela[0].add(self.simbolo_inicial)
        
        passos = []

        for i in range(n):
            for cabeca, producoes in self.regras.items():
                for producao in producoes:
                    if len(producao) == 1 and producao in self.terminais and producao == palavra[i]:
                        tabela[i + 1].add(cabeca)
                        passos.append(f'{cabeca} -> {producao}')

            for j in range(i + 1):
                for cabeca, producoes in self.regras.items():
                    for producao in producoes:
                        if len(producao) == 2 and producao[0] in tabela[j] and producao[1] == palavra[j:i + 1]:
                            tabela[i + 1].add(cabeca)
                            passos.append(f'{cabeca} -> {producao[0]}{producao[1]}')

        print('Passos de derivação:')
        for passo in passos:
            print(passo)

        return self.simbolo_inicial in tabela[n]

# Leitura da gramática a partir do arquivo
arquivo_gramatica = 'grammar.txt'
gramatica = GramaticaRegular(arquivo_gramatica)

# Receber a palavra do usuário
palavra = input('Digite a palavra a ser verificada: ')
if gramatica.pertence_gramatica(palavra):
    print(f'A palavra "{palavra}" pertence à gramática.')
else:
    print(f'A palavra "{palavra}" não pertence à gramática.')
