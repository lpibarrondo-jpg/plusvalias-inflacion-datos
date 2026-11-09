"""Construye el Excel de IPC con fórmulas a partir de data/raw.

Uso: python scripts/construir_hoja_ipc.py
Requiere openpyxl. Abre el resultado en Excel o LibreOffice para que se calculen las fórmulas.
"""
import csv, pathlib
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.comments import Comment
RAIZ = pathlib.Path(__file__).resolve().parents[1]
base = RAIZ / 'data'; out = RAIZ / 'data' / 'processed' / 'IPC_Espana_base_INE.xlsx'
rows = list(csv.DictReader(open(base / 'raw' / 'ine_ipc_indice_general_mensual.csv')))
pre = [kv.split(',') for kv in open(base / 'raw' / 'ine_IPC290752_variacion_mensual_1961_2001.txt').read().strip().split(';')]

F='Arial'; BLUE=Font(name=F,color='0000FF'); BLK=Font(name=F); BOLD=Font(name=F,bold=True)
HDR=Font(name=F,bold=True,color='FFFFFF'); HFILL=PatternFill('solid',fgColor='1F3864')
GREEN=Font(name=F,color='008000'); TITLE=Font(name=F,bold=True,size=14)
thin=Side(style='thin',color='BFBFBF')
def header(ws,r,cols,widths):
    for i,(c,w) in enumerate(zip(cols,widths),1):
        x=ws.cell(r,i,c); x.font=HDR; x.fill=HFILL; x.alignment=Alignment(wrap_text=True,vertical='center',horizontal='center')
        ws.column_dimensions[get_column_letter(i)].width=w
    ws.row_dimensions[r].height=45; ws.freeze_panes=ws.cell(r+1,1)

wb=Workbook()
# ---- Léeme
L=wb.active; L.title='Leeme'
n=len(rows); last=n+1
info=[
 ('IPC España — hoja base para el artículo sobre plusvalías nominales e inflación',TITLE),
 ('',None),
 ('Fuente','INE, Índice de Precios de Consumo (IPC). Serie IPC290751 «Nacional. Índice general. Índice», base 2025.'),
 ('Tabla INE','24077 / 76125 (API JSON Tempus3: servicios.ine.es/wstempus/js/ES/DATOS_SERIE/IPC290751)'),
 ('Web INE','https://www.ine.es/dyngs/INEbase/operacion.htm?c=Estadistica_C&cid=1254736176802&idp=1254735976607'),
 ('Descargado','9 de noviembre de 2026, desde la API oficial del INE'),
 ('Periodo','Enero 2002 – septiembre 2026 (297 meses, todos «Definitivo»). Octubre 2026 solo tiene avance y no se incluye.'),
 ('Verificación','Suma de los 297 índices = 23.424,447, idéntica a la de la API. Las 285 tasas interanuales recalculadas coinciden con las publicadas por el INE (serie IPC290750) con tolerancia de 0,1 pp.'),
 ('',None),
 ('Último dato (fecha)',None),
 ('Último índice',None),
 ('',None),
 ('Cómo leer la hoja','Texto azul = dato copiado de la fuente; texto negro = fórmula; verde = referencia a otra hoja.'),
 ('IPC_mensual','Índice mensual y tasas calculadas con fórmula.'),
 ('IPC_anual','Medias anuales, inflación acumulada hasta el último dato y coeficiente de actualización (lo que habría que multiplicar al precio de compra).'),
 ('Cifras_clave','Datos citables en el artículo, todos con fórmula.'),
 ('Anexo_1961_2001','Variaciones mensuales oficiales 1961–2001 (redondeadas a 1 decimal). Solo contexto: encadenarlas acumula error de redondeo.'),
 ('Nota metodológica','El IPC base 2025 es un cambio de escala: las tasas de variación no cambian respecto a bases anteriores. Para comparar un año completo se usa el índice medio anual; para fechas concretas, el índice del mes.'),
]
for i,(a,b) in enumerate(info,1):
    c=L.cell(i,1,a); c.font=TITLE if b is TITLE else BOLD
    if b is not None and b is not TITLE:
        d=L.cell(i,2,b); d.font=BLK; d.alignment=Alignment(wrap_text=True,vertical='top')
L['B10']=f'=INDEX(IPC_mensual!$A$2:$A${last},COUNT(IPC_mensual!$D$2:$D${last}))'; L['B10'].font=GREEN
L['B11']=f'=INDEX(IPC_mensual!$D$2:$D${last},COUNT(IPC_mensual!$D$2:$D${last}))'; L['B11'].font=GREEN; L['B11'].number_format='0.000'
L.column_dimensions['A'].width=22; L.column_dimensions['B'].width=110

# ---- Mensual
M=wb.create_sheet('IPC_mensual')
header(M,1,['Fecha','Año','Mes','Índice general (base 2025)','Variación mensual','Variación interanual','Inflación acumulada hasta el último dato','Valor real hoy de 1.000 € de ese mes (€)','Tipo de dato INE'],[11,8,6,14,12,12,16,16,12])
for i,r in enumerate(rows,2):
    y,m=r['fecha'].split('-')
    M.cell(i,1,r['fecha']).font=BLUE
    M.cell(i,2,f'=VALUE(LEFT(A{i},4))').font=BLK
    M.cell(i,3,f'=VALUE(RIGHT(A{i},2))').font=BLK
    c=M.cell(i,4,float(r['indice_base2025'])); c.font=BLUE; c.number_format='0.000'
    if i>2: M.cell(i,5,f'=D{i}/D{i-1}-1')
    if i>13: M.cell(i,6,f'=D{i}/D{i-12}-1')
    M.cell(i,7,f'=Leeme!$B$11/D{i}-1')
    M.cell(i,8,f'=1000*D{i}/Leeme!$B$11')
    M.cell(i,9,r['tipo_dato']).font=BLUE
    for col,fmt in ((5,'0.0%'),(6,'0.0%'),(7,'0.0%'),(8,'#,##0')):
        M.cell(i,col).number_format=fmt; M.cell(i,col).font=BLK
M['D1'].comment=Comment('INE, serie IPC290751, descargada de la API Tempus3 el 09/11/2026.','Claude')

# ---- Anual
A=wb.create_sheet('IPC_anual')
header(A,1,['Año','Meses con dato','Índice medio anual','Índice de diciembre','Inflación media anual','Inflación diciembre a diciembre','Inflación acumulada desde la media del año hasta el último dato','Coeficiente de actualización (× precio de compra)','Valor real hoy de 1.000 € guardados desde ese año (€)','€ de hoy necesarios para igualar 1.000 € de ese año'],[8,10,12,12,12,14,18,16,18,18])
years=sorted({int(r['fecha'][:4]) for r in rows})
rng=f'IPC_mensual!$B$2:$B${last}'; vr=f'IPC_mensual!$D$2:$D${last}'; mr=f'IPC_mensual!$C$2:$C${last}'
for i,y in enumerate(years,2):
    A.cell(i,1,y).font=BLK
    A.cell(i,2,f'=COUNTIF({rng},A{i})')
    A.cell(i,3,f'=AVERAGEIF({rng},A{i},{vr})')
    A.cell(i,4,f'=IF(COUNTIFS({rng},A{i},{mr},12)=0,"",SUMIFS({vr},{rng},A{i},{mr},12))')
    if i>2:
        A.cell(i,5,f'=IF(AND(B{i}=12,B{i-1}=12),C{i}/C{i-1}-1,"")')
        A.cell(i,6,f'=IF(AND(D{i}<>"",D{i-1}<>""),D{i}/D{i-1}-1,"")')
    A.cell(i,7,f'=Leeme!$B$11/C{i}-1')
    A.cell(i,8,f'=Leeme!$B$11/C{i}')
    A.cell(i,9,f'=1000*C{i}/Leeme!$B$11')
    A.cell(i,10,f'=1000*H{i}')
    for col,fmt in ((3,'0.000'),(4,'0.000'),(5,'0.0%'),(6,'0.0%'),(7,'0.0%'),(8,'0.0000'),(9,'#,##0'),(10,'#,##0')):
        A.cell(i,col).number_format=fmt; A.cell(i,col).font=BLK
lastA=len(years)+1
A.cell(lastA+2,1,f'Nota: {years[-1]} está incompleto (meses según columna B); su media no es comparable con años completos.').font=Font(name=F,italic=True)

# ---- Cifras clave
K=wb.create_sheet('Cifras_clave')
header(K,1,['Dato citable','Valor','Cálculo'],[70,14,70])
def idx(f): return f'INDEX(IPC_mensual!$D$2:$D${last},MATCH("{f}",IPC_mensual!$A$2:$A${last},0))'
def yr(y,col='C'): return f'INDEX(IPC_anual!${col}$2:${col}${lastA},MATCH({y},IPC_anual!$A$2:$A${lastA},0))'
items=[
 ('Subida de precios desde enero 2002 hasta el último dato',f'=Leeme!$B$11/{idx("2002-01")}-1','0.0%','Índice último / índice ene-2002 − 1'),
 ('Subida de precios desde la media de 2002',f'=Leeme!$B$11/{yr(2002)}-1','0.0%','Índice último / media 2002 − 1'),
 ('Valor real hoy de 1.000 € guardados desde 2002 (€)',f'=1000*{yr(2002)}/Leeme!$B$11','#,##0','1.000 × media 2002 / índice último'),
 ('Subida de precios desde enero 2015 (fin de los coeficientes de actualización)',f'=Leeme!$B$11/{idx("2015-01")}-1','0.0%','Ley 26/2014, efectos 1-1-2015'),
 ('Subida de precios desde enero 2021 (episodio inflacionario reciente)',f'=Leeme!$B$11/{idx("2021-01")}-1','0.0%','Índice último / índice ene-2021 − 1'),
 ('Inflación media de 2022 (récord de la serie desde 2002)',f'={yr(2022,"E")}','0.0%','Media 2022 / media 2021 − 1'),
 ('Pico de inflación interanual (julio 2022)',f'=INDEX(IPC_mensual!$F$2:$F${last},MATCH("2022-07",IPC_mensual!$A$2:$A${last},0))','0.0%','INE publica 10,8 %'),
 ('Coeficiente para actualizar un precio de compra de 2005 al último dato',f'={yr(2005,"H")}','0.0000','Media 2005 → índice último'),
]
for i,(a,f,fmt,c) in enumerate(items,2):
    K.cell(i,1,a).font=BLK; x=K.cell(i,2,f); x.font=GREEN; x.number_format=fmt; K.cell(i,3,c).font=BLK

# ---- Anexo
X=wb.create_sheet('Anexo_1961_2001')
header(X,1,['Fecha','Variación mensual oficial (%)'],[11,18])
for i,(f,v) in enumerate(pre,2):
    X.cell(i,1,f).font=BLUE; c=X.cell(i,2,float(v)); c.font=BLUE; c.number_format='0.0'
X['B1'].comment=Comment('INE, serie IPC290752, valores en puntos porcentuales redondeados a 1 decimal.','Claude')
wb.save(out)
