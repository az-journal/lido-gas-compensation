from ape_safe import multisend
from hexbytes import HexBytes


def prepare_multisig(spent_on_gas_by_user: dict[str, int]) -> multisend.MultiSend:
    txn = multisend.MultiSend()

    for user, value in spent_on_gas_by_user.items():
        txn.calls.append(
            {
                "operation": 0,
                "target": user,
                "value": value,
                "callData": HexBytes("0x"),
            }
        )
    return txn
