import tda
from tda.auth import client_from_manual_flow
import os

if __name__ == "__main__":

    api_key='LLGYGYRSAMWGZJNMXY8B8KGTOYG9BNDU@AMER.OAUTHAP'
    redirect_url='https://academycity.org/en/corporatevaluation/options'
    token_path='/home/amos/projects/development/academycity/data/corporatevaluation/options/token/token'
    client = client_from_manual_flow(api_key, redirect_url, token_path, asyncio=False)