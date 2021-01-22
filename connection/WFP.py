class WFP:
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
        """
    Report = []
    Solution = []

    def __init__(self, beam, Fy, Fu, Ry, tplate, bcol, phikh, B, Fue, FueG, gap, hangel):

        self.hangel = hangel
        self.delta_x = 0
        self.FueG = FueG
        self.gap = gap
        self.phikh = phikh
        self.B = B
        self.Fue = Fue
        self.bcol = bcol
        self.treport = {}
        self.beam = beam
        self.tplate = tplate
        self.tplate.sort()
        self.Ry = Ry
        self.Fu = Fu
        self.Fy = Fy
        self.report = {}
        self.sh = self.beam['d'] *1.5
        self.np = 1  #  تعداد ورق بک سمت یا دو سمت جان
        self.bp = 10  # عرض ورق جان
        self.tp = min(self.tplate)  # ضخامت ورق جان
        self.hp = round(self.beam['d']-2*self.beam['tf']-2*self.beam['tw']-6)  # ارتفاع ورق جان

        # Cpr
        self.Cpr = (self.Fy + self.Fu) / 2 * self.Fy
        if self.Cpr >= 1.2:
            self.Cpr = 1.2
        if self.Cpr <= 1.1:
            self.Cpr = 1.1

        # top plate
        self.btop = self.beam['bf']
        self.btop = round(self.btop)
        self.ttopmin = (self.beam['tf'] * self.beam['bf'] / self.btop)
        self.ttop = self.ttopmin

        # bot plate
        self.bbot = self.beam['bf']
        self.bbot = round(self.bbot)
        self.tbot = self.ttop
       
        # Mpr
        self.Mpr = self.Cpr * self.Ry * self.beam['Z'] * self.Fy
        
        # run design
        WFP.Design(self)

    # awmin
    def aw_min(self, t1, t2):
        self.t = min(t1, t2)
        if self.t <= 1.2:
            self.awmin = 0.5
        elif 1.2 < self.t <= 2:
            self.awmin = 0.6
        else:
            self.awmin = 0.8

    # awmax
    def aw_max(self, t):
        self.awmax = t - 0.2

    def Design_Top_Bot_Plate(self):
        self.Lh = self.beam['L'] - 2 * self.sh
        # Vpr
        self.Vpr = 2 * self.Mpr / self.Lh + self.beam['W'] * self.Lh / 2
        # Vu
        self.Vu = self.Vpr + self.beam['W'] * self.sh
        # Mu
        self.Mu = self.Mpr + self.Vpr * self.sh + self.beam['W'] * self.sh ** 2 / 2

        # Ap top
        for i in self.tplate:
            if i < self.ttopmin:
                continue
            self.ttop = i
            self.Fp = self.Mu / (self.beam['d'] + (self.ttop + self.tbot) / 2)
            # phi = 1
            self.Ap = self.Fp / self.Fy
            # درصد خطا قرار داده شده جهت طراحی بهینه
            self.Aptopp = self.btop * self.ttop
            self.Aptopr = round(self.Ap / self.Aptopp, 2)
            if self.Ap > self.Aptopp * self.phikh:
                continue
            else:
                break

        # Ap bot
        for j in self.tplate:
            if j < self.ttopmin:
                continue
            self.tbot = j
            self.Fp = self.Mu / (self.beam['d'] + (self.ttop + self.tbot) / 2)
            # phi = 1
            self.Ap = self.Fp / self.Fy
            # درصد خطا قرار داده شده جهت طراحی بهینه
            #self.Ap *= self.phikh  # lazem baraye varagh paeen
            self.Apbotp = self.bbot * self.tbot  # masahat varagh zir
            self.Apbotr = round(self.Ap / self.Apbotp, 2)  # nesbat
            if self.Ap > self.Apbotp*self.phikh:
                continue
            else:
                break

        # ========================= joosh varagh bala va paeen
        # آزمایش غیر مخرب 1   اجرای جوش در کارخانه 0.85   اجرای کارگاهی  0.75
        self.awmaxtop = min(min(self.beam['tf'], self.ttop), self.ttop - 0.2)
        self.awtop = round(self.awmaxtop, 1)
        self.Fnw = 0.6 * self.Fue  # joosh gooshe s155 aeenname
        self.Awetop = 0.707 * self.awmaxtop
        # phi = 0.9  همان فی بالا که برای طراحی ورق بود برای طراحی جوش نه دهم
        self.Rn = 0.9 * self.B * self.Fnw * self.Awetop
        self.Rntop = self.Rn
        self.Latop = self.Fp / (2 * self.Rn)  # طول جوش مورد نیاز در هر سمت ورق زیر سری و رو سری
        self.Latop = round(self.Latop, 1)
        self.Latopneed = self.Latop
        # Lp طول ورق زیر سری و روسری که باید با یک فرمول بدست باید یعنی به طول جوش مرد نیاز یک عددی اضافه بشود
        self.btopb = self.bbot
        self.y = round((self.btopb - self.btop) / 2, 1)
        from math import tan, radians
        self.alfa = radians(25)
        self.x = round(self.y / tan(self.alfa), 1)
        self.Lptop = self.Latop + 2.5 + self.x
        self.Lptop = (self.Lptop // 5) * 5 + 5
        self.Latop = self.Lptop - 2.5 - self.x  # Sh = Lp  میشود بجای فرض اولیه و روابط کنترل می شوند
        self.awmaxbot = min(min(self.beam['tf'], self.tbot), self.beam['tf'] - 0.2)
        self.awbot = round(self.awmaxbot, 1)
        self.Awebot = 0.707 * self.awmaxbot
        # phi = 0.9  همان فی بالا که برای طراحی ورق بود برای طراحی جوش نه دهم
        self.Rn = 0.9 * self.B * self.Fnw * self.Awebot
        self.Rnbot = self.Rn
        self.Labot = round(self.Fp / (2 * self.Rn), 1)  # طول جوش مورد نیاز در هر سمت ورق زیر سری و رو سری
        self.Labotneed = self.Labot
        # Lp طول ورق زیر سری و روسری که باید با یک فرمول بدست باید یعنی به طول جوش مرد نیاز یک عددی اضافه بشود
        self.Lpbot = self.Labot + self.gap
        self.Lpbot = (self.Lpbot // 5) * 5 + 5
        self.Labot = self.Lpbot - self.gap



    def Control_Top_Bot_Plate(self):
        self.btop -= round(2 * self.awtop + 1.5)
        from math import ceil
        self.bbot += ceil(2 * self.awbot+1.5) + 1
        WFP.Design_Top_Bot_Plate(self)
        while self.sh != max(self.Lptop, self.Lpbot):
            self.sh = max(self.Lptop, self.Lpbot)
            if self.sh >= self.beam['L']/2:
                self.sh = self.beam['d']*1.5
                WFP.Design_Top_Bot_Plate(self)
                self.sh = max(self.Lptop, self.Lpbot)
                WFP.Design_Top_Bot_Plate(self)
                break
            WFP.Design_Top_Bot_Plate(self)




    def Design_Vplate(self):
        # self.hp = round(self.beam['d']-2*self.beam['tf']-5)  # ارتفاع ورق جان
        # self.bp = 10  # عرض ورق جان
        # self.np = تعداد ورق جان
        # self.tp = min(self.tplate)  # ضخامت ورق جان
        self.Rn1 = 0.6 * self.Fy * self.hp * self.tp * self.np
        self.rvplate = round(self.Vu/self.Rn1, 2)

    def Control_Vplate(self):
        if self.rvplate > 1 * self.phikh:
            for i in self.tplate:
                for j in range(2):
                    if self.rvplate > 1 * self.phikh:
                        self.np = j+1
                        self.tp = i
                        WFP.Design_Vplate(self)
                    else:
                        break
                if self.rvplate < 1 * self.phikh:
                    break

    def aw_vplate(self):
        # جوش ناودانی شکل ورق جان
        self.b = self.bp - self.gap  # عرض ناودانی جوش
        self.d1 = self.hp  # ارتفاع ناودانی جوش
        self.xbar = self.b ** 2 / (2 * self.b + self.d1)  # مختصات ایکس مرکز جوش ناودانی
        self.Ip = (8 * self.b ** 3 + 6 * self.b * self.d1 ** 2 + self.d1 ** 3) / 12 - self.b ** 4 / (2 * self.b + self.d1)  # ممان اینرسی قطبی جوش ناودانی
        self.ex = self.bp - self.xbar
        self.Ta = self.Vu * self.ex  # لنگر پیچشی در جوش kg.cm
        self.fv = self.Vu / (self.np * (2 * self.b + self.d1))  # تنش برشی وارد شده در جوش
        self.x1 = self.b - self.xbar
        self.fvv = (self.Ta * self.x1) / (self.np * self.Ip)  # تنش قایم لنگر پیچشی
        self.ybar = self.hp / 2
        self.fh = (self.Ta * self.ybar) / (self.np * self.Ip)  # تنش افقی ایجاد شده توسط لنگر پیچشی
        from math import sqrt
        self.fr = sqrt(self.fh ** 2 + (self.fvv + self.fv) ** 2)
        self.fw = 0.75 * self.B * 0.6 * self.Fue * 0.707  # ارزش جوش گوشه برای برش
        self.awv = round(self.fr / self.fw, 1)  # cm  بعد جوش گوشه ناودانی ورق اتصال جان باید برای حداقل و حداکثر بعد جوش کنترل شود اگر جواب نداد تعداد پلیت تغییر کن
        self.awv_max_u = min(self.tp - 0.2, min(self.tp, self.beam['tw']))
        self.awv_ratio = round(self.awv/self.awv_max_u, 2)
        WFP.aw_min(self, self.tp, self.beam['tw'])


    def Control_aw_vplate(self):
        while self.awv > self.awv_max_u*self.phikh:
            for j in range(2):
                self.np = j + 1
                WFP.Design_Vplate(self)
                WFP.aw_vplate(self)
                if self.awv <= self.awv_max_u*self.phikh:
                    break
            if self.awv <= self.awv_max_u*self.phikh:
                break 
            self.bp += 5
        if self.awv < self.awmin:
            self.awv = self.awmin
        

    def joint_plate(self):
        self.join_pl = max(self.ttop, self.tbot, self.beam['tf'])


    def beam_with_hangel(self):
        if self.hangel:
            from math import radians, tan, ceil
            angel = radians(self.hangel)
            self.delta_x = ceil(tan(angel)*self.btopb)
            # self.Lptop += self.delta_x
            # self.Lpbot += self.delta_x



    def connection_report(self):
        self.rep = {'name': self.beam['name'], 'd': self.beam['d'], 'bf': self.beam['bf'], 'tf': self.beam['tf'], 'tw': self.beam['tw'], 'gap': self.gap,
                    'btop': self.btop, 'btopb': self.btopb, 'ttop': self.ttop, 'Latap': self.Latop, 'awtop': self.awtop,
                    'Lptop': self.Lptop, 'x': self.x, 'y': self.y, 'Aptop_ratio': self.Aptopr,
                    'bbot': self.bbot, 'tbot': self.tbot, 'Labot': self.Labot, 'Lpbot': self.Lpbot, 'awbot': self.awbot, 'Apbot_ratio': self.Apbotr,
                    'h_vplate': self.hp, 'b_vplate': self.bp, 'n_vplate': self.np, 't_vplate': self.tp, 'ratio_vplate': self.rvplate,
                    'aw_vplate': self.awv, 'aw/awmax_vplate_ratio': self.awv_ratio, 't_joint_plate': self.join_pl, 'h_angel': self.hangel, 'delta_x': self.delta_x}
        WFP.Report.append(self.rep)


        self.solu = f'''******
{self.beam['name']}
******

unit = Kg.f , Cm

h_angel = {self.hangel} deg
delta_x = {self.delta_x} cm

Cpr = {self.Cpr},  Ry = {self.Ry},  Z = {self.beam['Z']},  Fy = {self.Fy}, Fu = {self.Fu}

Mpr = Cpr * Ry * Z * Fy = {round(self.Mpr)}

Lptop = {round(self.Lptop)},  Lpbot = {round(self.Lpbot)}, L = {self.beam['L']}, W = {self.beam['W']}

sh = max(Lptop & Lpbot) = {round(self.sh)}
Lh = L - 2 sh = {round(self.Lh)}
Vpr = ( 2 * Mpr / Lh ) + ( W * Lh / 2 ) = {round(self.Vpr)}
Vu = Vpr + ( W * sh ) = {round(self.Vu)}
Mu = Mpr + ( Vpr * sh ) + ( W * sh ^ 2 ) / 2 = {round(self.Mu)}

d = {self.beam['d']}, ttop = {self.ttop}, btop = {self.btop}, tbot = {self.tbot}, bbot = {self.bbot}
                      
Fp = Mu / (d + (ttop + tbot) / 2) = {round(self.Fp,2)}
Ap = Fp / Fy = {round(self.Ap)} need
A_topplate = btop * ttop = {self.Aptopp} exist
ratio = Ap / A_topplate = {self.Aptopr} 
A_botplate = bbot * tbot = {self.Apbotp} exist
Ratio = Ap / A_botplate = {self.Apbotr}


Fue = {self.Fue}, awtop = {self.awtop}, awbot = {self.awbot}, B = {self.B}

Fn = 0.6 * Fue = {self.Fnw}

# top plate

Awe = 0.707 * awtop = {round(self.Awetop,3)}
Rn = 0.9 * B * Fn * Awe = {round(self.Rntop,2)}
La = Fp / (2 * Rn) = {self.Latopneed} need -> {self.Latop} exist

# bot plate

Awe = 0.707 * awbot = {round(self.Awebot,3)}
Rn = 0.9 * B * Fn * Awe ={round(self.Rnbot,2)}
La = Fp / (2 * Rn) = {self.Labotneed} need -> {self.Labot} exist 

### shear plate

hp = {self.hp}, bp = {self.bp}, tp = {self.tp}, np = {self.np}

Rn = 0.6 * Fy * hp * tp * np = {self.Rn1}
Ratio = Vu / Rn = {self.rvplate}

# beam weld

gap = {self.gap}
b = bp - gap = {self.b} 
d = hp = {self.hp}
xbar = b ^ 2 / (2 * b + d) = {round(self.xbar,3)}
Ip = (8 * b ^ 3 + 6 * b * d ^ 2 + d ^ 3) / 12 - b ^ 4 / (2 * b + d) = {round(self.Ip,3)}
ex = bp - xbar = {round(self.ex,3)}
Ta = Vu * ex = {round(self.Ta,3)}
fv = Vu / (np * (2 * b + d)) = {round(self.fv,3)}
x1 = b - xbar = {round(self.x1,3)}
fvv = (Ta * x1) / (np * Ip) = {round(self.fvv,3)}
ybar = hp / 2 = {self.ybar}
fh = (Ta * ybar) / (np * Ip) = {round(self.fh,3)}
fr = sqrt(fh ^ 2 + (fvv + fv) ^ 2) = {round(self.fr,3)}
fw = 0.75 * B * 0.6 * Fue * 0.707 = {round(self.fw,3)}
aw = fr / fw = {round(self.awv,1)}
aw_max = min(tp - 0.2, min(tp, tw)) = {round(self.awv_max_u,1)}
Ratio = aw / aw_max = {round(self.awv_ratio,2)}
   
'''

        self.solu.encode('utf-8')
        WFP.Solution.append(self.solu)




    def Design(self):
        WFP.Design_Top_Bot_Plate(self)
        WFP.Control_Top_Bot_Plate(self)
        WFP.Design_Vplate(self)
        WFP.Control_Vplate(self)
        WFP.aw_vplate(self)
        WFP.Control_aw_vplate(self)
        WFP.joint_plate(self)
        WFP.beam_with_hangel(self)
        WFP.connection_report(self)


if __name__ == '__main__':
    beam1 = {'name': 'PG', 'Z': 858.75, 'd': 39.5, 'bf': 15, 'tf': 1, 'tw': 0.8, 'L': 300, 'W': 21.465}
    beam2 = {'name': 'ipe270', 'Z': 484, 'd': 27, 'bf': 13.5, 'tf': 1.02, 'tw': 0.66, 'L': 600, 'W': 54}
    beam3 = {'name': 'PG', 'Z': 3620, 'd': 54, 'bf': 30, 'tf': 2, 'tw': 0.8, 'L': 760, 'W': 25.68}
    beam = [beam1, beam2, beam3]
    phikh = 1
    gap = 2
    bcol = 0
    Fy = 2400  # kg/cm2
    Fu = 3700  # kg/cm2
    Ry = 1.15  # 1.15 or 1.2 or 1.25
    tplate = [0.8, 1, 1.2, 1.5, 2, 2.5, 3, 3.5, 4]
    B = 0.75
    Fue = 4200  # kg/cm2 E60
    FueG = 4900  # kg/cm2 E70
    hangel = 20 # degree
    for item in beam:
        beamconnec = WFP(item, Fy, Fu, Ry, tplate, bcol, phikh, B, Fue, FueG, gap, hangel)

    var = beamconnec.Report
    for i in var:
        print('********************\n********************')
        for j in i:
            print(j, ':', i[j])


    var2 = beamconnec.Solution
    file = open('test.txt', '+w')
    for i in var2:
        print(i)
        file.write(i)
    file.close()

