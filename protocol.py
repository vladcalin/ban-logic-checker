import random
import string
from entities import SharedKey, EncryptedFormula, Message


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

    def __repr__(self):
        return self.id


class Value(ProtocolObject):
    def __init__(self, identifier=None):
        if not identifier:
            identifier = "value-{}".format("".join([random.choice(string.hexdigits) for _ in range(5)]))
        super(Value, self).__init__(identifier)

    def __eq__(self, other):
        if not isinstance(other, Value):
            return False

        return self.id == other.id

    def __repr__(self):
        return self.id


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
        return "Step({}, {} -> {})".format(self.msg, self.channel.actor1.name, self.channel.actor2.name)


class ProtocolSpecification(object):
    def __init__(self, name, actors, assumptions, channels, steps):
        self.name = name
        self.actors = actors
        self.assumptions = assumptions
        self.channels = channels
        self.steps = steps

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
    server = ProtocolActor("server")

    K_as = Value("K_as")
    K_sb = Value("K_sb")
    K_ab = Value("K_ab")
    K_bs = Value("K_bs")

    shared_key_a_s = SharedKey(K_as, alice, server)
    shared_key_s_b = SharedKey(K_sb, server, bob)
    shared_key_a_b = SharedKey(K_ab, alice, bob)

    Ts = Nonce("Ts")
    Ta = Nonce("Ta")

    a_to_b = ProtocolChannel("a_to_b", alice, bob)
    b_to_a = ProtocolChannel("b_to_a", bob, alice)
    s_to_a = ProtocolChannel("s_to_a", server, alice)

    protocol_kerberos = ProtocolSpecification(
        name="kerberos",
        actors=(alice, bob, server),
        assumptions=[
        ],
        channels=[
            a_to_b, b_to_a, s_to_a
        ],
        steps=[
            ProtocolStep(s_to_a, EncryptedFormula(
                Message(Ts, shared_key_a_b, EncryptedFormula(Message(Ts, shared_key_a_b), K_bs)),
                K_as)),
            ProtocolStep(a_to_b, Message(
                EncryptedFormula(Message(Ts, shared_key_a_b), K_bs),
                EncryptedFormula(Message(Ta, shared_key_a_b), K_ab)
            )),
            ProtocolStep(b_to_a, EncryptedFormula(Message(Ta, shared_key_a_b), K_ab)),
        ]
    )

    print(protocol_kerberos)
