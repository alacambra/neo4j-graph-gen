__author__ = 'alacambra'
import time
import uuid
import StringIO
import random
import logging


def configure_logger():
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

logger = logging.getLogger(__name__)
configure_logger()


def get_random_str():
    return str(random.randint(1, 10000000000000)) + random.choice('abcdefghijklmnopqrstuvwxyz')


def get_time_as_str():
    return str(long(time.time()))


def get_connectivity_value(seed):
    return "request" if (seed % 3 == 0) else "direct" if (seed % 2 == 0) else "none"


uuids = []

def get_uuid_as_string(name="lala"):
    id = uuid.uuid4()
    while True:
        if id not in uuids:
            uuids.append(id)
            break

        else:
            id = uuid.uuid4()

    return str(id)

class Label:
    channel = "channel"
    uuid = "uuid"
    user = "people"
    task = "task"
    channel_item = "c_item"
    bce = "bce"
    container = "container"
    roll = "roll"


class ChannelRelation:
    channel_to_first_item = "has_items"
    item_refers_to_next_item = "next"
    bce_item_refers_to_object = "refers_to"
    person_owns_channel = "owns"


class TaskRelation:
    user_is_creator_of_task = "created_by"
    user_is_assigned_to_task = "assigned_to"


class ChannelItem:

    counter = 0

    def __init__(self, query_builder):
        self.last_ref = ""
        self.counter = 0
        self.task_gen = Task(query_builder)
        self.user_gen = User(query_builder)
        self.channel_item_rel_gen = ChannelItemsRelation(query_builder)
        self.user_task_rel_gen = UserTaskRelation(query_builder)
        self.query_builder = query_builder

    def create_channel_item(self, item_type=Label.bce):
        ref = "CI" + str(self.counter)
        used_uuid = get_uuid_as_string(ref)

        self.query_builder.write(
            "CREATE (" + ref + ":" + item_type + ":" + Label.uuid +
            "{time: " + get_time_as_str() + ", type:'" + item_type + "'"
            ", " + Label.uuid + ":'" + used_uuid)

        if Label.bce == item_type:
            self.query_builder.write("'})\n")
            self.task_gen.create_task()
            self.channel_item_rel_gen.refer_bce_to_item(ref, self.task_gen.last_ref)
            self.user_gen.create_user()
            self.user_task_rel_gen.set_creator_of_task(self.task_gen.last_ref, self.user_gen.last_ref)
            self.user_gen.create_user()
            self.user_task_rel_gen.set_assignee_of_task(self.task_gen.last_ref, self.user_gen.last_ref)

        else:
            self.query_builder.write("', query_code:'SOME_CODE'})\n")

        self.last_ref = ref
        self.counter += 1

        return ref, used_uuid


class Channel:

    counter = 0

    def __init__(self, query_builder):
        self.last_ref = ""
        self.counter = 0
        self.query_builder = query_builder

    def create_channel(self):

        ref = "CH" + str(self.counter)
        used_uuid = get_uuid_as_string(ref)
        self.query_builder.write(
            "CREATE (" + ref + ":" + Label.uuid + ":" + Label.channel + " "
            "{time: " + get_time_as_str() + ""
            ", " + Label.uuid + ":'" + used_uuid + "'})\n")

        self.counter += 1;
        self.last_ref = ref
        return ref, used_uuid


class User:

    counter = 0
    last_ref = ""

    def __init__(self, query_builder, prefix="U"):
        self.counter = 0
        self.prefix = prefix
        self.query_builder = query_builder

    def create_user(self):
        ref = self.prefix + str(self.counter)
        uuid = get_uuid_as_string(ref)

        self.query_builder.write(
                "CREATE (" + ref + ":" + Label.uuid + ":" + Label.user + " "
                "{time:" + get_time_as_str() +
                ", "  + Label.uuid + ":'" + uuid + "'"
                ", name:'username" + get_random_str() + "'"
                ", occupation:'ocupation" + get_random_str() + "'"
                ", private:" + str(True).lower() +
                ", connectivity:'" + get_connectivity_value(self.counter) + "'"
                ", dateModified:" + get_time_as_str() +
                ", postalCode:123654})\n")

        self.last_ref = ref
        self.counter += 1
        return ref, uuid


class Roll:
    counter = 0
    last_ref = ""

    def __init__(self, name, query_builder, prefix="R"):
        self.counter = 0
        self.prefix = prefix
        self.query_builder = query_builder
        self.roll_name = name

    def create_roll(self):
        ref = self.prefix + str(self.counter)
        self.query_builder.write(
            "CREATE (" + ref + ":" + Label.uuid + ":" + Label.roll + " "
            "{name})\n")


class Task:

    counter = 0
    last_ref = ""

    def __init__(self, query_builder):
        self.counter = 0
        self.query_builder = query_builder

    def create_task(self):
        ref = "T" + str(self.counter)
        uuid = get_uuid_as_string(ref)
        self.query_builder.write("CREATE (" + ref + ":" + Label.uuid + ":" + Label.task + " " +
                "{time:" + get_time_as_str() +
                ", name: 'task" + get_random_str() + "'"
                ", "  + Label.uuid + ":'" + uuid + "'"
                ", description:'ipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsum'"
                ", location:'some place'"
                ", private:" + str(True).lower() +
                ", connectivity:'" + get_connectivity_value(self.counter) + "'"
                ", dateModified:" + get_time_as_str() +
                ", startDate:" + get_time_as_str() +
                ", endDate:" + get_time_as_str() +
                ", timeRequired:123654})\n")

        self.last_ref = ref
        self.counter += 1
        return ref, uuid


class ChannelItemsRelation:

    def __init__(self, query_builder):
        self.query_builder = query_builder

    def set_first_item(self, channel_ref, first_item_ref):
        self.query_builder.write("CREATE (" + channel_ref + ")-[:" + ChannelRelation.channel_to_first_item + "]->(" + first_item_ref + ")\n")

    def set_last_item(self, channel_ref, last_item_ref):
        self.query_builder.write("CREATE (" + last_item_ref + ")-[:" + ChannelRelation.item_refers_to_next_item + "]->(" + channel_ref + ")\n")

    def connect_items(self, first_ref, second_ref):
        self.query_builder.write("CREATE (" + first_ref + ")-[:" + ChannelRelation.item_refers_to_next_item + "]->(" + second_ref + ")\n")

    def refer_bce_to_item(self, item_ref, bce_ref):
        self.query_builder.write("CREATE (" + item_ref + ")-[:" + ChannelRelation.bce_item_refers_to_object + "]->(" + bce_ref + ")\n")

    def set_channel_owner(self, channel_ref, owner_ref):
        self.query_builder.write("CREATE (" + owner_ref + ")-[:" + ChannelRelation.person_owns_channel + "]->(" + channel_ref + ")\n")


class PrivateSphereRelations:

    def __init__(self, query_builder):
        self.query_builder = query_builder
        self.initialize_query_builders()
        self.uuid_ref = {}

    def add_subject_to_object_with_roll_name(self, subject_uuid, object_uuid, roll_name):

        subject_ref = "s" + get_random_str()
        object_ref = "o" + get_random_str()

        subject_ref = self.create_uuid_match(subject_uuid, subject_ref)
        object_ref = self.create_uuid_match(object_uuid, object_ref)

        self.create_query_builder.write(" " + subject_ref + "-[:" + roll_name + "]->" + object_ref + ",\n")

    def link_object(self, uuid_origin, uuid_target, merged=True, blacklisted=["assignee"], rolls=[], use_rolls=True):

        origin_ref = self.create_uuid_match(uuid_origin, "o" + get_random_str())
        target_ref = self.create_uuid_match(uuid_target, "o" + get_random_str())

        if use_rolls:
            rolls = rolls + blacklisted
            wl_match = "-[:linked]->" + target_ref

            for roll in rolls:
                roll_ref = "r" + get_random_str()
                self.merge_query_builder.write(
                    "merge " + origin_ref + "-[:has_roll]->(" + roll_ref + ":roll{name:\"" + roll + "\"})\n")

                if roll in blacklisted:
                    continue

                self.merge_query_builder.write("create " + roll_ref + wl_match + "\n")

        else:
            self.create_query_builder \
                .write(" " + origin_ref + "-[:linked {bl:\"" + ",".join(blacklisted) + "\"}]->" + target_ref + ",\n")

    def add_subject_to_object_with_roll_node(self, subject_uuid, object_uuid, roll_name):

        subject_ref = "s" + get_random_str()
        object_ref = "o" + get_random_str()
        roll_ref = "r" + get_random_str()

        subject_ref = self.create_uuid_match(subject_uuid, subject_ref)
        object_ref = self.create_uuid_match(object_uuid, object_ref)

        self.match_query_builder.\
            write("(" + roll_ref + ":roll{name:\"" + roll_name + "\"})-[:linked]->" + object_ref + ",\n")

        self.merge_query_builder.write(" merge " + subject_ref + "-[:has_roll]->" + roll_ref + "\n")

    def create_uuid_match(self, object_uuid, object_ref):
        if object_uuid in self.uuid_ref:
            object_ref = self.uuid_ref.get(object_uuid)
        else:
            self.uuid_ref[object_uuid] = object_ref
            self.match_query_builder.write(" (" + object_ref + ":uuid{uuid:\"" + object_uuid + "\"}),\n")

        return object_ref

    def build_subject_to_object_with_roll_name(self):

        if self.match_query_builder.tell() > 0:
            self.query_builder.write("match " + self.match_query_builder.getvalue())
            self.query_builder.seek(pos=-2, mode=2)
            self.query_builder.write("\n ")

        if self.create_query_builder.tell() > 0:
            self.query_builder.write("create " + self.create_query_builder.getvalue())
            self.query_builder.seek(pos=-2, mode=2)
            self.query_builder.write("\n ")

        if self.merge_query_builder.tell() > 0:
            self.query_builder.write(self.merge_query_builder.getvalue())

        self.uuid_ref = {}
        self.initialize_query_builders()

    def initialize_query_builders(self):
        self.match_query_builder = StringIO.StringIO()
        self.create_query_builder = StringIO.StringIO()
        self.merge_query_builder = StringIO.StringIO()

    def link_all(self):
        self.query_builder.write("match (n1:task)\n")
        self.query_builder.write("with collect(n1) as tasks\n")
        self.query_builder.write("foreach(t1 in tasks|\n")
        self.query_builder.write("foreach(t2 in tasks|\n")
        self.query_builder.write("MERGE (t1)-[r:linked {bl:\"assignee\"}]->(t2)\n")
        self.query_builder.write(")\n")
        self.query_builder.write(")\n")


class UserTaskRelation:

    def __init__(self, query_builder):
        self.query_builder = query_builder

    def set_creator_of_task(self, task_ref, creator_ref):
        self.query_builder.write("CREATE (" + task_ref + ")-[:" + TaskRelation.user_is_creator_of_task + "]->(" + creator_ref + ")\n")

    def set_assignee_of_task(self, task_ref, assignee_ref):
        self.query_builder.write("CREATE (" + task_ref + ")-[:" + TaskRelation.user_is_assigned_to_task + "]->(" + assignee_ref + ")\n")