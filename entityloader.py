__author__ = 'alacambra'
import neo4j
import uuid
import Entities
import StringIO

connection = neo4j.connect("http://localhost:7474")
cursor = connection.cursor()
execution = True


def create_channel(total_items=10):

    query_builder = StringIO.StringIO()
    channel_gen = Entities.Channel(query_builder)
    channel_items_rel_gen = Entities.ChannelItemsRelation(query_builder)
    user_gen = Entities.User(query_builder, "CH_O_U")
    items_gen = Entities.ChannelItem(query_builder)

    channel_creator_ref = user_gen.create_user()
    channel_ref, channel_uuid = channel_gen.create_channel()
    channel_items_rel_gen.set_channel_owner(channel_ref, channel_creator_ref)

    first_item, first_channel_item_uuid = items_gen.create_channel_item()
    channel_items_rel_gen.set_first_item(channel_ref, first_item)

    second_item = None

    step = 20

    for i in range(0, total_items - 1):

        if i%step == 0 and i != 0:
            print "-"*50 + str(i)
            execute(query_builder.getvalue())

            query_builder.truncate(0)
            query_builder.seek(0)

            query_builder.write("match (last:UUID {UUID:'" + last_channel_item_uuid +"'})")
            second_item = "last"

    # So should be the glue
    # CREATE (CI21:UUID:container {time: 1405602171, type:'container', UUID:'d8821d67-c409-4d13-9e1d-a3fbdade0423', query_code:'SOME_CODE'})
    # WITH CI21
    # match (pl)-[:NEXT]->(last) where not (last)-[:NEXT]->()
    # CREATE (last)-[:NEXT]->(CI21)

        if second_item is not None:
            first_item = second_item

        second_item, last_channel_item_uuid = items_gen.create_channel_item("bce" if i % 4 else "container")
        channel_items_rel_gen.connect_items(first_item, second_item)

    execute(query_builder.getvalue())

    query_builder.truncate(0)
    query_builder.seek(0)

    channel_query = "MATCH (channel: UUID {UUID:'" + channel_uuid + "'}), (last:UUID {UUID:'" + last_channel_item_uuid +"'})\n"
    query_builder.write(channel_query)
    channel_items_rel_gen.set_last_item("channel", "last")

    i = 0
    print "-"*50 + str(i)
    execute(query_builder.getvalue())


def clear_all():
    query = "MATCH n return count(n) as total"
    result = cursor.execute(query)

    (total, ) = result.next()

    step = 50

    print str(total) + " nodes to delete:"
    for i in range(0, total, step):
        print " - "*25 + str(i)
        query = "match n with n LIMIT " + str(step) + " optional match n-[r]-() delete r, n"
        execute(query)


def execute(query):

    # print query

    if execution:
        cursor.execute(query)
        connection.commit()


if __name__ == "__main__":
    print "hello"
    # clear_all();
    for i in range(0, 5):
        create_channel(250)