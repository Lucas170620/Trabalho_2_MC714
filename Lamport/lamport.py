import time
class Processo:
    def __init__(self,pulso):
        self.tempo_atual = 0 #C
        self.pulso = pulso

    def pulsar(self):
        self.tempo_atual = self.tempo_atual + self.pulso

    def atualiza_tempo_atual(self, tsm):

        self.tempo_atual = max(self.tempo_atual,tsm) #Cj <- max{Cj,ts(m)}

class Contador:
    def __init__(self):
        self.valor = 0
        self.incc = 1

    def contar(self):
        self.valor = self.valor + self.incc

    def reverter(self):
        if self.incc == 1:
            self.incc = -1
        else:
            self.incc = 1

class Lamport:

    def run(self):
        #Usando processos de exemplos dos slides da aula
        p1 = Processo(6)
        p2 = Processo(8)
        p3 = Processo(10)
        processos = [p1,p2,p3]
        contador = Contador()
        tsm = -1 #defini tsm = -1 para representar que não tem nenhuma mensagem montada
        auxiliar = 0
        print("=============")
        print("==iniciando==")
        print("=============")
        print("P1  P2  P3")
        print("{}  {}  {}".format(processos[0].tempo_atual,processos[1].tempo_atual,processos[2].tempo_atual))
        while True:
            for processo in processos:
                #todo inicio pulsa
                processo.pulsar()

            if auxiliar == 1:
                # no exemplo dos slides tem um lead time entre troca de mensagens quando inverte a troca de mensagens,
                # Esse if representa esse lead time
                print("{}  {}  {}".format(processos[0].tempo_atual, processos[1].tempo_atual, processos[2].tempo_atual))
                auxiliar = 0
                continue

            if tsm < 0: #verifica se te uma mensagem montada
                tsm = processos[contador.valor].tempo_atual
                contador.contar()
            else: # se tiver uma mensagem montada ele atualiza
                processos[contador.valor].atualiza_tempo_atual(tsm+1)
                tsm = -1

            if (contador.valor == 2 or contador.valor == 0) and tsm < 0:
                #Esse if verifica se ta nos extremos dos processos e se tem uma mensagem montada
                # se ta no extremo e não tem mensagem montado o processo vai mandar mensagem de volta
                contador.reverter()
                auxiliar = 1
            print("{}  {}  {}".format(processos[0].tempo_atual, processos[1].tempo_atual, processos[2].tempo_atual))

            time.sleep(1)





if __name__ == '__main__':
    Lamport().run()


