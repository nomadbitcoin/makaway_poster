import databasefunctions
from datetime import datetime

class ApiFunctions:
    '''
        Funcoes extras para uso da api que precisam ser criadas manualmente pois nao estao disponiveis no pacote
    '''
    
    '''
        deve ser instanciada no inicio do programa que usa a api
        cada vez que a api for usada chamar a funcao addCall
        no final do programa ou funcao, chamar uodate para que adicione todas as chamadas que o programa fez
        
        funciona basicamente como sessao, inicia faz uso e atualiza
    '''
    
    
    def __init__(self):
        self.uses = []
    
    #adiciona um is:issue is:open item na lista cada vez que ela eh chamada
    def addCall(self, program_use):
        self.uses.append(1)
        self.used_by = program_use
        return len(self.uses)
    
    #atualiza no banco de dados o numero de vezes que ela foi chamada
    def updateInDatabase(self, username_use):
        try:
            banco = databasefunctions.Database()
            banco.connect()
            cursor = banco.startCursor()
            query = 'insert into api_count(used_by, count, updated, username) values(%s,%s,%s,%s)'
            cursor.execute(query, (self.used_by, len(self.uses), datetime.now().strftime('%y/%m/%d %H:%M:%S'), username_use))
            banco.commitChanges()
            banco.closeConnection()
            self.uses = []
        except BaseException as error:
            print('Error ocurred in: updateInDatabase --> {}'.format(error)) 

    def getTotalFeed(self, user_id, api):
        self.api = api
        feed = []
        next_max_id = True
        while next_max_id:
            if next_max_id is True:
                next_max_id = ''

            _ = self.api.getUserFeed(user_id, maxid=next_max_id)
            self.addCall('getTotalFeed')
            feed.extend(self.api.LastJson['items'])
            next_max_id = self.api.LastJson.get('next_max_id', '')
        
        self.updateInDatabase(self.api.username)
        return feed

    def getTotalComments(self, media_id, api):
        self.api = api
        has_more_comments = True
        max_id = ''
        comments = []

        while has_more_comments:
            _ = self.api.getMediaComments(str(media_id), max_id=max_id)
            self.addCall('getTotalComments')
            # comments' page come from older to newer, lets preserve desc order in full list
            for c in api.LastJson['comments']:
                comments.append(c)
            has_more_comments = self.api.LastJson.get('has_more_comments', False)

            if has_more_comments:
                max_id = self.api.LastJson.get('next_max_id', '')
        
        self.updateInDatabase(self.api.username)
        self.uses = []
        return comments

