import bs4 as bs 
import urllib.request
import json
import io


url_list = ['grado-en-ingenieria-informatica-ingenieria-del-software#edit-group-plani', 'doble-grado-en-derecho-y-gestion-y-administracion-publica#edit-group-plani',
'grado-en-administracion-y-direccion-de-empresas#edit-group-plani','grado-en-medicina#edit-group-plani','grado-en-matematicas#edit-group-plani',
'doble-grado-en-ingenieria-informatica-tecnologias#edit-group-plani','grado-en-ingenieria-de-la-energia-por-la-universidad-de#edit-group-plani',
'grado-en-enfermeria#edit-group-plani', 'grado-en-biologia#edit-group-plani', 'grado-en-bioquimica-por-la-universidad-de-sevilla-y-la#edit-group-plani',
'grado-en-turismo#edit-group-plani', 'grado-en-arqueologia-por-la-universidad-de-granada#edit-group-plani']



def scraping_asignaturas():
        json_fixture = "["
        id = 1000
        counter_carreras = 1
        for url in url_list:
                source =  urllib.request.urlopen("https://www.us.es/estudiar/que-estudiar/oferta-de-grados/" + url).read()
                soup = bs.BeautifulSoup(source,"lxml")
                asignaturas = soup.find("table", class_ ="table-condensed").find("tbody").find_all("tr")
                asignatura_name = soup.find("h1", class_ = "text-center noticia grado").getText()
                
                for asignatura in asignaturas:
                        curso = asignatura.find("td", class_ = "views-field-field-cur-numcur").getText()
                        title = asignatura.find("td", class_ = "views-field views-field-title").find("a").getText()
                        if title!= "Trabajo Fin de Grado":
                                json_fixture = json_fixture + '{ "model": "app.asignatura", "pk":' + str(id) + ', "fields": {"nombre": "'+ title + '", "titulacion": "'+ asignatura_name + '", "anyo": '+ curso + '} },'
                                json_fixture = str.join("", json_fixture.splitlines())
                        id = id+1
                print(f"{counter_carreras}/12 ")
                counter_carreras +=1
        json_fixture = json_fixture[:-1]
        json_fixture = json_fixture + "]" 
        
        json_data = json.loads(json_fixture)   
        with open('datos_populate_asignaturas.json', 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)
scraping_asignaturas()