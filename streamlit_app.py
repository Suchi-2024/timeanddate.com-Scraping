from asyncore import write
import streamlit as st
st.title("Weather Scraping and Detailed Result")
st.write('\n')
st.write('\n')
st.write('\n')
check=st.button("Check Live Weather Report",use_container_width=True)
if check:

    import requests               # to get the webpage
    import json                   # to convert API to json format

    from urllib.parse import urlencode
    import numpy as np
    import pandas as pd
    import re                     # regular expression operators

    from bs4 import BeautifulSoup as bsp
    
    from io import BytesIO

    response=requests.get('https://www.timeanddate.com/weather/india')
    if (response.status_code)==200:
        st.write("Succesfully Fetched Data")
    soup=bsp(response.content,'html.parser')
    #st.write(soup)
    tab=soup.find('table',attrs={'class':"zebra fw tb-wt zebra va-m"})
    tds=tab.find_all('td')
    act_leng=len(tds)//4
    leng=len(tds)
    name=[tds[i].text.strip() for i in range(0,leng,4)]
    for i in name:
        if i=="":
            name.remove(i)

    s1=tab.find_all('td',attrs={'class':'rbi'})
    temp=[s1[i].text.strip() for i in range(len(s1))]

    time=[tds[i].text.strip() for i in range(1,len(name)*4,4)]
    im=tab.find_all('img')
    weather=[]
    for i in im:
    # s=i.find('title')
    # weather.append(s)
        weather.append(i.get('title'))
    tec=[int(re.search(r'\d+', x).group()) for x in temp]
    #tec
    cen=[round((5/9)*(tec[i]-32),1) for i in range(len(tec))]
    #cen
    centi=["{}{}".format(cen[i], " °C") for i in range(len(cen))]
    
    data=pd.DataFrame({
    'Location':name,
    'Time':time,
    'Temperature(°F)':temp,
    'Temperature(°C)':centi,
    'Weather':weather
    }
    )
    st.write("Glimpse of Data :\n")
    st.write(data.head(20))
    #if st.button('Download Excel File'):
    # Convert the DataFrame to an Excel file in memory
        #pass
    buffer = BytesIO()
    data.to_excel(buffer, index=False, header=True)
    buffer.seek(0)
    #st.download_button(label="Download Excel workbook", data=buffer.getvalue(), file_name="Live Weather Report of India.xlsx", mime="application/vnd.ms-excel")
    st.download_button(label='Download Excel File', data=buffer, file_name='Live Weather Report of India.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    #data.to_excel('Live Weather Report of India.xlsx')
