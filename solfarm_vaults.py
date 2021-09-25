from solfarm_layouts import VAULT_LAYOUT, USER_BALANCE_LAYOUT
from solana.publickey import PublicKey
from solana.rpc.api import Client
import base64

SOLANA_ENDPOINT = 'https://api.mainnet-beta.solana.com'
SOLFARM_PROGRAM_ID = '7vxeyaXGLqcp66fFShqUdHxdacp4k4kwUpRSSeoZLCZ4'

def main():
    """
    Solana Python API built on the JSON RPC API:
    https://github.com/michaelhly/solana-py

    """

    # Public Key with Solfarm RAY-SOL vault
    user_public_key = '6bTMLVCXWHu3suWzorXM6x9AVm5DMLoDPhcJ3dVJBaKn' 
    print('public key:', user_public_key)

    # RAY-SOL vault
    vault_account = 'HbLCyHdEK2btVvYny87as5xx9ap7RdMdXAMujSE5Ukw1' # RAY-SOL account, from https://gist.github.com/therealssj/c6049ac59863df454fb3f4ff19b529ee#file-solfarm_ray_vault-json-L1041
    vault_info_account = 'Hdp4Dk9xXDV5ezofS61Y8Q8iQ6EXU9TMwVSWm5Gk8eYu' # RAY-SOL oldInfoAccount, from https://gist.github.com/therealssj/c6049ac59863df454fb3f4ff19b529ee#file-solfarm_ray_vault-json-L1045
    LP_decimals = 6 

    # Get vault info
    solana = Client(SOLANA_ENDPOINT)
    vault_raw_data = solana.get_account_info(vault_account, commitment='confirmed')
    vault_decoded_data = VAULT_LAYOUT.parse(base64.b64decode(vault_raw_data['result']['value']['data'][0]))
    total_vault_balance = vault_decoded_data.total_vault_balance / (10 ** LP_decimals)
    total_vault_shares = vault_decoded_data.total_vlp_shares
    print('total_vault_balance:', total_vault_balance)
    print('total_vlp_shares:', total_vault_shares)

    # Find user balance account
    seeds = [bytes(PublicKey(vault_info_account)), bytes(PublicKey(user_public_key))]
    program_id = PublicKey(SOLFARM_PROGRAM_ID)
    user_balance_account, nonce = PublicKey.find_program_address(seeds=seeds, program_id=program_id)
    print('user_balance_account:', user_balance_account)

    # Get user shares and tokens
    user_balance_raw_data = solana.get_account_info(user_balance_account, commitment='confirmed') 
    user_balance_decoded_data = USER_BALANCE_LAYOUT.parse(base64.b64decode(user_balance_raw_data['result']['value']['data'][0]))
    user_vault_LP_shares = user_balance_decoded_data.amount
    user_vault_LP_tokens = total_vault_balance * (user_vault_LP_shares / total_vault_shares)
    print('user_vault_LP_shares:', user_vault_LP_shares)
    print('user_vault_LP_tokens:', user_vault_LP_tokens)

if __name__ == '__main__':
    main()