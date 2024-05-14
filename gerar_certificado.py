import os
import pandas as pd
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PyPDF2 import PdfMerger
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

def gerar_paragrafo_centralizado(documento, texto):
    centered_style = ParagraphStyle(
        name='Centered',
        alignment=1,  # 0=Left, 1=Center, 2=Right
        fontSize=13,  # 0=Left, 1=Center, 2=Right
        letterSpacing=3,
    )

    paragrafo_centralizado = Paragraph(texto, centered_style)
    largura_paragrafo, altura_paragrafo = paragrafo_centralizado.wrapOn(documento, 600, 300)

    x = (A4[1] - largura_paragrafo) / 2
    y = (A4[0] - altura_paragrafo) / 2

    paragrafo_centralizado.drawOn(documento, x, y)
    paragrafo_centralizado


def gerar_certificado(c, nome, data_inicio, data_fim, cidade):
    # Configurações do certificado
    # largura, altura = letter
    background = ImageReader("fundo_certificado.png")
    c.drawImage(background, 0, 0, width=A4[1], height=A4[0], preserveAspectRatio=True, mask='auto')

    c.setFont("Helvetica-Bold", 30)
    c.setFillColor(HexColor("#174639"))
    c.drawCentredString(420, 370, f"CERTIFICADO")
    c.setFont("Helvetica", 15)

    # Adicionando informações do participante
    '''
    texto = f"""
            Certificamos que <b>{nome}</b> participou da organização da <b>{evento}</b>, com duração de <b>{carga_horaria}</b> horas, ocorrido(a) na <b>1ª Feira de Agricultura Familiar do Sul do Piauí</b>, realizada entre os dias 09 a 11 de maio de 2024 em Corrente-PI.
            """
    '''
    texto = f"""
            Certificamos que <b>{nome}</b> participou da comissão organizadora da <b>1ª Feira de Agricultura Familiar do Sul do Piauí e do 1º Encontro de Agroecologia do Sul do Píaui</b>, realizado entre os dias 09 a 11 de maio de 2024 em Corrente-PI, com duração de <b>120</b> horas.
            """
    '''
    texto = f"""
            Certificamos que <b>{nome}</b> ministrou a(o) <b>{atividade}</b> de <b>{evento}</b>, com duração de <b>{carga_horaria}</b> horas, ocorrido na <b>1ª Feira de Agricultura Familiar do Sul do Piauí e no 1º Encontro de Agroecologia do Sul do Píaui</b>, realizado entre os dias 09 a 11 de maio de 2024 em Corrente-PI.
            """
    '''
    gerar_paragrafo_centralizado(c, texto)

def main():
    # Criando pasta para certificados se não existir
    if not os.path.exists("certificados"):
        os.makedirs("certificados")

    # Lendo os arquivos CSV da pasta "listas"
    for arquivo_csv in os.listdir("listas"):
        dados = pd.read_csv(os.path.join("listas", arquivo_csv))

        # Configurando o arquivo de saída
        arquivo_output = os.path.join("certificados", f"certificados_{os.path.splitext(arquivo_csv)[0]}.pdf")
        merger = PdfMerger()

        # Iterando sobre os participantes
        for indice, participante in dados.iterrows():
            nome = participante['Nome']
            data_inicio = '09/05/2023'
            data_fim = '11/05/2023'
            cidade = 'Corrente-PI'
            #evento = participante['Evento']
            #carga_horaria = participante['CH']
            #atividade = participante['Atividade']

            # Criando o certificado para cada participante
            nome_arquivo_temporario = f"temp_{nome.replace(' ', '_')}_{indice}.pdf"
            c = canvas.Canvas(nome_arquivo_temporario, pagesize=landscape(A4))
            gerar_certificado(c, nome, data_inicio, data_fim, cidade)
            c.save()

            # Adicionando o certificado ao arquivo de saída
            merger.append(nome_arquivo_temporario)
            

        # Salvando o arquivo de saída
        with open(arquivo_output, "wb") as f_out:
            merger.write(f_out)

if __name__ == "__main__":
    main()