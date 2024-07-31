import asyncio
from typing import Any

from eth_typing import HexStr
from web3 import AsyncWeb3, AsyncHTTPProvider

from aragon_vote.config import config


class GasCalculator:
    def __init__(self, address: str, abi: list[Any]):
        self.w3 = AsyncWeb3(
            provider=AsyncHTTPProvider(config.rpc_url),
            request_kwargs={"timeout": 600}
        )
        self.contract = self.w3.eth.contract(
            address=self.w3.to_checksum_address(address),
            abi=abi
        )

    async def get_transaction(self, tx_hash: HexStr, semaphore: asyncio.BoundedSemaphore) -> Any:
        async with semaphore:
            return await self.w3.eth.get_transaction(tx_hash)

    async def get_transaction_receipt(self, tx_hash: HexStr, semaphore: asyncio.BoundedSemaphore) -> Any:
        async with semaphore:
            return await self.w3.eth.get_transaction_receipt(tx_hash)

    async def get_spent_gas(self) -> dict[str, int]:
        semaphore = asyncio.BoundedSemaphore(5)
        events = await self.contract.events[config.event].get_logs(fromBlock=0,
                                                                   argument_filters={'voteId': config.vote_id})
        txs = await asyncio.gather(*[self.get_transaction(event["transactionHash"], semaphore) for event in events])
        txs_receipts = await asyncio.gather(
            *[self.get_transaction_receipt(event["transactionHash"], semaphore) for event in events])

        txs = [tx for tx in txs if not config.blacklist or tx["from"] not in config.blacklist]
        txs_receipts = [tx for tx in txs_receipts if not config.blacklist or tx["from"] not in config.blacklist]

        return {
            tx["from"]: txs_receipts[tx_num]["gasUsed"] * tx["gasPrice"]
            for tx_num, tx in enumerate(txs)
        }
