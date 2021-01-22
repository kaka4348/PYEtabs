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
    datacm=sorted(datacm, key=lambda D : D[1], reverse=True)
    data2 = []
    data3 = []
    for i in datacm:
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
    datacm = data3
    del data3
    del data2

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

    data2 = []
    data3 = []
    for i in dataw:
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
    dataw = data3
    del data3
    del data2



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


    data2 = []
    data3 = []
    for i in datam:
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
    datam = data3
    del data3
    del data2

    #============================================ vazhgooni

    xccm = float(datacm[-1][8])
    yccm = float(datacm[-1][9])
    w = float(dataw[0][13])
    j = 0
    for i in datam:
        if datam[j][0] == 'EX':
            my = abs(float(datam[j][6]))
        elif datam[j][0] == 'EY':
            mx = abs(float(datam[j][5]))
        j += 1

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



