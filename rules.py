from entities import Believes, Said, SharedKey, EncryptedFormula, Fresh, Controls


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
        if key.obj.actor1 == actor1:
            actor2 = key.obj.actor2
        else:
            actor2 = key.obj.actor1

        return [Believes(actor1, Said(actor2, msg.obj))]


class NonceVerification(Rule):
    def argsCount(self):
        return 2

    def apply(self, nonce, msg):
        if not isinstance(nonce, Believes): return []
        if not isinstance(nonce.obj, Fresh): return []
        if not isinstance(msg, Believes): return []
        if not isinstance(msg.obj, Said): return []
        if nonce.actor != msg.actor: return []
        if nonce.obj.obj != msg.obj.obj: return []

        return [Believes(msg.actor, Believes(msg.obj.actor, msg.obj.obj))]


class Jurisdiction(Rule):
    def argsCount(self):
        return 2

    def apply(self, controls, msg):
        if not isinstance(controls, Believes): return []
        if not isinstance(controls.obj, Controls): return []
        if not isinstance(msg, Believes): return []
        if not isinstance(msg.obj, Believes): return []
        if controls.actor != msg.actor: return []
        if controls.obj.actor != msg.obj.actor: return []
        if controls.obj.obj != msg.obj.obj: return []

        return [Believes(msg.actor, msg.obj.obj)]


class Decomposition(Rule):
    def argsCount(self):
        return 1

    def apply(self):
        pass
