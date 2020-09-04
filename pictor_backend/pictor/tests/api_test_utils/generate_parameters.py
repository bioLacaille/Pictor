import datetime
from pictor.tests.api_test_utils.base_helpers import *


def get_work_zone():
    serial_number = fake.ean8()
    name = fake.name()
    remark = fake.text(max_nb_chars=250)
    return {'serial_number': serial_number, 'name': name, 'remark': remark}


def get_user():
    nickname = fake.name()
    username = fake.user_name()
    password = username
    email = f'{username}@test.com'
    phone = fake.phone_number()
    gender = random.choice(['男', '女'])
    title = '全栈工程师'
    qq = f'{random.randint(1000000, 1000000000)}'
    remark = fake.text(max_nb_chars=250)
    return {'nickname': nickname, 'username': username, 'password': password, 'email': email,
            'phone': phone, 'gender': gender, 'title': title,
            'qq': qq, 'address': fake.address(),
            'remark': remark}


def get_project(work_zone):
    work_zone = work_zone
    serial_number = fake.ean8()
    name = fake.name()
    remark = fake.text(max_nb_chars=250)
    return {'work_zone': work_zone, 'serial_number': serial_number, 'name': name, 'remark': remark}