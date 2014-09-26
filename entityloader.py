__author__ = 'alacambra'
import neo4j
import Entities
import StringIO
from Entities import Label
import random
import math

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
    items_gen = Entities.ChannelItem(query_builder)

    channel_creator_ref = user_gen.create_user()
    channel_ref, channel_uuid = channel_gen.create_channel()
    channel_items_rel_gen.set_channel_owner(channel_ref, channel_creator_ref)

    first_item, first_channel_item_uuid = items_gen.create_channel_item()
    channel_items_rel_gen.set_first_item(channel_ref, first_item)

    second_item = None

    step = 20

    for i in range(0, total_items - 1):

        if i % step == 0 and i != 0:
            print "-" * 50 + str(i)
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
                    + Label.uuid + " {" + Label.uuid + ":'" + last_channel_item_uuid + "'})\n"
    query_builder.write(channel_query)
    channel_items_rel_gen.set_last_item("channel", "last")

    i = 0
    print "-" * 50 + str(i)
    execute(query_builder.getvalue())
    connection.commit()


def create_tasks(total_tasks=10):
    pass


def create_simple_private_sphere(total_tasks=10, total_users=10):
    step = 100
    tasks_uuids = []
    users_uuids = []

    query_builder = StringIO.StringIO()
    task_gen = Entities.Task(query_builder)
    private_sphere_relations = Entities.PrivateSphereRelations(query_builder)
    stepped_insertion(query_builder, total_tasks, step, task_gen.create_task, tasks_uuids)

    print "-" * 5 + " linking objects (wait)" + "-" * 50
    # private_sphere_relations.link_all()

    j = 0
    per_cent = 0
    per_cent_step = math.ceil(float(len(tasks_uuids)) / 5)
    total_done = 0

    for task_origin_uuid in tasks_uuids:

        done = []

        for i in range(0, 10):

            task_target_uuid = tasks_uuids[random.randint(0, len(tasks_uuids) - 1)]

            if task_target_uuid == task_origin_uuid or task_target_uuid in done:
                continue

            done.append(task_target_uuid)
            private_sphere_relations. \
                link_object(
                task_origin_uuid,
                task_target_uuid,
                blacklisted=["assignee", "observer"],
                rolls=["assignee", "observer", "owner"])

            if j % 100 == 0:
                private_sphere_relations.build_subject_to_object_with_roll_name()
                commit_and_restart(query_builder)

            j += 1

        if total_done % per_cent_step == 0:
            per_cent += 1
            print str((total_done * 100) / len(tasks_uuids)) + "%"

        total_done += 1

    private_sphere_relations.build_subject_to_object_with_roll_name()
    commit_and_restart(query_builder)

    print "-" * 5 + " READY: objects linked" + "-" * 50

    user_gen = Entities.User(query_builder)
    stepped_insertion(query_builder, total_users, step, user_gen.create_user, users_uuids)

    query_builder.truncate(0)
    query_builder.seek(0)

    j = 0
    print "-" * 5 + "connecting users and tasks" + "-" * 50
    for task_uuid in tasks_uuids:

        owner_index = random.randint(0, len(users_uuids) - 1)
        assignee_index = random.randint(0, len(users_uuids) - 1)

        private_sphere_relations.add_subject_to_object_with_roll_name(users_uuids[owner_index], task_uuid, "owner")
        private_sphere_relations.add_subject_to_object_with_roll_name(users_uuids[assignee_index], task_uuid,
                                                                      "assignee")

        for i in range(0, 5):
            private_sphere_relations.add_subject_to_object_with_roll_name(
                users_uuids[random.randint(0, len(users_uuids) - 1)], task_uuid, "observer")

        if j % 3 == 0:
            private_sphere_relations.build_subject_to_object_with_roll_name()
            commit_and_restart(query_builder)

        j += 1

    print "-" * 5 + "READY: users and tasks connected" + "-" * 50
    private_sphere_relations.build_subject_to_object_with_roll_name()
    commit_and_restart(query_builder)

    print "all_done"


def create_complex_private_sphere(total_tasks=10, total_users=10):
    step = 100
    tasks_uuids = []
    users_uuids = []

    query_builder = StringIO.StringIO()
    task_gen = Entities.Task(query_builder)
    private_sphere_relations = Entities.PrivateSphereRelations(query_builder)
    stepped_insertion(query_builder, total_tasks, step, task_gen.create_task, tasks_uuids)

    print "-" * 5 + " linking objects (wait)" + "-" * 50
    # private_sphere_relations.link_all()

    j = 0
    per_cent = 0
    per_cent_step = math.ceil(float(len(tasks_uuids)) / 100)
    total_done = 0

    for task_origin_uuid in tasks_uuids:

        done = []

        for i in range(0, 10):

            task_target_uuid = tasks_uuids[random.randint(0, len(tasks_uuids) - 1)]

            if task_target_uuid == task_origin_uuid or task_target_uuid in done:
                continue

            done.append(task_target_uuid)
            private_sphere_relations.link_object(task_origin_uuid, task_target_uuid)

            if j % 100 == 0:
                private_sphere_relations.build_subject_to_object_with_roll_name()
                commit_and_restart(query_builder)

            j += 1

        if total_done % per_cent_step == 0:
            per_cent += 1
            print str((total_done * 100) / len(tasks_uuids)) + "%"

        total_done += 1

    private_sphere_relations.build_subject_to_object_with_roll_name()
    commit_and_restart(query_builder)

    print "-" * 5 + " READY: objects linked" + "-" * 50

    user_gen = Entities.User(query_builder)
    stepped_insertion(query_builder, total_users, step, user_gen.create_user, users_uuids)

    query_builder.truncate(0)
    query_builder.seek(0)

    j = 0
    print "-" * 5 + "connecting users and tasks" + "-" * 50
    for task_uuid in tasks_uuids:

        owner_index = random.randint(0, len(users_uuids) - 1)
        assignee_index = random.randint(0, len(users_uuids) - 1)

        private_sphere_relations\
            .add_subject_to_object_with_roll_node(users_uuids[owner_index], task_uuid, "owner")

        private_sphere_relations\
            .add_subject_to_object_with_roll_node(users_uuids[assignee_index], task_uuid, "assignee")

        for i in range(0, 5):
            private_sphere_relations.add_subject_to_object_with_roll_node(
                users_uuids[random.randint(0, len(users_uuids) - 1)], task_uuid, "observer")

        if j % 3 == 0:
            private_sphere_relations.build_subject_to_object_with_roll_name()
            commit_and_restart(query_builder)

        j += 1

    print "-" * 5 + "READY: users and tasks connected" + "-" * 50
    private_sphere_relations.build_subject_to_object_with_roll_name()
    commit_and_restart(query_builder)

    print "all_done"


def commit_and_restart(query_builder):
    execute(query_builder.getvalue())
    connection.commit()
    query_builder.truncate(0)
    query_builder.seek(0)


def stepped_insertion(query_builder, total_items, step, creation_method, uuids=[]):
    for i in range(0, total_items - 1):

        uuids.append(creation_method()[1])

        if i % step == 0 and i != 0:
            print "-" * 50 + str(i)
            execute(query_builder.getvalue())
            connection.commit()

            query_builder.truncate(0)
            query_builder.seek(0)

    commit_and_restart(query_builder)


def clear_all():
    query = "MATCH n return count(n) as total"
    result = connection.get_cursor().execute(query)

    (total, ) = result.next()

    step = 50

    print str(total) + " nodes to delete:"
    total_removed = 0
    for i in range(0, total, step):
        print " - " * 25 + str(total_removed)
        query = "match n with n LIMIT " + str(step) + " optional match n-[r]-() delete r, n return count(n) as removed"
        result = execute(query)
        (removed, ) = result.next()
        total_removed += removed

    connection.commit()


def execute(query):
    print query

    if execution:
        result = connection.get_cursor().execute(query)
        # connection.commit()
        return result
    else:
        print query


if __name__ == "__main__":
    print "hello"
    # clear_all();
    # for i in range(0, 1):
    # create_channel()

    create_simple_private_sphere()