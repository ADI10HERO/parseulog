def get_battery_data_index(data_list):
    for i, obj in enumerate(data_list):
        if "battery" in obj.name:
            return i
    raise Exception("No battery information in this ulog file")
