{
    "version": "0.5.0",
    "columns": [{
        "field": "A",
        "width": 534,
        "editAble": true,
        "columnIndex": 1,
        "align": "center",
        "dataBind": "A",
        "title": "A"
    }, {
        "field": "B",
        "dataBind": "B",
        "width": 171,
        "editAble": true,
        "title": "B",
        "columnIndex": 2,
        "align": "center"
    }, {
        "field": "C",
        "width": 162,
        "editAble": true,
        "columnIndex": 3,
        "align": "center",
        "dataBind": "C",
        "title": "C"
    }, {
        "field": "D",
        "width": 177,
        "editAble": true,
        "columnIndex": 4,
        "align": "center",
        "dataBind": "D",
        "title": "D"
    }, {
        "field": "E",
        "width": 148,
        "editAble": true,
        "columnIndex": 5,
        "align": "center",
        "dataBind": "E",
        "title": "E"
    }, {
        "field": "F",
        "width": 214,
        "editAble": true,
        "columnIndex": 6,
        "align": "center",
        "dataBind": "F",
        "title": "F"
    }, {
        "field": "G",
        "dataBind": "G",
        "width": 140,
        "editAble": true,
        "title": "G",
        "columnIndex": 7,
        "align": "center"
    }, {
        "field": "H",
        "width": 165,
        "editAble": true,
        "columnIndex": 8,
        "align": "center",
        "dataBind": "H",
        "title": "H"
    }, {
        "field": "I",
        "width": 128,
        "editAble": true,
        "columnIndex": 9,
        "align": "center",
        "dataBind": "I",
        "title": "I"
    }],
    "rows": [{
        "_Raven_AutoKey": "_auto_51",
        "A": "所有者权益表"
    }, {
        "_Raven_AutoKey": "_auto_50"
    }, {
        "_Raven_AutoKey": "_auto_0",
        "F": "上年度可比区间",
        "A": "项                              目",
        "B": "本期"
    }, {
        "_Raven_AutoKey": "_auto_1",
        "F": "实收基金",
        "H": "未分配利润",
        "I": "净资产合计",
        "D": "未分配利润",
        "E": "净资产合计",
        "B": "实收基金",
        "C": "其他综合收益（若有）",
        "G": "其他综合收益（若有）"
    }, {
        "_Raven_AutoKey": "_auto_2",
        "A": "一、上期期末净资产（基金净值）",
        "C": "$balanceTDay('4003',$addDay($getYearFirstDate(Sdate), -1)  , 0, ProductId)",
        "D": "$balanceTDay('4103',$addDay($getYearFirstDate(Sdate), -1)   , 0, ProductId)+$balanceTDay('4104',$addDay($getYearFirstDate(Sdate), -1)   , 0, ProductId)-$balanceTDay('410404',$addDay($getYearFirstDate(Sdate), -1)   , 0, ProductId)",
        "E": "=B5+C5+D5",
        "F": "$nc('4001', $lastYearDate(Edate  ) , '', ProductId)",
        "H": "$nc('4103',$lastYearDate(Edate), 0, ProductId)+$nc('4104',$lastYearDate(Edate), 0, ProductId)-$nc('410404',$lastYearDate(Edate), 0, ProductId)",
        "I": "=F5+G5+H5",
        "B": "$balanceTDay('4001',$addDay($getYearFirstDate(Sdate), -1)  , 0, ProductId)",
        "G": "$nc('4003',$lastYearDate(Edate) , 0, ProductId)"
    }, {
        "_Raven_AutoKey": "_auto_53",
        "A": "加：会计政策变更（若有）",
        "B": "$iif($fdateInDuration(ProductId,Sdate), '0', $nc('4001', $getYearFirstDate(Sdate), 0, ProductId)-$balanceTDay('4001',$addDay($getYearFirstDate(Sdate), -1)  , 0, ProductId))",
        "C": "$iif($fdateInDuration(ProductId,Sdate), '0', $nc('4003',$getYearFirstDate(Sdate),0,ProductId)+$fsByBusType('6111','D',$getYearFirstDate(Sdate),$getYearFirstDate(Sdate),'JZZB_QCJZ,ZQZH_ZTZFL,XZZTZ_SGPZ',ProductId,'TZFL01,TZFL02,TZFL03,TZFL04,TZFL05,TZFL06')-$balanceTDay('4003',$addDay($getYearFirstDate(Sdate), -1)  , 0, ProductId))",
        "D": "$iif($fdateInDuration(ProductId,Sdate), '0', $nc('4103', $getYearFirstDate(Sdate), 0, ProductId)+$nc('4104', $getYearFirstDate(Sdate), 0, ProductId)-$nc('410404', $getYearFirstDate(Sdate), 0, ProductId)-($balanceTDay('4103',$addDay($getYearFirstDate(Sdate), -1), 0, ProductId)+$balanceTDay('4104',$addDay($getYearFirstDate(Sdate), -1), 0, ProductId)-$balanceTDay('410404',$addDay($getYearFirstDate(Sdate), -1), 0, ProductId)))",
        "E": "=B6+C6+D6",
        "F": "$iif($fdateInDuration(ProductId,Sdate), '0', $nc('4001', $lastYearDate(Edate  ) , '', ProductId)-$nc('4001', $lastYearDate(Edate  ) , '', ProductId))",
        "G": "$iif($fdateInDuration(ProductId,Sdate), '0', $nc('4003',$lastYearDate(Edate),0,ProductId)+$fsByBusType('6111','D',$lastYearDate($getYearFirstDate(Sdate)),$lastYearDate($getYearFirstDate(Sdate)),'JZZB_QCJZ,ZQZH_ZTZFL,XZZTZ_SGPZ',ProductId,'TZFL01,TZFL02,TZFL03,TZFL04,TZFL05,TZFL06')-$nc('4003',$lastYearDate(Edate) , 0, ProductId))",
        "H": "$iif($fdateInDuration(ProductId,Sdate), '0', $nc('4103', $getFirstDayBY(Sdate), 0, ProductId)+$nc('4104', $getFirstDayBY(Sdate), 0, ProductId)-$nc('410404', $getFirstDayBY(Sdate), 0, ProductId)-($nc('4103',$lastYearDate(Edate), 0, ProductId)+$nc('4104',$lastYearDate(Edate), 0, ProductId)-$nc('410404',$lastYearDate(Edate), 0, ProductId)))",
        "I": "=F6+G6+H6"
    }, {
        "_Raven_AutoKey": "_auto_52",
        "A": "        前期差错变更（若有）",
        "B": "0.00",
        "C": "0.00",
        "D": "0.00",
        "E": "=B7+C7+D7",
        "F": "0.00",
        "G": "0.00",
        "H": "0.00",
        "I": "=F7+G7+H7"
    }, {
        "_Raven_AutoKey": "_auto_54",
        "A": "        其他（若有）",
        "B": "0.00",
        "C": "0.00",
        "D": "0.00",
        "E": "=B8+C8+D8",
        "F": "0.00",
        "G": "0.00",
        "H": "0.00",
        "I": "=F8+G8+H8"
    }, {
        "_Raven_AutoKey": "_auto_3",
        "A": "二、本期期初净资产（基金净值）",
        "C": "$nc('4003',$getYearFirstDate(Sdate),0,ProductId)+$fsByBusType('6111','D',$getYearFirstDate(Sdate),$getYearFirstDate(Sdate),'JZZB_QCJZ,ZQZH_ZTZFL,XZZTZ_SGPZ',ProductId,'TZFL01,TZFL02,TZFL03,TZFL04,TZFL05,TZFL06')",
        "D": "$nc('4103', $getYearFirstDate(Sdate), 0, ProductId)+$nc('4104', $getYearFirstDate(Sdate), 0, ProductId)-$nc('410404', $getYearFirstDate(Sdate), 0, ProductId)",
        "E": "=B9+C9+D9",
        "F": "$nc('4001', $lastYearDate(Edate  ) , '', ProductId)",
        "H": "$nc('4103', $getFirstDayBY(Sdate), 0, ProductId)+$nc('4104', $getFirstDayBY(Sdate), 0, ProductId)-$nc('410404', $getFirstDayBY(Sdate), 0, ProductId)",
        "I": "=F9+G9+H9",
        "B": "$nc('4001', $getYearFirstDate(Sdate), 0, ProductId)",
        "G": "$nc('4003',$lastYearDate(Edate),0,ProductId)+$fsByBusType('6111','D',$lastYearDate($getYearFirstDate(Sdate)),$lastYearDate($getYearFirstDate(Sdate)),'JZZB_QCJZ,ZQZH_ZTZFL,XZZTZ_SGPZ',ProductId,'TZFL01,TZFL02,TZFL03,TZFL04,TZFL05,TZFL06')"
    }, {
        "_Raven_AutoKey": "_auto_4",
        "A": "三、本期增减变动额（减少以\"-\"号填列）",
        "C": "=C17-C9",
        "D": "=D17-D9",
        "E": "=B10+C10+D10",
        "F": "=F11+F12+F15+F16",
        "H": "=H17-H9",
        "I": "=F10+G10+H10",
        "B": "=B11+B12+B15+B16",
        "G": "=G17-G9"
    }, {
        "_Raven_AutoKey": "_auto_5",
        "A": "（一）、综合收益总额",
        "C": "=C10-C12-C16-C15",
        "D": "=D10-D12-D16-D15",
        "E": "=B11+C11+D11",
        "F": "0.00",
        "H": "=H10-H12-H16-H15",
        "I": "=F11+G11+H11",
        "B": "0.00",
        "G": "=G10-G12-G16-G15"
    }, {
        "_Raven_AutoKey": "_auto_55",
        "A": "（二）、本期基金份额交易产生的基金净值变动数（净值减少以”-“号填列）",
        "F": "=F13+F14",
        "G": "=G13+G14",
        "I": "=F12+G12+H12",
        "B": "=B13+B14",
        "C": "=C13+C14",
        "D": "=D13+D14",
        "E": "=B12+C12+D12",
        "H": "=H13+H14"
    }, {
        "_Raven_AutoKey": "_auto_56",
        "A": "其中：1.基金申购款",
        "B": "$itemCodeFs('4001', 'D', $getYearFirstDate(Sdate), Edate  , ProductId)",
        "C": "$fs('40110301', 'D', $getYearFirstDate(Sdate), Edate , ProductId)+$fs('40110303', 'D',$getYearFirstDate(Sdate), Edate  , ProductId)",
        "D": "$fs('40110101', 'D', $getYearFirstDate(Sdate), Edate , ProductId)+$fs('40110103', 'D',$getYearFirstDate(Sdate), Edate  , ProductId)+$fs('40110201', 'D', $getYearFirstDate(Sdate), Edate , ProductId)+$fs('40110203', 'D',$getYearFirstDate(Sdate), Edate  , ProductId)",
        "E": "=B13+C13+D13",
        "F": "$fs('4001', 'D', $getFirstDayBY(Sdate) , $lastYearDate(Edate), ProductId)",
        "G": "$fs('40110301', 'D', $getFirstDayBY(Sdate) , $lastYearDate(Edate), ProductId)+$fs('40110303', 'D', $getFirstDayBY(Sdate) , $lastYearDate(Edate), ProductId)",
        "H": "$fs('40110101', 'D', $getFirstDayBY(Sdate) , $lastYearDate(Edate), ProductId)+$fs('40110103', 'D', $getFirstDayBY(Sdate) , $lastYearDate(Edate), ProductId)+$fs('40110201', 'D', $getFirstDayBY(Sdate) , $lastYearDate(Edate), ProductId)+$fs('40110203', 'D', $getFirstDayBY(Sdate) , $lastYearDate(Edate), ProductId)",
        "I": "=F13+G13+H13"
    }, {
        "_Raven_AutoKey": "_auto_57",
        "A": "           2.基金赎回款",
        "B": "$itemCodeFs('4001', 'J', $getYearFirstDate(Sdate), Edate  , ProductId)*(-1)",
        "C": "$fs('40110302', 'J', $getYearFirstDate(Sdate), Edate , ProductId)+$fs('40110304', 'J', $getYearFirstDate(Sdate), Edate , ProductId)",
        "D": "0-($fs('40110102', 'J', $getYearFirstDate(Sdate), Edate , ProductId)+$fs('40110104', 'J', $getYearFirstDate(Sdate), Edate , ProductId)+$fs('40110202', 'J', $getYearFirstDate(Sdate), Edate , ProductId)+$fs('40110204', 'J', $getYearFirstDate(Sdate), Edate , ProductId))",
        "E": "=B14+C14+D14",
        "F": " $fs('4001', 'J', $getFirstDayBY(Sdate) , $lastYearDate(Edate), ProductId)",
        "G": "$fs('40110302', 'J', $getFirstDayBY(Sdate) , $lastYearDate(Edate), ProductId)+$fs('40110304', 'J', $getFirstDayBY(Sdate) ,$lastYearDate(Edate), ProductId)",
        "H": "0-($fs('40110102', 'J', $getFirstDayBY(Sdate) , $lastYearDate(Edate), ProductId)+$fs('40110104', 'J', $getFirstDayBY(Sdate) ,$lastYearDate(Edate), ProductId)+$fs('40110202', 'J', $getFirstDayBY(Sdate) , $lastYearDate(Edate), ProductId)+$fs('40110204', 'J', $getFirstDayBY(Sdate) , $lastYearDate(Edate), ProductId))",
        "I": "=F14+G14+H14"
    }, {
        "_Raven_AutoKey": "_auto_58",
        "A": "（三）、本期向基金份额持有人分配利润产生的基金净值变动（净值减少以”-“号填列）",
        "C": "0.00",
        "B": "0.00",
        "D": "0-($fs('410401', 'J', $getYearFirstDate(Sdate), Edate , ProductId))",
        "E": "=B15+C15+D15",
        "I": "=F15+G15+H15",
        "F": "0.00",
        "G": "0.00",
        "H": "0-($fs('410401', 'J', $getFirstDayBY(Sdate), $lastYearDate(Edate), ProductId))"
    }, {
        "_Raven_AutoKey": "_auto_59",
        "A": "（四）、其他综合收益结转留存收益（若有）",
        "B": "0.00",
        "C": "$fs('400302', 'D', $getYearFirstDate(Sdate), Edate , ProductId)",
        "D": "0-$fs('400302', 'D', $getYearFirstDate(Sdate), Edate , ProductId)",
        "E": "=B16+C16+D16",
        "I": "=F16+G16+H16",
        "F": "0.00",
        "G": "$fs('400302', 'D', $getFirstDayBY(Sdate), $lastYearDate(Edate), ProductId)",
        "H": "0-$fs('400302', 'D', $getFirstDayBY(Sdate), $lastYearDate(Edate), ProductId)"
    }, {
        "_Raven_AutoKey": "_auto_6",
        "A": "四、本期期末净资产（基金净值）",
        "C": "$balanceTDay('4003', Edate, 0, ProductId)",
        "D": "$balanceTDay('4103',Edate  , 0, ProductId)+$balanceTDay('4104',Edate  , 0, ProductId)-$balanceTDay('410404',Edate  , 0, ProductId)",
        "E": "=B17+C17+D17",
        "I": "=F17+G17+H17",
        "H": "$balanceTDay('4103',$lastYearDate(Edate), 0, ProductId)+$balanceTDay('4104',$lastYearDate(Edate), 0, ProductId)-$balanceTDay('410404',$lastYearDate(Edate), 0, ProductId)",
        "F": "=F9+F10",
        "B": "=B9+B10",
        "G": "$balanceTDay('4003',$lastYearDate(Edate)  , 0, ProductId)"
    }],
    "key2RowIndex": {
        "_auto_51": 0,
        "_auto_50": 1,
        "_auto_0": 2,
        "_auto_1": 3,
        "_auto_2": 4,
        "_auto_53": 5,
        "_auto_52": 6,
        "_auto_54": 7,
        "_auto_3": 8,
        "_auto_4": 9,
        "_auto_5": 10,
        "_auto_55": 11,
        "_auto_56": 12,
        "_auto_57": 13,
        "_auto_58": 14,
        "_auto_59": 15,
        "_auto_6": 16
    },
    "nowRowIndex2realyRowIndex": {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "11": 11,
        "12": 12,
        "13": 13,
        "14": 14,
        "15": 15,
        "16": 16
    },
    "cellSpan": [{
        "start": [2, 2],
        "end": [2, 5]
    }, {
        "start": [2, 1],
        "end": [3, 1]
    }, {
        "start": [2, 6],
        "end": [2, 9]
    }, {
        "start": [0, 1],
        "end": [1, 9]
    }],
    "func": {
        "_auto_2": {
            "E": "=B5+C5+D5",
            "I": "=F5+G5+H5"
        },
        "_auto_3": {
            "E": "=B9+C9+D9",
            "I": "=F9+G9+H9"
        },
        "_auto_4": {
            "C": "=C17-C9",
            "E": "=B10+C10+D10",
            "F": "=F11+F12+F15+F16",
            "I": "=F10+G10+H10",
            "D": "=D17-D9",
            "H": "=H17-H9",
            "B": "=B11+B12+B15+B16",
            "G": "=G17-G9"
        },
        "_auto_5": {
            "E": "=B11+C11+D11",
            "I": "=F11+G11+H11",
            "C": "=C10-C12-C16-C15",
            "D": "=D10-D12-D16-D15",
            "G": "=G10-G12-G16-G15",
            "H": "=H10-H12-H16-H15"
        },
        "_auto_6": {
            "E": "=B17+C17+D17",
            "I": "=F17+G17+H17",
            "B": "=B9+B10",
            "F": "=F9+F10"
        },
        "_auto_53": {
            "E": "=B6+C6+D6",
            "I": "=F6+G6+H6"
        },
        "_auto_52": {
            "E": "=B7+C7+D7",
            "I": "=F7+G7+H7"
        },
        "_auto_54": {
            "E": "=B8+C8+D8",
            "I": "=F8+G8+H8"
        },
        "_auto_56": {
            "E": "=B13+C13+D13",
            "I": "=F13+G13+H13"
        },
        "_auto_55": {
            "F": "=F13+F14",
            "G": "=G13+G14",
            "I": "=F12+G12+H12",
            "B": "=B13+B14",
            "C": "=C13+C14",
            "D": "=D13+D14",
            "E": "=B12+C12+D12",
            "H": "=H13+H14"
        },
        "_auto_57": {
            "E": "=B14+C14+D14",
            "I": "=F14+G14+H14"
        },
        "_auto_58": {
            "E": "=B15+C15+D15",
            "I": "=F15+G15+H15"
        },
        "_auto_59": {
            "E": "=B16+C16+D16",
            "I": "=F16+G16+H16"
        }
    },
    "stepInfo": {
        "step": 73,
        "styleStep": 135,
        "excelStep": 3,
        "idx": 59
    },
    "selRangeStyle": {
        "9,9,9,9": {
            "style": {
                "text-align": "right"
            },
            "step": 121
        },
        "undefined,2,16,2": {
            "style": {
                "text-align": "right"
            },
            "step": 91
        },
        "4,3,16,9": {
            "style": {
                "text-align": "right"
            },
            "step": 81
        },
        "4,1,4,1": {
            "style": {
                "text-align": "left"
            },
            "step": 80,
            "oldStep": 79
        },
        "0,1,1,9": {
            "style": {
                "font-weight": "bolder"
            },
            "step": 82
        },
        "14,9,14,9": {
            "style": {
                "text-align": "right"
            },
            "step": 126
        },
        "14,3,14,3": {
            "style": {
                "text-align": "right"
            },
            "step": 94
        },
        "10,7,10,7": {
            "style": {
                "text-align": "right"
            },
            "step": 112
        },
        "15,9,15,9": {
            "style": {
                "text-align": "right"
            },
            "step": 127
        },
        "13,5,13,5": {
            "style": {
                "text-align": "right"
            },
            "step": 105
        },
        "16,2,16,2": {
            "style": {
                "text-align": "right"
            },
            "step": 134
        },
        "15,3,15,3": {
            "style": {
                "text-align": "right"
            },
            "step": 95
        },
        "11,1,11,1": {
            "style": {
                "text-align": "left"
            },
            "step": 83,
            "oldStep": 80
        },
        "16,9,16,9": {
            "style": {
                "text-align": "right"
            },
            "step": 128
        },
        "10,9,10,9": {
            "style": {
                "text-align": "right"
            },
            "step": 122
        },
        "14,5,14,5": {
            "style": {
                "text-align": "right"
            },
            "step": 106
        },
        "15,5,15,5": {
            "style": {
                "text-align": "right"
            },
            "step": 107
        },
        "11,9,11,9": {
            "style": {
                "text-align": "right"
            },
            "step": 123
        },
        "14,6,14,6": {
            "style": {
                "text-align": "right"
            },
            "step": 130
        },
        "15,6,15,6": {
            "style": {
                "text-align": "right"
            },
            "step": 131
        },
        "14,7,14,7": {
            "style": {
                "text-align": "right"
            },
            "step": 132
        },
        "16,5,16,5": {
            "style": {
                "text-align": "right"
            },
            "step": 108
        },
        "12,9,12,9": {
            "style": {
                "text-align": "right"
            },
            "step": 124
        },
        "14,8,14,8": {
            "style": {
                "text-align": "right"
            },
            "step": 135
        },
        "13,9,13,9": {
            "style": {
                "text-align": "right"
            },
            "step": 125
        },
        "15,7,15,7": {
            "style": {
                "text-align": "right"
            },
            "step": 133
        },
        "14,2,14,2": {
            "style": {
                "text-align": "right"
            },
            "step": 96
        },
        "15,2,16,2": {
            "style": {
                "text-align": "right"
            },
            "step": 88
        },
        "6,3,6,3": {
            "style": {
                "text-align": "right"
            },
            "step": 92
        },
        "7,3,7,3": {
            "style": {
                "text-align": "right"
            },
            "step": 93
        },
        "6,4,6,4": {
            "style": {
                "text-align": "right"
            },
            "step": 97
        },
        "5,5,5,5": {
            "style": {
                "text-align": "right"
            },
            "step": 99
        },
        "7,4,7,4": {
            "style": {
                "text-align": "right"
            },
            "step": 98
        },
        "6,5,6,5": {
            "style": {
                "text-align": "right"
            },
            "step": 100
        },
        "7,5,7,5": {
            "style": {
                "text-align": "right"
            },
            "step": 101
        },
        "6,6,6,6": {
            "style": {
                "text-align": "right"
            },
            "step": 102
        },
        "6,7,6,7": {
            "style": {
                "text-align": "right"
            },
            "step": 110
        },
        "5,8,5,8": {
            "style": {
                "text-align": "right"
            },
            "step": 113
        },
        "7,6,7,6": {
            "style": {
                "text-align": "right"
            },
            "step": 103
        },
        "8,6,8,6": {
            "style": {
                "text-align": "right"
            },
            "step": 104
        },
        "7,7,7,7": {
            "style": {
                "text-align": "right"
            },
            "step": 111
        },
        "6,8,6,8": {
            "style": {
                "text-align": "right"
            },
            "step": 114
        },
        "7,8,7,8": {
            "style": {
                "text-align": "right"
            },
            "step": 115
        },
        "6,9,6,9": {
            "style": {
                "text-align": "right"
            },
            "step": 118
        },
        "7,9,7,9": {
            "style": {
                "text-align": "right"
            },
            "step": 119
        },
        "4,2,16,2": {
            "style": {
                "text-align": "right"
            },
            "step": 84
        },
        "4,1,16,1": {
            "style": {
                "text-align": "left"
            },
            "step": 80
        },
        "8,9,8,9": {
            "style": {
                "text-align": "right"
            },
            "step": 120
        }
    },
    "displayFormat": {
        "9,9,9,9": {
            "mask": "0,000.00",
            "step": 59
        },
        "undefined,2,16,2": {
            "mask": "0,000.00",
            "step": 29
        },
        "4,3,16,9": {
            "mask": "0,000.00",
            "step": 21
        },
        "14,9,14,9": {
            "mask": "0,000.00",
            "step": 64
        },
        "14,3,14,3": {
            "mask": "0,000.00",
            "step": 32
        },
        "10,7,10,7": {
            "mask": "0,000.00",
            "step": 50
        },
        "15,9,15,9": {
            "mask": "0,000.00",
            "step": 65
        },
        "13,5,13,5": {
            "mask": "0,000.00",
            "step": 43
        },
        "16,2,16,2": {
            "mask": "0,000.00",
            "step": 72
        },
        "15,3,15,3": {
            "mask": "0,000.00",
            "step": 33
        },
        "16,9,16,9": {
            "mask": "0,000.00",
            "step": 66
        },
        "10,9,10,9": {
            "mask": "0,000.00",
            "step": 60
        },
        "14,5,14,5": {
            "mask": "0,000.00",
            "step": 44
        },
        "15,5,15,5": {
            "mask": "0,000.00",
            "step": 45
        },
        "11,9,11,9": {
            "mask": "0,000.00",
            "step": 61
        },
        "14,6,14,6": {
            "mask": "0,000.00",
            "step": 68
        },
        "15,6,15,6": {
            "mask": "0,000.00",
            "step": 69
        },
        "14,7,14,7": {
            "mask": "0,000.00",
            "step": 70
        },
        "16,5,16,5": {
            "mask": "0,000.00",
            "step": 46
        },
        "12,9,12,9": {
            "mask": "0,000.00",
            "step": 62
        },
        "14,8,14,8": {
            "mask": "0,000.00",
            "step": 73
        },
        "13,9,13,9": {
            "mask": "0,000.00",
            "step": 63
        },
        "15,7,15,7": {
            "mask": "0,000.00",
            "step": 71
        },
        "14,2,14,2": {
            "mask": "0,000.00",
            "step": 34
        },
        "15,2,16,2": {
            "mask": "0,000.00",
            "step": 26
        },
        "6,3,6,3": {
            "mask": "0,000.00",
            "step": 30
        },
        "7,3,7,3": {
            "mask": "0,000.00",
            "step": 31
        },
        "6,4,6,4": {
            "mask": "0,000.00",
            "step": 35
        },
        "5,5,5,5": {
            "mask": "0,000.00",
            "step": 37
        },
        "7,4,7,4": {
            "mask": "0,000.00",
            "step": 36
        },
        "6,5,6,5": {
            "mask": "0,000.00",
            "step": 38
        },
        "7,5,7,5": {
            "mask": "0,000.00",
            "step": 39
        },
        "6,6,6,6": {
            "mask": "0,000.00",
            "step": 40
        },
        "6,7,6,7": {
            "mask": "0,000.00",
            "step": 48
        },
        "5,8,5,8": {
            "mask": "0,000.00",
            "step": 51
        },
        "7,6,7,6": {
            "mask": "0,000.00",
            "step": 41
        },
        "8,6,8,6": {
            "mask": "0,000.00",
            "step": 42
        },
        "7,7,7,7": {
            "mask": "0,000.00",
            "step": 49
        },
        "6,8,6,8": {
            "mask": "0,000.00",
            "step": 52
        },
        "7,8,7,8": {
            "mask": "0,000.00",
            "step": 53
        },
        "6,9,6,9": {
            "mask": "0,000.00",
            "step": 56
        },
        "7,9,7,9": {
            "mask": "0,000.00",
            "step": 57
        },
        "4,2,16,2": {
            "mask": "0,000.00",
            "step": 22
        },
        "8,9,8,9": {
            "mask": "0,000.00",
            "step": 58
        }
    }
}