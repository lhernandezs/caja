estado_colores = {
    'induccion': "IndianRed",
    'trasladado': "Violet",
    'aplazado': "Magenta",
    'condicionado': "DarkViolet",
    'por_certificar': "Lime",
    'certificado': "ForestGreen",
    'retiro_voluntario': "Aqua",
    'cancelado': "SteelBlue",
    'reintegrado': "DeepSkyBlue"
}

from config import ESTADO_COLORES
estado = 'en formacion'
try:
    color = ESTADO_COLORES[estado]
except:
    color = "coloreado"
print(color)
