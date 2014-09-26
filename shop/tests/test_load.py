# -*- coding: utf8 -*-
import pytest
import sys
print sys.path

from shop.base_good import BaseGood
from shop.store import Store


@pytest.fixture
def goods_static():
    return {
        'coins': {},
        'energy': {}
    }


@pytest.fixture
def source(goods_static):
    return {
        BaseGood: goods_static,
        TestBillingGood: {
            'vip': {}
        }
    }


@pytest.fixture
def store(source):
    return Store(source, {'energy': TestEnergyGood})


class TestEnergyGood(BaseGood):
    def buy(self, user, count):
        user['energy'] += count
        return user


class TestAnotherGood(BaseGood):
    pass


class TestBillingGood(BaseGood):
    pass


def test_default_good(store, goods_static):
    goods = store.load_goods(goods_static, {}, BaseGood)
    for good in goods.values():
        assert isinstance(good, BaseGood)


def test_mapper(goods_static, source):
    store = Store(source, {'energy': TestAnotherGood})
    assert isinstance(
        store.load_good('energy', goods_static['energy'], BaseGood),
        TestAnotherGood
    )


def test_load_sources(store):
    goods = store.load_source({
        BaseGood: {'food': {}}, TestBillingGood: {'vip': {}}
    })
    assert isinstance(goods['food'], BaseGood)
    assert isinstance(goods['vip'], TestBillingGood)


def test_init(store):
    assert isinstance(store.goods['energy'], TestEnergyGood)
    assert isinstance(store.goods['coins'], BaseGood)
    assert isinstance(store.goods['vip'], BaseGood)


def test_buy(store):
    user = {'energy': 0}
    assert store.buy('energy', user, 30)
