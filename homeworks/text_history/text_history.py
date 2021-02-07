from abc import ABC, abstractmethod
from math import inf

class TextHistory:
    def __init__(self, text='', actions=None, version=0):
        self._actions = [] if not actions else actions
        self._text = text
        self._version = version
        
    def __str__(self):
        return "TextHistory(ver.{}):\n{}".format(self._version, self._text)
    
    @property
    def text(self):
        return self._text
    
    @property
    def version(self):
        return self._version
    
    def action(self, act):
        if act._from_version != self._version:
            raise ValueError("Action version deffers from current text version.")
        self._text = act.apply(self._text)
        self._actions.append(act)
        self._version = act.to_version
        return act.to_version
    
    def insert(self, text, pos=None):
        if pos is None:
            pos = len(self._text)
        act = InsertAction(text, pos, self._version, self._version + 1)
        return self.action(act)

    def delete():
        pass
    
    def replace():
        pass
    
    def optimize(self, actions):
        id = 0
        while id < len(actions) - 1:
            f_act = actions[id]
            s_act = actions[id + 1]
            if f_act.merge(s_act):
                actions.pop(id + 1)
            id += 1
        return actions
        
    
    def get_actions(self, from_v = None, to_v = None):
        if from_v is None:
            from_v = 0
        if to_v is None:
            to_v = inf
        if from_v < 0 or to_v < 0:
            raise ValueError("Versions can not be negative.")
        if from_v > to_v:
            raise ValueError("Bad version range (from < to)")
        if to_v != inf and to_v > self._actions[-1].to_version:
            raise ValueError("Given version out of range")

        actions = []
        for action in self._actions:
            if action.from_version >= from_v and action.to_version <= to_v:
                action.append(action)
        return self.optimize(actions)
        


class Action(ABC):
    def __init__(self, from_v, to_v):
        if from_v >= to_v or from_v < 0 or to_v < 0:
            raise ValueError("Wrong version values.")
        self._from_version = from_v
        self._to_version = to_v

    @property
    def from_version(self):
        return self._from_version
    
    @property
    def to_version(self):
        return self._to_version

    @abstractmethod
    def apply(self, apply_to):
        pass


class InsertAction(Action):
    def __init__(self, text, pos, from_v,  to_v):
        if pos is not None and int(pos) < 0:
            raise ValueError("Pos can not be negative")
        self._text = text
        self._pos = pos
        super().__init__(from_v, to_v)

    def __repr__(self):
        return "InsertAction(text={}, pos='{}', from_version={}, to_version={})" \
               .format(self._text, self._pos, self._from_version, self._to_version)

    @property
    def text(self):
        return self._text

    @property
    def pos(self):
        return self._pos
    
    def apply(self, apply_to):
        if len(apply_to) < self._pos:
            raise ValueError("Insert position {} out of string length {}." \
                             .format(self._pos, len(apply_to)))
            return apply_to[:self._pos] + self._text + apply_to[self._pos:]


class ReplaceAction(Action):
    pass


class DeleteAction(Action):
    pass


h = TextHistory('weweqwewfwef\nwefwefwef')
print(h)
