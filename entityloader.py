__author__ = 'alacambra'
import neo4j
import time
import uuid

connection = neo4j.connect("http://localhost:7474")
cursor = connection.cursor()

def create_nodes(total, type):

    query = "";
    step = 25;

    for i in range(0, total):

        if i%step == 0 and i != 0:
            execute(query)
            query = ""
        else:
            query += "CREATE (n" + str(i) + ":" + type + \
                     ":UUID {" \
                     "privacy:" + str(i%4!=0).lower() + ", " \
                                                        "uuid:`" + str(uuid.uuid4()) + "`," \
                                                                                      "name:'albert'," \
                                                                                      "connectivity:'something'," \
                                                                                      "tuPichaLoca:'atributeado'})\n"

        i += 1;

    execute(query)


def create_channel(total):

    query = "";
    step = 25;

    for i in range(0, total):
        # if i%step == 0 and i != 0:
        #     execute(query)
        #     query = ""
        # else:
        query += "CREATE (n" + str(i) + ":channel" \
                 ":UUID {" \
                 "privacy:" + str(i%4!=0).lower() + ", " \
                                                    "uuid:`" + str(uuid.uuid4()) + "`," \
                                                                                   "name:'albert'," \
                                                                                   "connectivity:'something'," \
                                                                                   "tuPichaLoca:'atributeado'})\n"
        if i > 0:
            query += "CREATE (n" + str(i-1) + ")-[:NEXT]->(n" + str(i) + ")\n"
    execute(query)


def clear_all():
    query = "MATCH n, OPTIONAL MATCH n-[r]-m DELETE r, n"
    execute(query)


def execute(query):
    # cursor.execute(query)
    # connection.commit()
    print query


if __name__ == "__main__":
    print "hello"
    # clear_all();
    create_channel(2)