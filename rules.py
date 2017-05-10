from entities import Believes, SharedKey, EncryptedFormula

class Rule(object):
    def argsCount(self):
        raise NotImplementedError()

    def apply(self, *args, **kwargs):
        raise NotImplementedError()

class Decryption(Rule):
    def argsCount(self):
        return 2

    def apply(self, key, msg):
        if not isinstance(key, Believes): return []
        if not isinstance(key.obj, SharedKey): return []
        if not isinstance(msg, EncryptedFormula): return []
        if key.obj != msg.key: return []

        actor1 = key.actor
        pass



class NonceVerification(Rule):
    def argsCount(self):
        return 2

class Jurisdiction(Rule):
    def argsCount(self):
        return 2

class Decomposition(Rule):
    def argsCount(self):
        return 2
