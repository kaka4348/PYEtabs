def vazhgooni(x, y):
    
    import comtypes.client

    myETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
    SapModel = myETABSObject.SapModel
    #kgf_cm_C = 14
    #ret = SapModel.SetPresentUnits(kgf_cm_C)

    #======================================= cm data

    TableKey = 'Centers Of Mass And Rigidity'
    FieldKeyList = []
    GroupName = 'Centers Of Mass And Rigidity'
    TableVersion = 0
    FieldsKeysIncluded = []
    NumberRecords = 0
    TableData = []
    [FieldKeyList, TableVersion, FieldsKeysIncluded, NumberRecords, TableData, ret] = SapModel.DatabaseTables.GetTableForDisplayArray(TableKey, FieldKeyList, GroupName, TableVersion, FieldsKeysIncluded, NumberRecords, TableData)


    datacm=[]
    datat=[]
    len2=len(FieldsKeysIncluded)
    len1=len(TableData)/len2
    j=0
    for i in range(int(len1)):
        for i in range(int(len2)):
            datat.append(TableData[j])
            j+=1
        datacm.append(datat)
        datat=[]

    datacm = list(filter(lambda x: x[FieldsKeysIncluded.index('Diaphragm')] == 'D1', datacm))


    xccm = float(datacm[-1][FieldsKeysIncluded.index('XCCM')])
    yccm = float(datacm[-1][FieldsKeysIncluded.index('YCCM')])


    #================================================= W table

    TableKey = 'Load Pattern Definitions - Auto Seismic - User Coefficient'
    FieldKeyList = []
    GroupName = 'Load Pattern Definitions - Auto Seismic - User Coefficient'
    TableVersion = 0
    FieldsKeysIncluded = []
    NumberRecords = 0
    TableData = []
    [FieldKeyList, TableVersion, FieldsKeysIncluded, NumberRecords, TableData, ret] = SapModel.DatabaseTables.GetTableForDisplayArray(TableKey, FieldKeyList, GroupName, TableVersion, FieldsKeysIncluded, NumberRecords, TableData)


    dataw=[]
    datat=[]
    len2=len(FieldsKeysIncluded)
    len1=len(TableData)/len2
    j=0
    for i in range(int(len1)):
        for i in range(int(len2)):
            datat.append(TableData[j])
            j+=1
        dataw.append(datat)
        datat=[]

    w = float(dataw[0][FieldsKeysIncluded.index('WeightUsed')])


    #================================================ M (active) data

    TableKey = 'Base Reactions'
    FieldKeyList = []
    GroupName = 'Base Reactions'
    TableVersion = 0
    FieldsKeysIncluded = []
    NumberRecords = 0
    TableData = []
    [FieldKeyList, TableVersion, FieldsKeysIncluded, NumberRecords, TableData, ret] = SapModel.DatabaseTables.GetTableForDisplayArray(TableKey, FieldKeyList, GroupName, TableVersion, FieldsKeysIncluded, NumberRecords, TableData)


    datam=[]
    datat=[]
    len2=len(FieldsKeysIncluded)
    len1=len(TableData)/len2
    j=0
    for i in range(int(len1)):
        for i in range(int(len2)):
            datat.append(TableData[j])
            j+=1
        datam.append(datat)
        datat=[]



    #============================================ vazhgooni

    mx = 0
    my = 0
    for i in datam:
        if my < abs(float(i[FieldsKeysIncluded.index('MY')])):
            my = abs(float(i[FieldsKeysIncluded.index('MY')]))
        if mx < abs(float(i[FieldsKeysIncluded.index('MX')])):
            mx = abs(float(i[FieldsKeysIncluded.index('MX')]))


    if xccm <= x - xccm: xcm = xccm
    else : xcm = x - xccm
    if yccm <= y - yccm: ycm = yccm
    else : ycm = y - yccm
    fsx = w*xcm/my
    if fsx >= 1 : okx = 'ok'
    else : okx = ' not ok'
    fsy = w*ycm/mx
    if fsy >= 1 : oky = 'ok'
    else : oky = ' not ok'

    vazh = [['W', 'XCM', 'My(active)', 'F.S', 'ok or not'],
                 [str(w), '%.3f'%(xcm), str(my), '%.2f'%(fsx), okx],
                 ['W', 'YCM', 'Mx(active)', 'F.S', 'ok or not'],
                 [str(w), '%.3f'%(ycm), str(mx), '%.2f'%(fsy), oky]
                 ]
    return vazh



