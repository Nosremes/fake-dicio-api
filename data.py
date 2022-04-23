import requests 
from bs4 import BeautifulSoup as bs

def scrap_info_palavra(palavra:str) -> dict:
    """
        Recebe uma palavra e retorna um dicionario
        contendo informações sobre ela; descricao,
        classe gramatial, sinonimos, antonimos. 
    """
    palavra = palavra.strip().lower()
    palavra_info = {
        "status":True, "palavra":palavra, "descricao":None, 
        "classeGramatical":None, "sinonimos" : None, 
        "antonimos" : None
    }

    palavra_page = requests.get("https://www.dicio.com.br/" + palavra)
    soap = bs(palavra_page.text, "html.parser")
    
    #nao tem a palavra / digitou errado 
    if soap.title.text == "Ocorreu um Erro":
        response = {"status":False, "palavra":palavra, "sugestao": None}
        sugestao = soap.find_all("a", attrs={"class":"_sugg"})
        if sugestao:
            response["sugestao"] = [
                x.text.strip().replace("?","").replace("\n", "") 
                    for x in sugestao]
        return response
    #scrap classe gramatical
    classe_gramatical = soap.find("span",attrs={"class":"cl"}).text
    palavra_info["classe_gramatical"] = classe_gramatical
    
    #scrap descricao
    descricao = soap.find("p",attrs={"itemprop":"description","class":"significado textonovo"})
    if descricao:
        descricao = [x.text for x in descricao if x.text.strip() != ""]
        palavra_info["descricao"] = descricao
    
    #scrap sinonimos e antonimos
    sinonimos = soap.find_all("p",attrs={"class":"adicional sinonimos"})
    if sinonimos:
        for s in sinonimos:
            if "Sinônimos" in s.findPrevious().text:
                sinonimos = [x.text for x in s.find_all("a") if x.text.strip() != ""]
                palavra_info["sinonimos"] = sinonimos
            elif "Antônimos " in s.findPrevious().text:
                antonimos = [x.text for x in s.find_all("a") if x.text.strip() != ""]
                palavra_info["antonimos"] = antonimos

    return palavra_info

def pesquisar_palavra(palavra:str) -> list:
    """Pesquisar a palavra no site dicio.com.br"""
    response = []
    palavra = palavra.strip().lower()
    pesquisa_page = requests.get("https://www.dicio.com.br/pesquisa.php?q=" + palavra)
    soap = bs(pesquisa_page.text, "html.parser") 

    #pegar resultados
    resultados = soap.find_all("a",attrs={"class":"_sugg"})
    for i in resultados:
        if i.span and i.span.text != None:
            response.append(i.span.text)

    return response

if __name__ == "__main__":
    palavras_teste = ["MAMBA   "," LARANJADA   ","CASAR ","Amora","JIRAFA","coc"]
    results = []
    for palavra in palavras_teste:
        results.append(scrap_info_palavra(palavra))

    for i in results:
        print(i)
        if not i["status"]:
            print("PESQUISA ---> ",pesquisar_palavra(i["palavra"]))
        print("\n-----\n")
