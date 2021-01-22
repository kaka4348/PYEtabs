def MomentBeam():
    import comtypes.client

    myETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
    SapModel = myETABSObject.SapModel
    # ret = SapModel.SetModelIsLocked(False)
    ret = SapModel.Analyze.RunAnalysis()
    # ret = SapModel.DesignSteel.SetCode('AISC 360-05')
    ret = SapModel.DesignSteel.StartDesign()
    ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()


    kgf_cm_C = 14
    ret = SapModel.SetPresentUnits(kgf_cm_C)


    #=======================
    listofframeprop = {
    1:'I',
    2:'Channel',
    3:'T',
    4:'Angle',
    5:'DblAngle',
    6:'Box',
    7:'Pipe',
    8:'Rectangular',
    9:'Circle',
    10:'General',
    11:'DbChannel',
    12:'Auto',
    13:'SD',
    14:'Variable',
    15:'Joist',
    16:'Bridge',
    17:'Cold_C',
    18:'Cold_2C',
    19:'Cold_Z',
    20:'Cold_L',
    21:'Cold_2L',
    22:'Cold_Hat',
    23:'BuiltupICoverplate',
    24:'PCCGirderI',
    25:'PCCGirderU',
    26:'BuiltupIHybrid',
    27:'BuiltupUHybrid',
    28:'Concrete_L',
    29:'FilledTube',
    30:'FilledPipe',
    31:'EncasedRectangle',
    32:'EncasedCircle',
    33:'BucklingRestrainedBrace',
    34:'CoreBrace_BRB',
    35:'ConcreteTee',
    36:'ConcreteBox',
    37:'ConcretePipe',
    38:'ConcreteCross',
    39:'SteelPlate',
    40:'SteelRod',
    }
    #=======================


    #  دریافت کد انتخاب شده برای طراحی فلزی
    CodeName = ''
    [CodeName, ret] = SapModel.DesignSteel.GetCode(CodeName)


    # لیست تیرهای مورد نظر همراه با مشخصات لازم
    beamlist = []


    # پیدا کردن اسم بارهای مرده و زنده و برف تعریف شده
    d_load_name = []
    l_load_name = []
    s_load_name = []
    NumberNames = 0
    MyType = 0
    MyName = []
    [NumberNames, MyName, ret] = SapModel.LoadPatterns.GetNameList(NumberNames, MyName)
    for i in MyName:
        [MyType, ret] = SapModel.LoadPatterns.GetLoadType(i, MyType)
        if MyType == 1 or MyType == 2:  # d = 1 , sd = 2
            d_load_name.append(i)
        elif MyType == 3 or MyType == 4 or MyType == 11: # l = 3 , R-l = 4 , lroof = 11
            l_load_name.append(i)
        elif MyType == 7: # snow = 7
            s_load_name.append(i)


    #  GetAllFrames   Retrieves select data for all frame objects in the model
    NumberNames = 0
    MyName = []
    PropName = []
    StoryName = []
    PointName1 = []
    PointName2 = []
    Point1X = []
    Point1Y = []
    Point1Z = []
    Point2X = []
    Point2Y = []
    Point2Z = []
    Angle = []
    Offset1X = []
    Offset2X = []
    Offset1Y = []
    Offset2Y = []
    Offset1Z = []
    Offset2Z = []
    CardinalPoint = []
    [NumberNames, MyName, PropName, StoryName, PointName1,
    PointName2, Point1X, Point1Y, Point1Z, Point2X, Point2Y, Point2Z,
    Angle, Offset1X, Offset2X, Offset1Y, Offset2Y, Offset1Z, Offset2Z, CardinalPoint, ret] = SapModel.FrameObj.GetAllFrames(NumberNames, MyName, PropName, StoryName,PointName1,
    PointName2, Point1X, Point1Y, Point1Z, Point2X, Point2Y, Point2Z,
    Angle, Offset1X, Offset2X, Offset1Y, Offset2Y, Offset1Z, Offset2Z, CardinalPoint)


    def get_w_load(Name, L):
        # L = طول تیر
        # Name = '114' # input
        ItemTypeElm = 0 # elm type
        NumberResults = 0
        Obj = []
        ObjSta = []
        Elm = []
        ElmSta = []
        LoadCase = []
        StepType = []
        StepNum = []
        P = []
        V2 = []
        V3 = []
        T = []
        M2 = []
        M3 = []
        [NumberResults, Obj, ObjSta,
        Elm, ElmSta, LoadCase, StepType,
        StepNum, P, V2, V3, T, M2, M3,
        ret] = SapModel.Results.FrameForce(Name, ItemTypeElm, NumberResults, Obj, ObjSta,
                                                  Elm, ElmSta, LoadCase, StepType, StepNum, P, V2, V3, T, M2, M3)
        V2 = list(map(lambda x: float(x), V2))
        vmin0 = min(V2)
        vmax0 = max(V2)
        vmax = max(abs(vmax0), abs(vmin0))
        w = vmax*2/L

        return w


    # جدا کردن تیرهای خمشی
    for i in range(len(MyName)):
        beam = {}
        Name = MyName[i]
        II = []
        JJ = []
        StartValue = []
        EndValue = []
        [II, JJ, StartValue, EndValue, ret] = SapModel.FrameObj.GetReleases(Name, II, JJ, StartValue, EndValue)

        Label = ''
        Story = ''
        [Label, Story, ret] = SapModel.FrameObj.GetLabelFromName(Name, Label, Story)

        if (not(True in II or True in JJ)) and Label[0] == 'B':
            # Name = '114'  # input
            #Item = 18  # input
            Value = 0
            ProgDet = 0
            # بدست آوردن ضریب طول مهار نشده در راستای ماژور
            if CodeName == 'AISC 360-10':
                Item = 21
                [Value, ProgDet, ret] = SapModel.DesignSteel.AISC360_10.GetOverwrite(Name, Item, Value, ProgDet)
            elif CodeName == 'AISC 360-16':
                Item = 25
                [Value, ProgDet, ret] = SapModel.DesignSteel.AISC360_16.GetOverwrite(Name, Item, Value, ProgDet)
            else:
                Item = 18
                [Value, ProgDet, ret] = SapModel.DesignSteel.AISC360_05_IBC2006.GetOverwrite(Name, Item, Value, ProgDet)
            Value = round(Value, 3)
            from math import sqrt, atan, degrees
            xlen = abs(Point1X[i]-Point2X[i])
            ylen = abs(Point1Y[i]-Point2Y[i])
            zln = abs(Point1Z[i]-Point2Z[i])
            if xlen and ylen:
                h_angel = degrees(atan(ylen/xlen))
                if h_angel > 45:
                    h_angel = 90-h_angel
            else:
                h_angel = 0
            lenbeam = sqrt(xlen**2+ylen**2+zln**2)
            beam['name'] = PropName[i]
            beam['ID'] = Name
            beam['label'] = Label
            beam['story'] = Story
            beam['h_angel'] = round(h_angel,1)
            beam['L_ax'] = round(lenbeam, 3)
            beam['unbrace major ratio'] = Value
            if Value:
                beam['Ln'] = round(lenbeam*Value, 3)
            else:
                beam['Ln'] = round(lenbeam, 3)

            # بدست آوردن بار روی تیر
            all_load = d_load_name + l_load_name + s_load_name
            for j in all_load:
                ret = SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
                ret = SapModel.Results.Setup.SetCaseSelectedForOutput(j)
                wload = get_w_load(Name, beam['L_ax'])
                beam[j] = wload
            d_sum = 0
            l_sum = 0
            s_sum = 0
            for j in d_load_name:
                d_sum += beam[j]
            for j in l_load_name:
                l_sum += beam[j]
            for j in s_load_name:
                s_sum += beam[j]
            beam['d_sum'] = d_sum
            beam['l_sum'] = l_sum
            beam['s_sum'] = s_sum

            beamlist.append(beam)


    def property_of_section(Name):
        #Name = 'IPE160' # input
        Area = 0
        As2 = 0
        As3 = 0
        Torsion = 0
        I22 = 0
        I33 = 0
        S22 = 0
        S33 = 0
        Z22 = 0
        Z33 = 0
        R22 = 0
        R33 = 0
        [Area, As2, As3, Torsion,
        I22, I33, S22, S33, Z22, Z33,
        R22, R33, ret] = SapModel.PropFrame.GetSectProps(Name, Area, As2, As3, Torsion,
        I22, I33, S22, S33, Z22, Z33,
        R22, R33)
        return {'Area': Area, 'As2': As2, 'AS3': As3, 'Torsion': Torsion,
                'I22': I22, 'I33': I33, 'S22': S22, 'S33': S33, 'Z22': Z22,
                'Z33': Z33, 'R22': R22, 'R33': R33}


    def mateial_of_section_prop(Name):
        # Name = 'IPE160'# input
        Namematerial = ''
        [Namematerial, ret] = SapModel.PropFrame.GetMaterial(Name , Namematerial)
        Fy = 0
        Fu = 0
        EFy = 0
        EFu = 0
        SSType = 0
        SSHysType = 0
        StrainAtHardening = 0
        StrainAtMaxStress = 0
        StrainAtRupture = 0
        FinalSlope = 0
        [Fy, Fu, EFy, EFu, SSType, SSHysType,
        StrainAtHardening, StrainAtMaxStress, StrainAtRupture,
        FinalSlope,
        ret] = SapModel.PropMaterial.GetOSteel_1(Namematerial, Fy, Fu, EFy, EFu, SSType, SSHysType,
        StrainAtHardening, StrainAtMaxStress, StrainAtRupture,
        FinalSlope)
        Ry = EFy/Fy
        return {'material': Namematerial, 'Fy': Fy, 'Fu': Fu, 'Ry': Ry}


    NumberNames = 0
    MyName = []
    PropType = []
    t3 = []
    t2 = []
    tf = []
    tw = []
    t2b = []
    tfb = []
    [NumberNames, MyName, PropType,
    t3, t2, tf, tw, t2b, tfb,
    ret] = SapModel.PropFrame.GetAllFrameProperties(NumberNames, MyName, PropType,
                                                   t3, t2, tf, tw, t2b, tfb)

    # اضافه کردن مشخصات مقاطع به دیکشنری beamlist
    for i in beamlist:
        item_index = MyName.index(i['name'])
        sectionprop = property_of_section(i['name'])
        material = mateial_of_section_prop(i['name'])
        i['protype'] = listofframeprop[PropType[item_index]]
        i['protype_code'] = PropType[item_index]
        i['t3'] = round(t3[item_index], 2)
        i['t2'] = round(t2[item_index], 2)
        i['tf'] = round(tf[item_index], 2)
        i['tw'] = round(tw[item_index], 2)
        i['t2b'] = round(t2b[item_index], 2)
        i['tfb'] = round(tfb[item_index], 2)
        i.update(sectionprop)
        i.update(material)

    return beamlist


if __name__ == '__main__':
    
    wfpetabsreport = MomentBeam()








