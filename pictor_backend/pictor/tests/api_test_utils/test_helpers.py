from pictor.tests.api_test_utils.generate_parameters import *


class UserAPI(BaseAPI):
    def __init__(self, domain=domain, uri='users', token=None):
        super().__init__(domain=domain, uri=uri, token=token)

    def run(self, create_num=5):
        for _ in range(create_num):
            parameter = get_user()
            self.create(**parameter)
        parameter = get_user()
        self.crud(**parameter)
        object = self.get_random_obj()
        return object


class WorkZoneAPI(BaseAPI):
    def __init__(self, domain=domain, uri='work-zones', token=None):
        super().__init__(domain=domain, uri=uri, token=token)

    def members(self, instance_id, *args, **kwargs):
        url = f'{self.domain}/{self.uri}/{instance_id}/members/'
        results = self.base_request(url=url, method='get', **kwargs)
        return results

    def run(self, create_num=5):
        for _ in range(create_num):
            parameter = get_work_zone()
            self.create(**parameter)
        parameter = get_work_zone()
        self.crud(**parameter)
        object = self.get_random_obj()
        self.members(instance_id=object['id'])
        return object


class ProjectAPI(BaseAPI):
    def __init__(self, domain=domain, uri='projects', token=None):
        super().__init__(domain=domain, uri=uri, token=token)

    def run(self, work_zone, create_num=5):
        for _ in range(create_num):
            parameter = get_project(work_zone)
            self.create(**parameter)
        parameter = get_project(work_zone)
        self.crud(**parameter)
        object = self.get_random_obj()
        return object


if __name__ == '__main__':
    base_api = BaseAPI(domain=domain)
    auth_results = base_api.auth(username=username, password=password)

    work_zone_api = WorkZoneAPI(token=base_api.token)
    work_zone = work_zone_api.get_random_obj()

    test_api = UserAPI(token=base_api.token)
    test_api.run()