import random
import time
class Processo:
    def __init__(self,indice,lider):
        self.indice = indice
        self.disponivel = True
        self.lider = lider

    def montar_mensagem(self,candidatos):
        candidatos.append(self.indice)
        print("{} candidatado".format(self.indice))
        time.sleep(1.5)
        return candidatos

    def indisponibilidade(self):
        self.disponivel = False
        self.lider = False

    def disponibilidade(self):
        self.disponivel = True

    def novo_lider(self):
        self.lider = True



class Eleicao:

    def verificar_lider_ativo(self):
        for processo in self.processos:
            if processo.lider and processo.disponivel:
                return processo.indice
        return -1

    def convocar_eleicao(self):
        candidatos = []
        for processo in self.processos:
            if processo.disponivel:
                candidatos = processo.montar_mensagem(candidatos)
        if candidatos == []:
            return -1
        return max(candidatos)


    def run(self):
        p1 = Processo(1,False)
        p2 = Processo(2,False)
        p3 = Processo(3, False)
        p4 = Processo(4, False)
        p5 = Processo(5, False)

        self.processos = [ p1,p2,p3,p4,p5]
        while True:
            for y in range(2):
                rand = random.randint(0,4)
                self.processos[rand].disponibilidade()
            for x in range(2):
                rand = random.randint(0,4)
                self.processos[rand].indisponibilidade()


            lider = self.verificar_lider_ativo()
            if lider < 0:
                print("Sem Líder Disponível - Convocando novas Eleições")
                novo_líder = self.convocar_eleicao()
                for processo in self.processos:
                    if processo.indice == novo_líder and processo.disponivel:
                        print("{} é o novo líder".format(novo_líder))
                        processo.novo_lider()
                        break

            else:
                time.sleep(1.5)
                print("Líder {} Disponível".format(lider))






if __name__ == '__main__':
    Eleicao().run()