import databasefunctions

import pandas as pd
import math
from datetime import datetime, timedelta, date


# In[9]:


class OrganizeTable:
    def __init__(self, username):
        #rececebe um usuario referencia
        #pode ser referencia de feed para o poster ou perfil referencia para o follow engine
        self.database = databasefunctions.Database()
        self.username = str(username)
    
    def __call__(self):
        return self.organizePoster()


    def organizePoster(self):
        try:
            feed = self.database.getFeed(self.username, 'poster')
            pd.options.display.max_rows = len(feed)
            df = pd.DataFrame(feed, columns=['id','url','comments','likes'])
            # ordena  dataframe por imagens mais comentadas e mais curtidas, extrai 33% dos resultados e exporta em um dicionario com chaves como id e url como valor
            posts = df.sort_values(by='likes', ascending=False).sort_values(by='comments', ascending=False).head(int(len(feed)* 0.33))
            posts = posts.set_index('id')['url'].to_dict()

            #organiza os horarios
            last_date = self.database.saveScheduledPosts()[0] if self.database.saveScheduledPosts() != None else datetime.strptime(str(date.today()) + ' 20:00:00', "%Y-%m-%d %H:%M:%S")
            
            novo = {}
            for key in posts.keys():
                altered = False
                if str(last_date.strftime('%H')) == '16' and altered == False:
                    last_date = last_date + timedelta(hours=4)
                    novo.setdefault(key, {'url': posts[key], 'scheduled': str(last_date)})
                    altered = True
                
                if str(last_date.strftime('%H')) == '10' and altered == False:
                    last_date = last_date + timedelta(hours=6)
                    novo.setdefault(key, {'url': posts[key], 'scheduled': str(last_date)})
                    altered = True
                
                if str(last_date.strftime('%H')) == '20' and altered == False:
                    last_date = last_date + timedelta(days=1, hours=-10)
                    novo.setdefault(key, {'url': posts[key], 'scheduled': str(last_date)})
                    altered = True

            self.database.updatePoster(novo, self.username)
            return True
        
        except BaseException as error:
            #self.database.saveError(error, '__call__  -- OrganizeTable')
            print('Error ocurred in: OrganizeTable --> {}'.format(error))
            return False


# In[10]:


if __name__ == '__main__':
    # pass
    org = OrganizeTable('jonthephotographer')

#     org.organizePoster()
#     org.organizeFollowEngine()

    org('poster')
#     org('follow_engine')
#     db = databasefunctions.Database()
#     feed = db.getFeed('yaaanhue', 'poster')
