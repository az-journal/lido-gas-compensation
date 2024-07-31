from dataclasses import dataclass

import yaml

from aragon_vote.definitions import CONFIG_PATH


@dataclass
class Config:
    rpc_url: str
    event: str
    blacklist: set[str] | None
    vote_id: int
    multisig_wallet_name: str
    multisig_rpc_url: str  # for testing purpose we are using safe on different chain


with open(CONFIG_PATH, "r") as fp:
    config_raw = yaml.safe_load(fp)

config = Config(**config_raw)
