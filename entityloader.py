__author__ = 'alacambra'
import neo4j
import uuid
import Entities
import StringIO

connection = neo4j.connect("http://localhost:7474")
cursor = connection.cursor()
execution = True


def create_channel(total_items=10):

    query = ""

    query_builder = StringIO.StringIO()
    glue_query = "match (pl)-[:NEXT]->(last) where not (last)-[:NEXT]->()\n"
    channel_gen = Entities.Channel()

    user_gen = Entities.User("CH_O_U")
    query_builder.write(user_gen.get_query())
    
    channel_creator_ref = user_gen.last_ref

    query_builder.write(channel_gen.get_query())
    channel_ref = channel_gen.last_ref

    channel_items_rel_gen = Entities.ChannelItemsRelation()
    query_builder.write(channel_items_rel_gen.set_channel_owner(channel_ref, channel_creator_ref));

    items_gen = Entities.ChannelItem()
    query_builder.write(items_gen.create_channel_item())
    first_item = items_gen.last_ref

    query_builder.write(channel_items_rel_gen.set_first_item(channel_ref, first_item))

    second_item = None

    step = 20

    for i in range(0, total_items - 1):

        if i%step == 0 and i != 0:
            print "-"*50 + str(i)
            execute(query_builder.getvalue())
            query_builder.close()
            query_builder = StringIO.StringIO()
            query = glue_query
            second_item = "last"

    # So should be the glue
    # CREATE (CI21:UUID:container {time: 1405602171, type:'container', UUID:'d8821d67-c409-4d13-9e1d-a3fbdade0423', query_code:'SOME_CODE'})
    # WITH CI21
    # match (pl)-[:NEXT]->(last) where not (last)-[:NEXT]->()
    # CREATE (last)-[:NEXT]->(CI21)


        if second_item is not None:
            first_item = second_item

        query_builder.write(items_gen.create_channel_item("bce" if i % 4 else "container"))
        second_item = items_gen.last_ref

        query_builder.write(channel_items_rel_gen.connect_items(first_item, second_item))


    execute(query_builder.getvalue())
    # channel_query = "MATCH (channel: CHANNEL), (pl)-[:NEXT]->(last) where not (last)-[:NEXT]->()\n"
    # query = channel_query
    # query_builder.write(channel_items_rel_gen.set_last_item("channel", "last")

    print "-"*50 + str(i)
    # execute(query)


def clear_all():
    query = "MATCH n return count(n) as total"
    result = cursor.execute(query)

    (total, ) = result.next()

    step = 50

    print str(total) + " nodes to delete:"
    for i in range(0, total, step):
        print " - "*25 + str(i)
        query = "MATCH n with n LIMIT " + str(step) + " OPTIONAL MATCH n-[r]-m OPTIONAL MATCH m-[o]-() with o,r,n,m delete o, r, n, m"
        execute(query)

        # match n
        # optional match n-[r]-()
        # delete r, n


def execute(query):

    print query

    if execution:
        cursor.execute(query)
        connection.commit()


if __name__ == "__main__":
    print "hello"
    # clear_all();
    # for i in range(0, 10):
    create_channel(400)