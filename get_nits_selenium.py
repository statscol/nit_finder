import pandas as pd
import numpy as np
import agents_custom as agt
import datetime
import random
from selenium.webdriver import Chrome,ChromeOptions,Firefox,FirefoxOptions

from selenium.webdriver.chrome.options import Options

def get_info(driver,nit,timeout=5):
    """
    driver: driver session 
    nit: id to be searched
    timeout: time in seconds after information retrieval (for ip ban prevention)
    
    """
    
    aux_nit=int(str(nit).replace("-","").strip())
    nit_field=driver.find_element_by_id("search")
    nit_field.clear()
    nit_field.send_keys(aux_nit)
    driver.find_element_by_id("boton_cabecera").click()
    info=driver.find_element_by_xpath("//table")
    info=info.text.split("\n")
    info=[i.split(":")[1].strip() for i in info if len(i.split(":"))>1]
    try:
        data_nit=dict({'NIT':nit,'resp':'404','razon':info[2],'depto':info[4],'CIUU':info[8],'fecha_const':info[9],'ultim_dato':info[11],'ultim_act':info[12]})
    except:
        data_nit=dict({'NIT':nit,'resp':'202','desc':'Not Found'})
    driver.find_element_by_id("search").clear()
    time.sleep(timeout)
    return(data_nit)


def get_site(list_nit,timeout=5):

	"""
	REQUIRES CHROME & FIREFOX DRIVER
    list_nit: list of nits to be searched, int or string 
    """
    ini=datetime.datetime.now()
    options=ChromeOptions()
    #options.add_argument('headless');
    options.add_argument("--incognito")
    caps = options.to_capabilities()
    webdr = "chromedriver"
    driver = Chrome(webdr,desired_capabilities=caps)
    url="https://www.einforma.co/servlet/app/portal/ENTP/prod/LISTA_EMPRESAS/razonsocial/anynithere"
    driver.get(url)
    driver.maximize_window()
    time.sleep(1)
    result=[]
    cont_prog=0
    for i in list_nit:
        
        if(cont_prog%10==0):
            print(f"[PROCESS] Trying {i} ...{100*(1-(cont_prog/len(list_nit))):.2f} % left")
        cont_prog+=1
        try:
            result.append(get_info(driver=driver,nit=i,timeout=timeout))
            
        except:
            driver.close()
            selec=random.choice([0,1])
            try:
                ##if it fails, go to another browser again, 
                if selec==1:
                    driver=Firefox(executable_path="./geckodriver")
                else:
                    
                    driver=Chrome(webdr,desired_capabilities=caps)

                url="https://www.einforma.co/servlet/app/portal/ENTP/prod/LISTA_EMPRESAS/razonsocial/anynithere"
                driver.get(url)
                driver.maximize_window()
                time.sleep(1)
                result.append(get_info(driver=driver,nit=i))
            except:
                
                break

    driver.close()
    print(f"[RESULT] ALL POSSIBLE NITS PROCESSED... elapsed time {(datetime.datetime.now()-ini).total_seconds():.2f} seg")
    return(result)



##usage:


lista=[9010203965, 9009076513, 9006968021, 9007934475]

get_site(lista,timeout=0.1)