import os
import numpy as np
import pandas as pd

from flask      import ( request, session, Flask, render_template, redirect, url_for, jsonify)
from jinja2     import Environment, select_autoescape, FileSystemLoader

from config                     import Config
from cargadorDatos              import CargadorDatos
from procesadorJuicios          import ProcesadorJuicios
from entrada                    import Entrada

from correo                     import Correo
from modelo                     import DatosCorreoJuicios
from procesadorJuiciosHelper    import columnas_df_datos

from config                     import TEMPLATES_FOLDER, TEMPLATES

app = Flask(__name__, template_folder=TEMPLATES_FOLDER)
app.config.from_object(Config)
app.secret_key = app.config["SECRET_KEY"]

UPLOAD_FOLDER       = app.config["UPLOAD_FOLDER"] 
UPLOAD_FOLDER_DATA  = app.config["UPLOAD_FOLDER_DATA"]
ALLOWED_EXTENSIONS  = app.config["ALLOWED_EXTENSIONS"]

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_DATA, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def delete_file_disk(ficha):
    file_path = os.path.join(UPLOAD_FOLDER, f"{ficha}.xlsx")
    if os.path.isfile(file_path):
        os.remove(file_path)

@app.route("/", methods=["GET"])
def index():
    if 'fichas' not in session:
        session['fichas'] = {}
    if 'error' not in session:
        session['error'] = []
    if 'datos' not in session:
        session['datos'] = False
    if 'subio_fichas' not in session:
        session['subio_fichas'] = False        
    return render_template("index.html", variables = session)

@app.route("/upload_datos", methods=["POST"])
def upload_datos():
    session.pop('error', None)
    if "datos" not in request.files:
        return redirect(url_for("index"))
    file = request.files.get('datos')
    if file.filename == "datos.xlsx":
        file.save(os.path.join(UPLOAD_FOLDER_DATA, file.filename))
        session['datos'] = True
    else:
        session['error'] =f"el archivo elegido {file.filename} debe nombrarse 'datos.xlsx'"
    return redirect(url_for("index"))

@app.route("/upload", methods=["POST"])
def upload_files():
    session.pop('error', None)
    if "files" not in request.files:
        return redirect(url_for("index"))
    files = request.files.getlist("files")
    for file in files:
        if file and file.filename != "" and allowed_file(file.filename):
            try:
                file.save(os.path.join(UPLOAD_FOLDER, file.filename))
                if session['datos']:
                    datos = CargadorDatos(UPLOAD_FOLDER_DATA, "datos.xlsx").getDatos()
                    juiciosFicha = ProcesadorJuicios(UPLOAD_FOLDER, file.filename, datos['df_novedades'], datos['df_activos'], datos['df_instructores'])
                else:
                    juiciosFicha = ProcesadorJuicios(UPLOAD_FOLDER, file.filename)
                diccionario = juiciosFicha.procesar()
                ficha = diccionario['ficha']
                session['fichas'][ficha] = {
                                        'fecha_reporte'    : diccionario['fecha_reporte'],
                                        'programa'         : diccionario['programa'],
                                        'codigo_programa'  : diccionario['codigo_programa'],
                                        'version_programa' : diccionario['version_programa'],
                                        'fecha_inicio'     : diccionario['fecha_inicio'],
                                        'fecha_fin'        : diccionario['fecha_fin'],
                                        }
            except Exception as e:
                session['error'] = e
        if len(session['fichas']) > 0:
            session['subio_fichas'] = True
    return render_template("index.html", variables = session)

@app.route("/delete_multiple", methods=["POST"])
def delete_multiple_files():
    fichas = request.form.getlist("selectedFichasDelete")
    if len(fichas) == 1 and "," in fichas[0]:
        fichas = fichas[0].split(",")
        for ficha in fichas:
            delete_file_disk(ficha)
            if ficha in session['fichas'].keys():
                fichas = session['fichas']
                fichas.pop(ficha, None)
                session.pop('fichas', None)
                session['fichas'] = fichas
    if len(session['fichas']) == 0:
        session['subio_fichas'] = False                
    return render_template("index.html", variables = session)

@app.route("/delete/<ficha>", methods=["POST"])
def delete_file(ficha):
    delete_file_disk(ficha)
    if ficha in session['fichas'].keys():
        fichas = session['fichas']
        fichas.pop(ficha, None)
        session.pop('fichas', None)
        session['fichas'] = fichas
    if len(session['fichas']) == 0:
        session['subio_fichas'] = False
    return render_template("index.html", variables = session)

@app.route("/datos/<ficha>", methods=["POST"])
def view_datos(ficha):
    columnas = ["tipo", "documento", "nombres", "apellidos", "estado", "aprobado", "porEvaluar", "noAprobado", "enTramite", "activo", \
                          "IND", "BIL", "CIE", "COM", "CUL", "DER", "EMP", "ETI", "INV", "MAT", "SST", "TIC", "PRO", "TEC", "color" ]
    try:
        df_datos: pd.DataFrame = Entrada().getDataFrame(UPLOAD_FOLDER, f"{ficha}.xlsx", "Datos", columnas)
        for col in df_datos.columns:
            df_datos[col] = df_datos[col].apply(
            lambda x: '' if x == 0 or pd.isna(x) or x == '' else (int(x) if isinstance(x, (int, float)) and not isinstance(x, bool) and float(x).is_integer() else x))


        print("paso por aqui")

    except Exception as e:
        if 'error' not in session:
            session['error'] = f"Error: no fue posible abrir la hoja 'Datos' del archivo {e}"
        else: 
            session['error'].append(f"Error: no fue posible abrir la hoja 'Datos' del archivo {e}")
    return render_template("datos.html", dataFrame=df_datos, variables = session['fichas'][ficha], ficha= ficha)

# Ruta para recibir los datos del formulario y enviar el correo
@app.route('/mail', methods=["POST"])
def mail():
    form_data = request.form.to_dict(flat=True)
    variables = form_data['variables']
    ficha = form_data['ficha']
    body = form_data['body']

    return render_template("correo.html", variables = variables, ficha = ficha, body = body)    

@app.route('/send_mail', methods=["POST"])
def send_mail():

    form_data = request.form.to_dict(flat=True)
    datos_correo = form_data['datos_correo']
    print(datos_correo)

    destination_username, destination_domain = "lhernandezs@sena.edu.co".split('@')

    # correo = Correo('JUICI', destination_username, destination_domain, destination_username, datosCorreo)   # destino correo Leonardo            
    correo = Correo('NONE', destination_username, destination_domain, destination_username, datos_correo)   # destino correo Leonardo            

    try:
        correo.send_email()
        return jsonify({'message': 'Correo enviado exitosamente!'})
    except Exception as e:
        return jsonify({'message': f'Error al enviar el correo: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(debug=True)
