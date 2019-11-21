import os
from flask import current_app
from flask import *
from uuid import uuid4
from werkzeug.utils import secure_filename

class Foto(): 

    @staticmethod
    def salvar(arquivo):
        extencao_foto = arquivo.filename.split('.')[-1].lower()
        novo_nome_foto = uuid4()
        e_permitido = Foto.extensao_permitida(extencao_foto)
         
        if e_permitido:
            novo_nome_foto = str(novo_nome_foto) + '.' + extencao_foto
            foto = secure_filename(arquivo.filename).split('_')[-1]
            diretorio = os.path.join(current_app.config['UPLOAD_FOLDER'], foto)
            diretorio_novo = os.path.join(current_app.config['UPLOAD_FOLDER'], novo_nome_foto)
            foto_existe = os.path.isfile(diretorio)

            if foto_existe:
                os.remove(diretorio)
                arquivo.save(diretorio_novo)
            else:
                arquivo.save(diretorio)
                os.rename(diretorio, diretorio_novo)

            return novo_nome_foto
        else: 
            return False

    @staticmethod
    def excluir(nome_foto):
        try:
            foto = secure_filename(nome_foto).split('_')[-1]
            diretorio = os.path.join(current_app.config['UPLOAD_FOLDER'], foto)
            foto_existe = os.path.isfile(diretorio)

            if foto_existe:
                os.remove(diretorio)

            return True
        except Exception:
            return False

        
    @staticmethod
    def extensao_permitida(extencao): 
        return extencao in ['png', 'jpg', 'jpeg']