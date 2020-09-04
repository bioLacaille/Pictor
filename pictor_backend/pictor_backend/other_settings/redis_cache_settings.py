from pictor.utils.setup_helpers import get_configure

redis_host = get_configure('REDIS', 'REDIS_HOST', '127.0.0.1')
redis_port = get_configure('REDIS', 'REDIS_PORT', '6379')
redis_db_num = get_configure('REDIS', 'REDIS_DB_NUM', '1')
redis_password = get_configure('REDIS', 'REDIS_PASSWORD', None)

redis_url = f'redis://{redis_host}:{redis_port}/{redis_db_num}'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': redis_url,
        "OPTIONS": {
            "PASSWORD": redis_password,
            "IGNORE_EXCEPTIONS": True,  # memcached 异常行为
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},  # 配置默认连接池
            "PICKLE_VERSION": -1,
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}