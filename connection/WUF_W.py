class WUF_W:
    """
        Fy = 2400 kg/cm2 ST-37 int
        Fu = 3700 kg/cm2 ST-37 int
        Ry = 1.15 or 1.2 or 1.25 float
        tplate = [0.8, 1, 1.2, 1.5, 2, 2.5, 3, 3.5, 4] list
        unit = cm,kg
        beam = {'name': 'PG', 'Z': 858.75 cm, 'd': 39.5 cm, 'bf': 15 cm, 'tf': 1 cm, 'tw': 0.8 cm,
        'L': 300 cm, 'W': 21.465 kg/cm}
        bcol = 0 -> NC ( not calculate )
        phikh = درصد خطای قابل قبول 0.95 کلیه اعداد آیتم های مقاوم در 1.05 ضرب میشود ( Ap ,

        B = 0.75 # 1 or 0.85 or 0.75 zarib etminan moghavemat joosh
        Fue = 4200 # E60 s156 aeenname mahdoodiat estefade
        hangel = degree of horenzital angel in xy plan
        frametype = 0 # قاب خمشی معمولی صفر ویژه یک

        """

    def __init__(self, beam, Fy, Fu, Ry, tplate, phikh , hangel, frametype):

        self.frametype = frametype
        self.report = {}
        self.solu = ''
        self.error = []
        self.phikh = phikh
        self.hangel = hangel
        self.delta_x = 0
        self.beam = beam
        self.tplate = tplate
        self.tplate.sort()
        self.Ry = Ry
        self.Fu = Fu
        self.Fy = Fy
        self.sh = 0

        # Cpr
        self.Cpr = 1.4 # برای این نوع اتصال

        # MP
        self.Mp = self.beam['Z'] * self.Fy

        # Mpr
        self.Mpr = self.Cpr * self.Ry * self.Mp

        self.Lh = self.beam['L'] - 2 * self.sh

        # Vpr
        self.Vpr = 2 * self.Mpr / self.Lh + self.beam['W'] * self.Lh / 2

        # Vu
        self.Vu = self.Vpr

        # Mu
        self.Mu = self.Mpr

        # v plate

        self.l1 = max(4, 1.5 * self.beam['tw']) # طول سوراخ دست رسی
        self.h1 = min(max(2, self.beam['tw']), 5) # ارتفاع سوراخ دست رسی
        self._a = 1 # طول همپوشانی ورق برشی جان با سوراخ دست رسی که بین 6 تا 12 میلی متر باشد

        self.hp = self.beam['d'] - 2 * self.beam['tw'] - 2 * self.h1 + 2 * self._a # ارتفاع ورق برشی جان
        self.bp = self.l1 + 6 # پهنای ورق جان
        from math import tan , radians
        self.x = round(self.bp - 2.5 , 1)
        cangel = radians(30) # deg
        self.y = round(self.x * tan(cangel) , 1)

        self.tp_req = self.Vu / (self.hp * 0.6 * self.Ry * self.Fy) # ضخامت ورق برشی جان
        self.tp_req = max(self.tp_req , self.beam['tw'])

        for i in self.tplate:
            self.tp = i
            if i*phikh >= self.tp_req :
                break

        self.tp_ratio = self.tp_req/self.tp
        if self.tp_ratio > self.phikh:
            self.error.append(f'shear plate tp(need) = {self.tp_req}  and tp(max exist) = {self.tp}  , ratio = {self.tp_ratio} ')

        self.aw_vplate = min(self.tp-0.2, self.beam['tw']) # بعد جوش گوشه ورق برشی جان به جان تیر
        WUF_W.Design(self)


    def beam_control(self):
        if self.beam['d'] > 100:
            self.error.append(f'd of beam = {self.beam["d"]} cm must <= 100 cm')

        if self.beam['tf'] > 3:
            self.error.append(f'tf of beam = {self.beam["tf"]} cm must <= 3 cm')

        if self.frametype:
            if self.beam['L']/self.beam['d'] < 7:
                self.error.append(f'L / d of beam = {self.beam["L"]/self.beam["d"]}  must >= 7 cm')
        else:
            if self.beam['L']/self.beam['d'] < 5:
                self.error.append(f'L / d of beam = {self.beam["L"]/self.beam["d"]}  must >= 5 cm')

        Abeam = (2*(self.beam['bf']*self.beam['tf']) + ((self.beam['d']-2*self.beam['tf'])*self.beam['tw']))/10000
        Wbeamunit = 7850*Abeam
        if Wbeamunit>250:
            self.error.append(f'weight of beam = {Wbeamunit} kg/m must <= 250 kg/m')





    def joint_plate(self):
        self.join_pl = self.beam['tf']
        for i in self.tplate:
            if self.join_pl > i:
                continue
            else:
                self.join_pl = i
                break


    def beam_with_hangel(self):
        if self.hangel:
            from math import radians, tan
            angel = radians(self.hangel)
            self.delta_x = round(tan(angel)*self.beam['bf'], 1)


    def WUF_report(self):
        self.report = {'name': self.beam['name'], 'h_angel': self.hangel, 'delta_x': self.delta_x, 'wuf_vplate_hp': round(self.hp,1), 'wuf_vplate_bp': self.bp, 'wuf_vplate_tp': self.tp, 'wuf_vplate_aw': round(self.aw_vplate,1), 'self.wuf_tp_ratio': self.tp_ratio,
                       'l1': self.l1, 'h1': self.h1, 'x': self.x, 'y': self.y, 'joint_pl': self.join_pl}
        self.solu = f'''******
{self.beam['name']}
******

unit = Kg.f , Cm

h_angel = {self.hangel} deg
delta_x = {self.delta_x} cm


Cpr = {self.Cpr} , Z = {self.beam['Z']} , Ry = {self.Ry} , Fy = {self.Fy} , Fu = {self.Fu}

Mp = Z * Fy = {round(self.Mp,2)}
Mpr = Cpr * Ry * Mp = {round(self.Mpr,2)}

L = {self.beam['L']} , sh = {self.sh} , W = {self.beam['W']}

Lh = L - 2 * sh = {self.Lh}
Vpr = 2 * Mpr / Lh + W * Lh / 2 = {round(self.Vpr,2)}

Mu = Mpr = {round(self.Mpr,2)}
Vu = Vpr = {round(self.Vpr,2)}

shear plate :

hp = {self.hp}
tp_req = Vu / (hp * 0.6 * Ry * Fy) = {self.tp_req} need
tp = { self.tp} exist
ratio = tp_req / tp = {round(self.tp_ratio,2)}

'''


    def Design(self):
        WUF_W.beam_control(self)
        WUF_W.joint_plate(self)
        WUF_W.beam_with_hangel(self)
        WUF_W.WUF_report(self)



class E8S_SPLICE(WUF_W):
    '''
    navard = 0 , 1 -> 0 tir vargh , 1 navard shode
    E = modoul elastic foolad az roye masaleh
    v_condition = 0 , 1 پیچ معمولی همه حالات و پیچ پرمقاومت که سطح برش از قسمت دندانه شده بگذره صفر و پیچ پرمقاومت که سطح برش از قسمت دنده شده نمی گذرد یک
    sh_splice = محل درنظر گرفته شده وصله از بر ستون defult = 80 cm
    '''

    def __init__(self, beam, Fy, Fu, Ry, tplate, phikh, hangel, frametype, E, navard, bolt_Fu , list_boltsize, v_condition, sh_splice):
        super().__init__(beam, Fy, Fu, Ry, tplate, phikh, hangel, frametype)
        self.v_condition = v_condition
        self.list_boltsize = list_boltsize
        self.list_boltsize.sort()
        self.E = E
        self.navard = navard
        self.bolt_Fu = bolt_Fu
        self.sh_splice = sh_splice #cm
        E8S_SPLICE.design(self)


    # def beam_control(self):
    #     # for E8S
    #     tbf = (1.5,3)
    #     bbf = (20,35)
    #     d = (44,100)
    #
    #     if not(tbf[0] <= self.beam['tf'] <= tbf[1]):
    #         self.error.append(f"tf={self.beam['tf']} of beam not ok ({min(tbf)}<=tf<={max(tbf)}) cm")
    #     if not(bbf[0] <= self.beam['bf'] <= bbf[1]):
    #         self.error.append(f"bf={self.beam['bf']} of beam not ok ({min(bbf)}<=bf<={max(bbf)}) cm")
    #     if not(d[0] <= self.beam['d'] <= d[1]):
    #         self.error.append(f"d={self.beam['d']} of beam not ok ({min(d)}<=d<={max(d)}) cm")




    def Mpf(self):
        # Mp = Z * Fy
        self.Mp = 0.9 * self.Mp


        #  Vu=Vs برای وصله=================================
    def Vsf(self):
        self.v1 = self.Vu # جهت اطمینان برش در بر تکیه گاه لحاظ شد بجای برش در محل وصله
        self.Aw = self.beam['d'] * self.beam['tw']

            # Cv
        self.h = self.beam['d']-2*self.beam['tf']
        self.htw = self.h/self.beam['tw']
        from math import sqrt

                # Kv طراحی برشی به گونه ای هست که نیاز به سخت کننده نیست
        self.Kv = 5

        self.phi_v = 0.9

        if self.htw <= 2.24 * sqrt(self.E/self.Fy) and self.navard:
            self.Cv = 1
            self.phi_v = 1
        else:
            if self.htw <= 1.1*sqrt(self.Kv*self.E/self.Fy):
                self.Cv = 1
            elif 1.1*sqrt(self.Kv*self.E/self.Fy) < self.htw <= 1.37*sqrt(self.Kv*self.E/self.Fy):
                self.Cv = 1.1*sqrt((self.Kv*self.E/self.Fy))/self.htw
            elif self.htw > 1.37*sqrt(self.Kv*self.E/self.Fy):
                self.Cv = 1.51*self.Kv*self.E/((self.htw**2)*self.Fy)
            else:
                self.Cv = 1
        self.v2 = self.phi_v* 0.6 * self.Fy * self.Aw * self.Cv
        self.Vs = min(self.v1, self.v2)


    def flang_bolt_design(self):
        from math import sqrt, pi
        # for E8S
        bp = (24,40)
        g = (15,20)
        pfo = (4,5)
        pfi = (4,5)
        pb = (9,10)

        # bp
        self.flang_bp = self.beam['bf']
        if self.flang_bp < min(bp):
            self.flang_bp = min(bp)
        elif self.flang_bp > max(bp):
            self.flang_bp = max(bp)
            # self.error.append(f"b={self.flang_bp} of flange is smaller than bf={self.beam['bf']} of beam please reduce bf")


        self.flang_g = min(g)
        self.flang_pfo = min(pfo)
        self.flang_pfi = min(pfi)
        self.flang_pb = min(pb)

        # for E8S
        self.flang_h1 = self.beam['d']+self.flang_pfo+self.flang_pb-self.beam['tf']/2
        self.flang_h2 = self.flang_h1-self.flang_pb
        self.flang_h3 = self.flang_h2 - self.beam['tf'] - self.flang_pfi - self.flang_pfo
        self.flang_h4 = self.flang_h3 - self.flang_pb

        self.phi_n = 0.9
        self.Fnt = 0.75 * self.bolt_Fu

        # for E8S
        # bolt size
        self.bolt_db_req = sqrt(2 * self.Mp/(pi * self.phi_n * self.Fnt * (self.flang_h1 + self.flang_h2+self.flang_h3 + self.flang_h4)))
        
        for i in self.list_boltsize:
            self.bolt_db = i
            if self.phikh*i >= self.bolt_db_req:
                break
      

    def flang_bolt_design2(self):
        from math import sqrt, pi

        self.bolt_db_ratio = self.bolt_db_req/self.bolt_db
        # if self.bolt_db_ratio > self.phikh:
        #     self.error.append(f'db(need) = {self.bolt_db_req} and db(max exist) = {self.bolt_db} , ratio = {self.bolt_db_ratio}')

        self.edge_dis = (self.flang_bp - self.flang_g) / 2
        if self.edge_dis < 2 * self.bolt_db:
            from math import ceil
            self.flang_bp += ceil((2 * (2 * self.bolt_db - self.edge_dis)))


        # for E8S
        self.phi_d = 1

            # Yp
        self.s = 0.5*sqrt(self.flang_bp*self.flang_g)
        if self.s < self.flang_pfi:
            self.flang_pfi = self.s
            # طوری de انتخاب شد که برای فرمول Yp که شکل کیس اول اجرا شود
        self.flang_de = 2 * self.bolt_db # فاصله بالاترین سوراخ تا لبه بالای ورق
        if self.flang_de > self.s:
            self.flang_de = self.s

        self.Yp = 0.5*self.flang_bp*(self.flang_h1*(1/(2*self.flang_de))+self.flang_h2*(1/self.flang_pfo)+self.flang_h3*(1/self.flang_pfi)+self.flang_h4*(1/self.s))+ \
            (2/self.flang_g)*(self.flang_h1*(self.flang_de+3*self.flang_pb/4)+self.flang_h2*(self.flang_pfo+self.flang_pb/4)+self.flang_h3*(self.flang_pfi+3*self.flang_pb/4)+self.flang_h4*(self.s+self.flang_pb/4))+ \
            self.flang_g

        # tp flang
        tp = (2, 7)
        self.flang_tp_req = sqrt(1.11 * self.Mp/(self.phi_d*self.Fy*self.Yp))
               
        if self.flang_tp_req < min(tp):
            self.flang_tp_req = min(tp)
        # elif self.flang_tp_req > max(tp):
        #     self.error.append(f"tp_flange = {self.flang_tp_req} cm is need, it must between ({min(tp)}, {max(tp)}) cm")

        for i in self.tplate:
            self.flang_tp = i
            if self.phikh*i >= self.flang_tp_req:
                break
        
        self.flang_tp_ratio = self.flang_tp_req/self.flang_tp

        # if self.flang_tp_ratio > self.phikh:
        #     self.error.append(f'flang tp(need) = {self.flang_tp_req} and flang tp(max exist) = {self.flang_tp} , ratio = {self.flang_tp_ratio}')


        # Ffu  برای بدون سخت کننده کار برد دارد فرمول
        self.Ffu = self.Mp/(self.beam['d']-self.beam['tf'])

        # ابعاد سخت کننده در اتصال E8S , E4S
        self.stif_hst = self.flang_de+self.flang_pb+self.flang_pfo
        self.stif_Lst = 1.75*self.stif_hst
        self.stif_ts_req = self.beam['tw']

        if self.stif_ts_req < self.stif_hst/(0.56*sqrt(self.E/self.Fy)):
            self.stif_ts_req = self.stif_hst/(0.56*sqrt(self.E/self.Fy))

        
        for i in self.tplate:
            self.stif_ts = i
            if self.phikh*i >= self.stif_ts_req:
                break
            
        self.stif_ts_ratio = self.stif_ts_req/self.stif_ts
        # if self.stif_ts_ratio > self.phikh:
        #     self.error.append(f'stiff ts(need) = {self.stif_ts_req} and stiff ts(max exist) = {self.stif_ts} , ratio = {self.stif_ts_ratio}')

        # کنترل برش وارد بر پیچ ها در هر وجه بالا و پایین اتصال

        self.nb = 8 # تعداد پیچ های هر سمت اتصال

        # برش از قسمت رزوه شده بگذرد یا خیر
        if self.v_condition:
            self.Fnv = 0.55*self.bolt_Fu
        else:
            self.Fnv = 0.45 * self.bolt_Fu

        self.bolt_Ab = pi * self.bolt_db**2/4

        self.Vall = self.phi_n * self.nb * self.Fnv * self.bolt_Ab
        self.VsVall_ratio = self.Vs/self.Vall


    def flang_bolt_design2_control(self):

        if self.Vs > self.Vall*self.phikh:
            for i in self.list_boltsize:
                if i <= self.bolt_db:
                    continue
                else:
                    self.bolt_db = i
                    E8S_SPLICE.flang_bolt_design2(self)
                    if self.Vs <= self.Vall:
                        break

        self.VsVall_ratio = self.Vs/self.Vall


    def flang_bolt_design3(self):
        # نوع سوراخ استاندارد
        if self.bolt_db in (1.6,2,2.2):
            self.hole_size_incrase = 0.2
        elif self.bolt_db in (2.4,2.7,3):
            self.hole_size_incrase = 0.3
        elif self.bolt_db >= 3.6:
            self.hole_size_incrase = 0.3
        else:
            self.hole_size_incrase = 0.2


        self.ni = 4
        self.no = 4
        self.Lci1 = self.flang_pb-(self.bolt_db + self.hole_size_incrase)
        self.Lci2 = self.flang_pfo+self.beam['tf']+self.flang_pfi-(self.bolt_db+self.hole_size_incrase)
        self.Lci = min(self.Lci1, self.Lci2)
        self.rni1 = 1.2*self.Lci*self.flang_tp*self.Fu
        self.rni2 = 2.4*self.bolt_db*self.flang_tp*self.Fu
        self.rni = min(self.rni1, self.rni2)
        self.Lco = self.flang_de-(self.bolt_db+self.hole_size_incrase)/2
        self.rno1 = 1.2*self.Lco*self.flang_tp*self.Fu
        self.rno2 = 2.4*self.bolt_db*self.flang_tp*self.Fu
        self.rno = min(self.rno1, self.rno2)
        self.Rn = self.phi_n * (self.ni * self.rni + self.no * self.rno)
        self.VsRn_ratio = self.Vs / self.Rn


    def flang_bolt_design3_control(self):
        if self.Vs > self.Rn*self.phikh:
            for i in self.list_boltsize:
                if i <= self.bolt_db:
                    continue
                else:
                    self.bolt_db = i
                    E8S_SPLICE.flang_bolt_design2(self)
                    E8S_SPLICE.flang_bolt_design3(self)
                    if self.Vs <= self.Rn:
                        break
        self.VsVall_ratio = self.Vs / self.Vall
        # if self.VsVall_ratio > self.phikh:
        #     self.error.append(f'max bolt size = {self.bolt_db} , Vu = {self.Vs} , Vall = {self.Vall} , ratio = {self.VsVall_ratio}')

        self.VsRn_ratio = self.Vs / self.Rn
        # if self.VsRn_ratio > self.phikh:
        #     self.error.append(f'max bolt size = {self.bolt_db} , Vu = {self.Vs} , Rn = {self.Rn} , ratio = {self.VsRn_ratio}')

        self.flang_hp = self.beam['d'] + 2 * (self.flang_pfo+self.flang_pb+self.flang_de)


    def sh_splice_control(self):
        if self.sh_splice < self.sh + self.beam['d'] + self.stif_Lst+self.flang_tp:
            self.sh_splice = self.sh + self.beam['d'] + self.stif_Lst + self.flang_tp
            self.sh_splice = (self.sh_splice//5*5)+5


    def error_report(self):
        tbf = (1.5,3)
        bbf = (20,35)
        d = (44,100)
        if not (tbf[0] <= self.beam['tf'] <= tbf[1]):
            self.error.append(f"tf={self.beam['tf']} of beam not ok ({min(tbf)}<=tf<={max(tbf)}) cm")
        if not (bbf[0] <= self.beam['bf'] <= bbf[1]):
            self.error.append(f"bf={self.beam['bf']} of beam not ok ({min(bbf)}<=bf<={max(bbf)}) cm")
        if not (d[0] <= self.beam['d'] <= d[1]):
            self.error.append(f"d={self.beam['d']} of beam not ok ({min(d)}<=d<={max(d)}) cm")

        bp = (24, 40)
        if self.flang_bp > max(bp):
            self.error.append(f"b={self.flang_bp} of flange is smaller than bf={self.beam['bf']} of beam please reduce bf")

        if self.bolt_db_ratio > self.phikh:
            self.error.append(f'db(need) = {self.bolt_db_req} and db(max exist) = {self.bolt_db} , ratio = {self.bolt_db_ratio}')

        tp = (2, 7)
        if self.flang_tp_req > max(tp):
            self.error.append(f"tp_flange = {self.flang_tp_req} cm is need, it must between ({min(tp)}, {max(tp)}) cm")

        if self.flang_tp_ratio > self.phikh:
            self.error.append(f'flang tp(need) = {self.flang_tp_req} and flang tp(max exist) = {self.flang_tp} , ratio = {self.flang_tp_ratio}')

        if self.stif_ts_ratio > self.phikh:
            self.error.append(f'stiff ts(need) = {self.stif_ts_req} and stiff ts(max exist) = {self.stif_ts} , ratio = {self.stif_ts_ratio}')

        if self.VsVall_ratio > self.phikh:
            self.error.append(f'max bolt size = {self.bolt_db} , Vu = {self.Vs} , Vall = {self.Vall} , ratio = {self.VsVall_ratio}')

        if self.VsRn_ratio > self.phikh:
            self.error.append(f'max bolt size = {self.bolt_db} , Vu = {self.Vs} , Rn = {self.Rn} , ratio = {self.VsRn_ratio}')



    def E8S_report(self):
        e8s_rep = {'sh_splice': self.sh_splice, 'f_hp': self.flang_hp, 'f_bp': self.flang_bp, 'f_tp': self.flang_tp,
                   'bolt_db': self.bolt_db , 'holesize': self.bolt_db+self.hole_size_incrase,'bolt_n': self.nb*2, 'edge_dis': self.edge_dis, 'f_de': self.flang_de,
                   'f_g': self.flang_g, 'f_pfo': self.flang_pfo, 'f_pfi': self.flang_pfi,
                   'f_pb': self.flang_pb, 'stif_hst': self.stif_hst, 'stif_lst': round(self.stif_Lst,1), 'stif_ts': self.stif_ts}
        self.report.update(e8s_rep)
        self.solu += f'''
*** splice ***

Mu = 0.9 * Mp = {self.Mp}

V1 = Vu = {self.Vu}
phi_v = {self.phi_v} , d = {self.beam['d']} , tw = {self.beam['tw']}
Aw = d * tw = {self.Aw}
Cv = {self.Cv}
v2 = phi_v* 0.6 * Fy * Aw * Cv = {self.v2}

Vu = min(v1, v2) = {self.Vs}

g = {self.flang_g}
pfo = {self.flang_pfo}
pfi = {self.flang_pfi}
pb = {self.flang_pb}
tf = {self.beam['tf']}
h1 = d + pfo + pb - tf/2 = {self.flang_h1}
h2 = h1 - pb = {self.flang_h2}
h3 = h2 - tf - pfi - pfo = {self.flang_h3}
h4 = h3 - pb = {self.flang_h4}

phi_n = {self.phi_n}
Fu(bolt) = {self.bolt_Fu}
Fnt = 0.75 * Fu(bolt) = {self.Fnt}

db_req = sqrt(2 * Mu/(3.14 * phi_n * Fnt * (h1 + h2 + h3 + h4))) = {self.bolt_db_req} need
db = {self.bolt_db} exist
ratio = {self.bolt_db_ratio}

phi_d = {self.phi_d} , Yp (case 1 ) = {self.Yp}

flange_tp_req = sqrt(1.11 * Mu/(phi_d * Fy * Yp)) = {self.flang_tp_req} need
flange_tp = {self.flang_tp} exist
ratio = {self.flang_tp_ratio}


*** stiff ***

E = {self.E}
hst = de + pb+ pfo = {self.stif_hst}
Lst = 1.75 * hst = {self.stif_Lst}
ts_req = max( tw , hst/( 0.56*sqrt ( E / Fy ) ) = {self.stif_ts_req} need
ts = {self.stif_ts} exist
ratio = {self.stif_ts_ratio}

*** shear control1 ***

Vu = {self.Vs} 

phi_n = {self.phi_n} , bolt_Fu = {self.bolt_Fu} , nb = {self.nb} , bolt_Ab = {self.bolt_Ab}

Fnv = (0.55 * bolt_Fu) or (0.45 * bolt_Fu) = {self.Fnv}       
Vall = phi_n * nb * Fnv * bolt_Ab = {self.Vall}
ratio = {self.VsVall_ratio}

*** shear control2 ***

ni = {self.ni}
no = {self.no}
Fu = {self.Fu}
hole_size_incrase = {self.hole_size_incrase}

Lci1 = pb-(db + hole_size_incrase) = {self.Lci1}
Lci2 = pfo+tf+pfi-(db+hole_size_incrase) = {self.Lci2}
Lci = min(Lci1, Lci2) = {self.Lci}
rni1 = 1.2*Lci*flang_tp*Fu = {self.rni1}
rni2 = 2.4*db*flang_tp*Fu = {self.rni2}
rni = min(rni1, rni2) = {self.rni}
Lco = de-(db+hole_size_incrase)/2 = {self.Lco}
rno1 = 1.2*Lco*flang_tp*Fu = {self.rno1}
rno2 = 2.4*db*flang_tp*Fu = {self.rno2}
rno = min(rno1, rno2) = {self.rno}
Rn = phi_n * (ni * rni + no * rno) = {self.Rn}
ratio = {self.VsRn_ratio}




'''





    def design(self):
        # E8S_SPLICE.beam_control(self)
        E8S_SPLICE.Mpf(self)
        E8S_SPLICE.Vsf(self)
        E8S_SPLICE.flang_bolt_design(self)
        E8S_SPLICE.flang_bolt_design2(self)
        E8S_SPLICE.flang_bolt_design2_control(self)
        E8S_SPLICE.flang_bolt_design3(self)
        E8S_SPLICE.flang_bolt_design3_control(self)
        E8S_SPLICE.sh_splice_control(self)
        E8S_SPLICE.error_report(self)
        E8S_SPLICE.E8S_report(self)








class E4S_SPLICE(WUF_W):
    '''
    navard = 0 , 1 -> 0 tir vargh , 1 navard shode
    E = modoul elastic foolad az roye masaleh
    v_condition = 0 , 1 پیچ معمولی همه حالات و پیچ پرمقاومت که سطح برش از قسمت دندانه شده بگذره صفر و پیچ پرمقاومت که سطح برش از قسمت دنده شده نمی گذرد یک
    sh_splice = محل درنظر گرفته شده وصله از بر ستون defult = 80 cm
    '''

    def __init__(self, beam, Fy, Fu, Ry, tplate, phikh, hangel, frametype, E, navard, bolt_Fu, list_boltsize, v_condition,
                 sh_splice):
        super().__init__(beam, Fy, Fu, Ry, tplate, phikh, hangel, frametype)
        self.v_condition = v_condition
        self.list_boltsize = list_boltsize
        self.list_boltsize.sort()
        self.E = E
        self.navard = navard
        self.bolt_Fu = bolt_Fu
        self.sh_splice = sh_splice  # cm
        E4S_SPLICE.design(self)

    # def beam_control(self):
    #     # for E4S
    #     tbf = (1, 2.5)
    #     bbf = (15, 25)
    #     d = (34, 70)
    #
    #     if not (tbf[0] <= self.beam['tf'] <= tbf[1]):
    #         self.error.append(f"tf={self.beam['tf']} of beam not ok ({min(tbf)}<=tf<={max(tbf)}) cm")
    #     if not (bbf[0] <= self.beam['bf'] <= bbf[1]):
    #         self.error.append(f"bf={self.beam['bf']} of beam not ok ({min(bbf)}<=bf<={max(bbf)}) cm")
    #     if not (d[0] <= self.beam['d'] <= d[1]):
    #         self.error.append(f"d={self.beam['d']} of beam not ok ({min(d)}<=d<={max(d)}) cm")

    def Mpf(self):
        # Mp = Z * Fy
        self.Mp = 0.9 * self.Mp

        #  Vu=Vs برای وصله=================================

    def Vsf(self):
        self.v1 = self.Vu  # جهت اطمینان برش در بر تکیه گاه لحاظ شد بجای برش در محل وصله
        self.Aw = self.beam['d'] * self.beam['tw']

        # Cv
        self.h = self.beam['d'] - 2 * self.beam['tf']
        self.htw = self.h / self.beam['tw']
        from math import sqrt

        # Kv طراحی برشی به گونه ای هست که نیاز به سخت کننده نیست
        self.Kv = 5

        self.phi_v = 0.9

        if self.htw <= 2.24 * sqrt(self.E / self.Fy) and self.navard:
            self.Cv = 1
            self.phi_v = 1
        else:
            if self.htw <= 1.1 * sqrt(self.Kv * self.E / self.Fy):
                self.Cv = 1
            elif 1.1 * sqrt(self.Kv * self.E / self.Fy) < self.htw <= 1.37 * sqrt(self.Kv * self.E / self.Fy):
                self.Cv = 1.1 * sqrt((self.Kv * self.E / self.Fy)) / self.htw
            elif self.htw > 1.37 * sqrt(self.Kv * self.E / self.Fy):
                self.Cv = 1.51 * self.Kv * self.E / ((self.htw ** 2) * self.Fy)
            else:
                self.Cv = 1
        self.v2 = self.phi_v * 0.6 * self.Fy * self.Aw * self.Cv
        self.Vs = min(self.v1, self.v2)

    def flang_bolt_design(self):
        from math import sqrt, pi
        # for E4S
        bp = (18, 30)
        g = (10, 16)
        pfo = (5, 15)
        pfi = (5, 15)


        # bp
        self.flang_bp = self.beam['bf']
        if self.flang_bp < min(bp):
            self.flang_bp = min(bp)
        elif self.flang_bp > max(bp):
            self.flang_bp = max(bp)
            # self.error.append(
            #     f"b={self.flang_bp} of flange is smaller than bf={self.beam['bf']} of beam please reduce bf")

        self.flang_g = min(g)
        self.flang_pfo = min(pfo)
        self.flang_pfi = min(pfi)


        # for E4S
        self.flang_h0 = self.beam['d']+self.flang_pfo-(self.beam['tf']/2)
        self.flang_h1 = self.flang_h0-self.flang_pfo-self.flang_pfi-self.beam['tf']


        self.phi_n = 0.9
        self.Fnt = 0.75 * self.bolt_Fu

        # for E4S
        # bolt size
        self.bolt_db_req = sqrt(2 * self.Mp / (pi * self.phi_n * self.Fnt * (self.flang_h1 + self.flang_h0)))
        
        for i in self.list_boltsize:
            self.bolt_db = i
            if self.phikh*i >= self.bolt_db_req:
                break
      

    def flang_bolt_design2(self):
        from math import sqrt, pi

        self.bolt_db_ratio = self.bolt_db_req / self.bolt_db
        # if self.bolt_db_ratio > self.phikh:
        #     self.error.append(f'db(need) = {self.bolt_db_req} and db(max exist) = {self.bolt_db} , ratio = {self.bolt_db_ratio}')


        self.edge_dis = (self.flang_bp - self.flang_g) / 2
        if self.edge_dis < 2 * self.bolt_db:
            from math import ceil
            self.flang_bp += ceil((2 * (2 * self.bolt_db - self.edge_dis)))

        # for E4S
        self.phi_d = 1

        # Yp
        self.s = 0.5 * sqrt(self.flang_bp * self.flang_g)
        if self.s < self.flang_pfi:
            self.flang_pfi = self.s
            # طوری de انتخاب شد که برای فرمول Yp که شکل کیس اول اجرا شود
        self.flang_de = 2 * self.bolt_db  # فاصله بالاترین سوراخ تا لبه بالای ورق
        if self.flang_de > self.s:
            self.flang_de = self.s

        self.Yp = 0.5 * self.flang_bp * (self.flang_h1*(1/self.flang_pfi+1/self.s)+self.flang_h0*(1/self.flang_pfo+1/(2*self.s))) + \
                  (2/self.flang_g)*(self.flang_h1*(self.flang_pfi+self.s)+self.flang_h0*(self.flang_de+self.flang_pfo))

        # tp flang
        tp = (1.2, 5)
        self.flang_tp_req = sqrt(1.11 * self.Mp / (self.phi_d * self.Fy * self.Yp))
        
        if self.flang_tp_req < min(tp):
            self.flang_tp_req = min(tp)
        # elif self.flang_tp_req > max(tp):
        #     self.error.append(f"tp_flange = {self.flang_tp_req} cm is need, it must between ({min(tp)}, {max(tp)}) cm")

        for i in self.tplate:
            self.flang_tp = i
            if self.phikh*i >= self.flang_tp_req:
                break

        self.flang_tp_ratio = self.flang_tp_req / self.flang_tp

        # if self.flang_tp_ratio > self.phikh:
        #     self.error.append(f'flang tp(need) = {self.flang_tp_req} and flang tp(max exist) = {self.flang_tp} , ratio = {self.flang_tp_ratio}')


        # Ffu  فرمول
        self.Ffu = self.Mp / (self.beam['d'] - self.beam['tf'])

        # ابعاد سخت کننده در اتصال E8S , E4S
        self.stif_hst = self.flang_de + self.flang_pfo
        self.stif_Lst = 1.75 * self.stif_hst
        self.stif_ts_req = self.beam['tw']

        if self.stif_ts_req < self.stif_hst / (0.56 * sqrt(self.E / self.Fy)):
            self.stif_ts_req = self.stif_hst / (0.56 * sqrt(self.E / self.Fy))

        for i in self.tplate:
            self.stif_ts = i
            if self.phikh*i >= self.stif_ts_req:
                break
            
        self.stif_ts_ratio = self.stif_ts_req/self.stif_ts
        # if self.stif_ts_ratio > self.phikh:
        #     self.error.append(f'stiff ts(need) = {self.stif_ts_req} and stiff ts(max exist) = {self.stif_ts} , ratio = {self.stif_ts_ratio}')

        # کنترل برش وارد بر پیچ ها در هر وجه بالا و پایین اتصال

        self.nb = 4  # تعداد پیچ های هر سمت اتصال

        # برش از قسمت رزوه شده بگذرد یا خیر
        if self.v_condition:
            self.Fnv = 0.55 * self.bolt_Fu
        else:
            self.Fnv = 0.45 * self.bolt_Fu

        self.bolt_Ab = pi * self.bolt_db ** 2 / 4

        self.Vall = self.phi_n * self.nb * self.Fnv * self.bolt_Ab
        self.VsVall_ratio = self.Vs/self.Vall


    def flang_bolt_design2_control(self):

        if self.Vs > self.Vall * self.phikh:
            for i in self.list_boltsize:
                if i <= self.bolt_db:
                    continue
                else:
                    self.bolt_db = i
                    E4S_SPLICE.flang_bolt_design2(self)
                    if self.Vs <= self.Vall:
                        break

        self.VsVall_ratio = self.Vs / self.Vall

    def flang_bolt_design3(self):
        # نوع سوراخ استاندارد
        if self.bolt_db in (1.6, 2, 2.2):
            self.hole_size_incrase = 0.2
        elif self.bolt_db in (2.4, 2.7, 3):
            self.hole_size_incrase = 0.3
        elif self.bolt_db >= 3.6:
            self.hole_size_incrase = 0.3
        else:
            self.hole_size_incrase = 0.2

        self.ni = 2
        self.no = 2

        self.Lci = self.flang_pfi+self.beam['tf']+self.flang_pfo - (self.bolt_db+self.hole_size_incrase)
        self.rni1 = 1.2 * self.Lci * self.flang_tp * self.Fu
        self.rni2 = 2.4 * self.bolt_db * self.flang_tp * self.Fu
        self.rni = min(self.rni1, self.rni2)
        self.Lco = self.flang_de - (self.bolt_db + self.hole_size_incrase) / 2
        self.rno1 = 1.2 * self.Lco * self.flang_tp * self.Fu
        self.rno2 = 2.4 * self.bolt_db * self.flang_tp * self.Fu
        self.rno = min(self.rno1, self.rno2)
        self.Rn = self.phi_n * (self.ni * self.rni + self.no * self.rno)
        self.VsRn_ratio = self.Vs / self.Rn

    def flang_bolt_design3_control(self):
        if self.Vs > self.Rn * self.phikh:
            for i in self.list_boltsize:
                if i <= self.bolt_db:
                    continue
                else:
                    self.bolt_db = i
                    E4S_SPLICE.flang_bolt_design2(self)
                    E4S_SPLICE.flang_bolt_design3(self)
                    if self.Vs <= self.Rn:
                        break
        
        self.VsVall_ratio = self.Vs / self.Vall
        # if self.VsVall_ratio > self.phikh:
        #     self.error.append(f'max bolt size = {self.bolt_db} , Vu = {self.Vs} , Vall = {self.Vall} , ratio = {self.VsVall_ratio}')

        self.VsRn_ratio = self.Vs / self.Rn
        # if self.VsRn_ratio > self.phikh:
        #     self.error.append(f'max bolt size = {self.bolt_db} , Vu = {self.Vs} , Rn = {self.Rn} , ratio = {self.VsRn_ratio}')

        self.flang_hp = self.beam['d'] + 2 * (self.flang_pfo + self.flang_de)

    def sh_splice_control(self):
        if self.sh_splice < self.sh + self.beam['d'] + self.stif_Lst + self.flang_tp:
            self.sh_splice = self.sh + self.beam['d'] + self.stif_Lst + self.flang_tp
            self.sh_splice = (self.sh_splice // 5 * 5) + 5

    def error_report(self):
        tbf = (1, 2.5)
        bbf = (15, 25)
        d = (34, 70)
        if not (tbf[0] <= self.beam['tf'] <= tbf[1]):
            self.error.append(f"tf={self.beam['tf']} of beam not ok ({min(tbf)}<=tf<={max(tbf)}) cm")
        if not (bbf[0] <= self.beam['bf'] <= bbf[1]):
            self.error.append(f"bf={self.beam['bf']} of beam not ok ({min(bbf)}<=bf<={max(bbf)}) cm")
        if not (d[0] <= self.beam['d'] <= d[1]):
            self.error.append(f"d={self.beam['d']} of beam not ok ({min(d)}<=d<={max(d)}) cm")

        bp = (18, 30)
        if self.flang_bp > max(bp):
            self.error.append(f"b={self.flang_bp} of flange is smaller than bf={self.beam['bf']} of beam please reduce bf")

        if self.bolt_db_ratio > self.phikh:
            self.error.append(f'db(need) = {self.bolt_db_req} and db(max exist) = {self.bolt_db} , ratio = {self.bolt_db_ratio}')

        tp = (1.2, 5)
        if self.flang_tp_req > max(tp):
            self.error.append(f"tp_flange = {self.flang_tp_req} cm is need, it must between ({min(tp)}, {max(tp)}) cm")

        if self.flang_tp_ratio > self.phikh:
            self.error.append(f'flang tp(need) = {self.flang_tp_req} and flang tp(max exist) = {self.flang_tp} , ratio = {self.flang_tp_ratio}')

        if self.stif_ts_ratio > self.phikh:
            self.error.append(f'stiff ts(need) = {self.stif_ts_req} and stiff ts(max exist) = {self.stif_ts} , ratio = {self.stif_ts_ratio}')

        if self.VsVall_ratio > self.phikh:
            self.error.append(f'max bolt size = {self.bolt_db} , Vu = {self.Vs} , Vall = {self.Vall} , ratio = {self.VsVall_ratio}')

        if self.VsRn_ratio > self.phikh:
            self.error.append(f'max bolt size = {self.bolt_db} , Vu = {self.Vs} , Rn = {self.Rn} , ratio = {self.VsRn_ratio}')




    def E4S_report(self):
        e4s_rep = {'sh_splice': self.sh_splice, 'f_hp': self.flang_hp, 'f_bp': self.flang_bp, 'f_tp': self.flang_tp,
                   'bolt_db': self.bolt_db , 'holesize': self.bolt_db+self.hole_size_incrase, 'bolt_n': self.nb*2, 'edge_dis': self.edge_dis, 'f_de': self.flang_de,
                   'f_g': self.flang_g, 'f_pfo': self.flang_pfo, 'f_pfi': self.flang_pfi,
                   'stif_hst': self.stif_hst, 'stif_lst':round(self.stif_Lst,1), 'stif_ts': self.stif_ts}
        self.report.update(e4s_rep)

        self.solu += f'''
*** splice ***

Mu = 0.9 * Mp = {self.Mp}

V1 = Vu = {self.Vu}
phi_v = {self.phi_v} , d = {self.beam['d']} , tw = {self.beam['tw']}
Aw = d * tw = {self.Aw}
Cv = {self.Cv}
v2 = phi_v* 0.6 * Fy * Aw * Cv = {self.v2}

Vu = min(v1, v2) = {self.Vs}

g = {self.flang_g}
pfo = {self.flang_pfo}
pfi = {self.flang_pfi}
tf = {self.beam['tf']}
h0 = d + pfo - (tf/2) = {self.flang_h0}
h1 = h0 - pfo - pfi - tf = {self.flang_h1}

phi_n = {self.phi_n}
Fu(bolt) = {self.bolt_Fu}
Fnt = 0.75 * Fu(bolt) = {self.Fnt}

db_req = sqrt(2 * Mu/(3.14 * phi_n * Fnt * (h0 + h1))) = {self.bolt_db_req} need
db = {self.bolt_db} exist
ratio = {self.bolt_db_ratio}

phi_d = {self.phi_d} , Yp (case 1 ) = {self.Yp}

flange_tp_req = sqrt(1.11 * Mu/(phi_d * Fy * Yp)) = {self.flang_tp_req} need
flange_tp = {self.flang_tp} exist
ratio = {self.flang_tp_ratio}


*** stiff ***

E = {self.E}
hst = de +  pfo = {self.stif_hst}
Lst = 1.75 * hst = {self.stif_Lst}
ts_req = max( tw , hst/( 0.56*sqrt ( E / Fy ) ) = {self.stif_ts_req} need
ts = {self.stif_ts} exist
ratio = {self.stif_ts_ratio}

*** shear control1 ***

Vu = {self.Vs} 

phi_n = {self.phi_n} , bolt_Fu = {self.bolt_Fu} , nb = {self.nb} , bolt_Ab = {self.bolt_Ab}

Fnv = (0.55 * bolt_Fu) or (0.45 * bolt_Fu) = {self.Fnv}       
Vall = phi_n * nb * Fnv * bolt_Ab = {self.Vall}
ratio = {self.VsVall_ratio}

*** shear control2 ***

ni = {self.ni}
no = {self.no}
Fu = {self.Fu}
hole_size_incrase = {self.hole_size_incrase}

Lci = pfo+tf+pfi-(db+hole_size_incrase) = {self.Lci}
rni1 = 1.2*Lci*flang_tp*Fu = {self.rni1}
rni2 = 2.4*db*flang_tp*Fu = {self.rni2}
rni = min(rni1, rni2) = {self.rni}
Lco = de-(db+hole_size_incrase)/2 = {self.Lco}
rno1 = 1.2*Lco*flang_tp*Fu = {self.rno1}
rno2 = 2.4*db*flang_tp*Fu = {self.rno2}
rno = min(rno1, rno2) = {self.rno}
Rn = phi_n * (ni * rni + no * rno) = {self.Rn}
ratio = {self.VsRn_ratio}




'''



    def design(self):
        # E4S_SPLICE.beam_control(self)
        E4S_SPLICE.Mpf(self)
        E4S_SPLICE.Vsf(self)
        E4S_SPLICE.flang_bolt_design(self)
        E4S_SPLICE.flang_bolt_design2(self)
        E4S_SPLICE.flang_bolt_design2_control(self)
        E4S_SPLICE.flang_bolt_design3(self)
        E4S_SPLICE.flang_bolt_design3_control(self)
        E4S_SPLICE.sh_splice_control(self)
        E4S_SPLICE.error_report(self)
        E4S_SPLICE.E4S_report(self)



class TBplate_SPLICE(WUF_W):
    '''
    navard = 0 , 1 -> 0 tir vargh , 1 navard shode
    E = modoul elastic foolad az roye masaleh
    v_condition = 0 , 1 پیچ معمولی همه حالات و پیچ پرمقاومت که سطح برش از قسمت دندانه شده بگذره صفر و پیچ پرمقاومت که سطح برش از قسمت دنده شده نمی گذرد یک
    sh_splice = محل درنظر گرفته شده وصله از بر ستون defult = 80 cm
    max_n_bolt =  تعداد پیچ های مدنظر در هر سمت اتصال ( وصله ) در بال
    '''

    def __init__(self, beam, Fy, Fu, Ry, tplate, phikh, hangel, frametype, E, navard, bolt_Fu, list_boltsize, v_condition,
                 sh_splice, gap, max_n_bolt):
        super().__init__(beam, Fy, Fu, Ry, tplate, phikh, hangel, frametype)
        self.max_n_bolt = max_n_bolt
        self.gap = gap
        self.v_condition = v_condition
        self.list_boltsize = list_boltsize
        self.list_boltsize.sort()
        self.E = E
        self.navard = navard
        self.bolt_Fu = bolt_Fu
        self.sh_splice = sh_splice  # cm
        self.plate_tp = self.tplate[0]
        self.plate_b = self.beam['bf']
        self.f_bolt_db = self.list_boltsize[0]
        self.ns2 = 1
        self.v_bolt_col = 2
        TBplate_SPLICE.TBplate_SPLIC_desgine(self)


    def Mpf(self):
        # Mp = Z * Fy
        self.Mp = 0.9 * self.Mp

        #  Vu=Vs برای وصله=================================

    def Vsf(self):
        self.v1 = self.Vu  # جهت اطمینان برش در بر تکیه گاه لحاظ شد بجای برش در محل وصله
        self.Aw = self.beam['d'] * self.beam['tw']

        # Cv
        self.h = self.beam['d'] - 2 * self.beam['tf']
        self.htw = self.h / self.beam['tw']
        from math import sqrt

        # Kv طراحی برشی به گونه ای هست که نیاز به سخت کننده نیست
        self.Kv = 5

        self.phi_v = 0.9

        if self.htw <= 2.24 * sqrt(self.E / self.Fy) and self.navard:
            self.Cv = 1
            self.phi_v = 1
        else:
            if self.htw <= 1.1 * sqrt(self.Kv * self.E / self.Fy):
                self.Cv = 1
            elif 1.1 * sqrt(self.Kv * self.E / self.Fy) < self.htw <= 1.37 * sqrt(self.Kv * self.E / self.Fy):
                self.Cv = 1.1 * sqrt((self.Kv * self.E / self.Fy)) / self.htw
            elif self.htw > 1.37 * sqrt(self.Kv * self.E / self.Fy):
                self.Cv = 1.51 * self.Kv * self.E / ((self.htw ** 2) * self.Fy)
            else:
                self.Cv = 1
        self.v2 = self.phi_v * 0.6 * self.Fy * self.Aw * self.Cv
        self.Vs = min(self.v1, self.v2)

        #  نیرو وارد بر ورق بالا و پایین

    def _F(self):
        self.F = self.Mp / (self.beam['d'] + self.plate_tp)

    def _Ag_req(self):
        self.ag_req = self.F / (0.9 * self.Fy)
        self.plate_tp_req = max((self.ag_req / self.plate_b), self.beam['tf'])/2
        self.plate_tp_ratio = self.plate_tp_req / self.plate_tp

    def _Ag_control(self):
        if self.plate_tp_ratio > self.phikh:
            for i in self.tplate:
                self.plate_tp = i
                TBplate_SPLICE._F(self)
                TBplate_SPLICE._Ag_req(self)
                if self.plate_tp_ratio <= self.phikh:
                    break

    def f_bolt_size_max(self):
        if self.f_bolt_db in (1.6, 2, 2.2):
            self.hole_size_incrase = 0.2
        elif self.f_bolt_db in (2.4, 2.7, 3):
            self.hole_size_incrase = 0.3
        elif self.f_bolt_db >= 3.6:
            self.hole_size_incrase = 0.3
        else:
            self.hole_size_incrase = 0.2

        self.f_bolt_db_max = 0.5*self.beam['bf']*(1-(1.3*self.Fy)/(1.2*self.Fu))-0.3
        # if self.f_bolt_db > self.f_bolt_db_max:
        #     self.error.append(f'f_bolt_db = {self.f_bolt_db} must <= f_bolt_db_max = {self.f_bolt_db_max} , reduce bolt size or increase bf of beam')
        
        self.Ag = self.beam['tf']*self.beam['bf']
        self.fbeam_Anet = self.beam['tf'] * (self.beam['bf'] - 2 * (self.f_bolt_db + self.hole_size_incrase + 0.2))
        self.ff1 = 0.6*self.Fy/(0.5*self.Fu)
        self.ff2 = self.fbeam_Anet / self.Ag
        # if self.ff1>self.ff2:
        #     self.error.append(f'0.6*self.Fy/(0.5*self.Fu) > Anet/Ag reduce bolt size or increase bf of beam')


    def f_bolt_desgin(self):
        # if self.bolt_Fu < 7250:
        #     self.error.append(f'acceptabel  bolt standard is A490 or A325, fu >=7250 kg/cm2')

        if self.v_condition:
            self.Fnv = 0.55 * self.bolt_Fu
        else:
            self.Fnv = 0.45 * self.bolt_Fu

        if self.bolt_Fu >= 10000:
            self.Tb_list = {1.6:11400, 2:17900, 2.2:22100, 2.4:25700, 2.7:33400, 3:40800, 3.6:59500}
        else:
            self.Tb_list = {1.6:9100, 2:14200, 2.2:17600, 2.4:20500, 2.7:26700, 3:32600, 3.6:47500}

        self.Tb = self.Tb_list[self.f_bolt_db]

        self.f_bolt_Ab = (3.14*self.f_bolt_db**2)/4
        self.meu = 0.3
        self.ns = 2
        self.phi_n = 0.9
        self.Rn1 = 1.13*self.meu*self.Tb*self.ns*self.ns
        self.Rn11 = self.phi_n*self.Fnv*self.f_bolt_Ab*self.ns
        self.Rn2 = 2.4*self.Fu*self.f_bolt_db*self.beam['tf']
        self.Rn3 = 2.4*self.ns*self.Fu*self.f_bolt_db*self.plate_tp
        self.Rn = min(self.Rn11, self.Rn2, self. Rn3)
        from math import ceil
        self.f_bolt_n = ceil(self.F/self.Rn)
        if self.f_bolt_n % 2 != 0:
            self.f_bolt_n += 1

    def f_bolt_control(self):
        if self.f_bolt_n > self.max_n_bolt:
            for j in self.list_boltsize:
                self.f_bolt_db = j
                TBplate_SPLICE.f_bolt_size_max(self)
                TBplate_SPLICE.f_bolt_desgin(self)
                if self.f_bolt_n <= self.max_n_bolt:
                    break

    def _Ag_control2(self):
        self.plate_Anet = self.ns*(self.plate_tp * (self.plate_b - 2 * (self.f_bolt_db + self.hole_size_incrase + 0.2)))-self.beam['tw']*self.plate_tp
        self.plate_Anet_req = (self.F/(0.75*self.Fu))
        if self.plate_Anet*self.phikh < self.plate_Anet_req:
            for i in self.tplate:
                self.plate_tp = i
                TBplate_SPLICE._F(self)
                TBplate_SPLICE._Ag_req(self)
                TBplate_SPLICE.f_bolt_size_max(self)
                TBplate_SPLICE.f_bolt_desgin(self)
                TBplate_SPLICE.f_bolt_control(self)
                self.plate_Anet = self.ns*(self.plate_tp * (self.plate_b - 2 * (self.f_bolt_db + self.hole_size_incrase + 0.2)))-self.beam['tw']*self.plate_tp
                self.plate_Anet_req = (self.F / (0.75 * self.Fu))
                if self.plate_Anet * self.phikh >= self.plate_Anet_req:
                    break
        self.plate_Anet_ratio = self.plate_Anet_req/self.plate_Anet


    def f_plate_designe(self):
        from math import ceil
        self.f_de = ceil(2 * self.f_bolt_db)
        self.f_pb_max = min(14 * min(self.plate_tp, self.beam['tf']), 20)
        self.f_pb = ceil(3 * self.f_bolt_db)
        if self.f_pb > self.f_pb_max:
            self.f_pb = self.f_pb_max
            # self.error.append(f'pb = {self.f_pb} > pb(max) = {self.f_pb_max} reduce bolt size')

        self.edge_dis = (self.beam['bf']-self.beam['tw'])/4
        # if self.edge_dis < 2 * self.f_bolt_db:
        #     self.error.append(f'edge_dis = {self.edge_dis} must >= 2*db ={2 * self.f_bolt_db} reduce bolt size or increase bf of beam')

        self.plate_l = 2*(2*self.f_de+ (self.f_bolt_n/2 -1)*self.f_pb)+self.gap
        self.f_ypb = 2*self.edge_dis + self.beam['tw']
        self.vplate_h = round(self.beam['d'] - 2 * self.beam['tf'] - 2 * self.plate_tp - 6)

    def sh_splice_control(self):
        if self.sh_splice < self.sh + self.beam['d'] + self.plate_l/2:
            self.sh_splice = self.sh + self.beam['d'] + self.plate_l/2
            self.sh_splice = (self.sh_splice // 5 * 5) + 5

    def _Vplate_tp(self):
        self.vplate_tp_req = self.Vs/(0.75*0.6*self.Fy*self.vplate_h*self.ns2)
        for i in self.tplate:
            self.vplate_tp = i
            if i*self.phikh >= self.vplate_tp_req:
                break
        self.vplate_tp_ratio = self.vplate_tp_req/self.vplate_tp
        # if self.vplate_tp_ratio > self.phikh:
        #     self.error.append(f'splice shear plate tp = {self.vplate_tp} must >= tp_req = {self.vplate_tp_req}')

        self.v_bolt_db = self.f_bolt_db

    def _Vbolt(self):
        from math import floor, sqrt, ceil
        self.v_xde = ceil(2 * self.v_bolt_db)
        self.v_yde = ceil(2 * self.v_bolt_db)
        self.v_xpb = ceil(3*self.v_bolt_db)
        self.v_ypb = ceil(3*self.v_bolt_db)
        n = (self.vplate_h - 2 * self.v_yde) / self.v_ypb
        self.v_bolt_row = floor(n) + 1
        if self.v_bolt_row < 2:
            self.v_bolt_row = 2

        self.v_ypb = max(round((self.vplate_h-2*self.v_yde)/(self.v_bolt_row-1)), ceil(3*self.v_bolt_db))
        self.vplate_h = 2*self.v_yde + (self.v_bolt_row-1)*self.v_ypb
        TBplate_SPLICE._Vplate_tp(self)

        # فاصله نیروی برشی تا مرکز پیچ ها
        self.xc = self.v_xde + (self.v_bolt_col - 1) * self.v_xpb / 2

        # لنگر پیچشی
        self.Tu = self.Vs * self.xc
        self.ntotal_vbolt = self.v_bolt_row * self.v_bolt_col
        self.fvy = self.Vs/self.ntotal_vbolt

        # مرکز پیچ ها نسبت به مرکز بیرونی ترین پیچ
        self._x = (self.v_bolt_col - 1) * self.v_xpb / 2
        self._y = (self.v_bolt_row - 1) * self.v_ypb / 2

        # j ممان اینرسی قطبی پیچ ها
        if self.v_bolt_col % 2 == 0:
            self.xi = self.v_xpb/2
            self.sum_xi2 = self.xi**2
            self.nx_block = int(self.v_bolt_col / 2)
            for i in range(self.nx_block - 1):
                self.xi += self.v_xpb
                self.sum_xi2 += self.xi ** 2
        else:
            self.xi = self.v_xpb
            self.sum_xi2 = self.xi**2
            self.nx_block = int((self.v_bolt_col - 1) / 2)
            for i in range(self.nx_block - 1):
                self.sum_xi2 += self.xi ** 2
                self.xi += self.v_xpb

        if self.v_bolt_row % 2 == 0:
            self.yi = self.v_ypb/2
            self.sum_yi2 = self.yi**2
            self.ny_block = int(self.v_bolt_row / 2)
            for i in range(self.ny_block - 1):
                self.yi += self.v_ypb
                self.sum_yi2 += self.yi ** 2
        else:
            self.yi = self.v_ypb
            self.sum_yi2 = self.yi ** 2
            self.ny_block = int((self.v_bolt_row - 1) / 2)
            for i in range(self.ny_block - 1):
                self.yi += self.v_ypb
                self.sum_yi2 += self.yi ** 2

        self.sum_xi2 *= 4*self.ny_block
        self.sum_yi2 *= 4*self.nx_block
        self.j = self.sum_yi2+self.sum_xi2

        self.ftx = self.Tu * self._y /self.j
        self.fty = self.Tu * self._x / self.j
        self.fv = sqrt( self.ftx**2 + (self.fty + self.fvy)**2)

        self.v_bolt_Ab = 3.14 * self.v_bolt_db**2/4
        # self.Rnv1 = 1.13 * self.meu * self.Tb * self.ns2 * self.ns2
        self.Rnv11 = self.phi_n * self.Fnv * self.v_bolt_Ab * self.ns2
        self.Rnv2 = 2.4 * self.Fu * self.v_bolt_db * self.beam['tw']
        self.Rnv3 = 2.4 * self.ns2 * self.Fu * self.f_bolt_db * self.vplate_tp
        self.Rnv = min(self.Rnv11, self.Rnv2, self.Rnv3)
        self.fvv_ratio = self.fv/self.Rnv

    def _Vbolt_control(self):
        if self.fvv_ratio > self.phikh:
            while self.fvv_ratio <= self.phikh:
                for i in range(1, 3):
                    self.ns2 = i
                    TBplate_SPLICE._Vplate_tp(self)
                    TBplate_SPLICE._Vbolt(self)
                    if self.fvv_ratio <= self.phikh :
                        break
                if self.fvv_ratio <= self.phikh:
                    break
                self.v_bolt_col += 1
                TBplate_SPLICE._Vbolt(self)

        self.vplate_l = 2 * (2 * self.v_xde + (self.v_bolt_col - 1 ) * self.v_xpb) + self.gap


    def error_report(self):

        if self.f_bolt_db > self.f_bolt_db_max:
            self.error.append(f'f_bolt_db = {self.f_bolt_db} must <= f_bolt_db_max = {self.f_bolt_db_max} , reduce bolt size or increase bf of beam')

        if self.ff1 > self.ff2:
            self.error.append(f'0.6 * Fy/(0.5 * Fu) > Anet/Ag , {self.ff1} > {self.ff2} , reduce bolt size or increase bf of beam')

        if self.bolt_Fu < 7250:
            self.error.append(f'acceptabel  bolt standard is A490 or A325, fu >=7250 kg/cm2')

        if self.f_pb > self.f_pb_max:
            self.error.append(f'pb = {self.f_pb} > pb(max) = {self.f_pb_max} reduce bolt size')

        if self.edge_dis < 2 * self.f_bolt_db:
            self.error.append(f'edge_dis = {self.edge_dis} must >= 2*db ={2 * self.f_bolt_db} reduce bolt size or increase bf of beam')

        if self.vplate_tp_ratio > self.phikh:
            self.error.append(f'splice shear plate tp = {self.vplate_tp} must >= tp_req = {self.vplate_tp_req}')



    def TB_report(self):
        TB_rep = {'sh_splice': self.sh_splice, 'f_tp': self.plate_tp, 'f_b': self.plate_b, 'f_l': self.plate_l,
                   'f_bolt_db': self.f_bolt_db ,'f_bolt_n': self.f_bolt_n, 'edge_dis': round(self.edge_dis,1), 'f_de': self.f_de,'f_g':round(self.plate_b-2*self.edge_dis,1),
                   'f_pb': self.f_pb, 'f_ypb': self.f_ypb, 'holesize': self.f_bolt_db+self.hole_size_incrase, 'plate_tp_ratio': self.plate_tp_ratio,
                    'vplate_tp': self.vplate_tp, 'ns2': self.ns2,'vplate_h': self.vplate_h, 'vplate_l': self.vplate_l, 'v_bolt_db': self.v_bolt_db,
                    'v_bolt_row': self.v_bolt_row, 'v_bolt_col': self.v_bolt_col, 'v_bolt_n': self.ntotal_vbolt,
                    'v_xde': self.v_xde, 'v_yde': self.v_yde, 'v_xpb': self.v_xpb, 'v_ypb': self.v_ypb,
                    'vplate_tp_ratio': self.vplate_tp_ratio}
        self.report.update(TB_rep)

        self.solu += f'''
*** splice ***

Mu = 0.9 * Mp = {self.Mp}

V1 = Vu = {self.Vu}
phi_v = {self.phi_v} , d = {self.beam['d']} , tw = {self.beam['tw']}
Aw = d * tw = {self.Aw}
Cv = {self.Cv}
v2 = phi_v* 0.6 * Fy * Aw * Cv = {self.v2}

Vu = min(v1, v2) = {self.Vs}


top and bot plate:

tp_plate = {self.plate_tp} , d = {self.beam['d']} , b_plate = {self.plate_b} , l_plate = {self.plate_l}
F = Mu / (d + tp_plate) = {round(self.F,2)}

Ag_need = F / (0.9 * Fy) = {round(self.ag_req,2)}
b_plate = {self.plate_b} , tf_beam = {self.beam['tf']}
tp_need = max((Ag_need / b_plate) , tf_beam) / 2 = {round(self.plate_tp_req,2)}
ratio = tp_need/ tp_plate = {round(self.plate_tp_ratio,2)}


phi_n = {self.phi_n} , bolt_db = {self.f_bolt_db} , ns = {self.ns}

Fnv = (0.55Fu or 0.45Fu )bolt = {self.Fnv}
Fu(bolt) = {self.bolt_Fu}

Rn1 = phi_n * Fnv * bolt_Ab * ns = {self.Rn11}
Rn2 = 2.4 * Fu(plate) * bolt_db * tf_beam = {self.Rn2}
Rn3 = 2.4 * ns * Fu(plate) * bolt_db * tp_plate = {self.Rn3}
Rn = min(self.Rn1, self.Rn2, self. Rn3) = {self.Rn}

bolt_n = F/Rn = {self.f_bolt_n} rounded


Anet control:

hole_size_incrase = {self.hole_size_incrase}
plate_Anet = ns*(plate_tp * (plate_b - 2 * (bolt_db + hole_size_incrase + 0.2)))-tw] * plate_tp = {self.plate_Anet}
plate_Anet_req = (F/(0.75*Fu)) = {round(self.plate_Anet_req,2)}
ratio = plate_Anet_req / plate_Anet = {round(self.plate_Anet_ratio,2)}


shear plate:

vplate_h = {self.vplate_h} , vplate_tp = {self.vplate_tp} , vplate_l = {self.vplate_l} , ns2 = {self.ns2}

vplate_tp_req = Vu / (0.75 * 0.6 Fy * vplate_h * ns2) = {round(self.vplate_tp_req,2)}
ratio = vplate_tp_req / vplate_tp = {round(self.vplate_tp_ratio,2)}


bolts of shear plate:

v_bolt_db = {self.v_bolt_db}
v_bolt_Ab = {self.v_bolt_Ab}
v_bolt_row = {self.v_bolt_row}
v_bolt_col = {self.v_bolt_col}
v_bolt_n = {self.ntotal_vbolt}

v_xde = {self.v_xde}
v_yde = {self.v_yde}
v_xpb = {self.v_xpb}
v_ypb = {self.v_ypb}
xc = {self.xc}

fvy = Vs / v_bolt_n = {self.fvy}

Tu = Vs * xc = {self.Tu}

_y = {self._y} , _x = {self._x} , j = {self.j}

ftx = Tu * _y / j = {self.ftx}
fty = Tu * _x / j = {self.fty}

fv = sqrt( ftx^2 + (fty + fvy)^2) = {self.fv}

phi_n = {self.phi_n} , bolt_db = {self.v_bolt_db}

Fnv = (0.55Fu or 0.45Fu )bolt = {self.Fnv}
Fu(bolt) = {self.bolt_Fu}

Rn1 = phi_n * Fnv * v_bolt_Ab * ns2  = {self.Rnv11}
Rn2 = 2.4 * Fu(plate) * v_bolt_db * tw_beam = {self.Rnv2}
Rn3 = 2.4 * Fu(plate) * v_bolt_db * vplate_tp * ns2 = {self.Rnv3}
Rn = min(self.Rn1, self.Rn2, self. Rn3) = {self.Rnv}

ratio = self.fv / self.Rnv = {round(self.fvv_ratio,2)}




'''
        
        



    def TBplate_SPLIC_desgine(self):
        TBplate_SPLICE.Mpf(self)
        TBplate_SPLICE.Vsf(self)
        TBplate_SPLICE._F(self)
        TBplate_SPLICE._Ag_req(self)
        TBplate_SPLICE._Ag_control(self)
        TBplate_SPLICE.f_bolt_size_max(self)
        TBplate_SPLICE.f_bolt_desgin(self)
        TBplate_SPLICE.f_bolt_control(self)
        TBplate_SPLICE._Ag_control2(self)
        TBplate_SPLICE.f_plate_designe(self)
        TBplate_SPLICE.sh_splice_control(self)
        TBplate_SPLICE._Vplate_tp(self)
        TBplate_SPLICE._Vbolt(self)
        TBplate_SPLICE._Vbolt_control(self)
        TBplate_SPLICE.error_report(self)
        TBplate_SPLICE.TB_report(self)


if __name__ == '__main__':
    beam = {'name': 'PG', 'Z': 3354.375, 'd': 47.5, 'bf': 25, 'tf': 2.5, 'tw': 1.2, 'L': 1000, 'W': 51.84}
    Fy = 2400  # kg/cm2
    Fu = 3700  # kg/cm2
    bolt_Fu = 10000 # kg/cm2
    E = 2000000 # kg/cm2
    phikh = 1.05
    navard = 0 # tir varagh = 0 ,,, navard shode = 1 defult = 0
    v_condition = 0 # defult = 0
    sh_splice = 80 # cm
    Ry = 1.15  # 1.15 or 1.2 or 1.25
    tplate = [0.8, 1, 1.2, 1.5, 2, 2.5, 3, 3.5, 4]
    list_boltsize = [1.6, 2, 2.2, 2.4, 2.7, 3, 3.6]
    # list_boltsize = [1.6, 2]
    # tplate = [0.8, 1]
    # list_boltsize = [1.6]
    Fue = 4200  # kg/cm2 E60
    FueG = 4900  # kg/cm2 E70
    hangel = 20 # degree
    frametype = 0 # قاب خمشی معمولی صفر ویژه یک
    gap = 2
    max_n_bolt = 8
    beamconnec = WUF_W(beam, Fy, Fu, Ry, tplate, phikh, hangel, frametype)
    beamconnec2 = E8S_SPLICE(beam, Fy, Fu, Ry, tplate, phikh, hangel, frametype, E, navard, bolt_Fu, list_boltsize, v_condition, sh_splice)
    beamconnec3 = TBplate_SPLICE(beam, Fy, Fu, Ry, tplate, phikh, hangel, frametype, E, navard, bolt_Fu, list_boltsize, v_condition, sh_splice, gap, max_n_bolt)
    for i in beamconnec3.__dict__:
        print(i, ' = ', beamconnec3.__dict__[i])

