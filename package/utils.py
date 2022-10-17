from browser import window
import json

from . import config


def getBlockAttrs(id):
    return window.fetch(
        f"{config.protocol}://{config.host}/api/attr/getBlockAttrs",
        {
            'body': json.dumps({'id': id}),
            'method': 'POST',
            'headers': config.headers,
        }
    ).then(
        lambda response: response.json()
    ).catch(lambda error: print('error', error))


def setBlockAttrs(id, attrs):
    return window.fetch(
        f"{config.protocol}://{config.host}/api/attr/setBlockAttrs",
        {
            'body': json.dumps({
                'id': id,
                'attrs': attrs,
            }),
            'method': 'POST',
            'headers': config.headers,
        }
    ).then(
        lambda response: response.json()
    ).catch(lambda error: print('error', error))
