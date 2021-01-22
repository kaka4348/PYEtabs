def maxdrift(cdx, cdy):

    import comtypes.client

    myETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
    SapModel = myETABSObject.SapModel
    #kgf_cm_C = 14
    #ret = SapModel.SetPresentUnits(kgf_cm_C)
    #ret = SapModel.Analyze.RunAnalysis()

    #======================================= show table data

    TableKey = 'Diaphragm Max Over Avg Drifts'
    FieldKeyList = []
    GroupName = 'Diaphragm Max Over Avg Drifts'
    TableVersion = 0
    FieldsKeysIncluded = []
    NumberRecords = 0
    TableData = []

    [FieldKeyList, TableVersion, FieldsKeysIncluded, NumberRecords, TableData, ret] = SapModel.DatabaseTables.GetTableForDisplayArray(TableKey, FieldKeyList, GroupName, TableVersion, FieldsKeysIncluded, NumberRecords, TableData)

    #======================================== sort table data to list data
    data=[]
    datat=[]
    len2=len(FieldsKeysIncluded)
    len1=len(TableData)/len2
    j=0
    for i in range(int(len1)):
        for i in range(int(len2)):
            datat.append(TableData[j])
            j+=1
        data.append(datat)
        datat=[]
    #  moratab sazi bar asas onsore 2 listhaye dakheli ke bar ha hastan
    data=sorted(data, key=lambda load : load[1])
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

    # tedad tabaghat
    i=1
    n=1
    while data[i][0]!=data[0][0]:
        n+=1
        i+=1

    #============================================ max drift

    drift=[]
    for i in range(len(data)):
        if n <= 5:
            nn = 0.025
        else:
            nn = 0.02
        if data[i][3][-1] == 'X':
            cd = cdx
        elif data[i][3][-1] == 'Y':
            cd = cdy
        alldrift = nn/cd
        if float(data[i][4]) <= alldrift:
            ok = 'ok'
        else:
            ok = 'not ok'
        p=[data[i][0], data[i][1], data[i][3], data[i][4],'%.6f'%(alldrift), ok]
        drift.append(p)
        i+=1
    return drift

