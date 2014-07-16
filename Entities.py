__author__ = 'alacambra'
import time


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

    def get_query(self):
        item_type = "bce"
        ref = "CI" + str(self.counter)
        query = "CREATE (" + ref + ":" + item_type + ": " \
                "{time: " + get_time_as_str() + ", type:'" + item_type + "'})"

        self.last_ref = ref
        return query


class Channel:

    counter = 0

    def __init__(self):
        self.counter = 0

    def get_query(self):
        ref = "CH" + str(self.counter)
        query = "CREATE (" + ref + ":CHANNEL " \
                "{time: " + get_time_as_str() + "})"

        self.counter += self.counter;
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
                ", name:'username" + get_random_str() + "'"\
                ", occupation:'ocupation" + get_random_str() + "'"\
                ", private:" + str(True).lower() + \
                ", connectivity:'" + get_connectivity_value(self.counter) + "'" \
                ", dateModified:" + get_time_as_str() + \
                ", postalCode:123654})"

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
                ", name: 'task" + get_random_str() + "'"\
                ", description:'ipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsumipsum'" \
                ", location:'some place'" \
                ", private:" + str(True).lower() + \
                ", connectivity:'" + get_connectivity_value(self.counter) + "'"\
                ", dateModified:" + get_time_as_str() + \
                ", startDate:" + get_time_as_str() + \
                ", endDate:" + get_time_as_str() + \
                ", timeRequired:123654})"

        self.last_ref = ref
        self.counter += 1;
        return query


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
