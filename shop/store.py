# -*- coding: utf8 -*-


class Store(object):
    def __init__(self, source, mapper={}):
        self.mapper = mapper
        self.goods = self.load_source(source)

    def load_source(self, model_mapper):
        store = {}
        for base_cls, source in model_mapper.iteritems():
            self.load_goods(source, store, base_cls)
        return store

    def load_goods(self, source, store, base_cls):
        for name, model in source.iteritems():
            good = self.load_good(name, model, base_cls)
            store[name] = good
        return store

    def load_good(self, name, data, base_cls):
        return self.mapper.get(name, base_cls)(name, data)
