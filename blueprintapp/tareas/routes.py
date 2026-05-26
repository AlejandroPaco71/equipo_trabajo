# Librerias a usar en el modulo
from flask import request,render_template,redirect,url_for,Blueprint

# Referencia a la base de datos
from blueprintapp.app import db
# Modelos con los que interactura el modulo
from blueprintapp.tareas.models import Tarea

bp_tarea = Blueprint('bp_tarea',__name__,template_folder='templates')

@bp_tarea.route("/")
def index():
    tareas = Tarea.query.all()
    return render_template('tareas/index.html',tareas=tareas)

@bp_tarea.route("/create",methods=['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('tareas/create.html')
    elif request.method == 'POST':
        descripcion = request.form.get('descripcion')
        completado = True if 'completado' in request.form.keys() else False
        # Crear un objeto miembro
        tarea = Tarea(descripcion=descripcion,completado=completado)
        # Insertar en la bd a traves del ORM
        db.session.add(tarea)
        db.session.commit()
        # Redireccion al listado de miembros
        return redirect(url_for('bp_tarea.index'))
    

# Para actualizar una tarea
@bp_tarea.route("/edit/<int:id>" , methods=["GET", "POST"])
def edit(id):
    if request.method == "POST":
        descripcion = request.form['descripcion']
        completado = True if 'completado' in request.form.keys() else False
        # Buscamos la tarea en la BD
        tarea = Tarea.query.get(id)
        # Actualizamos los datos la tarea
        tarea.descripcion = descripcion
        tarea.completado = completado
        db.session.commit()
        # Redirigimos al listado
        return redirect(url_for("bp_tarea.index"))
    
    # Si es GET, mostramos el formulario con datos actuales
    tarea = Tarea.query.get(id)
    
    return render_template("tareas/edit.html" , tarea=tarea)

# Para eliminar una tarea
@bp_tarea.route("/delete/<int:id>")
def delete(id):
    # Buscamos la tarea en la BD por su id
    tarea = Tarea.query.get(id)
    # Eliminamos el registro
    db.session.delete(tarea)
    db.session.commit()
    # Redirigimos al listado de tareas
    return redirect(url_for("bp_tarea.index"))
        
        
        


