import os
import pandas as pd

from flask import ( request, session, Flask, render_template, redirect, url_for)

from config                 import Config
from cargadorDatos          import CargadorDatos
from procesadorJuicios      import ProcesadorJuicios
from entrada                import Entrada

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config["SECRET_KEY"]

UPLOAD_FOLDER       = app.config["UPLOAD_FOLDER"] 
UPLOAD_FOLDER_DATA  = app.config["UPLOAD_FOLDER_DATA"]
ALLOWED_EXTENSIONS  = app.config["ALLOWED_EXTENSIONS"]

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_DATA, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def index():
    if 'fichas' not in session:
        session['fichas'] = {}
    if 'error' not in session:
        session['error'] = []
    if 'datos' not in session:
        session['datos'] = False
    return render_template("index.html", variables = session)

@app.route("/upload_datos", methods=["POST"])
def upload_datos():
    session['error'] = []
    if "datos" not in request.files:
        return redirect(url_for("index"))
    file = request.files.get('datos')
    if file.filename == "datos.xlsx":
        file.save(os.path.join(UPLOAD_FOLDER_DATA, file.filename))
        session['datos'] = True
    else:
        session['error'].append(f"el archivo elegido {file.filename} debe nombrarse 'datos.xlsx'")
    return redirect(url_for("index"))

@app.route("/upload", methods=["POST"])
def upload_files():
    session['error'] = []
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
                session['fichas'][diccionario['ficha']] = {
                                    'fecha_reporte'         : diccionario['fecha_reporte'],
                                    'ficha'                 : diccionario['ficha'],
                                    'programa'              : diccionario['programa'],
                                    'codigo_programa'       : diccionario['codigo_programa'],
                                    'version_programa'      : diccionario['version_programa'],
                                    'fecha_inicio'          : diccionario['fecha_inicio'],
                                    'fecha_fin'             : diccionario['fecha_fin'],
                                                           }
            except Exception as e:
                session['error'].append(e)
    return render_template("index.html", variables = session)

@app.route("/delete_multiple", methods=["POST"])
def delete_multiple_files():
    selected_files = request.form.getlist("selectedFilesDeleteInput")
    if len(selected_files) == 1 and "," in selected_files[0]:
        selected_files = selected_files[0].split(",")
        for filename in selected_files:
            file_path = os.path.join(UPLOAD_FOLDER, f"{filename}.xlsx")
            if os.path.isfile(file_path):
                os.remove(file_path)
            if int(filename) in session['fichas'].keys():
                session['fichas'].pop(int(filename), None)
    return render_template("index.html", variables = session)

@app.route("/delete/<filename>", methods=["POST", "GET"])
def delete_file(filename):
    print(f"filename : {filename}" )
    file_path = os.path.join(UPLOAD_FOLDER, f"{filename}.xlsx")
    if os.path.isfile(file_path):
        os.remove(file_path)
    if filename in session['fichas'].keys():
        session['fichas'].pop(int(filename), None)
    return render_template("index.html", variables = session)

@app.route("/dfDatos/<filename>", methods=["POST"])
def view_datos(filename):
    columnas = ["tipo", "documento", "nombres", "apellidos", "estado", "aprobado", "porEvaluar", "noAprobado", "enTramite", "activo", \
                          "IND", "BIL", "CIE", "COM", "CUL", "DER", "EMP", "ETI", "INV", "MAT", "SST", "TIC", "PRO", "TEC" ]
    try:
        #OJO.. tener en cuenta que leerARchivo está colocando un directorio, debe mejorarse los parametros de este metodo en EntradaSalida
        dfDatos: pd.DataFrame = Entrada().getDataFrame(UPLOAD_FOLDER, f"{filename}.xlsx", "Datos", columnas)
        dfDatos.fillna("", inplace=True)
        # OJO.. como mejorar la presentacion del DATAFRAME
        # dfDatos['porEvaluar'] = dfDatos['porEvaluar'].round().astype(int)
        # dfDatos.style.apply(color_rows, axis=1)
    except Exception as e:
        session['error'].append(f"Error: no fue posible abrir la hoja 'Datos' del archivo {e}")
    return render_template("datos.html", dataFrame=dfDatos)

if __name__ == "__main__":
    app.run(debug=True)
