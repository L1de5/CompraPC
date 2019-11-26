import json
from flask import *

class CarrinhoCompras():

    def __init__(self):
        self._itens = []
    
    def get_itens(self):
        return self._itens

    def limpar(self):
        self._itens = []
        self.set_carrinho_on_session()

    def remover_item(self, dict_item):
        indice_item = self.existe_item(dict_item)

        if indice_item:
            self._itens.pop(indice_item)
        else:
            return False

        self.set_carrinho_on_session()
        return True

    def alterar_quantidade_item(self, indice_item, quantidade_nova):
        if self._itens[indice_item]:
            item = self._itens[indice_item]
            quantidade_estoque = int(item['produto']['quantidade'])

            if (quantidade_nova <= quantidade_estoque):
                self._itens[indice_item]['quantidade'] = quantidade_nova
            else:
                return False
        else:
            return False
        
        self.set_carrinho_on_session()

        return True

    def adicionar_item(self, dict_item):
        indice_item = self.existe_item(dict_item['produto'])

        if indice_item != -1:
            item = self._itens[indice_item]
            quantidade_nova = self.adicionar_quantidade_item(item)
            
            if quantidade_nova != False:
                self._itens[indice_item]['quantidade'] = quantidade_nova
            else:
                return False
        else:
            quantidade_estoque = int(dict_item['produto']['quantidade'])
            quantidade_compra = int(dict_item['quantidade'])

            if (quantidade_compra <= quantidade_estoque):
                self._itens.append(dict_item)
            else:
                return False
        
        self.set_carrinho_on_session()

        return True

    def existe_item(self, produto_dict):
        resultado = -1
        indice = -1

        for item in self._itens:
            indice += 1

            if item['produto'] == produto_dict:
                resultado = indice
                
        return resultado

    def adicionar_quantidade_item(self, item):
        quantidade_estoque = int(item['produto']['quantidade'])
        quantidade_compra = int(item['quantidade'])

        if (quantidade_compra < quantidade_estoque):
            return quantidade_compra + 1
        else:    
            return False

    def get_valor_total(self):
        valor_total = 0

        for item in self._itens:
            item_preco = int(item['produto']['preco'])
            item_quantidade = int(item['quantidade'])
            valor_total += item_preco * item_quantidade

        return valor_total
    
    def set_carrinho_on_session(self):
        itens_json = json.dumps(self._itens)
        session['carrinho'] = itens_json
        
    def set_itens_from_session(self):
        itens_session = session.get('carrinho', False)

        if itens_session:
            itens_dict = json.loads(itens_session)
            self._itens = itens_dict
