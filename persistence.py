import sqlite3
from constants import DATABASE


if __name__ == '__main__':

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Create tweets table
    # c.execute('''CREATE TABLE tweets (id_str PRIMARY KEY, datetime, region, text, lang, image_url, score)''')

    # Delete tweets table
    # c.execute('''DROP TABLE tweets''')

    # Delete tweets tables rows
    # c.execute('''DELETE FROM tweets''')

    # Show tweets table
    c.execute('''SELECT * FROM tweets''')
    for row in c:
        print(row)

    # Save (commit) the changes
    conn.commit()
    conn.close()
