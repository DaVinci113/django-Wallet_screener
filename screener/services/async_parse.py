# import json
# from screener.models import Address
# import aiohttp
# import asyncio
# from config_parse import headers, params, devision, time_out
#
#
# async def a_get_token_amount_cosmostation(chain, user_address):
#     async with aiohttp.ClientSession(timeout=time_out) as session:
#         async with session.get(
#                 f'https://lcd-{chain}.cosmostation.io/cosmos/staking/v1beta1/delegations/{user_address}',
#                 params=params,
#                 headers=headers,
#         ) as response:
#             response_staked = await response.json()
#
#         async with session.get(
#                 f'https://lcd-{chain}.cosmostation.io/cosmos/bank/v1beta1/balances/{user_address}',
#                 params=params,
#                 headers=headers,
#         ) as response:
#             response_available = await response.json()
#
#         async with session.get(
#                 f'https://lcd-{chain}.cosmostation.io/cosmos/distribution/v1beta1/delegators/{user_address}/rewards',
#                 params=params,
#                 headers=headers,
#         ) as response:
#             response_reward = await response.json()
#
#         stake = 0
#         reward = 0
#
#         count_validators = 0
#         for num in response_staked:
#             if 'delegation_responses' in num:
#                 count_validators += 1
#
#         for i in range(count_validators):
#             stake += float(response_staked['delegation_responses'][0]['balance']['amount']) / devision[chain]
#             reward += float(response_reward['rewards'][i]['reward'][-1]['amount']) / devision[chain]
#
#         available = float(response_available['balances'][-1]['amount']) / devision[chain]
#
#         user_address.stake = stake
#         user_address.available = available
#         user_address.reward = reward
#
#
# async def main(addresses):
#     dct = {}
#     task_list = []
#     for address in addresses:
#         chain = address[:-39]
#         task_list.append(asyncio.create_task(a_get_token_amount_cosmostation(chain, address)))
#     await asyncio.gather(*task_list)
#
#
# if __name__ == '__main__':
#     all_addresses = Address.objects.all().only('id')
#     asyncio.run(main(all_addresses))
