__author__ = 'alacambra'
import time
import uuid


def get_random_str():
    return get_time_as_str()


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
        self.query_builder.write(
                "CREATE (" + ref + ":"  + Label.uuid + ":" + Label.user + " "
                "{time:" + get_time_as_str() +
                ", "  + Label.uuid + ":'" + get_uuid_as_string(ref) + "'"
                ", name:'username" + get_random_str() + "'"
                ", occupation:'ocupation" + get_random_str() + "'"
                ", private:" + str(True).lower() + \
                ", connectivity:'" + get_connectivity_value(self.counter) + "'"
                ", dateModified:" + get_time_as_str() +
                ", postalCode:123654})\n")

        self.last_ref = ref
        self.counter += 1;
        return ref


class Task:

    counter = 0
    last_ref = ""

    def __init__(self, query_builder):
        self.counter = 0
        self.query_builder = query_builder

    def create_task(self):
        ref = "T" + str(self.counter)
        self.query_builder.write("CREATE (" + ref + ":" + Label.uuid + ":" + Label.task + " " +
                "{time:" + get_time_as_str() +
                ", name: 'task" + get_random_str() + "'"
                ", "  + Label.uuid + ":'" + get_uuid_as_string(ref) + "'"
                ", description:'ipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsum'"
                ", location:'some place'"
                ", private:" + str(True).lower() +
                ", connectivity:'" + get_connectivity_value(self.counter) + "'"
                ", dateModified:" + get_time_as_str() +
                ", startDate:" + get_time_as_str() +
                ", endDate:" + get_time_as_str() +
                ", timeRequired:123654})\n")

        self.last_ref = ref
        self.counter += 1;
        return ref


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


class UserTaskRelation:

    def __init__(self, query_builder):
        self.query_builder = query_builder

    def set_creator_of_task(self, task_ref, creator_ref):
        self.query_builder.write("CREATE (" + task_ref + ")-[:" + TaskRelation.user_is_creator_of_task + "]->(" + creator_ref + ")\n")

    def set_assignee_of_task(self, task_ref, assignee_ref):
        self.query_builder.write("CREATE (" + task_ref + ")-[:" + TaskRelation.user_is_assigned_to_task + "]->(" + assignee_ref + ")\n")