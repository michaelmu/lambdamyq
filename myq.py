import datetime
import json
import base64
import urllib.parse
import asyncio
from pymyq import login
from pymyq.api import API
from pymyq.account import MyQAccount
from pymyq.garagedoor import MyQGaragedoor
from aiohttp import ClientSession

STATE_CLOSED = "closed"
STATE_CLOSING = "closing"
STATE_OPEN = "open"
STATE_OPENING = "opening"
STATE_STOPPED = "stopped"
STATE_TRANSITION = "transition"
STATE_AUTOREVERSE = "autoreverse"
STATE_UNKNOWN = "unknown"

MYQ_EMAIL = "michael.musson@gmail.com"
MYQ_PASSWORD = "myq2023FTW!"

GARAGE_DOOR_OPENER = "CG0846A0A31B"
MYQ_ACCOUNT = "ef50064e-60cb-4ab4-a794-2e986e251cec"

ACTION_OPEN = "open"
ACTION_CLOSE = "close"
ACTION_GETSTATE = "get_state"

MODE_TEST = "test_mode"
MODE_NONTEST = "nontest_mode"

PIN = "3338"

async def get_devices(api: API):
    await api.update_device_info()
    device_json = list()
    for device_id in api.devices:
        device_json.append(api.devices[device_id].device_json)
    return device_json

async def get_garagedoor_json(api: API):
    await api.update_device_info()
    for device_id in api.devices:
        device_json = api.devices[device_id].device_json
        if device_json['serial_number'] == GARAGE_DOOR_OPENER:
            return device_json
    return None

async def get_garagedoor_state():
    async with ClientSession() as websession:
        api = await login(MYQ_EMAIL, MYQ_PASSWORD, websession)
        garage_json = await get_garagedoor_json(api)
        account = api.accounts[MYQ_ACCOUNT]
        return MyQGaragedoor(garage_json, account, None).device_state

async def open_garagedoor():
    async with ClientSession() as websession:
        api = await login(MYQ_EMAIL, MYQ_PASSWORD, websession)
        garage_json = await get_garagedoor_json(api)
        account = api.accounts[MYQ_ACCOUNT]
        await MyQGaragedoor(garage_json, account, None).open()


async def close_garagedoor():
    async with ClientSession() as websession:
        api = await login(MYQ_EMAIL, MYQ_PASSWORD, websession)
        garage_json = await get_garagedoor_json(api)
        account = api.accounts[MYQ_ACCOUNT]
        await MyQGaragedoor(garage_json, account, None).close()

def lambda_handler(event, context):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # decode our parameters
    if "body" in event.keys():
        raw_params = base64.b64decode(event.get("body")).decode('utf-8')
        # Use qsl to only get one value per param key
        params = dict(urllib.parse.parse_qsl(raw_params))
        if params.get("mode", MODE_NONTEST) and params.get("pin", "unknown") == PIN:
            # Only allow open/close in non-test mode with correct pin
            if params.get("action", "unknown") == ACTION_OPEN:
                asyncio.get_event_loop().run_until_complete(open_garagedoor())
            if params.get("action", "unknown") == ACTION_CLOSE:
                asyncio.get_event_loop().run_until_complete(close_garagedoor())
    state = asyncio.get_event_loop().run_until_complete(get_garagedoor_state())
    return {
        'statusCode': 200,
        'body': json.dumps({
            "current_time": current_time,  
            "state": state, 
            "event": json.dumps(event), 
            }
        )
    }
        
    