from brownie import (
    accounts,
    config,
    network,
    VRFCoordinatorMock,
    LinkToken,
    Contract,
    chain
)
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENT = ["hardhat", "development", "ganache", "mainnet-fork"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        return accounts[0]
    if id:
        return accounts.load(id)
    if network.show_active() in config["networks"]:
        return accounts.add(config["wallets"]["from_key"])
    return None

amount = Web3.toWei(0.1, "ether")

def fund_with_link(
    contract_address, account=None, link_token=None, amount=amount
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    funding_tx = link_token.transfer(contract_address, 1000000000000000000, {"from": account})
    funding_tx.wait(1)
    print(f"Funded {contract_address}")
    return funding_tx


contract_to_mock = {
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT:  # Local
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:  # online
        contract_address = config["networks"][network.show_active()][contract_name]
        # address
        # ABI
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
        # MockV3Aggregator.abi
    return contract


DECIMALS = 18
INITIAL_VALUE = 2000


def deploy_mocks(decimal=DECIMALS, initial=INITIAL_VALUE):
    account = get_account()
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(
        link_token, {"from": account.address, "gas_price": chain.base_fee}
    )
    print("Deployed!")
