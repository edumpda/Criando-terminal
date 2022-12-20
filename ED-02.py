class Node:
    def __init__(self, dado):
        self.dado = dado
        self.tipo = 'nodo'
        self.path = []
        self.arquivos = {}

    def __str__(self):
        return str(self.dado)

    def inserir(self, nome):
        aux = Node(nome)
        aux.path = self.path + [self.dado]
        self.arquivos[nome] = aux#Node(nome)
        
    def inserir_arquivo(self, nome):
        aux = Arquivo(nome)
        aux.path = self.path + [self.dado]
        self.arquivos[nome] = aux#Node(nome)
        
class Arquivo:
    def __init__(self, dado):
        self.dado = dado
        self.tipo = 'arquivo'
    
    def __str__(self):
        return str(self.dado)
        
class Arvore:
    def __init__(self, root='/'):
        self.root = Node(root)
        self.caminhos = []
        self.noAtual = self.root
        self.tempo = None
        self.pathFull = ['/']
        self.pwd = ['/']

    def adiciona_referencia(self, destino, add, root='/'):
        if root == '/':
            root = self.root
        if len(destino)==0:
            root.arquivos[add.dado] = add
        else:
            return self.adiciona_referencia(destino[1:], add, root.arquivos[destino[0]])
        
    def exclui_referencia(self, destino, origem, remover, root='/'):
        if root == '/':
            root = self.root
        if len(origem)==0:
            add = root.arquivos.pop(remover)
            return self.adiciona_referencia(destino, add)
        else:
            return self.exclui_referencia(destino, origem[1:], remover, root.arquivos[origem[0]])       
    
    def formato(self, path):
        temp = self.pwd[:]
        k = path.count('..')
        for p in range(0, k):
            temp.pop()
            path.pop(0)
        for p in path:
            temp.append(p)
        return temp
            
    def mostra_pwd(self):
        if len(self.pwd) == 1:
            return print('/')
        a = '/'.join(self.pwd[1:])
        print('/'+a)
     
    def cd(self, path, root='/' ):
        if root == '/':
            root = self.root
        
        if len(path) == 0:
            self.noAtual = root
            self.pwd.append(root.dado)
            return self.noAtual
        
        try:
            if root.dado != '/':
                self.pwd.append(root.dado)
            return self.cd(path[1:], root.arquivos[path[0]])
        except KeyError:
            return False
    
    def mkdir(self, path, nome, root='/'):

        if root == '/':
            root = self.root

        if len(path)==0:
            #MV : Use as verificaçãos, o destino não pode ser um arquivo, e origem tem que existir == True
            #MV : Somente o return do try, pois ja foi feita a verificação
            #MV : aqui root.arquivos.pop(nome)
            #MV : Para adicionar vai ser como aqui, sem o nome if nome in blabla
            if nome in root.arquivos:
                return print('DIRETÓRIO JÁ EXISTE')
            return root.inserir(nome)
        else:
            try:
                return self.mkdir(path[1:], nome, root.arquivos[path[0]])
            except KeyError:
                root.inserir(path[0])
                return self.mkdir(path[1:], nome, root.arquivos[path[0]])    
    
    def touch(self, path, nome, root='/'):
        '''
        O mkdir cria um caminho quando não existe, já o touch fala q o caminho eh inválido.
        
        Ao invés de criar um nó como o mkdir, ele cria um arquivo da classe Arquivo
        ''' 
        if root == '/':
            root = self.root
        
        if len(path) == 0:
            if nome in root.arquivos:
                return print('ARQUIVO JÁ EXISTE')
            else:
                return root.inserir_arquivo(nome)
        else:
            try:
                return self.touch(path[1:], nome, root.arquivos[path[0]])
            except KeyError:
                return print('CAMINHO INVÁLIDO')

    def rm(self, path, nome, root='/'):
        
        if root == '/':
            root = self.root

        if len(path)==0:
            if nome not in root.arquivos:
                return print('ARQUIVO ou DIRETÓRIO não existe')
            if self.noAtual.dado == nome:
                self.noAtual = self.root
            self.tempo = root.arquivos.pop(nome)
            return 0
        
        else:
            try:
                return self.rm(path[1:], nome, root.arquivos[path[0]])
            except KeyError:
                self.tempo = root.arquivos.pop(path[0])
                return self.rm(path[1:], nome, root.arquivos[path[0]])
    
    def aux_find(self, var = False):
        if not var:
            caminho = '/'.join(self.caminhos[1:])
        else:
            caminho = '/'.join(self.caminhos[1:])
            return print(f'/{caminho}')
    
    def find(self, coord, root='/'):
        if self.tempo is None:
            self.tempo = self.root
        if root == '/':
            root = self.tempo
        self.caminhos.append(root.dado)
        try:
            c = root.arquivos.keys()
        except AttributeError:
            c = []
        for key in sorted(c):
            try:
                self.find(coord, root.arquivos[key])
            except AttributeError:
                if root.arquivos[c].dado == coord:
                    self.aux_find(var = True)
                    self.caminhos.pop()
        if root.dado == coord:
            self.aux_find(var = True)
            self.caminhos.pop()
        else:
            self.caminhos.pop()

    def show(self, root='/', level=0):
        if root == '/':
            root = self.root

        print(f'{"---" * level}{root.dado}')

        for child in sorted(root.arquivos):
            try:
                self.show(root.arquivos[child], level + 1)
            except AttributeError:
                continue
            
    def verificaCaminho(self, caminho, root = None):
        if root is None:
            root = self.root
        if len(caminho) == 0:
            return True
        else:
            try:
                return self.verificaCaminho(caminho[1:], root.arquivos[caminho[0]])
            except KeyError:
                return False
            
    def verificaType(self, caminho, root = None):
        #implementar para dir corrente
        if root is None:
            root = self.root
        if len(caminho) == 0:
            if root.tipo == 'arquivo':
                return True
            else:
                return False
        else:
            try:
                return self.verificaType(caminho[1:], root.arquivos[caminho[0]])
            except KeyError:
                return False

estrutura = Arvore()
while True:
    comando = input().split(maxsplit=1)

    if comando[0] == 'cd':
        if not comando[1] == '/':            
            if '..' in comando[1]:
                path = estrutura.formato(comando[1].split('/'))
            else:
                path = comando[1].split('/')
            if not path == ['.']:
                if path[0] == '.':
                    estrutura.pwd = ['/']
                    estrutura.cd(path[1:], estrutura.noAtual)
                else:
                    if estrutura.verificaCaminho(path[1:]):
                        if not estrutura.verificaType(path[1]):
                            estrutura.pwd = ['/']
                            estrutura.cd(path[1:])
                        else:
                            print('COMANDO INVÁLIDO')
                    else:
                        print('CAMINHO INVÁLIDO')
        else:
            estrutura.pwd = ['/']
        
    elif comando[0] == 'pwd':
        estrutura.mostra_pwd()

    elif comando[0] == 'mkdir':
        if comando[1] == '/':
            print('DIRETÓRIO JÁ EXISTE')
        path = comando[1].split('/')
        estrutura.mkdir(path[1:-1], path[-1])

    elif comando[0] == 'mv':
#MV : Use as verificaçãos, o destino não pode ser um arquivo, e origem tem que existir == True
        caminhos = comando[1].split()
        if '..' in caminhos[0]:
            path1 = estrutura.formato(caminhos[0].split('/'))
        else:
            path1 = caminhos[0].split('/')
        if '..' in caminhos[1]:
            path2 = estrutura.formato(caminhos[1].split('/'))
        else:
            path2 = caminhos[1].split('/')
        if path1[0] == '.':
            estrutura.exclui_referencia(path2[1:], path1[1:-1], path[-1], estrutura.noAtual)
        #modificar para checagem do tamanho
        if caminhos[0] != '/' and caminhos[1] != '/':
            origem = caminhos[0].split('/')
            destino = caminhos[1].split('/')
            if estrutura.verificaCaminho(origem[1:-1]):
                if estrutura.verificaCaminho(destino[1:-1]):
                    if estrutura.verificaCaminho(origem[1:]):
                        estrutura.exclui_referencia(destino[1:], origem[1:-1], origem[-1])
                        #estrutura.adiciona_referencia(destino[1:], origem[-1])
                    else:
                        print('ARQUIVO ou DIRETÓRIO não existe')
                else:
                    print('CAMINHO INVÁLIDO')
            else:
                print('CAMINHO INVÁLIDO')

    elif comando[0] == 'touch':
        if '..' in comando[1]:
            path = estrutura.formato(comando[1].split('/'))
        else:
            path = comando[1].split('/')
        if path[0] == '.':
            estrutura.touch(path[1:-1], path[-1], estrutura.noAtual)
        else:
            if path[1:] == []:
                estrutura.touch(path[1:-1], path[-1])
            else:    
                if estrutura.verificaCaminho(path[1:-1]):
                    if estrutura.verificaType(path[1:]):
                        estrutura.touch(path[1:-1], path[-1])
                    else:
                        if not estrutura.verificaCaminho(path[1:]):
                            estrutura.touch(path[1:-1], path[-1])
                        else:
                            print('CAMINHO INVÁLIDO')
                else:
                    print('CAMINHO INVÁLIDO')
    
    elif comando[0] == 'show':
        estrutura.show()
        
    elif comando[0] == 'rm':
        if '..' in comando[1]:
            path = estrutura.formato(comando[1].split('/'))
        else:
            path = comando[1].split('/')
        if path[0] == '.':
            estrutura.rm(path[1:-1], path[-1], estrutura.noAtual)
        if path != '/':
            estrutura.rm(path[1:-1], path[-1])
        
    elif comando[0] == 'find':
        path = comando[1].split('/')
        estrutura.find(path[-1])
    
    else:
        break





