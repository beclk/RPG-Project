import time
import os

def limpar_tela():
    os.system('cls')

class Ser:
    def __init__(self, nome, vida, dano, nivel=1):
        self.nome = nome
        self.vida = vida
        self.dano = dano
        self.nivel = nivel

    def atk(self, alvo):
        # Polimorfismo: o método 'atk' vai ser sobrescrito nas classes filhas (Personagem e Monstro)
        pass

    def atacado(self, dano):
        self.vida -= dano
        print(f'{self.nome} agora tem {self.vida} de vida.')


class Personagem(Ser):
    def __init__(self, nome, vida, dano, nivel=1):
        super().__init__(nome, vida, dano, nivel)
        self.nome_do_item = None
        self.item = []

    def atk(self, monstro):
        # Polimorfismo: o método atk é implementado para o Personagem
        monstro.vida -= self.dano
        print(f'{self.nome} desferiu {self.dano} de dano em {monstro.nome}.')
        if monstro.vida < 0:
            monstro.vida = 0
        print(f'{monstro.nome} agora tem {monstro.vida} pontos de vida.')

    def cura(self):
        self.vida += 20
        print(f'{self.nome} se curou, agora possui {self.vida} de vida.')

    def pegar(self, item):
        # Associação: o jogador pega um item
        self.item.append(item)
        print(f'{self.nome} pegou o item {item.nome}')

    def status(self):
        print(f'{self.nome}: Vida={self.vida}, Dano={self.dano}, Nível={self.nivel}')
        print(f'Há {self.item} no inventário de {self.nome}')


class Monstro(Ser):
    def __init__(self, nome, vida, dano, item, nivel=1):
        super().__init__(nome, vida, dano, nivel)
        self.item = item  # Associação: o monstro tem um item que pode ser dropado

    def atk(self, jogador):
        # Polimorfismo: o método atk é implementado para o Monstro
        jogador.vida -= self.dano
        print(f'{self.nome} desferiu {self.dano} de dano em {jogador.nome}.')
        if jogador.vida < 0:
            jogador.vida = 0
        print(f'{jogador.nome} agora tem {jogador.vida} pontos de vida.')

    def drop(self):
        # O monstro solta o item quando morre
        print(f'{self.nome} largou o item {self.item.nome}.')
        return self.item


class Item:
    def __init__(self, nome, tipo, efeito):
        self.nome = nome
        self.tipo = tipo
        self.efeito = efeito

    def buff(self, personagem):
        # 'Usar item' - A aplicação de buff do item no personagem
        if self.tipo == 'cura':
            personagem.vida += self.efeito
            print(f'{personagem.nome} usou {self.nome} e agora tem {personagem.vida} de vida.')
        elif self.tipo == 'ataque':
            personagem.dano += self.efeito
            print(f'{personagem.nome} usou {self.nome} e agora causa {personagem.dano} de dano.')
        else:
            print('Tipo de item inválido.')


class Missao:
    def __init__(self, nome, monstro, item, estado=0):
        self.estado = estado
        self.monstro = monstro
        self.item = item
        self.nome = nome

    def comecar(self, jogador):
        # Associação: jogador e monstro estão associados à missão
        self.estado = 1
        print(f'Missão {self.nome} iniciada. Objetivo: Derrotar {self.monstro.nome}.')
        while jogador.vida > 0 and self.monstro.vida > 0:
            opcoes = int(input('Atacar(1); Curar(2); Fugir(3): '))
            if opcoes == 1:
                jogador.atk(self.monstro)
                if self.monstro.vida > 0:
                    self.monstro.atk(jogador)
                else:
                    self.terminar(jogador)
            elif opcoes == 2:
                jogador.cura()
            elif opcoes == 3:
                print(f'{jogador.nome} fugiu da missão.')
                break
            else:
                print('Opção inválida.')

    def terminar(self, jogador):
        self.estado = 2
        print('Missão concluída.')
        item = self.monstro.drop()
        jogador.pegar(item)  # O jogador pega o item do monstro
        item.buff(jogador)
        #jogador.nivel += 1

    def fugir(self):
        # foge do monstro
        menu()


class NPC:
    def __init__(self, nome, mensagem):
        self.nome = nome
        self.mensagem = mensagem

    def falar(self):
        print(f'{self.nome} diz: "{self.mensagem}"')


def criar_personagem():
    nome = input("Informe o nome do seu personagem: ")
    personagem = Personagem(nome, 50, 30)
    print(f'Personagem {personagem.nome} criado com sucesso!')
    time.sleep(1)
    limpar_tela()
    return personagem

def menu():
    print("\n=== Menu do Jogo ===")
    print("1. Criar personagem")
    print("2. Iniciar missão")
    print("3. Status do personagem")
    print("4. Sair")
    escolha = int(input("Escolha uma opção: "))
    return escolha


def escolher_monstro():
    print("\nEscolha o monstro para enfrentar:")
    print("1. Gárgula (Vida: 50, Dano: 25)")
    print("2. Dragão (Vida: 100, Dano: 40)")
    escolha = int(input("Escolha o número do monstro: (1) ou (2) "))

    if escolha == 1:
        item = Item('Cajado', 'ataque', 10)
        monstro = Monstro('Gárgula', 50, 25, item)
        return monstro, item
    elif escolha == 2:
        item = Item('Escudo', 'cura', 20)
        monstro = Monstro('Dragão', 100, 40, item)
        return monstro, item
    else:
        print("Opção inválida. Escolha o número correto.")
        return escolher_monstro()


def jogar():
    personagem = None
    npc = NPC("Guarda", "Bem-vindo ao nosso reino! Há monstros poderosos à sua frente, escolha com sabedoria.")

    while True:
        escolha = menu()

        if escolha == 1:
            personagem = criar_personagem()
        elif escolha == 2:
            if personagem is None:
                print("Você precisa criar um personagem primeiro!")
                continue

            npc.falar()  # O NPC fala com o jogador

            # Escolher um monstro para enfrentar
            monstro, item = escolher_monstro()

            # Iniciar missão
            missao = Missao('Caverna', monstro, item)
            missao.comecar(personagem)

        elif escolha == 3:
            if personagem is None:
                print("Você precisa criar um personagem primeiro!")
                continue
            Personagem.status(personagem)

        elif escolha == 4:
            print("Saindo do jogo...")
            break
        else:
            print("Opção inválida, tente novamente.")

# Iniciar o jogo
jogar()