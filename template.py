from string import Template


def _datetime_to_js_str(datetime):
    return 'new Date({},{},{},{},{},{})'.format(
        datetime.year,
        datetime.month,
        datetime.day,
        datetime.hour,
        datetime.minute,
        datetime.second
    )


def cn0_dict_to_string(cn0_dict):

    def _sat_cn0_dict_to_str(sat_cn0_dict):
        res_str = ''
        for k, v in sat_cn0_dict.items():
            res_str += '[new Date({}, {}, {}, {}, {}, {}), {}],'.format(
                k.year, k.month, k.day, k.hour, k.minute, k.second, v
            )
        return res_str

    res = ''
    for svid in cn0_dict:
        data_map = {
            'SVID': '\'{}\''.format(svid),
            'Cn0_LIST': _sat_cn0_dict_to_str(cn0_dict[svid])
        }
        res += Template(template_cn0).safe_substitute(data_map)
    return res


def apply_template(file_name, time_list, cn0_dict, visible_list):
    time_str_list = []
    for t in time_list:
        time_str_list.append(t.strftime('\'%H:%M:%S\''))
    svid_list = list(cn0_dict.keys())
    svid_str_list = []
    for svid in svid_list:
        svid_str_list.append('\'{}\''.format(svid))
    print(svid_str_list)
    data_map = {
        'FILE_NAME': file_name,
        'TIME_LIST': ', '.join(time_str_list),
        'SVID_LIST': ', '.join(svid_str_list),
        'Cn0_DATA': cn0_dict_to_string(cn0_dict),
        'VISIBLE_SATS': ', '.join(visible_list),
        'SVID_TRUE': ': true,'.join(svid_str_list) + ': true',
        'SVID_FALSE': ': false,'.join(svid_str_list) + ': false'
    }
    return Template(template_str).safe_substitute(data_map)


template_cn0 = \
    '                {\n' + \
    '                    name: ${SVID},\n' + \
    '                    type: \'line\',\n' + \
    '                    data: [${Cn0_LIST}]\n' + \
    '                },\n'

template_str = '<!DOCTYPE html>\n' + \
    '<html style=\"height: 100%\" lang=\"en\">\n' + \
    '\n' + \
    '<head>\n' + \
    '    <meta charset=\"utf-8\">\n' + \
    '    <title>${FILE_NAME} - SatellitesView</title>\n' + \
    '\n' + \
    '    <style>\n' + \
    '        table {\n' + \
    '            cellspacing: 0;\n' + \
    '            *border-collapse: collapse;\n' + \
    '            border-spacing: 0;\n' + \
    '            width: 100%;\n' + \
    '            user-select: all;\n' + \
    '        }\n' + \
    '\n' + \
    '        .bordered tr:hover {\n' + \
    '            background: #fbf8e9;\n' + \
    '            -o-transition: all 0.1s ease-in-out;\n' + \
    '            -webkit-transition: all 0.1s ease-in-out;\n' + \
    '            -moz-transition: all 0.1s ease-in-out;\n' + \
    '            -ms-transition: all 0.1s ease-in-out;\n' + \
    '            transition: all 0.1s ease-in-out;\n' + \
    '        }\n' + \
    '\n' + \
    '        .bordered th {\n' + \
    '            padding: 7px;\n' + \
    '            text-align: center;\n' + \
    '            cellspacing: 0;\n' + \
    '        }\n' + \
    '\n' + \
    '        .bordered td {\n' + \
    '            padding: 7px;\n' + \
    '            text-align: center;\n' + \
    '            cellspacing: 0;\n' + \
    '        }\n' + \
    '\n' + \
    '\n' + \
    '        .bordered th {\n' + \
    '            background-image: -webkit-gradient(linear, left top, left bottom, from(#ebf3fc), to(#dce9f9));\n' + \
    '            background-image: -webkit-linear-gradient(top, #ebf3fc, #dce9f9);\n' + \
    '            background-image: -moz-linear-gradient(top, #ebf3fc, #dce9f9);\n' + \
    '            background-image: -ms-linear-gradient(top, #ebf3fc, #dce9f9);\n' + \
    '            background-image: -o-linear-gradient(top, #ebf3fc, #dce9f9);\n' + \
    '            background-image: linear-gradient(top, #ebf3fc, #dce9f9);\n' + \
    '        }\n' + \
    '\n' + \
    '        .bordered td:first-child,\n' + \
    '        .bordered th:first-child {\n' + \
    '            border-left: none;\n' + \
    '        }\n' + \
    '\n' + \
    '\n' + \
    '\n' + \
    '        .bordered tr:nth-of-type(2n) {\n' + \
    '            background: #FFFFFF;\n' + \
    '        }\n' + \
    '\n' + \
    '        .bordered tr:nth-of-type(2n+1) {\n' + \
    '            background: #F7FAFC;\n' + \
    '        }\n' + \
    '\n' + \
    '        .bordered tbody tr:hover {\n' + \
    '            background: #fbf8e9;\n' + \
    '            -o-transition: all 0.1s ease-in-out;\n' + \
    '            -webkit-transition: all 0.1s ease-in-out;\n' + \
    '            -moz-transition: all 0.1s ease-in-out;\n' + \
    '            -ms-transition: all 0.1s ease-in-out;\n' + \
    '            transition: all 0.1s ease-in-out;\n' + \
    '        }\n' + \
    '\n' + \
    '        h4 {\n' + \
    '            visibility: hidden;\n' + \
    '        }\n' + \
    '    </style>\n' + \
    '\n' + \
    '</head>\n' + \
    '\n' + \
    '<body style=\"height: 100%; margin:0; padding:0; font-size: 12px;\" onload=\"init();\">\n' + \
    '    <div id=\"btn_container\" style=\"height: 60px;position:absolute; top: 20; padding-top: 20px;\">\n' + \
    '        <button type=\"button\" style=\"margin-left:20px; font-size: 14px;\" onclick=\"SelectAllCn0();\">Select All</button>\n' + \
    '        <button type=\"button\" style=\"margin-left:20px; font-size: 14px;\" onclick=\"UnSelectAllCn0();\">UnSelect All</button>\n' + \
    '        <a style=\"margin-left:20px; font-size: 14px;\">Cn0 Threshold</a>\n' + \
    '        <input type=\"number\" style=\"width: 36px; font-size: 14px;\" value=\"37\" onchange=\"cn0_threshold = this.value; ApplyThreshold();\" onclick=\"cn0_threshold = this.value; ApplyThreshold();\">\n' + \
    '    </div>\n' + \
    '    <div id=\"cn0_container\" style=\"width:100%; top: 60px; bottom: 40px; height: auto; position:absolute;\"></div>\n' + \
    '    <div id=\"blank_space\" style=\"height: 40px; bottom: 0;position:absolute;\"></div>\n' + \
    '    <script type=\"text/javascript\" src=\"http://echarts.baidu.com/gallery/vendors/echarts/echarts.min.js\"></script>\n' + \
    '    <script type=\"text/javascript\">\n' + \
    '\n' + \
    '        let cn0_dom = document.getElementById(\"cn0_container\");\n' + \
    '        let cn0_chart = echarts.init(cn0_dom);\n' + \
    '        window.onresize = cn0_chart.resize;\n' + \
    '        let cn0_threshold = 37;\n' + \
    '\n' + \
    '        function init() {\n' + \
    '            cn0_option = {\n' + \
    '                title: {\n' + \
    '                    text: \'${FILE_NAME}\'\n' + \
    '                },\n' + \
    '                tooltip: {\n' + \
    '                    trigger: \'axis\'\n' + \
    '                },\n' + \
    '                legend: {\n' + \
    '                    data: [\'\', \'\', \'\', ${SVID_LIST}, \'\', \'\', \'\', \'\'],\n' + \
    '                    left: 100\n' + \
    '                },\n' + \
    '                grid: [\n' + \
    '                    {\n' + \
    '                        left: 50,\n' + \
    '                        right: 50,\n' + \
    '                        height: \'60%\',\n' + \
    '                        containLabel: true\n' + \
    '                    },\n' + \
    '                    {\n' + \
    '                        left: 50,\n' + \
    '                        right: 50,\n' + \
    '                        top: \'70%\',\n' + \
    '                        containLabel: true\n' + \
    '                    }\n' + \
    '                ],\n' + \
    '                toolbox: {\n' + \
    '                    feature: {\n' + \
    '                        dataZoom: {\n' + \
    '                            title: {\n' + \
    '                                zoom: \'zoom\',\n' + \
    '                                back: \'zoom reset\'\n' + \
    '                            }\n' + \
    '                        },\n' + \
    '                        dataView: {\n' + \
    '                            show: true,\n' + \
    '                            title: \'Statistics\',\n' + \
    '                            readOnly: true,\n' + \
    '                            optionToContent: function (opt) {\n' + \
    '                                var dataview = opt.toolbox[0].feature.dataView;\n' + \
    '                                var table = \'<div style=\"margin:10px; line-height: 1.4em;text-align:center;font-size:14px;\">\' + dataview.title + \'</div>\'\n' + \
    '                                table += getTable(opt);\n' + \
    '                                return table;\n' + \
    '                            }\n' + \
    '                        },\n' + \
    '                        saveAsImage: {\n' + \
    '                            title: \'Save PNG\',\n' + \
    '                            type: \'png\'\n' + \
    '                        },\n' + \
    '                    },\n' + \
    '                },\n' + \
    '                xAxis: [\n' + \
    '                    {\n' + \
    '                        name: \'UTC\',\n' + \
    '                        type: \'time\',\n' + \
    '                        splitNumber: 10,\n' + \
    '                        gridIndex: 0,\n' + \
    '                        boundaryGap: false,\n' + \
    '                        axisLine: { onZero: true },\n' + \
    '                        axisLabel:{\n' + \
    '                            formatter: function (value){\n' + \
    '                                var hour = (value.getHour()).toString();  \n' + \
    '                                var minute = (value.getMinute()).toString();  \n' + \
    '                                var hour = (value.getSecond()).toString();  \n' + \
    '                                return hour + \':\' + minute + \':\' + second;\n' + \
    '                            }\n' + \
    '                        }\n' + \
    '                    }, {\n' + \
    '                        name: \'UTC\',\n' + \
    '                        type: \'time\',\n' + \
    '                        splitNumber: 10,\n' + \
    '                        show: false,\n' + \
    '                        gridIndex: 1,\n' + \
    '                        position: \'top\',\n' + \
    '                        boundaryGap: false,\n' + \
    '                    }\n' + \
    '                ],\n' + \
    '                yAxis: [\n' + \
    '                    {\n' + \
    '                        name: \'Cn0(db)\',\n' + \
    '                        type: \'value\',\n' + \
    '                        gridIndex: 0,\n' + \
    '                        scale: true\n' + \
    '                    },\n' + \
    '                    {\n' + \
    '                        name: \'Visible Satellites\',\n' + \
    '                        type: \'value\',\n' + \
    '                        gridIndex: 1,\n' + \
    '                    }\n' + \
    '                ],\n' + \
    '                series: [\n' + \
    '                    {\n' + \
    '                        name: \'Visible Satellites\',\n' + \
    '                        type: \'line\',\n' + \
    '                        xAxisIndex: 1,\n' + \
    '                        yAxisIndex: 1,\n' + \
    '                        areaStyle: { normal: {} }\n' + \
    '                    },\n' + \
    '${Cn0_DATA}' + \
    '                ],\n' + \
    '                dataZoom: [\n' + \
    '                    {\n' + \
    '                        type: \'slider\',\n' + \
    '                        show: true,\n' + \
    '                        realtime: true,\n' + \
    '                        start: 0,\n' + \
    '                        end: 100,\n' + \
    '                        xAxisIndex: [0, 1]\n' + \
    '                    },\n' + \
    '                    {\n' + \
    '                        type: \'inside\',\n' + \
    '                        realtime: false,\n' + \
    '                        start: 0,\n' + \
    '                        end: 100,\n' + \
    '                        zoomOnMouseWheel: true,\n' + \
    '                        moveOnMouseMove: true,\n' + \
    '                        xAxisIndex: [0, 1]\n' + \
    '                    }\n' + \
    '                ],\n' + \
    '            };\n' + \
    '            ApplyThreshold();\n' + \
    '        }\n' + \
    '\n' + \
    '        function ApplyThreshold() {\n' + \
    '            if (cn0_option) {\n' + \
    '                // Deep copy first\n' + \
    '                let filtered_option = JSON.parse(JSON.stringify(cn0_option));\n' + \
    '                filtered_option.toolbox.feature.dataView.optionToContent = cn0_option.toolbox.feature.dataView.optionToContent;\n' + \
    '\n' + \
    '                let series_size = filtered_option.series.length;\n' + \
    '                let sat_count = new Array();\n' + \
    '                for (let i = 1; i < series_size; i++) {\n' + \
    '                    for (let j = 0; j < filtered_option.series[i].data.length; j++) {\n' + \
    '                        if (filtered_option.series[i].data[j][1] == null) continue;\n' + \
    '                        else if (filtered_option.series[i].data[j][1] < cn0_threshold)\n' + \
    '                            filtered_option.series[i].data[j] = null;\n' + \
    '                        else {\n' + \
    '                            if (!sat_count[j]) sat_count[j] = [filtered_option.series[i].data[j][0], 1];\n' + \
    '                            else sat_count[j][1]++;\n' + \
    '                        }\n' + \
    '                    }\n' + \
    '                }\n' + \
    '                filtered_option.series[0].data = sat_count;\n' + \
    '                cn0_chart.setOption(filtered_option, true);\n' + \
    '            }\n' + \
    '        }\n' + \
    '\n' + \
    '        function SelectAllCn0() {\n' + \
    '            cn0_option.legend.selected = { ${SVID_TRUE} };\n' + \
    '            ApplyThreshold();\n' + \
    '        }\n' + \
    '\n' + \
    '        function UnSelectAllCn0() {\n' + \
    '            cn0_option.legend.selected = { ${SVID_FALSE} };\n' + \
    '            ApplyThreshold();\n' + \
    '        }\n' + \
    '\n' + \
    '        function getTable(option) {\n' + \
    '            let statistics = new Array();\n' + \
    '            for (let i = 1; i < option.series.length; i++) {\n' + \
    '                let curr_obj = {};\n' + \
    '                let sat_id = option.series[i].name;\n' + \
    '                let cn0_max = 0;\n' + \
    '                let cn0_min = 0;\n' + \
    '                let cn0_sum = 0;\n' + \
    '                let total_count = option.series[i].data.length;\n' + \
    '                let valid_count = 0;\n' + \
    '                let first_6_unnormal_moments = new Array();\n' + \
    '                for (let j = 0; j < option.series[i].data.length; j++) {\n' + \
    '                    let curr_cn0 = option.series[i].data[j][1];\n' + \
    '                    if (curr_cn0 == null) {\n' + \
    '                        if (first_6_unnormal_moments.length < 6) {\n' + \
    '                            first_6_unnormal_moments[first_6_unnormal_moments.length] = j + 1;\n' + \
    '                        }\n' + \
    '                    }\n' + \
    '                    else {\n' + \
    '                        curr_cn0 = Number(curr_cn0);\n' + \
    '                        cn0_sum += curr_cn0;\n' + \
    '                        if (cn0_max < curr_cn0) cn0_max = curr_cn0;\n' + \
    '                        if (cn0_min == 0 || cn0_min > curr_cn0 && curr_cn0 > 0) cn0_min = curr_cn0;\n' + \
    '                        valid_count += 1;\n' + \
    '                    }\n' + \
    '                }\n' + \
    '\n' + \
    '                curr_obj.sat_id = sat_id;\n' + \
    '                curr_obj.cn0_average = (cn0_sum / valid_count).toFixed(2);\n' + \
    '                curr_obj.cn0_max = cn0_max.toFixed(2);\n' + \
    '                curr_obj.cn0_min = cn0_min.toFixed(2);\n' + \
    '                curr_obj.num_of_valid_moments = valid_count;\n' + \
    '                curr_obj.num_of_losing_moments = total_count - valid_count;\n' + \
    '                curr_obj.percent_of_moments = valid_count / total_count;\n' + \
    '                curr_obj.first_6_unnormal_moments = first_6_unnormal_moments;\n' + \
    '                statistics[statistics.length] = curr_obj;\n' + \
    '            }\n' + \
    '\n' + \
    '\n' + \
    '            var table = \'<table class=\"bordered\"><thead><tr>\'\n' + \
    '                + \'<th>Satellite ID</th>\'\n' + \
    '                + \'<th>CN0 Average</th>\'\n' + \
    '                + \'<th>CN0 Max</th>\'\n' + \
    '                + \'<th>CN0 Min</th>\'\n' + \
    '                + \'<th>Num Of Valid Moments</th>\'\n' + \
    '                + \'<th>Num Of Losing Moments</th>\'\n' + \
    '                + \'<th>Percentage Of Moments(%)</th>\'\n' + \
    '                + \'<th>First 6 Unnormal Moments\\\' Indexes </th >\';\n' + \
    '            table += \'</tr></thead><tbody>\';\n' + \
    '\n' + \
    '            for (let i = 0; i < statistics.length; i++) {\n' + \
    '                curr_obj = statistics[i];\n' + \
    '                if (curr_obj.num_of_valid_moments == 0) continue;\n' + \
    '                table += \'<tr>\';\n' + \
    '                table += \'<td>\' + curr_obj.sat_id + \'</td>\';\n' + \
    '                table += \'<td>\' + curr_obj.cn0_average + \'</td>\';\n' + \
    '                table += \'<td>\' + curr_obj.cn0_max + \'</td>\';\n' + \
    '                table += \'<td>\' + curr_obj.cn0_min + \'</td>\';\n' + \
    '                table += \'<td>\' + curr_obj.num_of_valid_moments + \'</td>\';\n' + \
    '                table += \'<td>\' + curr_obj.num_of_losing_moments + \'</td>\';\n' + \
    '                table += \'<td>\' + (Number(curr_obj.percent_of_moments) * 100).toFixed(2) + \'</td>\';\n' + \
    '                table += \'<td>\' + curr_obj.first_6_unnormal_moments + \'</td>\';\n' + \
    '                table += \'</tr>\';\n' + \
    '            }\n' + \
    '            table += \'</tr></tbody></table>\';\n' + \
    '            return table;\n' + \
    '        }\n' + \
    '    </script>\n' + \
    '</body>\n' + \
    '\n' + \
    '</html>\n'
