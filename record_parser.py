import json
import os
from datetime import datetime, timedelta
from time_utils import gps_time_to_utc
from el_az_calculator import get_elaz
from record import Record, SateInfo


class RecordParser:

    @staticmethod
    def parse_uart_proto_file(file_path):
        lines = []
        with open(file_path, 'rt') as f:
            lines = f.readlines()
        record_list = []
        for line in lines:
            lbra_index = line.find('(')
            rbra_index = line.rfind(')')
            simplified_str = line[lbra_index+1:rbra_index]
            split_index = simplified_str.find(',', 75)

            params = (simplified_str[0:split_index] +
                      simplified_str[-16:]).split(',')
            record = Record()
            record.lat = float(params[0])
            record.lng = float(params[1])
            record.alt = float(params[2])
            record.server_time = gps_time_to_utc(float(params[3]),
                                                 float(params[4]))

            if len(params) > 5:
                record.time = datetime.strptime(
                    params[-1].strip(), "%Y%m%d%H%M%S")
            else:
                record.time = record.server_time

            if len(simplified_str) >= 70:
                j_str = simplified_str[split_index+1:-16]
                jarray = json.loads(j_str.replace('\'', '\"'))
                for jobj in jarray:
                    constellation = 'G'
                    svid = '%02d' % (int(list(jobj.keys())[0]))
                    el, az = get_elaz(record.time, constellation, svid)
                    record.sat_infos.append(
                        SateInfo(constellation, svid,
                                 list(jobj.values())[0], el, az))
            record_list.append(record)
        return record_list

    @staticmethod
    def parse_android_log(file_path):
        lines = []
        with open(file_path, 'rt') as f:
            lines = f.readlines()

        record_list = []
        index = 0
        while index < len(lines):
            if not lines[index].startswith('Satellite'):
                index += 1
                continue

            curr_record = Record()
            time_str = lines[index].split(',')[1]
            curr_record.time = datetime.strptime(
                time_str, '%Y%m%d_%H%M%S') + timedelta(hours=-8)

            sats_num = int(lines[index].split(',')[2])
            for _ in range(0, sats_num):
                index += 1
                curr_line = lines[index]
                if curr_line.startswith('GPS'):
                    constellation = 'G'
                    svid = '%02d' % (int(curr_line.split(',')[1]))
                    el, az = get_elaz(curr_record.time, constellation, svid)
                    curr_record.sat_infos.append(
                        SateInfo('G', svid, curr_line.split(',')[2], el, az))
            record_list.append(curr_record)
            index += 1
        return record_list

    @staticmethod
    def parse_nmea_file(ubx_path):
        def get_utctime_from_rmc(rmc: str) -> datetime:
            RMC_FORMAT = '%d%m%y%H%M%S.%f'
            segments = rmc.strip().split(',')
            if len(segments) < 12:
                return None
            if not segments[9] or not segments[1]:
                return None
            return datetime.strptime(segments[9] + segments[1], RMC_FORMAT)

        def get_cleaned_lines(file_path):
            with open(file_path, 'rb') as f:
                binary = f.read()
                resetting_index = binary.find(b'Resetting')
                binary = binary[resetting_index:]
                dollar_index = binary.find(b'$GNRMC')
                binary = binary[dollar_index:].replace(b'\xb5', b'')
                return binary.decode().split('$')

        lines = []
        if not os.path.isdir(ubx_path):
            lines = get_cleaned_lines(ubx_path)
        else:
            files = os.listdir(ubx_path)
            files.sort()
            for file_name in files:
                if file_name.endswith('.ubx'):
                    lines += get_cleaned_lines(
                        os.path.join(ubx_path, file_name))

        record_list = []
        index = 0
        lines_count = len(lines)
        while index < lines_count:
            if not lines[index].startswith('GNRMC'):
                index += 1
                continue

            record = Record()
            record.time = get_utctime_from_rmc(lines[index])
            index += 1
            if not record.time:
                continue
            while index < lines_count:
                if not lines[index].startswith('GPGSV'):
                    index += 1
                    continue
                gsv_line_count = int(lines[index].split(',')[1])
                if lines_count - index <= gsv_line_count:
                    break
                for i in range(0, gsv_line_count):
                    if not lines[index + i].startswith('GPGSV'):
                        break
                    gsv_strs = lines[index + i].split(',')
                    sat_num = (len(gsv_strs) - 5) // 4
                    for j in range(0, sat_num):
                        if gsv_strs[7 + 4*j]:
                            constellation = 'G'
                            svid = gsv_strs[4 + 4*j]
                            el, az = get_elaz(
                                record.time, constellation, svid)
                            record.sat_infos.append(
                                SateInfo('G', svid, gsv_strs[7 + 4*j], el, az))
                index += gsv_line_count
                break

            if record.sat_infos:
                record_list.append(record)
        return record_list
