import httpx


class Telegram:
    def __init__(self, token: str):
        self._token = token

    @property
    def send_url(self):
        return f'https://api.telegram.org/bot{self._token}/sendMessage'

    @property
    def updates_url(self):
        return f'https://api.telegram.org/bot{self._token}/getUpdates'

    def send_message(self, cids: set[int], message: str, markdown=False):
        send_info = dict()
        for cid in cids:
            with httpx.Client() as client:
                try:
                    client.headers['Content-Type'] = 'application/json'
                    res = client.post(self.send_url, json={'chat_id': cid, 'text': message} | ({'parse_mode': 'Markdown'} if markdown else {}))
                    send_info |= {
                        cid: res.json()
                    }
                except httpx.TransportError:
                    send_info |= {
                        cid: None
                    }
        return send_info

    def get_updates(self):
        with httpx.Client() as client:
            try:
                client.headers['Content-Type'] = 'application/json'
                res = client.post(self.updates_url)
                return res.json()
            except httpx.TransportError:
                return None
