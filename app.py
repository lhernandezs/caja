import os
import pandas as pd

from flask import ( request, session, Flask, render_template, render_template_string, redirect, url_for)

from config                 import Config
from cargadorDatos          import CargadorDatos
from procesadorJuicios      import ProcesadorJuicios
from entrada                import Entrada

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config["SECRET_KEY"]

UPLOAD_FOLDER = app.config["UPLOAD_FOLDER"] 
UPLOAD_FOLDER_DATA = app.config["UPLOAD_FOLDER_DATA"]
ALLOWED_EXTENSIONS = app.config["ALLOWED_EXTENSIONS"]
DATA_FILE = app.config["DATA_FILE"]

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_DATA, exist_ok=True)

variables = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def index():
    if 'fichas' not in session:
        session['fichas'] = []
    if 'error' not in session:
        session['error'] = []
    if 'datos' not in session:
        session['datos'] = False
    return render_template("index.html", variables = session)

@app.route("/upload_datos", methods=["POST"])
def upload_datos():
    session['error'] = []
    file = request.files.get('datos_file')
    if file.filename == "datos.xlsx":
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER_DATA, filename))
        session['datos'] = True
    else:
        session['error'].append(f"el archivo elegido es {file.filename}, debe ser datos.xlsx")
    return redirect(url_for("index"))

@app.route("/upload", methods=["POST"])
def upload_files():
    session['error'] = []
    if "files" not in request.files:
        return redirect(url_for("index"))
    files = request.files.getlist("files")
    print(f"cantidad de fichas: {len(files)}, tipo de files: {type(files)}")
    for file in files:
        if file and file.filename != "" and allowed_file(file.filename):
            print(f"file.name: {file.filename}")
            filename = file.filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            try:
                print(f"session[datos] : {session['datos']}")
                if session['datos']:
                    datos = CargadorDatos(UPLOAD_FOLDER_DATA, "datos.xlsx").getDatos()
                    juiciosFicha = ProcesadorJuicios(UPLOAD_FOLDER, filename, datos['df_novedades'], datos['df_activos'], datos['df_instructores'])
                else:
                    juiciosFicha = ProcesadorJuicios(UPLOAD_FOLDER, filename)
                diccionario = juiciosFicha.procesar()
                session['fichas'].append(diccionario['ficha'])
            except Exception as e:
                session['error'].append(e)
    return redirect(url_for("index"))

@app.route("/delete_multiple", methods=["POST"])
def delete_multiple_files():
    selected_files = request.form.getlist("selectedFilesDeleteInput")

    if len(selected_files) == 1 and "," in selected_files[0]:
        selected_files = selected_files[0].split(",")
        for filename in selected_files:
        # for filename in selected_files[0].split(","):
            print(f"filename : {filename} tipo: {type(filename)}")
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], f"{filename}.xlsx")
            if os.path.isfile(file_path):
                os.remove(file_path)
            print(f"session[fichas]: 1 {session['fichas']}")
            if int(filename) in session['fichas']:
                print("paso por aqui")
                session['fichas'].remove(int(filename))
            print(f"session[fichas]: 2 {session['fichas']}")
    return render_template("index.html", variables = session)


@app.route("/delete/<filename>", methods=["POST"])
def delete_file(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], f"{filename}.xlsx")
    if os.path.isfile(file_path):
        os.remove(file_path)
        if filename in session['fichas']:
            session['fichas'].remove(filename)
    return redirect(url_for("index"))


@app.route("/dfDatos/<filename>", methods=["POST"])
def view_datos(filename):
    print(f"entro a view_datos: filename {filename}")
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
        raise e
    return render_template("datos.html", dataFrame=dfDatos)

@app.route("/prueba")
def prueba():
    redirect('index.html')
#     user_name = "Alice"
#     return render_template_string(
#         "hola",
#         name=user_name,
# )


if __name__ == "__main__":
    app.run(debug=True)
