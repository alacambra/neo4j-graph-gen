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
                     "uuid:" + str(time.clock()) + "," \
                                                   "name:'albert'," \
                                                   "connectivity:'something'," \
                                                   "tuPichaLoca:'atributeado'})\n"

        i += 1;

    execute(query)


def clear_all():
    query = "MATCH n, OPTIONAL MATCH n-[r]-m DELETE r, n"
    execute(query)


def execute(query):
    a = cursor.execute(query)
    connection.commit()
    print query


if __name__ == "__main__":
    print "hello"