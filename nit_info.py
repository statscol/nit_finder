import numpy as np
import agents_custom as agt
from datetime import datetime

from bs4 import BeautifulSoup
import requests

def get_info_nit(nit):
    """
    Obtiene información del nit en repositorios públicos, tales como la actividad económica CIUU o su fecha de constitución.
    
    """
    url=f"https://www.einforma.co/servlet/app/portal/ENTP/prod/LISTA_EMPRESAS/razonsocial/{int(str(nit).replace('-','').strip())}"
    #print(url)
    page = requests.get(url,headers=agt.get_agent())
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        info=soup.find("table")
        info=[i.get_text().split(":") for i in info.findAll("tr") if len(i.get_text().split(":"))>1]
        data_nit=dict({'NIT':nit,'resp':'404','razon':info[2][1],'depto':info[4][1],'CIUU':info[8][1],'fecha_const':info[9][1],'ultim_dato':info[11][1],'ultim_act':info[12][1]})
        return(data_nit)
    except:
        return(dict({'NIT':nit,'resp':'202','desc':'Not Found'}))

get_info_nit(9007934475)  

