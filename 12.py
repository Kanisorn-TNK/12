import fastapi
import mysql.connector
app = fastapi.FastAPI()
class Managerdb:
    def __init__(self,host,user,password,database):
        self.mydb = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database = database
        )
        self.mycursor = self.mydb.cursor( )
    
    def Tselect (self,table):
        sql = f"SELECT * FROM {table}"
        self.mycursor.execute(sql)
        show = self.mycursor.fetchall()
        return show
    
    def add_categories(self,category_name):
        sql = "INSERT INTO categories VALUES (%s,%s)"
        val_sql = (None,category_name)
        self.mycursor.execute(sql,val_sql)
        self.mydb.commit()
        if self.mycursor.rowcount >0 :
            return True
        else:
            return False
        
    def add_product(self,product_name,description,price,stock):
        sql = "INSERT INTO products VALUES (%s, %s, %s, %s,%s)"
        val_sql = (None,product_name, description, price, stock)
        self.mycursor.execute(sql, val_sql)
        self.mydb.commit()
        if self.mycursor.rowcount >0 :
            return True
        else:
            return False
        
    def add_order(self,order_date,total_amount,status):
        sql = "INSERT INTO orders VALUES (%s,%s,%s,%s)"
        val_sql = (None,order_date,total_amount,status)
        self.mycursor.execute(sql,val_sql)
        self.mydb.commit()   
        if self.mycursor.rowcount >0 :
            return True    
        else:
            return False
        
    def add_user(self,username,password,email,user_role):
        sql = "INSERT INTO users VALUES (%s,%s,%s,%s,%s)"
        val_sql = (None,username,password,email,user_role)
        self.mycursor.execute(sql,val_sql)
        self.mydb.commit()
        if self.mycursor.rowcount >0 :
            return True
        else:
            return False
        
    def Tdelete(self,table,colum,id):
        sql = f"DELETE FROM {table} WHERE {colum} = %s"
        val_sql = (id,)
        self.mycursor.execute(sql,val_sql)
        self.mydb.commit()
        if self.mycursor.rowcount >0:
            return True
        else:
            return False
        
    def Tedit(self,table,columname,val,columid,id):
        sql = f"UPDATE {table} SET {columname} = %s WHERE {columid} = %s"
        val_sql = (val,id)
        self.mycursor.execute(sql,val_sql)
        self.mydb.commit()
        if self.mycursor.rowcount >0:
            return True
        else:
            return False
db={
    "shop_db" : Managerdb("localhost","root","1234","yumyum")
}
@app.get('/select/{database}/{table}')
async def select(database,table):
    all_db = db[database]
    result = all_db.Tselect(table)
    return {"select_data" : result}
# http://127.0.0.1:8000/selectdb/shop_db/products

@app.get('/add_categories/{database}/{category_name}')
async def addcategories(database,category_name):
   result = db[database].add_categories(category_name)
   return {'add_categories': result}
    
@app.get('/addproduct/{database}/{product_name}/{description}/{price}/{stock}')
async def addproduct(database, product_name, description, price, stock):
    result = db[database].add_product(product_name, description, price, stock)
    return {'add_product': result}
    
@app.get('/addorder/{database}/{order_date}/{total_amount}/{status}')
async def addorder(database,order_date,total_amount,status):
    result = db[database].add_order(order_date,total_amount,status)
    return {'add_order': result}
    
@app.get('/adduser/{database}/{username}/{password}/{email}/{user_role}')
async def adduser(database,username,password,email,user_role):
    result = db[database].add_user(username,password,email,user_role)
    return {'add_user': result}
    
@app.get('/delete/{database}/{table}/{column}/{id}')
async def delete(database, table, column, id):
    all_db = db[database]
    result = all_db.Tdelete(table, column, id)
    return {"delete" : result}
    
@app.get('/edit/{database}/{table}/{columname}/{val}/{columid}/{id}')
async def edit(database,table,columname,val,columid,id):
    all_db = db[database]
    result = all_db.Tedit(table,columname,val,columid,id)
    return {"edit" : result}