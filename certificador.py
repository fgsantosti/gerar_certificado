from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.colors import HexColor
from datetime import datetime
from binascii import hexlify
import os
import pandas as pd

class Certificado:

    def __init__(self, nome_arquivo, dados):
        self.nome_arquivo = nome_arquivo
        self.documento = canvas.Canvas(self.nome_arquivo, pagesize=landscape(A4))
        self.dados = dados
        self.data_emissao = datetime.now().strftime('%d/%m/%Y')
        self.codigo = str(hexlify(os.urandom(15))).split("'")[1]

        background = ImageReader("fundo_certificado.png")
        self.documento.drawImage(background, 0, 0, width=A4[1], height=A4[0], preserveAspectRatio=True, mask='auto')

        self.documento.setFont("Helvetica-Bold", 10)
        self.documento.setFillColor(HexColor("#000"))
        self.draw_paragraph_centered("Nome da Presidente Aqui", A4[1] / 2 - 150, 140)
        self.draw_paragraph_centered("Presidente da 1ª Feira de Agricultura Familiar do Sul do Piauí", A4[1] / 2 - 150, 130)

        self.draw_paragraph_centered("Nome do Diretor Aqui", A4[1] / 2 + 150, 140)
        self.draw_paragraph_centered("Diretor Geral IFPI Campus Corrente", A4[1] / 2 + 150, 130)

        self.documento.setFont("Helvetica-Oblique", 10)
        self.documento.setFillColor(HexColor("#222"))
        self.documento.drawString(25, 25, f"Emitido em {self.data_emissao} e credencial gerada automaticamente {self.codigo}")

        self.gerar_certificados()

    def draw_paragraph_centered(self, text, x, y):
        centered_style = ParagraphStyle(
            name='Centered',
            alignment=1,  # 0=Left, 1=Center, 2=Right
            fontSize=12,  # Font size
            leading=14,   # Line spacing
        )
        paragrafo_centralizado = Paragraph(text, centered_style)
        largura_paragrafo, altura_paragrafo = paragrafo_centralizado.wrapOn(self.documento, 600, 300)
        paragrafo_centralizado.drawOn(self.documento, x, y)

    def gerar_certificados(self):
        for indice, participante in self.dados.iterrows():
            nome = participante['nome']
            data_inicio = '09/05/2023'
            data_fim = '11/05/2023'
            cidade = 'Corrente-PI'
            minicurso = participante['minicurso']
            carga_horaria = participante['carga_horaria']

            self.documento.setFont("Helvetica", 12)
            self.draw_paragraph_centered(f"Certificamos que {nome} participou do evento 1ª Feira de Agricultura Familiar do Sul do Piauí", A4[1] / 2, A4[0] * 0.55)
            self.draw_paragraph_centered(f"realizado em {data_inicio} a {data_fim} em {cidade}", A4[1] / 2, A4[0] * 0.5)
            self.draw_paragraph_centered(f"e realizou o {minicurso},", A4[1] / 2, A4[0] * 0.45)
            self.draw_paragraph_centered(f"com a carga horária de {carga_horaria} horas.", A4[1] / 2, A4[0] * 0.4)
            self.documento.showPage()

        self.documento.save()

# Lendo o arquivo CSV
arquivo_csv = "participantes.csv"
dados = pd.read_csv(arquivo_csv)

# Gerando os certificados
certificado = Certificado("certificados.pdf", dados)
