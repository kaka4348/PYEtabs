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
        if i[FieldsKeysIncluded.index('XDir')] == 'Yes' or i[FieldsKeysIncluded.index('XDirPlusE')] == 'Yes' or i[FieldsKeysIncluded.index('XDirMinusE')] == 'Yes':
            x_loadname.append(i[FieldsKeysIncluded.index('Name')])
        if i[FieldsKeysIncluded.index('YDir')] == 'Yes' or i[FieldsKeysIncluded.index('YDirPlusE')] == 'Yes' or i[FieldsKeysIncluded.index('YDirMinusE')] == 'Yes':
            y_loadname.append(i[FieldsKeysIncluded.index('Name')])

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
    data = list(filter(lambda x: x[FieldsKeysIncluded.index('Item')] == 'Diaph D1 X' or x[FieldsKeysIncluded.index('Item')] == 'Diaph D1 Y', data))

    #حذف نتایج بارهای زلزله در جهت مخالف مثلا وای برای ex===========

    datax = list(filter(lambda x: x[FieldsKeysIncluded.index('OutputCase')] in x_loadname and x[FieldsKeysIncluded.index('Item')] == 'Diaph D1 X', data))
    datay = list(filter(lambda x: x[FieldsKeysIncluded.index('OutputCase')] in y_loadname and x[FieldsKeysIncluded.index('Item')] == 'Diaph D1 Y', data))
    data = datax+datay
    data.sort(key=lambda x: x[FieldsKeysIncluded.index('OutputCase')], reverse=True)


    # tedad tabaghat
    storyname = []
    for i in data:
        storyname.append(i[FieldsKeysIncluded.index('Story')])
    storyname = list(set(storyname))
    n = len(storyname)

    # ============================================ pichesh
    pich = []
    for i in range(len(data)):
        ratio = float(data[i][FieldsKeysIncluded.index('Ratio')])
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
        p = [data[i][FieldsKeysIncluded.index('Story')], data[i][FieldsKeysIncluded.index('OutputCase')], data[i][FieldsKeysIncluded.index('Item')], data[i][FieldsKeysIncluded.index('Max Drift')], data[i][FieldsKeysIncluded.index('Avg Drift')], data[i][FieldsKeysIncluded.index('Ratio')], Ajst, t]
        pich.append(p)
        i += 1
    return pich





