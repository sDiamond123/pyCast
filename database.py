import sqlite3

PRINT_SQL = True

class Database ():
    DB_NAME = "game_data.db"
    def __init__(self):
        self.db = sqlite3.connect(self.DB_NAME)
        self.cur = self.db.cursor()
        
    def execute(self, line):
        return self.cur.execute(line)
    
    def save(self):
        self.db.commit()

    def insert(self, table, value):
        self.__base_command("INSERT INTO",table,"VALUES",value, base_where=None, iterator=",")
        self.save() 

    def get_tables(self):
        return self.get("name", "sqlite_master")

    def __base_command(self, command, type, do, table, base_where = None, iterator = "AND"):
        where = ""
        if (base_where != None):
            where = " WHERE " + str(base_where[0]) + " = " + str(base_where[1])
            for i in range(1, int(len(base_where)/2)):
                where += iterator+ " " + str(base_where[2 * i]) + " = " + str(base_where[2*i + 1])
        if PRINT_SQL:
            print(command + " " + type + " " + do + " " + table + where)
        self.cur = self.execute(command + " " + type + " " + do + " " + table + where)
        return self.cur

    def get(self, type, table, where = None):
        return self.__base_command("SELECT", type, "FROM", table, where).fetchall()
    
    def delete(self, table, where = None):
        self.__base_command("DELETE FROM", table, "", "", where)
        self.save()

    def update (self, type, table, value, where = None):
        self.__base_command("UPDATE", table, "SET", type + " = " + value, where)
        self.save()

    def make_db(self):
        self.db.execute("CREATE TABLE dialouge(id, body, npc, header, choices)")
        self.db.execute("CREATE TABLE npc(id, name, sentiment, entry_point, dialouge_entry_points, attributes, textures)")
        self.db.execute("CREATE TABLE item(id, name, icon, equipable, attributes)")
        self.db.execute("CREATE TABLE flags(id, value)")

    def kill(self):
        self.db.close()
DB = Database()
#DB.make_db()
DB.delete("npc",("id", 0))
DB.delete("dialouge",("id", 0))
#DB.insert("npc", "(0,\'test_npc\',100,0,0,0,0)")
DB.insert("npc", "(0, \"empty\", 0, 0, \"[0]\", \"[]\", \"data/npc_profiles/empty.png\")")
DB.insert("dialouge","(0,\"You awaken in a sea of static. It is not black nor is it white, it is just blurry.\", 0, \"The void.\", \"[]\")")
#print(DB.get_tables())
#print(DB.get("*","npc",("name","\'test_npc\'")))
#print(DB.get("*", "npc"))
#DB.update("\'name\'", "npc", "\'name_2\'",("name","\'test_npc\'"))
#DB.delete( "npc",("name","\'name_2\'"))
#print(DB.get("*", "npc"))