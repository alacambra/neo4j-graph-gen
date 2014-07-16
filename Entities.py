__author__ = 'alacambra'
import time
import uuid

def get_random_str():
    return get_time_as_str()


def get_time_as_str():
    return str(long(time.time()))


def get_connectivity_value(seed):
    return "request" if (seed % 3 == 0) else "direct" if (seed % 2 == 0) else "none"


class ChannelItem:

    counter = 0

    def __init__(self):
        self.last_ref = ""
        self.counter = 0
        self.task_gen = Task()
        self.channel_item_rel_gen = ChannelItemsRelation()

    def create_channel_item(self):
        item_type = "bce"
        ref = "CI" + str(self.counter)

        query = "CREATE (" + ref + ":" + item_type + " " \
                "{time: " + get_time_as_str() + ", type:'" + item_type + "'" \
                ", UUID:'" + str(uuid.uuid4()) + "'})\n"

        query += self.task_gen.get_query()
        query += self.channel_item_rel_gen.refer_bce_to_item(ref, self.task_gen.last_ref)

        self.last_ref = ref
        self.counter += 1
        return query


class Channel:

    counter = 0

    def __init__(self):
        self.last_ref = ""
        self.counter = 0

    def get_query(self):
        ref = "CH" + str(self.counter)
        query = "CREATE (" + ref + ":CHANNEL " \
                "{time: " + get_time_as_str() + "" \
                ", UUID:'" + str(uuid.uuid4()) + "'})\n"


        self.counter += 1;
        self.last_ref = ref
        return query


class User:

    counter = 0
    last_ref = ""

    def __init__(self):
        self.counter = 0

    def get_query(self):
        ref = "U" + str(self.counter)
        query = "CREATE (" + ref + ":USER " \
                "{time:" + get_time_as_str() + \
                ", UUID:'" + str(uuid.uuid4()) + "'" \
                ", name:'username" + get_random_str() + "'"\
                ", occupation:'ocupation" + get_random_str() + "'"\
                ", private:" + str(True).lower() + \
                ", connectivity:'" + get_connectivity_value(self.counter) + "'" \
                ", dateModified:" + get_time_as_str() + \
                ", postalCode:123654})\n"

        self.last_ref = ref
        self.counter += 1;
        return query


class Task:

    counter = 0
    last_ref = ""

    def __init__(self):
        self.counter = 0

    def get_query(self):
        ref = "T" + str(self.counter)
        query = "CREATE (" + ref + ":TASK " + \
                "{time:" + get_time_as_str() + \
                ", name: 'task" + get_random_str() + "'" \
                ", UUID:'" + str(uuid.uuid4()) + "'" \
                ", description:'ipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsum'" \
                ", location:'some place'" \
                ", private:" + str(True).lower() + \
                ", connectivity:'" + get_connectivity_value(self.counter) + "'"\
                ", dateModified:" + get_time_as_str() + \
                ", startDate:" + get_time_as_str() + \
                ", endDate:" + get_time_as_str() + \
                ", timeRequired:123654})\n"

        self.last_ref = ref
        self.counter += 1;
        return query

class ChannelItemsRelation:

    def set_first_item(self, channel_ref, first_item_ref):
        return "CREATE (" + channel_ref + ")-[:HAS_ITEMS]->(" + first_item_ref + ")\n"

    def set_last_item(self, channel_ref, last_item_ref):
        return "CREATE (" + last_item_ref + ")-[:LAST]->(" + channel_ref + ")\n"

    def connect_items(self, first_ref, second_ref):
        return "CREATE (" + first_ref + ")-[:NEXT]->(" + second_ref + ")\n"

    def refer_bce_to_item(self, item_ref, bce_ref):
        return "CREATE (" + item_ref + ")-[:REFERS_TO]->(" + bce_ref + ")\n"


class UserTaskRelation:
    def set_creator_of_task(self, task_ref, creator_ref):
        return "CREATE (" + task_ref + ")-[:CREATED_BY]->(" + creator_ref + ")\n"

    def set_assignee_of_task(self, task_ref, assignee_ref):
        return "CREATE (" + task_ref + ")-[:ASSIGNED_TO]->(" + assignee_ref + ")\n"

if __name__ == "__main__":

    channel = Channel()
    print channel.get_query();

    # for i in range(0, 100):


    p = User()
    print p.get_query()
    print p.get_query()
    print p.get_query()
    print p.get_query()

    print ""

    t = Task()
    print t.get_query()
    print t.get_query()
    print t.get_query()
    print t.get_query()
