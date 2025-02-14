from utils.sendEmail.use_case import send_mail_atualization
from utils.extranet_push.use_case import push_extranet
from utils.api import use_case as doc
from dotenv import load_dotenv
import os

load_dotenv()

__LOGIN_EXTRANET = os.getenv("LOGIN_EXTRANET")
__PASSWORD_EXTRANET = os.getenv("LOGIN_EXTRANET")

# endpoint
urlEstoque = 'https://sistema.maxiprod.com.br/api/v1/Estoques'
urlItem = 'https://sistema.maxiprod.com.br/api/v1/Itens'
urlGrupos = 'https://sistema.maxiprod.com.br/api/v1/Grupos'
urlItensPC = 'https://sistema.maxiprod.com.br/api/v1/ItensDosPedidosDeCompra'
urlReserva = 'https://sistema.maxiprod.com.br/api/v1/Reservas'
urlEmpresas = 'https://sistema.maxiprod.com.br/api/v1/Empresas'

# push items
def atualize_extranet():

    doc.update_data_Empresas(urlEmpresas, './files/Empresas_Maxi.csv')
    doc.update_data_Itens(urlItem, './files/Itens_Maxi.csv')
    doc.update_data_Estoque(urlEstoque,'./files/Itens_Estoque.csv')

    itens = doc.analyze_data()
    doc.generate_document(itens, './output/export_extranet.csv')

    result = push_extranet(__LOGIN_EXTRANET,__PASSWORD_EXTRANET)
    send_mail_atualization(result)

if __name__ == '__main__':

    atualize_extranet()