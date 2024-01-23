import sqlite3


class CRUD:
    def __init__(self):
        self.file_name = 'users.db'
        self.db = sqlite3.connect(self.file_name)
        self.cur = self.db.cursor()

    def add_user(self, data):
        '''
        :param data: tuple(name, result, is_complited)
        '''

        self.cur.execute(f'''INSERT INTO users (name, result, is_complited) VALUES {data};''')
        self.db.commit()

    def update_user(self, **kwargs):
        """
        :param kwargs:  name='Имя_игрока', result=счет, is_complited=0/1(итог)
        """
        f = f'''
            UPDATE users 
            SET {", ".join([f"{key} = {value}" for key, value in kwargs.items() if key != "name"])}
            WHERE name = "{kwargs['name']}";
            '''
        self.cur.execute(f)
        self.db.commit()

    def get_user(self, name):
        result = self.cur.execute(f'''
                SELECT *
                FROM users
                WHERE name="{name}"''').fetchall()
        return result

    def get_top(self):
        result = self.cur.execute(f'''
                        SELECT *
                        FROM users
                        WHERE is_complited=1''').fetchall()
        return result

    def close(self):
        self.db.close()

if __name__ == '__main__':
    crud = CRUD()
    #crud.add_user(('Test', 100, 0))
    #crud.update_user(name='Egor', result=352, is_complited=1)
    print(crud.get_top())
