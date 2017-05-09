import random
import string


class ProtocolActor(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Actor('{}')".format(self.name)

    def generate_nonce(self):
        token = "".join([random.choice(string.hexdigits) for _ in range(5)])
        return Nonce("{}-nonce-{}".format(self.name, token))


class ProtocolObject(object):
    def __init__(self, identifier):
        self.id = identifier


class Nonce(ProtocolObject):
    def __init__(self, identifier=None):
        if not identifier:
            identifier = "nonce-{}".format("".join([random.choice(string.hexdigits) for _ in range(5)]))
        super(Nonce, self).__init__(identifier)


class Value(ProtocolObject):
    def __init__(self, identifier=None):
        if not identifier:
            identifier = "nonce-{}".format("".join([random.choice(string.hexdigits) for _ in range(5)]))
        super(Value, self).__init__(identifier)


class EncryptedValue(ProtocolObject):
    def __init__(self, key, *items):
        self.key = key
        self.items = items
        super(EncryptedValue, self).__init__("{{}}_{}".format(self.items, self.key))


class ProtocolChannel(object):
    def __init__(self, identifier, actor1, actor2):
        """
        Represents the communication channel from ACTOR1 to ACTOR2
        """
        self.id = identifier
        self.actor1 = actor1
        self.actor2 = actor2

    def __repr__(self):
        return "Channel(id='{}', {} -> {})".format(self.id, self.actor1.name, self.actor2.name)


class ProtocolStep(object):
    def __init__(self, channel, msg):
        self.channel = channel
        self.msg = msg
    
    def __repr__(self):
        return "Step({}, {} -> {})", self.msg, self.channel.actor1.name, self.channel.actor2.name


class ProtocolSpecification(object):
    def __init__(self, name, actors, channels, steps):
        self.name = name
        self.actors = actors
        self.steps = steps
        self.channels = channels

    def __repr__(self):
        template = """
Protocol {}

Actors:
\t{}

Channels:
\t{}

Steps:
\t{}
        """

        return template.format(
            self.name, self._get_actors_repr(), self._get_channels_repr(), self._get_steps_repr()
        )

    def _get_actors_repr(self):
        return "\n\t".join(str(a) for a in self.actors)

    def _get_channels_repr(self):
        return "\n\t".join(str(c) for c in self.channels)

    def _get_steps_repr(self):
        return "\n\t".join(str(s) for s in self.steps)


if __name__ == '__main__':
    alice = ProtocolActor("alice")
    bob = ProtocolActor("bob")

    protocol = ProtocolSpecification(
        name="example_protocol",
        actors=(alice, bob),
        channels=[
            ProtocolChannel("a_to_b", alice, bob),
            ProtocolChannel("b_to_a", bob, alice)
        ],
        steps=[
        ]
    )

    print(protocol)
