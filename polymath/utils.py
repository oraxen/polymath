import os
import json
import collections.abc


def get_path(name):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), name)


class SavedDict(collections.abc.MutableMapping):
    def __init__(self, file_name):
        self.file = get_path(file_name)

        if not os.path.isfile(self.file):
            self.store = dict()
        else:
            with open(self.file, "r") as json_file:
                self.store = json.load(json_file)
                if type(self.store) is not dict:
                    raise ValueError()

    def write(self):
        with open(self.file, "w") as outfile:
            json.dump(self.store, outfile)

    def __getitem__(self, key):
        return self.store[self._keytransform(key)]

    def __setitem__(self, key, value):
        self.store[self._keytransform(key)] = value
        self.write()

    def __delitem__(self, key):
        del self.store[self._keytransform(key)]
        self.write()

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def _keytransform(self, key):
        return str(key)
