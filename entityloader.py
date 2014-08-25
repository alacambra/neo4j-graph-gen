__author__ = 'alacambra'
import neo4j
import Entities
import StringIO
from Entities import Label

execution = True


class Connection:

    connection = None
    cursor = None

    def __init__(self, host="localhost", port=7474):
        self.host = host
        self.port = port

    def set_connection_url(self, host, port):
        self.host = host
        self.port = port
        self.create();
        return self

    def set_connection_port(self, port):
        self.port = port
        self.create()
        return self

    def create(self):
        if self.connection is not None:
            self.connection.close()

        self.connection = neo4j.connect("http://" + self.host + ":" + str(self.port));
        self.cursor = self.connection.cursor()
        return self

    def commit(self):
        self.connection.commit();

    def get_cursor(self):

        if self.cursor is None:
            raise Exception("cursor is not initialized")

        return self.cursor

connection = Connection().create()

def create_channel(total_items=10):

    query_builder = StringIO.StringIO()

    channel_gen = Entities.Channel(query_builder)
    channel_items_rel_gen = Entities.ChannelItemsRelation(query_builder)
    user_gen = Entities.User(query_builder, "CH_O_U")

    channel_creator_ref = user_gen.create_user()
    items_gen = Entities.ChannelItem(query_builder, channel_creator_ref)
    channel_ref, channel_uuid = channel_gen.create_channel()
    channel_items_rel_gen.set_channel_owner(channel_ref, channel_creator_ref)

    first_item, first_channel_item_uuid = items_gen.create_first_item()
    channel_items_rel_gen.set_first_item(channel_ref, first_item)

    second_item = None

    step = 20

    for i in range(0, total_items - 1):

        if i%step == 0 and i != 0:
            print "-"*50 + str(i)
            execute(query_builder.getvalue())
            connection.commit()

            query_builder.truncate(0)
            query_builder.seek(0)

            query_builder.write("match (last:" + Label.uuid + " {" + Label.uuid + ":'" + last_channel_item_uuid + "'})")
            second_item = "last"

        if second_item is not None:
            first_item = second_item

        second_item, last_channel_item_uuid = items_gen.create_channel_item(Label.bce if i % 4 else Label.container)
        channel_items_rel_gen.connect_items(first_item, second_item)

    execute(query_builder.getvalue())
    connection.commit()

    query_builder.truncate(0)
    query_builder.seek(0)

    channel_query = "MATCH (channel: " + Label.uuid + " {" + Label.uuid + ":'" + channel_uuid + "'}), (last:" \
                    + Label.uuid + " {" + Label.uuid + ":'" + last_channel_item_uuid +"'})\n"
    query_builder.write(channel_query)
    channel_items_rel_gen.set_last_item("channel", "last")

    i = 0
    print "-"*50 + str(i)
    execute(query_builder.getvalue())
    connection.commit()


def clear_all():
    query = "MATCH n return count(n) as total"
    result = connection.get_cursor().execute(query)

    (total, ) = result.next()

    step = 50

    print str(total) + " nodes to delete:"
    total_removed = 0
    for i in range(0, total, step):
        print " - "*25 + str(total_removed)
        query = "match n with n LIMIT " + str(step) + " optional match n-[r]-() delete r, n return count(n) as removed"
        result = execute(query)
        (removed, ) = result.next()
        total_removed += removed

    connection.commit()


def execute(query):

    # print query

    if execution:
        result = connection.get_cursor().execute(query)
        # connection.commit()
        return result;
    else:
        print query


def setup_db(clear_db=False):
    if clear_db:
        clear_all()

    # uniqueness
    unique_fields = ["uuid", "email"]

    for field in unique_fields:
        query = "CREATE CONSTRAINT ON (node:" + field + ") ASSERT node." + field + " IS UNIQUE"
        execute(query)

    connection.commit()


if __name__ == "__main__":
    print "hello"
    # clear_all();
    for i in range(0, 1):
        create_channel()