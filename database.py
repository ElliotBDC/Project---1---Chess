# File for handling interactions between sqlite3 database and main program
import sqlite3

def createDatabase():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL
                        )
                   ''')
    print("HELLO")
    connection.commit()
    connection.close()

def registerUser(username, password):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    # Check if username already exists

    cursor.execute("SELECT * FROM users WHERE username = (?)", (username,))
    result = cursor.fetchone()
    if result:
        connection.commit()
        connection.close()
        return False

    cursor.execute('''
                   INSERT INTO users (username, password) VALUES (?, ?)
                   ''', (username, password))
    
    connection.commit()
    connection.close()
    return True

def checkUserData(username, password):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute('''
                   SELECT * FROM users WHERE username = (?) AND password = (?)
                   ''', (username, password))
    user = cursor.fetchone()
    
    connection.commit()
    connection.close()

    if user:
        return True
    return False

if __name__ == "__main__":
    createDatabase()
    result = registerUser("Hello", '123')
    print(result)
    print(checkUserData("Hello", '8'))
