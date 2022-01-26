from unittest.mock import Mock
import pytest
from eth_abi.codec import ABICodec
from web3._utils.abi import build_default_registry

from starknet_py.net.l1.messages import (
    L1ToL2Message,
    L2ToL1Message,
    L1ToL2MessageContent,
    L2ToL1MessageContent,
)
from starknet_py.net.models import StarknetChainId


@pytest.mark.asyncio
async def test_l1_l2_messages():
    mock_w3 = Mock()
    mock_messages_amt = 123

    def mock_call(_tx, _bn) -> bytes:
        return mock_messages_amt.to_bytes(32, "big")

    mock_w3.eth.call = mock_call
    mock_w3.codec = ABICodec(build_default_registry())

    l2_to_l1 = await L2ToL1Message.from_content(
        L2ToL1MessageContent(l2_sender=123, l1_recipient=123, payload=[])
    ).count_queued(
        chain_id=StarknetChainId.TESTNET,
        web3=mock_w3,
    )

    l1_to_l2 = await L1ToL2Message.from_content(
        L1ToL2MessageContent(
            l1_sender=123,
            l2_recipient=123,
            nonce=1,
            function_name="dummy",
            payload=[],
        )
    ).count_queued(chain_id=StarknetChainId.TESTNET, web3=mock_w3)

    assert l1_to_l2 == mock_messages_amt
    assert l2_to_l1 == mock_messages_amt
