import imp
from multiprocessing.spawn import import_main_path
from brownie import config, network, accounts
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENT
from scripts.simple_collectible.deploy_and_create import deploy_and_create
import pytest


def test_can_create_simple_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        pytest.skip()
    simple_collectible = deploy_and_create()
    assert simple_collectible.ownerOf(0) == get_account()