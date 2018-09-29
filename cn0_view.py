import os.path as op
from datetime import timedelta
from math import isnan
import fire
from record import Record, SateInfo
from cn0_template import apply_cn0_template
from elaz_template import apply_elaz_template
from el_az_calculator import get_elaz


def _get_sat_id(sat_info):
    return '{}{}'.format(sat_info.constellation, sat_info.svid)


def analyze_log(records):
    svid_list = []
    for record in records:
        for sat_info in record.sat_infos:
            sat_id = _get_sat_id(sat_info)
            if sat_id not in svid_list:
                svid_list.append(sat_id)
    svid_list.sort()

    cn0_dict = {}
    for svid in svid_list:
        cn0_dict[svid] = {}

    datetime_list = []
    start_time = records[0].time
    end_time = records[-1].time
    time_scan = start_time
    while time_scan <= end_time:
        datetime_list.append(time_scan)
        time_scan += timedelta(seconds=1)

    visible_list = []
    for curr_record in records:
        curr_time = curr_record.time
        if not curr_record.sat_infos:
            for svid in svid_list:
                cn0_dict[svid][curr_time] = 'null'
            continue
        visible_count = 0
        curr_dict = {}
        for sat_info in curr_record.sat_infos:
            curr_dict[_get_sat_id(sat_info)] = sat_info.cn0
        for svid in svid_list:
            if svid in curr_dict:
                visible_count += 1
                cn0_dict[svid][curr_time] = str(curr_dict[svid])
            else:
                cn0_dict[svid][curr_time] = 'null'
        visible_list.append(str(visible_count))
    return datetime_list, cn0_dict, visible_list


def enrich_record_elaz(old_records):
    svid_list = []
    sat_dict = {}
    for record in old_records:
        for sat_info in record.sat_infos:
            sat_id = _get_sat_id(sat_info)
            if sat_id not in svid_list:
                svid_list.append(sat_id)
                sat_dict[sat_id] = [sat_info, ]
            else:
                sat_dict[sat_id].append(sat_info)
    svid_list.sort()

    entire_sat_list = []
    for i in range(1, 33):
        entire_sat_list.append('G%02d' % i)

    new_records = []
    for record in old_records:
        new_record = record
        old_sat_infos = record.sat_infos
        new_record.sat_infos = []
        for svid in entire_sat_list:
            el, az = get_elaz(
                record.time, svid[0:1], svid[1:3])
            if isnan(el) or isnan(az):
                continue
            sat_info = next((sat_info for sat_info in old_sat_infos if
                             _get_sat_id(sat_info) == svid), None)
            if not sat_info:
                sat_info = SateInfo(svid[0:1], svid[1:3], -1, el, az)
            new_record.sat_infos.append(sat_info)
        new_records.append(new_record)
    return new_records


def show_records(records, file_path):
    _, file_extension = op.splitext(file_path)
    if not file_extension:
        file_extension = '.txt'

    time_list, cn0_dict, visible_list = analyze_log(records)
    with open(file_path.replace(file_extension, '') + '_cn0.html', 'wt') as f:
        f.write(apply_cn0_template(op.basename(file_path),
                                   time_list, cn0_dict, visible_list))

    new_records = enrich_record_elaz(records)
    with open(file_path.replace(file_extension, '') + '_elaz.html', 'wt') as f:
        f.write(apply_elaz_template(op.basename(file_path), new_records))


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
    fire.Fire({
        'kolmo': kolmo,
        'android': android,
        'nmea': nmea
    })
