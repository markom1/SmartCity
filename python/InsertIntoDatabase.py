from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config

def insert_temperature(temperature):
    query = "INSERT INTO temperature(id, field1, field2) " \
            "VALUES(%s,%s,%s)"

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.executemany(query, temperature)

        conn.commit()
    except Error as e:
        print('Error: ', e)

    finally:
        cursor.close()
        conn.close()

def main():
    temperature = [('25', '6.7', '4.5'),
                   ('26', '9.5', '5.3')]
    insert_temperature(temperature)

if __name__ == '__main__':
    main()
