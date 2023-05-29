__data = {}

def register(name, update_func):
    __init_data_name(name)
    __data[name][1].append(update_func)
    return len(__data[name][1]) - 1

def unregister(name,index):
    if name in __data and index < len(__data[name][1]):
        __data[name][1].pop(index)

def update(name, value):
    __init_data_name(name)
    __data[name][0] = value
    for func in __data[name][1]:
        func(value)

def get(name):
    __init_data_name(name)
    return __data[name][0]

def __init_data_name(name):
    if name not in __data:
        __data[name] = [None,[]]