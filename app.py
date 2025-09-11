import os
import pandas as pd

from flask   import ( request, session, Flask, render_template, redirect, url_for, jsonify)

from config               import COLUMNAS_ACTIVOS, COLUMNAS_INSTRUCTORES, COLUMNAS_NOVEDADES, Config, TEMPLATES_FOLDER
from procesadorJuicios1   import ProcesadorJuicios1
from entradaHelper        import getDataFrame
from correo               import Correo

app = Flask(__name__, template_folder=TEMPLATES_FOLDER)

app.config.from_object(Config)
app.secret_key = app.config["SECRET_KEY"]

UPLOAD_FOLDER       = app.config["UPLOAD_FOLDER"] 
UPLOAD_FOLDER_DATA  = app.config["UPLOAD_FOLDER_DATA"]
ALLOWED_EXTENSIONS  = app.config["ALLOWED_EXTENSIONS"]

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_DATA, exist_ok=True)

def allowed_file(filename) -> bool:
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
    if 'novedades' not in session:
        session['novedades'] = None
    if 'activos' not in session:
        session['activos'] = None
    if 'instructores' not in session:
        session['instructores'] = None
    return render_template("index.html", variables = session)

@app.route("/upload_datos", methods=["POST"])
def upload_datos():
    session.pop('error', None)
    if "datos" not in request.files:
        return redirect(url_for("index"))
    file = request.files.get('datos')
    if file.filename == "datos.xlsx":
        if file.content_length is not None and file.content_length > 32786:
            session['error'] = f"el archivo que seleccionó no puede tener mas de 32K"
            return render_template("index.html", variables=session)
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        if size > 32786:
            session['error'] = f"el archivo que seleccionó no puede tener mas de 32K"
            return render_template("index.html", variables=session)
        try:
            df_novedades                = pd.read_excel(file, sheet_name='novedades').drop_duplicates()
            df_activos                  = pd.read_excel(file, sheet_name='activos').drop_duplicates()
            df_instructores             = pd.read_excel(file, sheet_name='instructores').drop_duplicates()    
            df_novedades.columns        = COLUMNAS_NOVEDADES
            df_activos.columns          = COLUMNAS_ACTIVOS
            df_instructores.columns     = COLUMNAS_INSTRUCTORES
            df_novedades['documento']   = pd.to_numeric(df_novedades['documento'], errors='coerce').astype('Int64')
            df_activos['documento']     = pd.to_numeric(df_activos['documento'], errors='coerce').astype('Int64')
            session['novedades']        = df_novedades.to_dict(orient='records')
            session['activos']          = df_activos.to_dict(orient='records')
            session['instructores']     = df_instructores.to_dict(orient='records')
            print(f"Tamaño de la session : {len(str(session).encode('utf-8'))}")
        except:
            session['error'] =f"no fue posible leer las hojas del archivo de 'datos.xlsx'"
    else:
        session['error'] =f"el archivo elegido {file.filename} debe llamarse 'datos.xlsx'"
    return render_template("index.html", variables = session)

@app.route("/delete_datos", methods=["POST"])
def delete_datos():
    session.pop('error', None)
    session['novedades']    = None
    session['activos']      = None
    session['instructores'] = None
    return render_template("index.html", variables=session)

@app.route("/upload_files", methods=["POST"])
def upload_files():
    session.pop('error', None)
    if "files" not in request.files:
        return redirect(url_for("index"))
    files = request.files.getlist("files")
    for file in files:
        if file and file.filename != "" and allowed_file(file.filename):
            try:
                file.save(os.path.join(UPLOAD_FOLDER, file.filename))
                juiciosFicha = ProcesadorJuicios1(UPLOAD_FOLDER, file.filename, session['novedades'], session['activos'], session['instructores'])
                diccionario = juiciosFicha.procesar()
                ficha = diccionario['ficha']
                session['fichas'][ficha] = {
                    'fecha_reporte'         : diccionario['fecha_reporte'],
                    'programa'              : diccionario['programa'],
                    'codigo_programa'       : diccionario['codigo_programa'],
                    'version_programa'      : diccionario['version_programa'],
                    'fecha_inicio'          : diccionario['fecha_inicio'],
                    'fecha_fin'             : diccionario['fecha_fin'],
                    'fin_etapa_lectiva'     : diccionario['fin_etapa_lectiva'],
                    'reglamento'            : diccionario['reglamento'],
                    'vencimiento'           : diccionario['vencimiento'],
                    'limite'                : diccionario['limite']
                }
            except Exception as e:
                session['error'] = e
        if len(session['fichas']) > 0:
            session['subio_fichas'] = True
        print(f"Tamaño de la session : {len(str(session).encode('utf-8'))}")
    return render_template("index.html", variables = session)

@app.route("/delete_multiple", methods=["POST"])
def delete_multiple_files():
    session.pop('error', None)    
    fichas = request.form.getlist("selectedFichasDelete")
    fichas = fichas[0].split(",")
    for ficha in fichas:
        try: 
            delete_file_disk(ficha)
        except Exception as e:
            session['error'] = e
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
    session.pop('error', None)    
    try: 
        delete_file_disk(ficha)
    except Exception as e:
        session['error'] = e
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
    session.pop('error', None)    
    try:
        df_datos: pd.DataFrame = getDataFrame(UPLOAD_FOLDER, f"{ficha}.xlsx", "datos")
        for col in df_datos.columns:
            df_datos[col] = df_datos[col].apply(
            lambda x: '' if x == 0 or pd.isna(x) or x == '' else (int(x) if isinstance(x, (int, float)) and not isinstance(x, bool) and float(x).is_integer() else x))
    except Exception as e:
        if 'error' not in session:
            session['error'] = f"Error: no fue posible abrir la hoja 'Datos' del archivo {e}"
        else: 
            session['error'].append(f"Error: no fue posible abrir la hoja 'Datos' del archivo {e}")
    return render_template("datos.html", dataFrame=df_datos, variables = session['fichas'][ficha], ficha= ficha)

@app.route('/mail/<ficha>', methods=["POST"])
def prepare_mail(ficha):
    return render_template("correo.html", variables = session['fichas'][ficha], ficha = ficha)    

@app.route('/send_mail', methods=["POST"])
def send_mail():
    form_data = request.form.to_dict(flat=True)
    datos_correo = form_data['datos_correo']
    print(datos_correo)
    destination_username, destination_domain = "lhernandezs@sena.edu.co".split('@')
    correo = Correo(destination_username, destination_domain, destination_username, datos_correo)
    try:
        correo.send_email()
        return jsonify({'message': 'Correo enviado exitosamente!'})
    except Exception as e:
        return jsonify({'message': f'Error al enviar el correo: {str(e)}'}), 500

@app.route('/dowmload/<ficha>', methods=["POST"])
def download(ficha):
    form_data = request.form.to_dict(flat=True)
    variables = form_data['variables']
    ficha = form_data['ficha']
    body = form_data['body']
    return render_template("correo.html", variables = variables, ficha = ficha, body = body)    

@app.route('/prueba', methods=["GET"])
def preuba():
    return render_template("prueba.html")    




if __name__ == "__main__":
    app.run(debug=True)