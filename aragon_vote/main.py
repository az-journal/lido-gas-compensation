import asyncio

import ape.exceptions
from ape import accounts, networks

from aragon_vote.abi.aragon_voting import ARAGON_VOTING_ABI
from aragon_vote.config import config
from aragon_vote.gas_calculator import GasCalculator
from aragon_vote.multisig import prepare_multisig


async def main():
    event_scraper = GasCalculator(
        address="0x2e59A20f205bB85a89C53f1936454680651E618e",
        abi=ARAGON_VOTING_ABI
    )
    spent_on_gas_by_user = await event_scraper.get_spent_gas()
    for user, amount in spent_on_gas_by_user.items():  # dct.iteritems() in Python 2
        print("{} {} eth".format(user, amount / 10 ** 18))
    print(f"total spent: {sum(spent_on_gas_by_user.values()) / 10 ** 18}")

    compensate = input("Compensate y/n?")
    if compensate.lower() == "y":
        with networks.ethereum.sepolia.use_provider(config.multisig_rpc_url):
            safe = accounts.load(config.multisig_wallet_name)
            send_tx = prepare_multisig(spent_on_gas_by_user)
            try:
                send_tx(sender=safe, value=sum(spent_on_gas_by_user.values()), submit=False)
            except ape.exceptions.SignatureError:
                pass
            print("tx prepared, use ape safe to send")


if __name__ == '__main__':
    asyncio.run(main())
