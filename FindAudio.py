# -*- coding: utf-8 -*-


import pymongo
import os, sys
'''O pygame exibe uma mensagem ao ser importado, para que isso não ocorra, utilize esse trecho para importação'''
with open(os.devnull, 'w') as f:
    oldstdout = sys.stdout
    sys.stdout = f
    import pygame
    sys.stdout = oldstdout



class FindAudio():
    def __init__(self, nome):
        '''necessario passar os parâmetros conforme as configurações do seu projeto. Como não passei nenhum parametro,
        o MongoDB usará a configuração padrão. Ou seja, é a mesma coisa que  self.conn = pymongo.MongoCliente('localhost', 27017) '''
        self._conn = pymongo.MongoClient()
        #self.instance = self.conn+'.{}'.format(instance) #instacia do MongoDB
        #troque o atributo musics pelo nome do seu banco de dados
        self._database = self._conn.musics #Banco de dados da instância
        #troque o tributo posts pelo nome da sua coleção
        self._collection = self._database.posts #colecao do bando de dados
        musics = self._pesquisa_audio(nome)
        if len(musics) == 1:
            try:
                self._toca_audio(musics[0]['path']+musics[0]['name'])
            except:
                print("Não foi possível reproduzir o arquivo!")
        elif len(musics) >1:
            print("Escolha uma opção: ")
            for a in range(len(musics)):
                print("{} - {}".format(a, musics[a]['name']))
            op = int(input(" "))
            if op > len(musics):
                print("Opção Inválida")
            else:
                try:
                    self._toca_audio(musics[op]['path']+musics[op]['name'])
                except:
                    print("Não foi possível reproduzir o arquivo!")
        else:
            print("Música não encontrada.")

    #realiza a pesquisa no mongoDB
    def _pesquisa_audio(self, nome):
        results = []
        for a in self._collection.find({'name': nome+'.mp3'}):
            results.append(a)
        return results

    #toca o audio usando a biblioteca pygame
    def _toca_audio(self, path):
        pygame.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        pygame.event.wait()


if __name__ == '__main__':
    musica = input("Digite a o nome da música: ")
    f = FindAudio(musica)