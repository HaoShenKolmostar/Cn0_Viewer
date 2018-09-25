import fire
import os.path as op
from datetime import timedelta
from template import apply_template
from record import Record


def analyze_log(records):
    def _quota_(origin_str):
        return '\'%s\'' % (origin_str)

    def _key_str_(sat_info):
        return _quota_(sat_info.constellation + sat_info.svid)

    svid_list = []
    for record in records:
        for sat_info in record.sat_infos:
            if _key_str_(sat_info) not in svid_list:
                svid_list.append(_key_str_(sat_info))
    svid_list.sort()

    cn0_dict = {}
    for svid in svid_list:
        cn0_dict[svid] = []

    datetime_list = []
    start_time = records[0].time
    end_time = records[-1].time
    time_scan = start_time
    while time_scan <= end_time:
        datetime_list.append(time_scan)
        time_scan += timedelta(seconds=1)

    time_index = 0
    record_index = 0
    curr_record = records[record_index]
    visible_list = []
    time_list = []
    while time_index < len(datetime_list):
        curr_time = datetime_list[time_index]
        if record_index < len(records)-1 and \
                records[record_index + 1].time <= curr_time:
            record_index += 1
            curr_record = records[record_index]
        time_list.append(curr_time.strftime('\'%H:%M:%S\''))
        visible_count = 0
        curr_dict = {}
        for sat_info in curr_record.sat_infos:
            curr_dict[_key_str_(sat_info)] = sat_info.cn0
        for svid in svid_list:
            if svid in curr_dict:
                visible_count += 1
                cn0_dict[svid].append(str(curr_dict[svid]))
            else:
                cn0_dict[svid].append('null')
        visible_list.append(str(visible_count))
        time_index += 1
    return time_list, cn0_dict, visible_list


def show_records(records, file_path):
    time_list, cn0_dict, visible_list = analyze_log(records)
    filename, file_extension = op.splitext(file_path)
    if not file_extension:
        file_extension = '.txt'
    with open(file_path.replace(file_extension, '') + '_cn0.html', 'wt') as f:
        f.write(apply_template(op.basename(file_path),
                               time_list, cn0_dict, visible_list))


def kolmo(file_path):
    records = Record.parse_uart_proto_file(file_path)
    show_records(records, file_path)


def android(file_path):
    records = Record.parse_android_log(file_path)
    show_records(records, file_path)


def nmea(file_path):
    records = Record.parse_nmea_file(file_path)
    show_records(records, file_path)


if __name__ == '__main__':
    # nmea('/Users/sol/Documents/KolmoStar/GitHub/ublox_box/20180910073249/20180910073250.ubx')
    # nmea('/Users/sol/Documents/KolmoStar/Data/uart_proto_collection/0910/ublox/long/20180910021011.ubx')
    fire.Fire({
        'kolmo': kolmo,
        'android': android,
        'nmea': nmea
    })
