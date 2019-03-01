import sqlite3


class DB:
    def __init__(self, database):
        conn = sqlite3.connect(database, check_same_thread=False)
        self.conn = conn
 
    def get_connection(self):
        return self.conn
 
    def __del__(self):
        self.conn.close()
    pass


class NewsModel:
    def __init__(self, connection):
        self.connection = connection
        self.init_table()
    
    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS news 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             title VARCHAR(100),
                             content VARCHAR(1000),
                             user_id INTEGER
                             )''')
        cursor.close()
        self.connection.commit()    
    
    def insert(self, title, content, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO news 
                          (title, content, user_id) 
                          VALUES (?,?,?)''', (title, content, str(user_id)))
        cursor.close()
        self.connection.commit()
    
    def update(self, title=None, content=None, news_id=None):
        if news_id: news_id = int(news_id)
        cursor = self.connection.cursor()
        if title:
            cursor.execute('''UPDATE news SET title = ? WHERE id = ?''', (title, str(news_id)))
        if content:
            cursor.execute('''UPDATE news SET content = ? WHERE id = ?''', (content, str(news_id)))
        cursor.close()
        self.connection.commit()
    
    def get(self,news_id):
        cursor = self.connection.cursor()
        print("ID:",news_id)
        cursor.execute("SELECT * FROM news WHERE id = "+str(news_id))
        row = cursor.fetchone()
        return row
     
    def get_all(self, user_id = None):
        cursor = self.connection.cursor()
        if user_id:
            cursor.execute("SELECT title, user_id FROM news WHERE user_id = "+str(user_id))
        else:
            cursor.execute("SELECT title, id FROM news")
        rows = cursor.fetchall()
        return rows
    
    def delete(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM news WHERE id = '''+str(news_id))
        cursor.close()
        self.connection.commit()    
    pass


class UsersModel:
    def __init__(self, connection):
        self.connection = connection
        self.init_table()
        
    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_name VARCHAR(50),
                             password_hash VARCHAR(128)
                             )''')
        cursor.close()
        self.connection.commit()
    
    def insert(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash) 
                          VALUES (?,?)''', (user_name, password_hash))
        cursor.close()
        self.connection.commit()
        
    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?"+str(user_id))
        row = cursor.fetchone()
        return row
     
    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows
    
    def exists(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ? AND password_hash = ?",
                       (user_name, password_hash))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)  
    
    def get_pwd(self, user_name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = '"+str(user_name)+"'")
        row = cursor.fetchone()
        if row:
            return row
        return False
    pass


if __name__ == '__main__':
    base = DB("FLASK.db")
    n = NewsModel(base.get_connection())
    u = UsersModel(base.get_connection())