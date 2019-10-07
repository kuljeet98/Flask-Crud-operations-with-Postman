from flask import Flask,jsonify,request
import sqlalchemy as db 
engine = db.create_engine('mysql://kuljeet:root@localhost/kuljeet')


conn = engine.connect()
metadata = db.MetaData()
flask = db.Table('flask', metadata, autoload=True, autoload_with=engine)

app = Flask(__name__)
@app.route('/insert', methods=['POST'])
def insert():
	value = request.get_json()
	un = value['Username']
	ps = value['Password']
	
	a = conn.execute("select Username from flask where Username= '%s'"%un )
	b=len(a.fetchall())
	
	if (b==0):
		conn.execute("insert into flask (Username,Password) values ('%s','%s')"%(un,ps))
		return jsonify("success")
	else:
		return jsonify("user alreadsy exists")

@app.route('/update', methods=['PUT'])
def update():
	value = request.get_json()
	un = value['Username']
	ops = value['Password']
	nps = value['new_password']
	a = conn.execute("select Username from flask where Username= '%s' and Password = '%s'"%(un,ops) )
	b=len(a.fetchall())
	
	if (b!=0): 
		conn.execute("update flask set Password ='%s' where Username = '%s'"%(nps,un))
		return jsonify("Updated Successfully!")
	else:
		return jsonify("No user Exicts!")

@app.route('/remove', methods=['DELETE'])
def remove():
	value = request.get_json()
	un = value['Username']
	a = conn.execute("select Username from flask where Username= '%s'"%un )
	b=len(a.fetchall())
	
	if (b!=0):
		conn.execute("Delete from flask where Username = '%s'"%(un))
		return jsonify("Deleted Successfully!")
	else:
		return jsonify("oops wrong user!")

if __name__ == '__main__':
	app.run(debug=True)