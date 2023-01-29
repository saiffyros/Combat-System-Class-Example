define a = Character('', color="#c8ffc8")

init python:
    from enum import Enum

    class Manobras(Enum):
        ATAQUE = 1
        CURA = 2
        ESPERAR = 3

##########################################################

    class player:
        def __init__(self, name):
            self.name = name
            self.vida = 100
            self.max_vida = 100
            self.ataques = []
            self.armadura = 15

##########################################################

    class Ataque:
        def __init__(self, name, dano, tipo, bonus_ataque, description):
            self.name = name
            self.dano = dano
            self.tipo = tipo
            self.bonus_ataque = bonus_ataque
            self.description = description

##########################################################

    class Monster:
        def __init__(self, name, vida, dano, armadura, bonus_ataque):
            self.name = name
            self.vida = vida
            self.max_vida = vida
            self.dano = dano
            self.armadura = armadura
            self.bonus_ataque = bonus_ataque

###########################################################

    class Batalha:
        def __init__(self, jogador, monstro):
            self.jogador = jogador
            self.monstro = monstro
            self.manobra_escolhida = None

        def battle(self):

            renpy.show_screen("lutadores", hero = self.jogador, enemy = self.monstro)

            while(self.monstro.vida > 0 or self.jogador.vida > 0):

                renpy.call_screen("stats")

                if self.manobra_escolhida.tipo == Manobras.ATAQUE:
                    renpy.say(a, "Você ataca " + self.monstro.name + " com " + self.manobra_escolhida.description + ".")
                    rolagem_dado_jogador = renpy.random.randint(0, 20)
                    renpy.say(a, "Você tirou um " + str(rolagem_dado_jogador) + " no dado e possui bônus de ataque de +" + str(self.manobra_escolhida.bonus_ataque) + ", totalizando: " + str(rolagem_dado_jogador + self.manobra_escolhida.bonus_ataque) + " e a armadura do inimigo é: " + str(self.monstro.armadura) + ".")
                    if rolagem_dado_jogador + self.manobra_escolhida.bonus_ataque < self.monstro.armadura:
                        renpy.say(a, self.monstro.name + " esquivou do seu ataque.")
                    else:
                        self.monstro.vida -= self.manobra_escolhida.dano
                        renpy.say(a, "Você causa " + str(self.manobra_escolhida.dano) + " de dano no " + self.monstro.name + ".")

                if self.manobra_escolhida.tipo == Manobras.CURA:
                    renpy.say(a, "Você usa uma magia de " + self.manobra_escolhida.description + ".")
                    self.jogador.vida += self.manobra_escolhida.dano
                    if self.jogador.vida > self.jogador.max_vida:
                        self.jogador.vida = self.jogador.max_vida
                    renpy.say(a, "Você recuperou " + str(self.manobra_escolhida.dano) + " pts de vida.")

                if self.manobra_escolhida.tipo == Manobras.ESPERAR:
                    renpy.say(a, "Você não faz nada neste turno.")
                    renpy.pause(1)

                if self.monstro.vida <= 0:
                    renpy.say(a, self.monstro.name + " foi derrotado.")
                    store.vitoria = True
                    break

                renpy.say(a, self.monstro.name + " tenta atacar você.")

                rolagem_dado_monstro = renpy.random.randint(0, 20)
                
                renpy.say(a, self.monstro.name + " tirou um " + str(rolagem_dado_monstro) + " no dado e possui bônus de ataque de +" + str(self.monstro.bonus_ataque) + ", totalizando: " + str(rolagem_dado_monstro + self.monstro.bonus_ataque) + " e sua armadura é: " + str(self.jogador.armadura) + ".")

                if rolagem_dado_monstro + self.monstro.bonus_ataque <= self.jogador.armadura:
                    renpy.say(a, "Você consequiu esquivar.")

                else:
                    self.jogador.vida -= self.monstro.dano
                    renpy.say(a, "Você tem " + str(self.jogador.vida) + " pontos de vida.")

                    if self.jogador.vida <= 0:
                        renpy.say(a, "Você morreu")
                        store.vitoria = False
                        break

label start:
    default vitoria = None
    default enemy = Monster("Lobo", 60, 23, 12, 5)
    default hero = player("Roger")
    default ataque_simples = Ataque("Ataque Simples", 30, Manobras.ATAQUE, 5, "punhos" )
    default magia_cura = Ataque("Cura Simples", 5, Manobras.CURA, 0, "Magia de Cura")
    default magia_cura_2 = Ataque("Cura", 10, Manobras.CURA, 0, "Magia de Cura reforçada")
    default magia_fogo = Ataque("Bola de Fogo", 40, Manobras.ATAQUE, 10, "bola de fogo")
    default esperar = Ataque("Esperar", 0, Manobras.ESPERAR, 0, "Aguardar")

    $ hero.ataques = [ataque_simples, magia_cura, magia_cura_2, magia_fogo, esperar]

    #default batalha = Batalha(hero, Monster("Lobo", 60, 23, 12, 5))
    default batalha = Batalha(hero, enemy)

    "Vamos lutar!"

    $ batalha.battle()

    if vitoria == True:
        "Você venceu a batalha."
    else:
        "Você perdeu a batalha."

    "Fim"

    return

screen stats:
    frame:
        xalign 0.5
        yalign 0.65

        vbox:
            for ataque in hero.ataques:
                textbutton ataque.name action SetVariable("batalha.manobra_escolhida", ataque), Return()

screen lutadores(hero, enemy):
    frame:
        xalign 0.01 yalign 0.05
        vbox:
            text hero.name size 22 xalign 0.5
            null height 5
            hbox:
                bar:
                    xmaximum hero.max_vida
                    value hero.vida
                    range hero.max_vida
                    left_gutter 0
                    right_gutter 0
                    thumb None
                    thumb_shadow None

                null width 5

            text "[hero.vida] / [hero.max_vida]" size 10

    frame:
        xalign 0.9 yalign 0.05
        vbox:
            text enemy.name size 22 xalign 0.5
            null height 5
            hbox:
                bar:
                    xmaximum enemy.max_vida
                    value enemy.vida
                    range enemy.max_vida
                    left_gutter 0
                    right_gutter 0
                    thumb None
                    thumb_shadow None

                null width 5

            text "[enemy.vida] / [enemy.max_vida]" size 10
