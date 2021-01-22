def ajstatic(loadandratio):
    '''  loadandratio = {'EXP': '0.08', 'EYN': '0.09'} key and value is str  '''

    import comtypes.client

    myETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
    SapModel = myETABSObject.SapModel

    ret = SapModel.SetModelIsLocked(False)

    NumberNames = 0
    MyName = []
    [NumberNames, MyName, ret] = SapModel.LoadPatterns.GetNameList(NumberNames,MyName)  # بدست آوردن اسم همه بارهای تعریف شده

    LoadPatternList = MyName
    ret = SapModel.DatabaseTables.SetLoadPatternsSelectedForDisplay(LoadPatternList)  # ست کردن همه بارهای موجود برای نمایش در جدول

    ############################ GetTableForDisplayArray  ( اطلاعات و دیتای جدولی که به آن داده می شود کامل در یک آرایه یا لیست نمایش می دهد )
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

    FieldsKeysIncluded1 = ['Name', 'Is Auto Load', 'X Dir?', 'X Dir Plus Ecc?', 'X Dir Minus Ecc?',
                           'Y Dir?', 'Y Dir Plus Ecc?', 'Y Dir Minus Ecc?',
                           'Ecc Ratio', 'Top Story', 'Bot Story', 'C',
                           'K']  # توجه اگر اسم ستونهای موجود در جدول اصلی را اینجا نیاوریم خود برنامه مقدار پیش فرض خود را برای آن قرار میدهد اگر هم تعدا اسمهای اینجا نسبت به جدول اصلی خیلی کم باشد برنامه ایتبس قاطی میکند و جدول درست وارد نمی شود
    TableData2 = list(TableData)

    TableData1 = []
    for i in TableData2:
        if i == None:
            continue
        TableData1.append(i)

    for i in TableData1:
        if i in loadandratio:
            indexx = TableData1.index(i)
            n = indexx + 8
            TableData1[n] = loadandratio[i]
    ret = SapModel.DatabaseTables.SetTableForEditingArray(TableKey, TableVersion, FieldsKeysIncluded1, NumberRecords,
                                                          TableData1)

    FillImportLog = True
    NumFatalErrors = 0
    NumErrorMsgs = 0
    NumWarnMsgs = 0
    NumInfoMsgs = 0
    ImportLog = ''
    [NumFatalErrors, NumErrorMsgs, NumWarnMsgs, NumInfoMsgs, ImportLog,
     ret] = SapModel.DatabaseTables.ApplyEditedTables(FillImportLog, NumFatalErrors,
                                                      NumErrorMsgs, NumWarnMsgs, NumInfoMsgs, ImportLog)

    del NumberNames
    del MyName
    del LoadPatternList
    del TableData2
    del TableData
    del FieldsKeysIncluded
    del FieldKeyList
    del TableData1


def ajdynamic(loadandratio):
    '''  loadandratio = {'SPXE': '0.08', 'SPYE': '0.09'} key and value is str  '''

    import comtypes.client
    myETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
    SapModel = myETABSObject.SapModel

    ret = SapModel.SetModelIsLocked(False)

    for i in loadandratio:
        Name = i
        Eccen = float(loadandratio[i])
        ret = SapModel.LoadCases.ResponseSpectrum.SetEccentricity(Name, Eccen)


def aj(static, dynamic, defult):
    '''static and dynamic and defult are True  '''
    
    import comtypes.client
    from e2018.pich import pich
    myETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
    SapModel = myETABSObject.SapModel
    ret = SapModel.Analyze.RunAnalysis()
    # ret = SapModel.SetModelIsLocked(False)
    # =================
    TableKey = 'Load Case Definitions - Response Spectrum'
    FieldKeyList = []
    GroupName = ''
    TableVersion = 0
    FieldsKeysIncluded = []
    NumberRecords = 0
    TableData = []
    [FieldKeyList,
     TableVersion,
     FieldsKeysIncluded,
     NumberRecords,
     TableData,
     ret] = SapModel.DatabaseTables.GetTableForDisplayArray(TableKey,
                                                            FieldKeyList,
                                                            GroupName,
                                                            TableVersion,
                                                            FieldsKeysIncluded,
                                                            NumberRecords,
                                                            TableData)
    dynamicload = []
    dynamicload2 = []
    j = 0
    n = len(FieldsKeysIncluded)
    for i in range(NumberRecords):
        dynamicload.append(TableData[j])
        if TableData[j+11] != '0':
            dynamicload2.append(TableData[j])
        j += n
    # ====================================
    Eload = []
    NumberNames = 0
    MyType = 0
    MyName = []
    [NumberNames, MyName, ret] = SapModel.LoadPatterns.GetNameList(NumberNames, MyName)
    for i in MyName:
        [MyType, ret] = SapModel.LoadPatterns.GetLoadType(i, MyType)
        if MyType == 5:  # 5 = quick
            Eload.append(i)
    # ===================================
    ret = SapModel.DatabaseTables.SetLoadPatternsSelectedForDisplay(Eload)
    loadcase = Eload + dynamicload
    loadcase2 = Eload + dynamicload2
    ret = SapModel.DatabaseTables.SetLoadCasesSelectedForDisplay(loadcase)
    ret = SapModel.DatabaseTables.SetLoadCombinationsSelectedForDisplay('')

    # ===================================
    pichdata = pich()
    ajeccx = 0.05
    ajeccy = 0.05
    for i in pichdata:
        if i[1] in dynamicload:
            continue
        else:
            if i[-2] != '1.00':
                var = float(i[-2]) * 0.05
                if i[2] == 'Diaph D1 Y' and var > ajeccy:
                    ajeccy = var
                elif i[2] == 'Diaph D1 X' and var > ajeccx:
                    ajeccx = var
                else:
                    continue
    ajeccx = '%.4f' % (ajeccx)
    ajeccy = '%.4f' % (ajeccy)

    loadandratio = {}
    for i in pichdata:
        if i[1] in loadandratio:
            continue
        else:
            if i[1] in loadcase2:
                if i[2] == 'Diaph D1 Y':
                    loadandratio[i[1]] = ajeccy
                elif i[2] == 'Diaph D1 X':
                    loadandratio[i[1]] = ajeccx
                else:
                    break
    if defult == True:
        for i in loadandratio:
            loadandratio[i] = '0.05'
    if static == True:
        ajstatic(loadandratio)
    if dynamic == True:
        ajdynamic(loadandratio)
    ret = SapModel.Analyze.RunAnalysis()

