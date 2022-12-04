# -*- coding: utf-8 -*-
import  time 
from random import randint
from threading import Thread


class Processo ():

    def __init__(self, id):
        self.id = id
        self.tag = ' Número do processo {}\n'.format(self.id)
        self.coordenador = None
        self.isAtivo = True
        Thread(target=self.run_p).start()

    def run_p(self):
        print('{} Inicializado'.format(self.tag))
        print('{}'.format(self.tag))
        while self.isAtivo:
            self.consumir_recurso()
            time.sleep(randint(1,5))

    def set_coordenador(self, coordenador):
        self.coordenador = coordenador

    def set_ativo(self,ativo):
        self.isAtivo = ativo

    def stop(self):
        del self

    def __repr__(self):
        return str(self,__dict__)

    def consumir_recurso(self):
        coordenador = self.coordenador
        if coordenador is None:
            Processos().gera_novo_coordenador()
        elif coordenador is not None and self.id != self.coordenador.id:
            print('\n')
            print('{} Solicita acesso do recurso ao coordenador {}\n'.format(self.tag,coordenador.id) )
            
            if coordenador.isRecursoHabilitado == False:
                self.processa_recurso()
            else:
                coordenador.fila.append(self)
                print('!!!!!Fila de espera= {}!!!!!'.format(self.fila_coordenador(coordenador)))
                valida = True
                while valida:
                    if coordenador.isRecursoHabilitado == False and coordenador.fila[0].id == self.id:
                        self.processa_recurso()
                        valida = False

    def processa_recurso(self):
        coordenador = self.coordenador
        if coordenador is not None:
            print('---O cordenador de ID: {} concede acesso ao processo {}---'.format(coordenador.id,self.id) )
            print('Iniciado processo do recurso!'.format(self.tag))
            coordenador.isRecursoHabilitado = True
            sleep = randint(2,7)
            time.sleep(sleep)
            print(' {} Recursso processado em {} segundos!'.format(self.tag, sleep))
            print('@@@ O processo {} liberou recurso! @@@'.format(self.id))
            print('\n')
            coordenador.isRecursoHabilitado = False
            self.remover_fila(coordenador)
    
    def remover_fila(self,coordenador):
        for f in coordenador.fila:
            if f.id == self.id:
                coordenador.fila.remove(self)

    def fila_coordenador(self,coordenador):
        s=[]
        for f in coordenador.fila:
            s.append(f.id)
        return s

class Coordenador:

    def __init__(self,id):
        self.id = id
        self.isRecursoHabilitado = False
        self.fila = []

    def stop(self):
        del self

    def __repr__(self):
        return str(self,__dict__)

class Singleton:
    _intance = None

    @classmethod

    def instance(cls):
        if cls._intance is None:
            cls._intance = ()
        return cls._instance
    
class Processos(Singleton):
    processos = []

    def gera_processo(self):
        while (True):
            valida = False
            while valida == False:
                ran_id = randint(0,2048)
                valida =self.verifica_id_existente(ran_id)
            processo = Processo(ran_id)
            processo.set_coordenador(self.get_coordenador())
            self.processos.append(processo)
            time.sleep(10)


    def intativa_coordenador(self):
        while(True):
            time.sleep(30)
            if len(self.processos) > 0:
                coordenador = self.processos[0].coordenador
                if coordenador is not None:
                    id = coordenador.id
                    processo= self.retorna_processo(coordenador.id)
                    processo.set_ativo(False)
                    self.remove_coordenador()
                    self.processos.remove(processo)
                    coordenador.stop()
                    processo.stop()
                    print('##### Coordenador inativado {} #####'.format(id))
    

    def get_coordenador(self):
        if(len(self.processos) > 0):
            return self.processos[0].coordenador
        return None
    
    def gera_novo_coordenador(self):
        if len(self.processos):
            print('\n')
            print(' Elegendo um novo coordenador aleatoriamente')
            print('Processos ativos: '.format(self.processos_ativos()))
            processo = self.processos[randint(0,len(self.processos) - 1)]
            coordenador = Coordenador(processo.id)
            print('Novo coordenador!'.format(processo.tag))
            self.adicionar_coordenador_processos(coordenador)

    def adicionar_coordenador_processos(self, coordenador):
        print('Notificando processos do novo coodenador')
        for p in self.processos:
            p.set_coordenador(coordenador)
        print('\n')

    def processos_ativos(self):
        s=[]
        for p in self.processos:
            s.append(p.id)
        return s

    def retorna_processo(self, id):
        for p in self.processos:
            if p.id == id:
                return p

    def remove_coordenador(self):
        for p in self.processos:
            p.set_coordenador(None)

    def verifica_id_existente(self,id):
        for i in self.processos:
            if i.id == id:
                return False
        return True

    def run(self):
        Thread(target=self.gera_processo).start()
        Thread(target=self.intativa_coordenador).start()

if __name__ == '__main__':
    Processos().run()

