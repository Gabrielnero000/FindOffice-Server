from backend.api import Api


class AuthApi(Api):
    def __init__(self, today):
        super().__init__(today)

    def login(self, email, password, user_type):
        cursor = self._db.getCursor()

        # Check if there is any users with that email
        query_sql = f"SELECT * FROM {user_type} WHERE email = '{email}'"
        cursor.execute(query_sql)
        db_user = cursor.fetchone()

        if db_user is None:
            return {
                'success': False,
                'user': None,
                'error': f'There is no {user_type} with that email'
            }

        # Check password
        if db_user['password'] != password:
            return {
                'success': False,
                'user': None,
                'error': 'Wrong password'
            }

        db_user['type'] = user_type
        return {
            'success': True,
            'user': db_user,
            'error': None
        }

    def signUp(self, user):
        cursor = self._db.getCursor()

        # Check if there is any users with that email
        query_sql = f"SELECT * FROM {user['type']} WHERE email = '{user['email']}'"
        cursor.execute(query_sql)

        if cursor.fetchone() is not None:
            return {
                'success': False,
                'user': None,
                'error': 'Email already in use'
            }

        # Insert user
        insert_sql = (
            f"INSERT INTO {user['type']} (name, email, password)"
            f"VALUES ('{user['name']}', '{user['email']}', '{user['password']}')"
        )
        cursor.execute(insert_sql)

        # Return inserted user
        query_sql = f"SELECT * FROM {user['type']} WHERE {user['type']+'Id'} = last_insert_id()"
        cursor.execute(query_sql)
        db_user = cursor.fetchone()
        db_user['type'] = user['type']

        return {
            'success': True,
            'user': db_user,
            'error': None
        }
