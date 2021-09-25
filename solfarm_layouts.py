from construct import Bytes, Padding, Int64ul, Int8ul, Struct

VAULT_LAYOUT = Struct(
    Padding(8),
    "authority" / Bytes(32),
    "token_program" / Bytes(32),
    "pda_token_account" / Bytes(32),
    "pda" / Bytes(32),
    "nonce" / Int8ul,
    "info_nonce" / Int8ul,
    "reward_a_nonce" / Int8ul,
    "reward_b_nonce" / Int8ul,
    "swap_to_nonce" / Int8ul,
    "total_vault_balance" / Int64ul,
    "info_account" / Bytes(32),
    "lp_token_account" / Bytes(32),
    "lp_token_mint" / Bytes(32),
    "reward_a_account" / Bytes(32),
    "reward_b_account" / Bytes(32),
    "swap_to_account" / Bytes(32),
    "total_vlp_shares" / Int64ul
)

USER_BALANCE_LAYOUT = Struct(
  Padding(8),
  "owner" / Bytes(32),
  "amount" / Int64ul
)
