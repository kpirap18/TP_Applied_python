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
        pass

    def delete():
        pass
    
    def replace():
        pass
    
    def optimize():
        pass
    
    def get_actions():
        pass


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
    pass


class ReplaceAction(Action):
    pass


class DeleteAction(Action):
    pass


h = TextHistory('weweqwewfwef\nwefwefwef')
print(h)
