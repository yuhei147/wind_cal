from bs4 import BeautifulSoup
import requests
import math
import streamlit as st

rjcc_url='https://www.aviationweather.gov/adds/tafs?station_ids=rjcc'
rjch_url='https://www.aviationweather.gov/adds/tafs?station_ids=rjch'
rjec_url='https://www.aviationweather.gov/adds/tafs?station_ids=rjec'
rjcb_url='https://www.aviationweather.gov/adds/tafs?station_ids=rjcb'
rjck_url='https://www.aviationweather.gov/adds/tafs?station_ids=rjck'
rjcm_url='https://www.aviationweather.gov/adds/tafs?station_ids=rjcm'
rjss_url='https://www.aviationweather.gov/adds/tafs?station_ids=rjss'
rjsf_url='https://www.aviationweather.gov/adds/tafs?station_ids=rjsf'
rjsn_url='https://www.aviationweather.gov/adds/tafs?station_ids=rjsn'
rjtt_url='https://www.aviationweather.gov/adds/tafs?station_ids=rjtt'
rjaa_url='https://www.aviationweather.gov/adds/tafs?station_ids=rjaa'
rjgg_url='https://www.aviationweather.gov/adds/tafs?station_ids=rjgg'
rjoo_url='https://www.aviationweather.gov/adds/tafs?station_ids=rjoo'
rjbb_url='https://www.aviationweather.gov/adds/tafs?station_ids=rjbb'
rjff_url='https://www.aviationweather.gov/adds/tafs?station_ids=rjff'
rjfu_url='https://www.aviationweather.gov/adds/tafs?station_ids=rjfu'
rjfo_url='https://www.aviationweather.gov/adds/tafs?station_ids=rjfo'
rjfr_url='https://www.aviationweather.gov/adds/tafs?station_ids=rjfr'


class wind_cal:
    def __init__(self, url,direction):
        self.url = url
        self.direction=direction
        
    def wind(self):
        res=requests.get(self.url)
        soup=BeautifulSoup(res.text,'html.parser')
        wx=soup.find('pre').text
        wx1=wx.split(' ')
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

        for wc,cg in enumerate(wind_c):
            if cg in wind_dict:
                for gu in gust:
                    wind_dict[gu]=wind_dict[wind_c[wc]]

        wx_new_list = []
        for data in wx1:
            changed_data = None

            for wind, add_text in wind_dict.items():
                if wind in data or len(data)==10:

                    new_cross, new_tail = add_text
                    changed_data = f'{data.strip()} {new_cross} {new_tail}' 
            
            if changed_data is None:
                wx_new_list.append(data.strip())
            else:
                wx_new_list.append(changed_data)

        new_wx_list = []
        for data in wx1:
            changed_data = None

            for wind, add_text in wind_dict.items():
                if wind in data or len(data)==10:
                    new_cross, new_tail = add_text
                    changed_data = f'{data.strip()} {new_cross} {new_tail}' 
            
            if changed_data is None:
                new_wx_list.append(data.strip())
            else:
                new_wx_list.append(changed_data)

        return wx_new_list

class wind_cal_no_tail:
    def __init__(self, url,direction):
        self.url = url
        self.direction=direction
        
    def wind(self):
        res=requests.get(self.url)
        soup=BeautifulSoup(res.text,'html.parser')
        wx=soup.find('pre').text
        wx1=wx.split(' ')
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

        for wc,cg in enumerate(wind_c):
            if cg in wind_dict:
                for gu in gust:
                    wind_dict[gu]=wind_dict[wind_c[wc]]

        wx_new_list = []
        for data in wx1:
            changed_data = None

            for wind, add_text in wind_dict.items():
                if wind in data or len(data)==10:

                    new_cross= add_text
                    changed_data = f'{data.strip()} {new_cross}' 
            
            if changed_data is None:
                wx_new_list.append(data.strip())
            else:
                wx_new_list.append(changed_data)

        return wx_new_list

class wind_cal_rjtt:
    def __init__(self, url,direction_1,direction_2):
        self.url = url
        self.direction_1=direction_1
        self.direction_2=direction_2
        
    def wind(self):
        res=requests.get(self.url)
        soup=BeautifulSoup(res.text,'html.parser')
        wx=soup.find('pre').text
        wx1=wx.split(' ')
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

        for wc,cg in enumerate(wind_c):
            if cg in wind_dict:
                for gu in gust:
                    wind_dict[gu]=wind_dict[wind_c[wc]]

        wx_new_list = []
        for data in wx1:
            changed_data = None

            for wind, add_text in wind_dict.items():
                if wind in data or len(data)==10:

                    new_cross= add_text
                    changed_data = f'{data.strip()} {new_cross}' 
            
            if changed_data is None:
                wx_new_list.append(data.strip())
            else:
                wx_new_list.append(changed_data)

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


rjfo_wind=wind_cal(rjfo_url,320)
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

