__author__ = 'alacambra'
import neo4j
import uuid
import Entities

connection = neo4j.connect("http://localhost:7474")
cursor = connection.cursor()
execution = True

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


# def create_channel(total):
#
#     query = "";
#     step = 25;
#
#     for i in range(0, total):
#         # if i%step == 0 and i != 0:
#         #     execute(query)
#         #     query = ""
#         # else:
#         query += "CREATE (n" + str(i) + ":channel" \
#                  ":UUID {" \
#                  "privacy:" + str(i%4!=0).lower() + ", " \
#                                                     "uuid:`" + str(uuid.uuid4()) + "`," \
#                                                                                    "name:'albert'," \
#                                                                                    "connectivity:'something'," \
#                                                                                    "tuPichaLoca:'atributeado'})\n"
#         if i > 0:
#             query += "CREATE (n" + str(i-1) + ")-[:NEXT]->(n" + str(i) + ")\n"
#     execute(query)


def create_channel(total_items = 10):

    query = ""
    channel_gen = Entities.Channel()
    query += channel_gen.get_query()
    channel_ref = channel_gen.last_ref

    items_gen = Entities.ChannelItem()
    query += items_gen.create_channel_item()
    first_item = items_gen.last_ref
    channel_items_rel_gen = Entities.ChannelItemsRelation()
    query += channel_items_rel_gen.set_first_item(channel_ref, first_item)

    second_item = None

    for i in range(0, total_items - 1):

        if second_item is not None:
            first_item = second_item

        query += items_gen.create_channel_item()
        second_item = items_gen.last_ref

        query += channel_items_rel_gen.connect_items(first_item, second_item)

    query += channel_items_rel_gen.set_last_item(channel_ref, second_item)

    execute(query)



def clear_all():
    query = "MATCH n, OPTIONAL MATCH n-[r]-m DELETE r, n"
    cursor.execute(query)
    connection.commit()

def execute(query):
    if execution:
        cursor.execute(query)
        connection.commit()

    print query


if __name__ == "__main__":
    print "hello"
    # clear_all();
    # create_channel(2)
    create_channel(25)