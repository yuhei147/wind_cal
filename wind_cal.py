from bs4 import BeautifulSoup
import requests
import math
import streamlit as st

rjcc_url='https://aviationweather.gov/cgi-bin/data/taf.php?ids=RJCC&sep=true'
rjch_url='https://aviationweather.gov/cgi-bin/data/taf.php?ids=RJCH&sep=true'
rjec_url='https://aviationweather.gov/cgi-bin/data/taf.php?ids=RJEC&sep=true'
rjcb_url='https://aviationweather.gov/cgi-bin/data/taf.php?ids=RJCB&sep=true'
rjck_url='https://aviationweather.gov/cgi-bin/data/taf.php?ids=RJCK&sep=true'
rjcm_url='https://aviationweather.gov/cgi-bin/data/taf.php?ids=RJCM&sep=true'
rjss_url='https://aviationweather.gov/cgi-bin/data/taf.php?ids=RJSS&sep=true'
rjsf_url='https://aviationweather.gov/cgi-bin/data/taf.php?ids=RJSF&sep=true'
rjsn_url='https://aviationweather.gov/cgi-bin/data/taf.php?ids=RJSN&sep=true'
rjtt_url='https://aviationweather.gov/cgi-bin/data/taf.php?ids=RJTT&sep=true'
rjaa_url='https://aviationweather.gov/cgi-bin/data/taf.php?ids=RJAA&sep=true'
rjgg_url='https://aviationweather.gov/cgi-bin/data/taf.php?ids=RJGG&sep=true'
rjoo_url='https://aviationweather.gov/cgi-bin/data/taf.php?ids=RJOO&sep=true'
rjbb_url='https://aviationweather.gov/cgi-bin/data/taf.php?ids=RJBB&sep=true'
rjff_url='https://aviationweather.gov/cgi-bin/data/taf.php?ids=RJFF&sep=true'
rjfu_url='https://aviationweather.gov/cgi-bin/data/taf.php?ids=RJFU&sep=true'
rjfo_url='https://aviationweather.gov/cgi-bin/data/taf.php?ids=RJFO&sep=true'
rjfr_url='https://aviationweather.gov/cgi-bin/data/taf.php?ids=RJFR&sep=true'

class wind_cal:
    def __init__(self, url,direction):
        self.url = url
        self.direction=direction
        
    def wind(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        res = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        wx1 = soup.text.split(' ')
        wind_data = []
        res=requests.get(self.url)
        soup=BeautifulSoup(res.text,'html.parser')
        wx1=soup.text.split(' ')
        wind_data=[]
        for a in wx1:
            if 'KT' in a:
                wind_data.append(a)

        gust=[]
        num=[]
        for wd,data in enumerate(wind_data):
            if 'G' in data:
                gust.append(data)
                num.append(wd)
        
        for d,data in enumerate(wind_data):
            if 'G' in data:
                wind_speed_g = int(wind_data[d][3:5])
                wind_gust_g = int(wind_data[d][6:8])
                a=round((wind_gust_g-wind_speed_g)/2+wind_speed_g )
                wind_data[d] = f"{data[:3]}{a:02d}KT"

        wind_c=[]
        for j in wind_data:
            for k in num:
              if wind_data.index(j) == k:
                  wind_c.append(j)

        wind_dict = {}
        magnetic_runway_direction = self.direction

        true_runway_direction = magnetic_runway_direction  

        for wni,data in enumerate(wind_data):

            wind_direction = int(wind_data[wni][:3])
            wind_speed = int(wind_data[wni][3:5])


            relative_wind_direction = wind_direction - true_runway_direction + 180
            if relative_wind_direction >= 350:
                relative_wind_direction -= 360

            crosswind_speed = abs(round(math.sin(math.radians(relative_wind_direction)) * wind_speed, 0))
            tailwind_speed = round(math.cos(math.radians(true_runway_direction - wind_direction)) * wind_speed, 0)

            new_cross = f"C{str(abs(crosswind_speed)).split('.')[0]}"
            new_tail =f"T{str(abs(tailwind_speed)).split('.')[0]}" if tailwind_speed < 0 else f"H{str(tailwind_speed).split('.')[0]}" 
            wind_dict[data] = (new_cross, new_tail)

        for cg in wind_c:
            if cg in wind_dict:
                for nn,gu  in enumerate(gust):
                    wind_dict[gu]=wind_dict[wind_c[nn]]

        wx_new_list = []
        for data in wx1:
            new_cross, new_tail = ('', '')
            for wind, add_text in wind_dict.items():
                if wind in data:
                    if isinstance(add_text, tuple):
                        new_cross, new_tail = add_text
                    else:
                        new_cross = add_text
                    break
            wx_new_list.append(f'{data.strip()} {new_cross} {new_tail}'.strip())

        return wx_new_list

class wind_cal_no_tail:
    def __init__(self, url,direction):
        self.url = url
        self.direction=direction
        
    def wind(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        res = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        wx1 = soup.text.split(' ')
        wind_data = []
        for a in wx1:
            if 'KT' in a:
                wind_data.append(a)

        gust=[]
        num=[]
        for wd,data in enumerate(wind_data):
            if 'G' in data:
                gust.append(data)
                num.append(wd)
        for d,data in enumerate(wind_data):
            if 'G' in data:
                wind_speed_g = int(wind_data[d][3:5])
                wind_gust_g = int(wind_data[d][6:8])
                a=round((wind_gust_g-wind_speed_g)/2+wind_speed_g )
                wind_data[d] = f"{data[:3]}{a:02d}KT"

        wind_c=[]
        for j in wind_data:
            for k in num:
              if wind_data.index(j) == k:
                  wind_c.append(j)

        wind_dict = {}
        magnetic_runway_direction = self.direction

        true_runway_direction = magnetic_runway_direction  

        for wni,data in enumerate(wind_data):

            wind_direction = int(wind_data[wni][:3])
            wind_speed = int(wind_data[wni][3:5])


            relative_wind_direction = wind_direction - true_runway_direction + 180
            if relative_wind_direction >= 350:
                relative_wind_direction -= 360

            crosswind_speed = abs(round(math.sin(math.radians(relative_wind_direction)) * wind_speed, 0))

            new_cross = f"C{str(abs(crosswind_speed)).split('.')[0]}"
            wind_dict[data] = (new_cross)

        for cg in wind_c:
            if cg in wind_dict:
                for nn,gu  in enumerate(gust):
                    wind_dict[gu]=wind_dict[wind_c[nn]]

        wx_new_list = []
        for data in wx1:
            new_cross, new_tail = ('', '')
            for wind, add_text in wind_dict.items():
                if wind in data:
                    if isinstance(add_text, tuple):
                        new_cross, new_tail = add_text
                    else:
                        new_cross = add_text
                    break
            wx_new_list.append(f'{data.strip()} {new_cross} {new_tail}'.strip())

        return wx_new_list

class wind_cal_rjtt:
    def __init__(self, url,direction_1,direction_2):
        self.url = url
        self.direction_1=direction_1
        self.direction_2=direction_2
        
    def wind(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        res = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        wx1 = soup.text.split(' ')
        wind_data = []
        for a in wx1:
            if 'KT' in a:
                wind_data.append(a)

        gust=[]
        num=[]
        for wd,data in enumerate(wind_data):
            if 'G' in data:
                gust.append(data)
                num.append(wd)
        for d,data in enumerate(wind_data):
            if 'G' in data:
                wind_speed_g = int(wind_data[d][3:5])
                wind_gust_g = int(wind_data[d][6:8])
                a=round((wind_gust_g-wind_speed_g)/2+wind_speed_g )
                wind_data[d] = f"{data[:3]}{a:02d}KT"

        wind_c=[]
        for j in wind_data:
            for k in num:
              if wind_data.index(j) == k:
                  wind_c.append(j)

        wind_dict = {}
        magnetic_runway_direction_1 = self.direction_1  # 磁北を基準とした滑走路の方向
        magnetic_runway_direction_2 = self.direction_2
        for i,data in enumerate(wind_data):

            # 風向と風速を取得
            wind_direction = int(wind_data[i][:3])
            wind_speed = int(wind_data[i][3:5])


            # 風向を飛行機の進行方向と合わせるために、風向を反転する
            relative_wind_direction_1 = wind_direction - magnetic_runway_direction_1 + 180
            if relative_wind_direction_1 >= 350:
                relative_wind_direction_1 -= 360

            relative_wind_direction_2 = wind_direction - magnetic_runway_direction_2 + 180
            if relative_wind_direction_2 >= 350:
                relative_wind_direction_2 -= 360

            # 風速と進行方向から横風と逆風の速度を計算
            crosswind_speed_1 = abs(round(math.sin(math.radians(relative_wind_direction_1)) * wind_speed, 0))
            crosswind_speed_2 = abs(round(math.sin(math.radians(relative_wind_direction_2)) * wind_speed, 0))

            new_cross_1 = f"34R C{str(abs(crosswind_speed_1)).split('.')[0]}"
            new_cross_2 = f"23 C{str(abs(crosswind_speed_2)).split('.')[0]}"
            wind_dict[data] = (new_cross_1, new_cross_2)

        for cg in wind_c:
            if cg in wind_dict:
                for nn,gu  in enumerate(gust):
                    wind_dict[gu]=wind_dict[wind_c[nn]]

        wx_new_list = []
        for data in wx1:
            new_cross, new_tail = ('', '')
            for wind, add_text in wind_dict.items():
                if wind in data:
                    if isinstance(add_text, tuple):
                        new_cross, new_tail = add_text
                    else:
                        new_cross = add_text
                    break
            wx_new_list.append(f'{data.strip()} {new_cross} {new_tail}'.strip())

        return wx_new_list
    
class write_taf:
    def __init__(self,ap):
        self.ap=ap
    def write_wind(self):
        output_list = []
        for i in range(len(self.ap)):
            if self.ap[i] == 'BECMG':
                output_list.append('\n     ')
                output_list.append(self.ap[i])
                output_list.append(' ')
            elif self.ap[i] == 'TEMPO':
                output_list.append('\n     ')
                output_list.append(self.ap[i])
                output_list.append(' ')
            else:
                output_list.append(self.ap[i])
                output_list.append(' ')

        output_str = ''.join(output_list)

        output_str = ''.join(output_list)
        return output_str

rjcc_wind=wind_cal_no_tail(rjcc_url,10)
rjcc=rjcc_wind.wind()
rjcc_taf=write_taf(rjcc)
rjcc=rjcc_taf.write_wind()

rjch_wind=wind_cal(rjch_url,120)
rjch=rjch_wind.wind()
rjch_taf=write_taf(rjch)
rjch=rjch_taf.write_wind()


rjec_wind=wind_cal(rjec_url,340)
rjec=rjec_wind.wind()
rjec_taf=write_taf(rjec)
rjec=rjec_taf.write_wind()

rjcb_wind=wind_cal(rjcb_url,350)
rjcb=rjcb_wind.wind()
rjcb_taf=write_taf(rjcb)
rjcb=rjcb_taf.write_wind()

rjck_wind=wind_cal(rjck_url,170)
rjck=rjck_wind.wind()
rjck_taf=write_taf(rjck)
rjck=rjck_taf.write_wind()

rjcm_wind=wind_cal_no_tail(rjcm_url,360)
rjcm=rjcm_wind.wind()
rjcm_taf=write_taf(rjcm)
rjcm=rjcm_taf.write_wind()

rjss_wind=wind_cal(rjss_url,270)
rjss=rjss_wind.wind()
rjss_taf=write_taf(rjss)
rjss=rjss_taf.write_wind()

rjsf_wind=wind_cal(rjsf_url,10)
rjsf=rjsf_wind.wind()
rjsf_taf=write_taf(rjsf)
rjsf=rjsf_taf.write_wind()

rjsn_wind=wind_cal(rjsn_url,280)
rjsn=rjsn_wind.wind()
rjsn_taf=write_taf(rjsn)
rjsn=rjsn_taf.write_wind()

rjtt_wind=wind_cal_rjtt(rjtt_url,340,230)
rjtt=rjtt_wind.wind()
rjtt_taf=write_taf(rjtt)
rjtt=rjtt_taf.write_wind()

rjaa_wind=wind_cal_no_tail(rjaa_url,340)
rjaa=rjaa_wind.wind()
rjaa_taf=write_taf(rjaa)
rjaa=rjaa_taf.write_wind()

rjgg_wind=wind_cal_no_tail(rjgg_url,360)
rjgg=rjgg_wind.wind()
rjgg_taf=write_taf(rjgg)
rjgg=rjgg_taf.write_wind()

rjoo_wind=wind_cal(rjoo_url,320)
rjoo=rjoo_wind.wind()
rjoo_taf=write_taf(rjoo)
rjoo=rjoo_taf.write_wind()

rjbb_wind=wind_cal_no_tail(rjbb_url,60)
rjbb=rjbb_wind.wind()
rjbb_taf=write_taf(rjbb)
rjbb=rjbb_taf.write_wind()

rjff_wind=wind_cal_no_tail(rjff_url,340)
rjff=rjff_wind.wind()
rjff_taf=write_taf(rjff)
rjff=rjff_taf.write_wind()

rjfu_wind=wind_cal(rjfu_url,320)
rjfu=rjfu_wind.wind()
rjfu_taf=write_taf(rjfu)
rjfu=rjfu_taf.write_wind()


rjfo_wind=wind_cal(rjfo_url,10)
rjfo=rjfo_wind.wind()
rjfo_taf=write_taf(rjfo)
rjfo=rjfo_taf.write_wind()

rjfr_wind=wind_cal(rjfr_url,180)
rjfr=rjfr_wind.wind()
rjfr_taf=write_taf(rjfr)
rjfr=rjfr_taf.write_wind()

st.title('WIND計算くん')
st.write(rjcc)
st.write(rjch)
st.write(rjec)
st.write(rjcb)
st.write(rjck)
st.write(rjcm)
st.write(rjss)
st.write(rjsf)
st.write(rjsn)
st.write(rjtt)
st.write(rjaa)
st.write(rjgg)
st.write(rjoo)
st.write(rjbb)
st.write(rjff)
st.write(rjfu)
st.write(rjfo)
st.write(rjfr)

