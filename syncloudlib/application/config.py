from connection import api_post, api_get


def set_dkim_key(dkim_key):
    return api_post('/config/dkim_key', data={"dkim_key": dkim_key})


def get_dkim_key():
    return api_get('/config/dkim_key')
