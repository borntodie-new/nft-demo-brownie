from brownie import AdvanceCollectible, config, network
from scripts.helpful_scripts import (
    get_account,
    OPENSEA_URL,
    get_contract,
    fund_with_link,
)

sample_token_uri = (
    "ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
)


def deploy_and_create():
    account = get_account()
    # We want to be able to use the deployed contracts if we are on a testnet
    # Otherwide, we want to deploy some mocks and use those
    # Rinkeby
    advance_collectible = AdvanceCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
    )
    fund_with_link(advance_collectible.address)
    creating_tx = advance_collectible.createCollectible({"from": account})
    creating_tx.wait(1)
    print("New token has been created!")


def main():
   deploy_and_create()
