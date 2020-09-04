"""
Author: Alan Fu
Email: fualan1990@gmail.com
拆分模块所需配置
"""
# 上机策略
START_STRATEGY = ['Lane Random', 'Lane Specified']

# 拆分策略
SPLIT_STRATEGY = ['Dual Index', 'Single Index']

# 测序策略
SEQUENCING_STRATEGY = ['Paired End', 'Single End']

# index错配数
INDEX_MISMATCH = {
    '0': '0个',
    '1': '1个',
    '2': '2个',
    'auto': '自动',
}

SEQ_UN_START = 10
SEQ_RUNNING = 20
SEQ_STOP = 30
SEQ_ERROR = 40
SEQ_SUCCESS = 50
SEQ_RESET = 60
# 测序状态
SEQUENCING_STATUS = {
    SEQ_UN_START: '未启动',
    SEQ_RUNNING: '进行中',
    SEQ_STOP: '停止',
    SEQ_ERROR: '错误结束',
    SEQ_SUCCESS: '成功结束',
    SEQ_RESET: '重置',
}