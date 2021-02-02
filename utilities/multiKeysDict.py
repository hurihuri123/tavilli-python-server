from collections import defaultdict


class MultiKeysDict(object):
    def __init__(self):
        super().__init__()
        self.dict = defaultdict(dict)  # Special dict that supports 2 keys

    def newItem(self, data, offset1, offset2):
        self.dict[offset1][offset2] = data

    def readItem(self, offset1, offset2):
        item = None
        try:
            item = self.dict[offset1][offset2]
        except:
            pass  # offset doesn't exists
        finally:
            return item

    def items(self):
        return self.dict.items()
