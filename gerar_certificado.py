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





def gerar_certificado(c, nome, data_inicio, data_fim, cidade, minicurso, carga_horaria):
    # Configurações do certificado
    largura, altura = letter
    background = ImageReader("fundo_certificado.png")
    c.drawImage(background, 0, 0, width=A4[1], height=A4[0], preserveAspectRatio=True, mask='auto')

    c.setFont("Helvetica-Bold", 30)
    c.setFillColor(HexColor("#174639"))
    c.drawCentredString(420, 370, f"CERTIFICADO")
    c.setFont("Helvetica", 14)

    # Adicionando informações do participante
    texto = f"""
                Certificamos que <b>{nome}</b> participou do evento <b>1ª Feira de Agricultura Familiar do Sul do Piauí</b> realizado em 09/05/2023 a 11/05/2023, realizado em 09/05/2023 a 11/05/2023 em Corrente-PI e realizou o(a) minicurso <b>{minicurso}</b>, com carga horária de {carga_horaria} horas.
            """
    
    gerar_paragrafo_centralizado(c, texto)

def main():
    # Lendo o arquivo CSV
    arquivo_csv = "participantes.csv"
    dados = pd.read_csv(arquivo_csv)

    # Configurando o arquivo de saída
    arquivo_output = "certificados.pdf"
    merger = PdfMerger()

    # Iterando sobre os participantes
    for indice, participante in dados.iterrows():
        nome = participante['nome']
        data_inicio = '09/05/2023'
        data_fim = '11/05/2023'
        cidade = 'Corrente-PI'
        minicurso = participante['minicurso']
        carga_horaria = participante['carga_horaria']

        # Criando o certificado para cada participante
        c = canvas.Canvas(f"temp_{nome.replace(' ', '_')}.pdf", pagesize=landscape(A4))
        #c.drawImage("fundo_certificado.png", 0, 0, width=letter[0], height=letter[1])
        gerar_certificado(c, nome, data_inicio, data_fim, cidade, minicurso, carga_horaria)
        c.save()

        # Adicionando o certificado ao arquivo de saída
        merger.append(f"temp_{nome.replace(' ', '_')}.pdf")

    # Salvando o arquivo de saída
    with open(arquivo_output, "wb") as f_out:
        merger.write(f_out)

if __name__ == "__main__":
    main()
