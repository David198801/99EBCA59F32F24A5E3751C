import sql_metadata
import re

sql = '''INSERT INTO T_PA_PRO_PARA(FID, FPROGRAM_ID, FPRODUCT_ID, FITEM_ID, FCODE, FNAME, FREMARK, FTYPE_CODE, FGROUP_CODE, FKJ_TYPE, FMULTISELECT, FVALUE, FVALUE_DISPLAY, FCONDITION, FCONDITION_DISPLAY, FEDIT_REASON, FDELETE_REASON, FCREATOR_ID, FCREATE_TIME, FLAST_EDITOR_ID, FLAST_EDIT_TIME, FDELETE_USER_ID, FMARK_DELETE_TIME, FDELETED, FCHECKED, FCHECKER_ID, FCHECK_TIME, FREL_ID, FAPLI_MODULE)
VALUES(20062909364863170773, 0, 0, 19120520380000000042, 'ZXSJ_DQGX', '财汇债品数据读取更新字段', '在读取债券信息时，对于未手工维护过的固定利率债券的特定字段进行更新。
字段代码：[{FXPL,付息频率},{ZQLX,债券类型},{SQPMLV:税前票面利率},{SHPMLV:税后票面利率},{JXQSR:计息起始日},{JXJZR:计息截止日},{SCFXR:首次付息日}
,{ZXMZ:最新面值},{TZFS:投资方式},{FXJG:发行价格}]。不设置默认更新SQPMLV,SHPMLV字段。例如：维护ZQLX表示更新证券类型字段，更新多个字段使用英文逗号{,}维护，例如：ZQLX,SQPMLV,SHPMLV,FXPL,SCFXR', 'CSFL04', 'CSMX_QTSD', 'TEXT', 0, 'SQPMLV,JXQSQ,ZXMZ,SCFXR,LLLX,JZRJXFS,FXJG', , NULL, NULL, NULL, NULL, 20071719473203000909, TIMESTAMP '2021-09-23 20:28:40.000000', 20071719473203000909, TIMESTAMP '2021-09-23 20:28:40.000000', NULL, NULL, 0, 1, 20071719473203000909, TIMESTAMP '2021-09-23 20:33:10.000000', NULL, NULL);
'''

def is_count_odd(s, c):
    n = s.count(c)
    return n % 2 != 0


def is_pairs(s, c1, c2):
    return s.count(c1) == s.count(c2)


def parse_insert(sql):
    sql = sql.replace("\n","")
    fields_str = None
    values_str = None
    s = re.search(r'INSERT\s+INTO.+\((.*)\)\s*VALUES\s*\((.*)\)', sql, re.IGNORECASE)
    if s and len(s.groups()) >= 2:
        fields_str = s.group(1)
        values_str = s.group(2)
    print(fields_str)

    fields = fields_str.split(",")
    fields = [x.strip() for x in fields]
    values = []

    # 处理括号包裹的逗号被分割的情况
    sp = values_str.split(",")
    flag = False
    count_left = 0
    count_right = 0
    for i in sp:
        trim = i.strip()
        if flag:
            count_left += trim.count("(")
            count_right += trim.count(")")
            if ")" in trim and count_left == count_right:
                flag = False
                count_left = 0
                count_right = 0
            values[-1] += "," + trim
        else:
            if "(" in trim and (not is_pairs(trim, "(", ")")):
                flag = True
                count_left += trim.count("(")
                count_right += trim.count(")")
            values.append(trim)

    # 处理单引号包裹的逗号被分割的情况
    sp = values
    values = []
    flag = False
    for i in sp:
        trim = i.strip()
        if flag:
            if (trim.endswith("'") and (not trim.startswith("'"))):
                flag = False
            values[-1] += "," + trim
        else:
            if trim.startswith("'") and (is_count_odd(trim, "'") or not trim.endswith("'")):
                flag = True
            values.append(trim)

    if fields and values and len(fields) == len(values):
        return {fields[i]: values[i] for i in range(len(fields))}
    else:
        print("未正确解析INSERT语句:")
        print("fields=", fields)
        print("values=", values)

print(parse_insert(sql))