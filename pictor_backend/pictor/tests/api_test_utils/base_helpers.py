from faker import Faker
import json
import random
import requests
from loguru import logger as test_logger

username = 'alan'
password = 'fu030632'
domain = 'http://192.168.1.105:8888/api'

fake = Faker("zh_CN")

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'


def get_token(resp):
    return json.loads(resp.text)['token']


def get_headers(token):
    return {
        'User-Agent': user_agent,
        'Content-Type': 'application/json',
        'Authorization': 'PICTOR {}'.format(token)
    }


def get_no_token_headers():
    return {
        'User-Agent': user_agent,
        'Content-Type': 'application/json',
    }


def get_file_headers(token):
    return {
        'User-Agent': user_agent,
        'Authorization': 'PICTOR {}'.format(token)
    }


class BaseAPI(object):
    """请求基础类, 包括认证与增删改查"""
    def __init__(self, domain, uri='', token=None):
        self.domain = domain
        self.uri = uri
        self.token = token
        self.user = None
        self.success = []
        self.warning = []
        self.error = []

    def base_request(self, url, is_file=False, method='get', *args, **kwargs):
        if is_file:
            headers = get_file_headers(self.token)
        else:
            headers = get_headers(self.token)
        files = kwargs.get('files', None)
        updated_files = kwargs.get('updated_files', None)
        if method.lower() == 'get':
            if is_file:
                resp = requests.get(url=url, headers=headers, params=kwargs, files=files)
            else:
                resp = requests.get(url=url, headers=headers, params=kwargs)
        elif method.lower() == 'post':
            if is_file:
                resp = requests.post(url=url, headers=headers, data=kwargs, files=files)
            else:
                resp = requests.post(url=url, headers=headers, data=json.dumps(kwargs))
        elif method.lower() == 'put':
            if is_file:
                resp = requests.put(url=url, headers=headers, data=kwargs, files=updated_files)
            else:
                resp = requests.put(url=url, headers=headers, data=json.dumps(kwargs))
        elif method.lower() == 'patch':
            if is_file:
                resp = requests.patch(url=url, headers=headers, data=kwargs, files=updated_files)
            else:
                resp = requests.patch(url=url, headers=headers, data=json.dumps(kwargs))
        elif method.lower() == 'delete':
            if is_file:
                resp = requests.delete(url=url, headers=headers, data=kwargs, files=files)
            else:
                resp = requests.delete(url=url, headers=headers, data=json.dumps(kwargs))
        else:
            if is_file:
                resp = requests.get(url=url, headers=headers, params=kwargs, files=files)
            else:
                resp = requests.get(url=url, headers=headers, params=kwargs)
        if resp.status_code == 200:
            test_logger.info(f"{method} {url} 请求成功")
            results = json.loads(resp.text)
            kwargs.pop('files', None)
            kwargs.pop('updated_files', None)
            test_logger.debug(f'请求参数:{kwargs}')
            test_logger.debug(f'返回相应:{results}')
            self.success.append(url)
            return results
        elif resp.status_code == 400:
            test_logger.warning(f"{method} {url} 拒绝请求")
            results = json.loads(resp.text)
            kwargs.pop('files', None)
            kwargs.pop('updated_files', None)
            test_logger.debug(f'请求参数:{kwargs}')
            test_logger.debug(f'返回相应:{results}')
            self.warning.append(url)
            return None
        else:
            test_logger.error(f"{method} {url}请求失败:{resp.status_code}, {resp.text}")
            self.error.append(url)
            return None

    def auth(self, username, password):
        url = f'{self.domain}/auth/'
        data = {'username': username, 'password': password}
        results = self.base_request(url=url, method='post', **data)['results']
        self.token = results['token']
        self.user = results['user']
        return results

    def create(self, is_file=False, *args, **kwargs):
        url = f'{self.domain}/{self.uri}/'
        results = self.base_request(url=url, is_file=is_file, method='post', **kwargs)
        return results

    def delete(self, instance_id,  is_file=False, *args, **kwargs):
        url = f'{self.domain}/{self.uri}/{instance_id}/'
        results = self.base_request(url=url, is_file=is_file, method='delete', **kwargs)
        return results

    def update(self, instance_id, method='patch', is_file=False, *args, **kwargs):
        url = f'{self.domain}/{self.uri}/{instance_id}/'
        results = self.base_request(url=url, is_file=is_file, method=method, **kwargs)
        return results

    def retrieve(self, instance_id, is_file=False, *args, **kwargs):
        url = f'{self.domain}/{self.uri}/{instance_id}/'
        results = self.base_request(url=url, is_file=is_file, method='get', **kwargs)
        return results

    def list(self, is_file=False, *args, **kwargs):
        url = f'{self.domain}/{self.uri}/'
        results = self.base_request(url=url, is_file=is_file, method='get', **kwargs)
        return results

    def bulk_delete(self, is_file=False, *args, **kwargs):
        url = f'{self.domain}/{self.uri}/bulk_delete/'
        results = self.base_request(url=url, is_file=is_file, method='delete', **kwargs)
        return results

    def get_random_obj(self, is_file=False, *args, **kwargs):
        list_results = self.list(not_page=True, is_file=is_file, *args, **kwargs)
        return random.choice(list_results['results'])

    def crud(self, is_file=False, *args, **kwargs):
        instance = self.create(is_file=is_file, *args, **kwargs)
        if instance:
            instance_id = instance['results']['id']
            test_logger.info(f'')
            self.retrieve(instance_id=instance_id)
            self.update(instance_id=instance_id, is_file=is_file, *args, **kwargs)
            self.list()
            self.list(search='test', ordering='-id')
            self.delete(instance_id=instance_id)


if __name__ == '__main__':
    pass
