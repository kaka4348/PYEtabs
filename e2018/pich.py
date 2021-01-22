def pich():

    import comtypes.client

    myETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
    SapModel = myETABSObject.SapModel
    # kgf_cm_C = 14
    # ret = SapModel.SetPresentUnits(kgf_cm_C)
    # ret = SapModel.Analyze.RunAnalysis()
    #========================================
    # بدست اوردن همه بارهای تعریف شده و انتخاب آنها در جدول لود پترن
    NumberNames = 0
    MyName = []
    [NumberNames, MyName, ret] = SapModel.LoadPatterns.GetNameList(NumberNames,MyName)  # بدست آوردن اسم همه بارهای تعریف شده
    LoadPatternList = MyName
    ret = SapModel.DatabaseTables.SetLoadPatternsSelectedForDisplay(LoadPatternList)  # ست کردن همه بارهای موجود برای نمایش در جدول

    #========================================
    # بدست آوردن اسم بارهای زلزله و جهت آنها
    TableKey = 'Load Pattern Definitions - Auto Seismic - User Coefficient'
    FieldKeyList = []
    GroupName = ''
    TableVersion = 0
    FieldsKeysIncluded = []
    NumberRecords = 0
    TableData = []
    [FieldKeyList, TableVersion, FieldsKeysIncluded, NumberRecords, TableData,
     ret] = SapModel.DatabaseTables.GetTableForDisplayArray(TableKey, FieldKeyList, GroupName, TableVersion,
                                                            FieldsKeysIncluded, NumberRecords, TableData)

    dataload = []
    datatload = []
    len2 = len(FieldsKeysIncluded)
    len1 = len(TableData) / len2
    j = 0
    for i in range(int(len1)):
        for i in range(int(len2)):
            datatload.append(TableData[j])
            j += 1
        dataload.append(datatload)
        datatload = []
    #تعین جهت بارهای زلزله ==================
    x_loadname = []
    y_loadname = []
    for i in dataload:
        if i[2] == 'Yes' or i[3] == 'Yes' or i[4] == 'Yes':
            x_loadname.append(i[0])
        if i[5] == 'Yes' or i[6] == 'Yes' or i[7] == 'Yes':
            y_loadname.append(i[0])

    # ======================================= show table data

    TableKey = 'Diaphragm Max Over Avg Drifts'
    FieldKeyList = []
    GroupName = 'Diaphragm Max Over Avg Drifts'
    TableVersion = 0
    FieldsKeysIncluded = []
    NumberRecords = 0
    TableData = []

    [FieldKeyList, TableVersion, FieldsKeysIncluded, NumberRecords, TableData,
     ret] = SapModel.DatabaseTables.GetTableForDisplayArray(TableKey, FieldKeyList, GroupName, TableVersion,
                                                            FieldsKeysIncluded, NumberRecords, TableData)

    # ======================================== sort table data to list data
    data = []
    datat = []
    len2 = len(FieldsKeysIncluded)
    len1 = len(TableData) / len2
    j = 0
    for i in range(int(len1)):
        for i in range(int(len2)):
            datat.append(TableData[j])
            j += 1
        data.append(datat)
        datat = []
    #  moratab sazi bar asas onsore 2 listhaye dakheli ke bar ha hastan
    data = sorted(data, key=lambda load: load[1])
    data2 = []
    data3 = []
    for i in data:
        for j in i:
            if j == None:
                continue
            if j == 'Max':
                continue
            if j == 'Min':
                continue
            data2.append(j)
        data3.append(data2)
        data2 = []
    data = data3
    del data3
    del data2

    #حذف نتایج بارهای زلزله در جهت مخالف مثلا وای برای ex===========

    datax = list(filter(lambda x: x[1] in x_loadname and x[3] == 'Diaph D1 X', data))
    datay = list(filter(lambda x: x[1] in y_loadname and x[3] == 'Diaph D1 Y', data))
    data = datax+datay
    data.sort(key=lambda x: x[1], reverse=True)


    # tedad tabaghat
    i = 1
    n = 1
    while data[i][0] != data[0][0]:
        n += 1
        i += 1

    # ============================================ pichesh
    pich = []
    for i in range(len(data)):
        ratio = float(data[i][6])
        t = ''
        if ratio <= 1.2:
            t = 'منظم پیچشی'
        elif 1.2 < ratio < 1.4:
            t = 'نامنظم پیچشی'
        else:
            t = 'نامنظمی شدید پیچشی'
        Aj = (ratio / 1.2) ** 2
        if Aj <= 1:
            Aj = 1
        elif Aj >= 3:
            Aj = 3
        Ajst = '%.2f' % (Aj)
        p = [data[i][0], data[i][1], data[i][3], data[i][4], data[i][5], data[i][6], Ajst, t]
        pich.append(p)
        i += 1
    return pich





