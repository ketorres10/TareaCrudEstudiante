import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

# enlace a base de datos vía sqlalchemy
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "estudiantedatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)


# modelado
class Estudiante(db.Model):
    """
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(40), unique=True, nullable=False)
    apellido = db.Column(db.String(40), unique=True, nullable=False)

    def __repr__(self):
        return "<Nombre: {}>".format(self.nombre)


@app.route("/", methods=["GET", "POST"])
def home():
    # return "My flask app"
    if request.form:
        print(request.form)
        estudiante = Estudiante(nombre=request.form.get("nombre"), apellido=request.form.get("apellido"))
        db.session.add(estudiante)
        db.session.commit()
        return redirect("/")  

    ests = Estudiante.query.all()
    return render_template("home.html", ests = ests)
    # return render_template("home.html")

@app.route("/update", methods=["POST"])
def update():
    newnombre = request.form.get("newnombre")
    #oldnombre = request.form.get("oldnombre")
    newapellido = request.form.get("newapellido")
    #oldapellido = request.form.get("oldapellido")
    idE = request.form.get("idE")
    estudiante = Estudiante.query.get(idE)
    estudiante.nombre = newnombre
    estudiante.apellido = newapellido
    db.session.commit()
    return redirect("/")  

@app.route("/delete", methods=["POST"])
def delete():
    idE = request.form.get("idE")
    estudiante = Estudiante.query.get(idE)
    db.session.delete(estudiante)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)