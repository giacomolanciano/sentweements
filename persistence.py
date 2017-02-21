import sqlite3
from constants import DATABASE
from datetime import datetime
from tweets_streaming import SQLITE_DATETIME_FORMAT


def get_regions_stats(since_date_time, until_date_time):
    result = {}
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute('''SELECT region, COUNT(*), AVG(score) FROM tweets WHERE datetime >= ? AND datetime <= ?
                   GROUP BY region''', (since_date_time, until_date_time))
    for res_tuple in cursor:
        result[res_tuple[0]] = [res_tuple[1], res_tuple[2]]
    connection.close()
    return result


if __name__ == '__main__':

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS tweets (id_str, region, datetime, text, lang, score,
              PRIMARY KEY (id_str, region))''')
    c.execute('''CREATE TABLE IF NOT EXISTS images (region , image_url, datetime, anger, contempt, disgust, fear,
              happiness, neutral, sadness, surprise, PRIMARY KEY (region, image_url))''')

    # Delete tables
    # c.execute("DROP TABLE tweets")
    # c.execute("DROP TABLE images")

    # Delete tables rows
    # c.execute("DELETE FROM tweets")
    # c.execute("DELETE FROM images")

    # Show  tables
    # print('\ntweets')
    # c.execute("SELECT * FROM tweets")
    # for row in c:
    #     print(row)
    # print('\nimages')
    # c.execute("SELECT * FROM images")
    # for row in c:
    #     print(row)

    # test regions averages
    since_date = '2017-02-17 20:21:00.000'
    until_date = datetime.now().strftime(SQLITE_DATETIME_FORMAT)
    print(until_date)
    # print('\nregion_score')
    # c.execute("SELECT region, score FROM tweets WHERE datetime >= ?", (date,))
    # for row in c:
    #     print(row)
    print('\navg')
    res = get_regions_stats(since_date, until_date)
    print(res)

    # Save (commit) the changes
    conn.commit()
    conn.close()
