from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

app=Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False



db=SQLAlchemy(app)

ma=Marshmallow(app)


#database
class ToDoList(db.Model):
    __tablename__='to_do_list'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    description=db.Column(db.String(400),nullable=False)
    completed=db.Column(db.Boolean,nullable=False,default=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return self.id


class ToDoList_schema(ma.Schema):
    class Meta:
        fields=('name','description','completed','date_created')


#instance of schema
todoList_schema=ToDoList_schema(many=False)
todoLists_schema=ToDoList_schema(many=True)


@app.route("/todolist", methods=['POST'])
def add_todo():

    try:
        name=request.json['name']
        description=request.json['description']

        new_todo = ToDoList(name=name,description=description)

        db.session.add(new_todo)
        db.session.commit()

        return todoList_schema.jsonify(new_todo)
    
    except Exception as e:
        print(e)
        return jsonify({"Error":"Invalid_Request"})
    


@app.route("/todolist",methods=['GET'])
def get_todos():
    todos=ToDoList.query.all()
    result_set= todoLists_schema.dump(todos)
    return jsonify(result_set)


@app.route("/todolist/<int:id>",methods=['GET'])
def get_todo(id):
    todo= ToDoList.query.get_or_404(int(id))
    return todoList_schema.jsonify(todo)



@app.route("/todolist/<int:id>", methods=['PUT'])
def update_todo(id):
    todo= ToDoList.query.get_or_404(int(id))

    name=request.json['name']
    description=request.json['description']
    completed= request.json['completed']

    todo.name=name
    todo.description=description
    todo.completed=completed

    db.session.commit()

    return todoList_schema.jsonify(todo)



@app.route("/todolist/<int:id>", methods=['DELETE'])
def delete_todo(id):
    todo= ToDoList.query.get_or_404(int(id))
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"Success":"To do deleted"})



if __name__ =="__main__":
    app.run(debug=True)