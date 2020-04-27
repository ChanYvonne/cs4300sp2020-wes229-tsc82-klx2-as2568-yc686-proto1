import json
import csv
import sys
import datetime
import psycopg2
from psycopg2 import connect, Error

update_podcasts_and_reviews = True

try:
    conn = connect(
        dbname="pea_podcast_proto1",
        user="postgres",
        host="localhost",
        password="1234",
        # attempt to connect for 3 seconds then raise exception
        connect_timeout=3
    )

    cur = conn.cursor()
    print("\ncreated cursor object:", cur)

except (Exception, Error) as err:
    print("\npsycopg2 connect error:", err)
    conn = None
    cur = None

# only attempt to execute SQL if cursor is valid
if cur != None:

    if update_podcasts_and_reviews:

        combinedData = {}

        with open('data/merged_podcasts.csv', newline='') as podcast_data:
            podcast_reader = csv.reader(podcast_data)
            next(podcast_reader)
            numPodcast = 0

            for row in podcast_reader:
                # each row is a list
                name = str(row[1]).replace('"', '')

                genres = row[6].replace('\'', '').split(", ")
                genres = [x.strip("]").strip("[") for x in genres]
                genres = ';'.join(genres)

                row[8] = row[8].split(", ")
                sum_ep_dur = 0
                for i in row[8]:
                    val = float(i.strip("]").strip("["))
                    sum_ep_dur += val
                avg_ep_dur = sum_ep_dur * 1.0 / len(row[8])

                podcastData = [row[0], float(row[3]), row[4], row[5],
                               genres, int(row[7]), avg_ep_dur, row[9], row[11]]
                combinedData[name] = podcastData
                numPodcast += 1

        # print("num podcasts:" + str(numPodcast)) = 6657
        # print(len(combinedData)) =  6598
        # print(combinedData["The Moth"])

        with open('data/combindedReviews.csv', newline='') as f:
            review_reader = csv.reader(f)
            next(review_reader)  # Skip the header row.

            numReviews = 0
            for row in review_reader:
                name = str(row[1]).replace('"', '')
                reviewData = [row[2], row[3], row[4], row[5],
                              row[6], row[7], row[8], row[9], row[10], row[11]]
                if name in combinedData.keys():
                    newData = combinedData[name] + reviewData
                    combinedData[name] = newData
                numReviews += 1

        # print("num Reviews: " + str(numReviews)) = 5889
        # print(combinedData["The Moth"])
        # print(len(combinedData["The Moth"]))

        try:
            for key in combinedData.keys():
                podcast = combinedData[key]
                podcast = [x if x != '' else None for x in podcast]
                if (len(podcast) == 19):
                    cur.execute(
                        """INSERT INTO podcasts VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (podcast[0], datetime.datetime.now(), datetime.datetime.now(),
                         key, podcast[1], podcast[2], podcast[3], podcast[4], podcast[5], podcast[6], podcast[7],
                         podcast[8], podcast[9], podcast[10], podcast[11], podcast[12], podcast[13], podcast[14],
                         podcast[15], podcast[16], podcast[17], podcast[18]))
                else:
                    cur.execute(
                        """INSERT INTO podcasts VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (podcast[0], datetime.datetime.now(), datetime.datetime.now(),
                         key, podcast[1], podcast[2], podcast[3], podcast[4], podcast[5], podcast[6], podcast[7],
                         podcast[8]))
            conn.commit()

            print('\nfinished INSERT INTO execution')

        except (Exception, Error) as error:
            print("\nexecute_sql() error:", error)
            conn.rollback()

    # close the cursor and connection
    cur.close()
    conn.close()

    # if update_podcasts:

    #     with open('data/merged_podcasts.json') as json_data:
    #         record_dict = json.load(json_data)
    #         table_name = "podcasts"

    #     # enumerate over the records' values
    #     records = record_dict.values()
    #     val_list = [[] for x in range(len(records))]
    #     # enumerate over the records' values
    #     for i, record in enumerate(records):

    #         # append each value to a new list of values
    #         for v, key in enumerate(record):
    #             val = record[key]
    #             if type(val) == list:
    #                 avg_ep_dur = 0
    #                 if type(val[0]) == float or type(val[0]) == int:
    #                     sum_ep_dur = sum(val)
    #                     avg_ep_dur = sum_ep_dur / len(val)
    #                     val = avg_ep_dur
    #                 else:
    #                     val = ';'.join(map(str, val))
    #                     val = str(val).replace('"', '')
    #             elif type(val) == str:
    #                 val = str((val)).replace('"', '')
    #             val_list[i].append(str(val))

    #     try:
    #         for i in range(len(list(records)[0])):
    #             cur.execute(
    #                 """INSERT INTO podcasts VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
    #                 (i, datetime.datetime.now(), datetime.datetime.now(),
    #                  val_list[0][i], val_list[1][i], val_list[2][i],  val_list[3][i],  val_list[4][i],  val_list[5][i],  val_list[6][i],
    #                  val_list[7][i], val_list[8][i], val_list[9][i], val_list[10][i]))
    #         conn.commit()
    #         print(len(list(records)[0]))

    #         print('\nfinished INSERT INTO execution')

    #     except (Exception, Error) as error:
    #         print("\nexecute_sql() error:", error)
    #         conn.rollback()

    # if update_reviews:
    #     with open('data/reviews.csv', newline='') as f:
    #         reader = csv.reader(f)
    #         next(reader)  # Skip the header row.

    #         try:
    #             numReviews = 0
    #             for row in reader:
    #                 # each row is a list
    #                 numReviews += 1
    #                 cur.execute(
    #                     """INSERT INTO reviews VALUES (%s, %s, %s, %s, %s, %s, %s)""",
    #                     (row[0], datetime.datetime.now(), datetime.datetime.now(), row[1], row[2], row[3], row[4]))

    #             print(numReviews)
    #             conn.commit()

    #             print('\nfinished INSERT INTO execution')

    #         except (Exception, Error) as error:
    #             print("\nexecute_sql() error:", error)
    #             conn.rollback()

    # # close the cursor and connection
    # cur.close()
    # conn.close()
