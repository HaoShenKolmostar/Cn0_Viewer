from string import Template


def apply_elaz_template(file_name, record_list):
    def _sat_infos_to_str_list(record):
        str_list = []
        for sat_info in record.sat_infos:
            str_list.append('{}, {}, {}, \"{}{}\"'.format(
                sat_info.el, sat_info.az, sat_info.cn0,
                sat_info.constellation, sat_info.svid
            ))
        return str_list

    time_str_list = []
    data_str_list = []
    for record in record_list:
        time_str = record.time.strftime('\'%H:%M:%S\'')
        time_str_list.append(time_str)
        data_str_list.append('{}:[[{}]]'.format(
            time_str,
            '], ['.join(_sat_infos_to_str_list(record))
        ))

    data_map = {
        'FILE_NAME': file_name,
        'TIME_LIST': ', '.join(time_str_list),
        'DATA_LIST': ', '.join(data_str_list),
    }
    return Template(template_elaz).safe_substitute(data_map)


template_elaz = \
    '<!DOCTYPE html>\n' + \
    '<html style=\"height: 100%\">\n' + \
    '\n' + \
    '<head>\n' + \
    '    <meta charset=\"utf-8\">\n' + \
    '    <title>${FILE_NAME} - ElAz View</title>\n' + \
    '    <script type=\"text/javascript\" src=\"http://echarts.baidu.com/gallery/vendors/echarts/echarts.min.js\"></script>\n' + \
    '    <link rel=\"stylesheet\" href=\"http://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css\">\n' + \
    '    <script src=\"https://code.jquery.com/jquery-1.12.4.js\"></script>\n' + \
    '    <script src=\"https://code.jquery.com/ui/1.12.1/jquery-ui.js\"></script>\n' + \
    '    <style type=\"text/css\">\n' + \
    '        input[type=number]::-webkit-inner-spin-button,\n' + \
    '        input[type=number]::-webkit-outer-spin-button {\n' + \
    '            opacity: 1;\n' + \
    '            font-size: 30px;\n' + \
    '        }\n' + \
    '\n' + \
    '        .circle {\n' + \
    '            float: left;\n' + \
    '            width: 20px;\n' + \
    '            height: 20px;\n' + \
    '            border: 2px solid #000000;\n' + \
    '            margin-left: 20px;\n' + \
    '            border-radius: 20px;\n' + \
    '        }\n' + \
    '    </style>\n' + \
    '</head>\n' + \
    '\n' + \
    '<body style=\"height: 100%; margin: 0; background-color:gainsboro;\">\n' + \
    '    <div id=\"div_progress\" style=\"width: 120px; height: 100%; float:left; padding-left: 20px;\">\n' + \
    '        <div id=\'slider\' min=\"0\" max=\"5\" style=\"height: 76%; position:absolute; top: 40px; left: 40px; bottom: 100px;\"></div>\n' + \
    '        <div id=\'div_selector\' style=\"position:absolute; bottom: 30px; height: 60px; \">\n' + \
    '            <label id=\"lblDay\" style=\"background: transparent; height: 32px; line-height: 32px;\">02-03-02</label>\n' + \
    '            <input id=\"selector\" type=\"number\" value=\"0\" style=\"float: right; width: 25px; height:32px; border: 0px; background: transparent; color: transparent; \" onclick=\"setData(this.value);\">\n' + \
    '        </div>\n' + \
    '        <div id=\'div_selector\' style=\"position:absolute; bottom: 0; height: 30px;\"></div>\n' + \
    '    </div>\n' + \
    '    <div id=\"div_container\" style=\" margin-left: 150px; margin-right: 100px; height: 100%;\"></div>\n' + \
    '    <table id=\"div_color_table\" style=\"position:absolute; width: 120px; height: 100%; right: 0px; background: transparent; top: 0px; text-align: center;\">\n' + \
    '        <thead><tr>\n' + \
    '            <th>Cn0</th>\n' + \
    '            <th>Color</th>\n' + \
    '        </tr></thead>\n' + \
    '        <tr><td>&lt;37</td><td class=\"circle\" style=\"background:white;\"></td></tr>\n' + \
    '        <tr><td>37</td><td class=\"circle\" style=\"background:#FFFF9F;\"></td></tr>\n' + \
    '        <tr><td>38</td><td class=\"circle\" style=\"background:#FFFF7F;\"></td></tr>\n' + \
    '        <tr><td>39</td><td class=\"circle\" style=\"background:#FFFF5F;\"></td></tr>\n' + \
    '        <tr><td>40</td><td class=\"circle\" style=\"background:#FFFF3F;\"></td></tr>\n' + \
    '        <tr><td>41</td><td class=\"circle\" style=\"background:#FFFF1F;\"></td></tr>\n' + \
    '        <tr><td>42</td><td class=\"circle\" style=\"background:#FFFF00;\"></td></tr>\n' + \
    '        <tr><td>43</td><td class=\"circle\" style=\"background:#FFDF00;\"></td></tr>\n' + \
    '        <tr><td>44</td><td class=\"circle\" style=\"background:#FFBF00;\"></td></tr>\n' + \
    '        <tr><td>45</td><td class=\"circle\" style=\"background:#FF9F00;\"></td></tr>\n' + \
    '        <tr><td>46</td><td class=\"circle\" style=\"background:#FF7F00;\"></td></tr>\n' + \
    '        <tr><td>47</td><td class=\"circle\" style=\"background:#FF5F00;\"></td></tr>\n' + \
    '        <tr><td>48</td><td class=\"circle\" style=\"background:#FF3F00;\"></td></tr>\n' + \
    '        <tr><td>49</td><td class=\"circle\" style=\"background:#FF1F00;\"></td></tr>\n' + \
    '        <tr><td>50</td><td class=\"circle\" style=\"background:#FF0000;\"></td></tr>\n' + \
    '        <tr><td>51</td><td class=\"circle\" style=\"background:#DF0000;\"></td></tr>\n' + \
    '        <tr><td>52</td><td class=\"circle\" style=\"background:#BF0000;\"></td></tr>\n' + \
    '        <tr><td>53</td><td class=\"circle\" style=\"background:#9F0000;\"></td></tr>\n' + \
    '        <tr><td>54</td><td class=\"circle\" style=\"background:#7F0000;\"></td></tr>\n' + \
    '        <tr><td>55</td><td class=\"circle\" style=\"background:#5F0000;\"></td></tr>\n' + \
    '        <tr><td>56</td><td class=\"circle\" style=\"background:#3F0000;\"></td></tr>\n' + \
    '        <tr><td>57</td><td class=\"circle\" style=\"background:#1F0000;\"></td></tr>\n' + \
    '        <tr><td>&gt;=58</td><td class=\"circle\" style=\"background:black;\"></td></tr>\n' + \
    '    </table>\n' + \
    '    <script type=\"text/javascript\">\n' + \
    '        const days = [${TIME_LIST}];\n' + \
    '\n' + \
    '        const allData = {${DATA_LIST}};\n' + \
    '\n' + \
    '        let slider = $(\"#slider\")\n' + \
    '        slider.slider({\n' + \
    '            animate: false,\n' + \
    '            orientation: \"vertical\",\n' + \
    '            min: 0,\n' + \
    '            max: days.length - 1,\n' + \
    '            range: false,\n' + \
    '            step: 1,\n' + \
    '            number: 0,\n' + \
    '            slide: function (event, ui) {\n' + \
    '                setData(ui.value);\n' + \
    '            }\n' + \
    '        });\n' + \
    '\n' + \
    '        let selector = document.getElementById(\"selector\");\n' + \
    '        selector.min = 0;\n' + \
    '        selector.max = days.length - 1;\n' + \
    '\n' + \
    '        let lblDay = document.getElementById(\"lblDay\");\n' + \
    '\n' + \
    '        var elazChart = echarts.init(document.getElementById(\"div_container\"));\n' + \
    '        window.onresize = elazChart.resize;\n' + \
    '        let option = {\n' + \
    '            title: {\n' + \
    '                text: \'${FILE_NAME}\'\n' + \
    '            },\n' + \
    '            polar: {},\n' + \
    '            tooltip: {\n' + \
    '                trigger: \'axis\',\n' + \
    '                axisPointer: {\n' + \
    '                    type: \'cross\'\n' + \
    '                },\n' + \
    '                formatter: function (params) {\n' + \
    '                    return `${params[0].value[3]} <br/>elevation: ${params[0].value[0]}<br/>azimuth: ${params[0].value[1]}<br/>Cn0: ${params[0].value[2]}`;\n' + \
    '                },\n' + \
    '            },\n' + \
    '            angleAxis: {\n' + \
    '                name: \'azimuth\',\n' + \
    '                type: \'value\',\n' + \
    '                startAngle: -90,\n' + \
    '                min: -180,\n' + \
    '                max: 180,\n' + \
    '                interval: 90,\n' + \
    '                splitLine: {\n' + \
    '                    show: true,\n' + \
    '                    lineStyle: {\n' + \
    '                        color: \'rgba(160,160,160,0.6)\',\n' + \
    '                        opacity: 0.8,\n' + \
    '                    }\n' + \
    '                },\n' + \
    '                axisPointer: {\n' + \
    '                    label: {\n' + \
    '                        show: false,\n' + \
    '                    },\n' + \
    '                },\n' + \
    '            },\n' + \
    '            radiusAxis: {\n' + \
    '                min: 0,\n' + \
    '                max: 90,\n' + \
    '                splitNumber: 9,\n' + \
    '                interval: 30,\n' + \
    '                inverse: true,\n' + \
    '                splitLine: {\n' + \
    '                    show: true,\n' + \
    '                    interval: 30,\n' + \
    '                    lineStyle: {\n' + \
    '                        color: \'rgba(160,160,160,0.6)\',\n' + \
    '                        opacity: 0.8,\n' + \
    '                    }\n' + \
    '                },\n' + \
    '                axisPointer: {\n' + \
    '                    label: {\n' + \
    '                        show: false,\n' + \
    '                    },\n' + \
    '                },\n' + \
    '            },\n' + \
    '            series: [{\n' + \
    '                coordinateSystem: \'polar\',\n' + \
    '                name: \'elevation\',\n' + \
    '                type: \'scatter\',\n' + \
    '                label:{\n' + \
    '                    show: true,\n' + \
    '                    color: \'black\',\n' + \
    '                    position: [12, 0],\n' + \
    '                    formatter: function (params) {\n' + \
    '                        if (params.value[0] <= 0) return \'\';\n' + \
    '                        return `${params.value[3]}`;\n' + \
    '                    },\n' + \
    '                },\n' + \
    '                itemStyle: {\n' + \
    '                    normal: {\n' + \
    '                        color: function (params) {\n' + \
    '                            let el = params.value[0];\n' + \
    '                            if (el < 0) return \'transparent\';\n' + \
    '                            let cn0 = params.value[2];\n' + \
    '                            if (cn0 > 58) return \'#000000\';\n' + \
    '                            else if (cn0 < 37) return \'#FFFFFF\';\n' + \
    '                            else {\n' + \
    '                                cn0 = 59 - cn0;\n' + \
    '                                let r = 0;\n' + \
    '                                let g = 0;\n' + \
    '                                let b = 0;\n' + \
    '                                r = cn0 > 8 ? 255 : cn0 * 16 - 1;\n' + \
    '                                g = cn0 > 16 ? 255 : cn0 > 8 ? (cn0 - 8) * 16 - 1 : 0;\n' + \
    '                                b = cn0 > 16 ? (cn0 - 16) * 16 - 1 : 0;\n' + \
    '                                return \'#\' +\n' + \
    '                                    (\'00\' + r.toString(16)).substr(-2) +\n' + \
    '                                    (\'00\' + g.toString(16)).substr(-2) +\n' + \
    '                                    (\'00\' + b.toString(16)).substr(-2);\n' + \
    '                            }\n' + \
    '                        },\n' + \
    '                    }\n' + \
    '                }\n' + \
    '            },],\n' + \
    '        };;\n' + \
    '\n' + \
    '        function setData(index) {\n' + \
    '            let data = allData[days[index]];\n' + \
    '            option.series[0].data = allData[days[index]];\n' + \
    '            elazChart.setOption(option, true);\n' + \
    '            selector.value = index;\n' + \
    '            lblDay.innerText = days[index];\n' + \
    '            slider.slider(\"value\", index);\n' + \
    '        };\n' + \
    '        setData(0);\n' + \
    '    </script>\n' + \
    '</body>\n' + \
    '\n' + \
    '</html>\n'
