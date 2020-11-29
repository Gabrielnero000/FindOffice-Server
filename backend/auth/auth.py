from backend.api import Api


class AuthApi(Api):
    def __init__(self):
        super().__init__()

    def login(self, email, password):
        cursor = self._db.getCursor()

        # Check if there is any users with that email
        query_sql = f"SELECT * FROM users WHERE email = '{email}'"
        cursor.execute(query_sql)
        db_user = cursor.fetchone()

        if db_user is None:
            return {
                'success': False,
                'user': None,
                'error': 'Email not found'
            }

        # Check password
        if db_user['password'] != password:
            return {
                'success': False,
                'user': None,
                'error': 'Wrong password'
            }

        return {
            'success': True,
            'user': db_user,
            'error': None
        }

    def singUp(self, user):
        cursor = self._db.getCursor()

        # Check if there is any users with that email
        query_sql = f"SELECT * FROM users WHERE email = '{user['email']}'"
        cursor.execute(query_sql)
        if cursor.fetchone() is not None:
            return {
                'success': False,
                'user': None,
                'error': 'Email already in use'
            }

        # Insert user
        insert_sql = "INSERT INTO users (name, email, password, type) VALUES (%s, %s, %s, %s)"
        values = (user['name'], user['email'], user['password'], user['type'])
        cursor.execute(insert_sql, values)
        self._db.commit()

        # Return inserted user
        query_sql = "SELECT * FROM users WHERE userId = last_insert_id()"
        cursor.execute(query_sql)
        db_user = cursor.fetchone()

        return {
            'success': True,
            'user': db_user,
            'error': None
        }
