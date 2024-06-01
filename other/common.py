import sqlite3
from queue import Queue

class Globals:
    username = ""  # when we login, there is <name> here, unless, it is empty(in logout)
    dstName = "11"


send_q = Queue()
recv_q = Queue()


def buildMsg(msgDst, msgSrc, msgType, msgData):
    print("2200", msgDst, msgSrc, msgType, msgData)
    data = ""
    for i in msgData:
        data = data + "," + i
    msg = msgDst + "," + msgSrc + "," + msgType + data
    print("1010", msg)
    return msg


def update_score(username, score_to_add):
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('user_database.db')
        cursor = conn.cursor()
        new_score = score_to_add
        old_score = int(get_user_score(username))
        if old_score is None:
            print("User is not found in database...")
        else:
            new_score += old_score
        # Execute an UPDATE statement to update the score for the specified user
        update_query = "UPDATE users SET score = ? WHERE username = ?"
        cursor.execute(update_query, (new_score, username))

        # Commit the changes to the database
        conn.commit()
        print("Score updated successfully for user:", username)

    except sqlite3.Error as e:
        print("Error updating score:", e)

    finally:
        # Close the database connection
        if conn:
            conn.close()


def get_user_score(username):
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('user_database.db')
        cursor = conn.cursor()

        # Execute a SELECT query to retrieve the score for the specified user
        cursor.execute("SELECT score FROM users WHERE username=?", (username,))
        score = cursor.fetchone()

        if score:
            return score[0]  # Return the score if user is found
        else:
            return None  # Return None if user is not found

    except sqlite3.Error as e:
        print("Error retrieving score:", e)
        return None

    finally:
        # Close the database connection
        if conn:
            conn.close()
