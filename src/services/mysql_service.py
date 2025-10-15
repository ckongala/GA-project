import mysql.connector
from mysql.connector import errorcode

from flask_restful import current_app as app


class mysql_service:

    def __init__(self, user: str, password: str, host: str, database: str):
        try:
            self.mysql_connection = mysql.connector.connect(user=user, password=password,
                                                            host=host, database=database)
            self.mysql_cursor = self.mysql_connection.cursor()
            app.logger.info('MySQL connection established to %s:%s', host, database)
        except mysql.connector.Error as error:
            if error == errorcode.ER_ACCESS_DENIED_ERROR:
                app.logger.error('Access denied while trying to connect to ', host + '/' + database)
            elif error == errorcode.ER_BAD_DB_ERROR:
                app.logger.error('Database does not exist: ', database)
            else:
                app.logger.error('mySQL ErrorCode: ', error)

    def close_connection(self):
        """
        Close the connection with MySQl
        """
        self.mysql_cursor.close()
        self.mysql_connection.close()

    def get_from_query(self, query: str):
        """
        Executing the query for MySQL.
        """
        self.mysql_cursor.execute(query)
        rows = self.mysql_cursor.fetchall()
        return rows
