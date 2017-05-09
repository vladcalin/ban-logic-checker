import random
import string

"""
Not yet finished. We might have to rethink a little bit how
we will model the logic constructions
"""


class BanObject(object):
    @staticmethod
    def get_rand_token(chars):
        return "".join([random.choice(string.hexdigits) for _ in range(chars)])


class BanActor(BanObject):
    pass


class BanConstruction(object):
    pass


class Believes(BanConstruction):
    def __init__(self, actor, obj):
        """
        ACTOR believes OBJ
        """
        self.actor = actor
        self.obj = obj


class Sees(BanConstruction):
    def __init__(self, actor, obj):
        """
        ACTOR sees OBJ
        """
        self.actor = actor
        self.obj = obj


class Said(BanConstruction):
    def __init__(self, actor, obj):
        """
        ACTOR said OBJ
        """
        self.actor = actor
        self.obj = obj


class Controls(BanConstruction):
    def __init__(self, actor, obj):
        """
        ACTOR controls OBJ
        """
        self.actor = actor
        self.obj = obj


class Fresh(BanConstruction):
    def __init__(self, obj):
        """
        OBJ is fresh
        """
        self.obj = obj


class SharedKey(BanConstruction):
    def __init__(self, key, actor1, actor2):
        """
        ACTOR1 and ACTOR2 may use the shared key KEY to communicate.
        """
        self.key = key
        self.actor1 = actor1
        self.actor2 = actor2


class HasPublicKey(BanConstruction):
    def __init__(self, actor, pub_key):
        """
        ACTOR has a public key PUB_KEY. The corresponding private key is PUB_KEY^(-1)
        """
        self.actor = actor
        self.pub_key = pub_key


class SharedSecret(BanConstruction):
    def __init__(self, actor1, actor2, secret):
        """
        ACTOR1 and ACTOR2 share a common secret SECRET
        """
        self.actor1 = actor1
        self.actor2 = actor2
        self.secret = secret


class Message(BanObject):
    def __init__(self, identifier, *msgs):
        self.msgs = msgs
        self.id = identifier


class EncryptedFormula(Message):
    def __init__(self, obj, key):
        self.obj = obj
        self.key = key
        super(EncryptedFormula, self).__init__("{{}}_{}".format(self.obj, self.key), obj)

    def __repr__(self):
        return "{{}}_{}".format(self.obj, self.key)


if __name__ == '__main__':
    Message("X")
    Message(Message("X"), Message("Y"))
