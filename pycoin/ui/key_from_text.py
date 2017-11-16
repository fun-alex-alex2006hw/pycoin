import binascii

from ..encoding import a2b_hashed_base58, EncodingError
from ..serialize import h2b
from ..contrib.segwit_addr import bech32_decode


def key_info_from_text(text, networks):
    from pycoin.ui.uiclass import metadata_for_text
    metadata = metadata_for_text(text)
    for network in networks:
        info = network.ui.parse_metadata_to_info(metadata, types=["key"])
        if info:
            yield network, info["info"]


def key_from_text(text, generator=None, key_types=None, networks=None):
    """
    This function will accept a BIP0032 wallet string, a WIF, or a bitcoin address.

    The "is_compressed" parameter is ignored unless a public address is passed in.
    """
    from ..networks.registry import network_codes, network_for_netcode
    networks = networks or [network_for_netcode(netcode) for netcode in network_codes()]
    for network, key_info in key_info_from_text(text, networks=networks):
        return key_info["key_class"](**key_info["kwargs"])
    return None
