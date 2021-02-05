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
            j += 1
        data.append(datat)
        datat=[]
    #  moratab sazi bar asas onsore 2 listhaye dakheli ke bar ha hastan
    data = sorted(data, key=lambda load: load[FieldsKeysIncluded.index('OutputCase')])
    data = list(filter(lambda x: x[FieldsKeysIncluded.index('Item')] == 'Diaph D1 X' or x[FieldsKeysIncluded.index('Item')] =='Diaph D1 Y', data))



    # tedad tabaghat
    storyname = []
    for i in data:
        storyname.append(i[FieldsKeysIncluded.index('Story')])
    storyname = list(set(storyname))
    n = len(storyname)

    #============================================ cm drift
    drift = []
    for i in range(len(data)):
        if n <= 5:
            nn = 0.025
        else:
            nn = 0.02
        if data[i][FieldsKeysIncluded.index('Item')] == 'Diaph D1 X':
            cd = cdx
        elif data[i][FieldsKeysIncluded.index('Item')] == 'Diaph D1 Y':
            cd = cdy
        alldrift = nn/cd
        if float(data[i][FieldsKeysIncluded.index('Max Drift')]) <= alldrift:
            ok = 'ok'
        else:
            ok = 'not ok'
        p = [data[i][FieldsKeysIncluded.index('Story')], data[i][FieldsKeysIncluded.index('OutputCase')], data[i][FieldsKeysIncluded.index('Item')], data[i][FieldsKeysIncluded.index('Max Drift')], '%.6f'%(alldrift), ok]
        drift.append(p)
        i += 1
    return drift
