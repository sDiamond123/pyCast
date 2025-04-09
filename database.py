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
        self.db.execute("CREATE TABLE dialogue(id int, body mediumtext, npc int, header varchar(128), background varchar(128), show_npc bit, choices mediumtext)")
        self.db.execute("CREATE TABLE npc(id int, name varchar(128), sentiment int, entry_point int, dialogue_entry_points mediumtext, attributes mediumtext, textures varchar(128))")
        self.db.execute("CREATE TABLE item(id int, name varchar(128), icon varchar(128), equipable bit, attributes mediumtext)")
        self.db.execute("CREATE TABLE flags(id int, value mediumtext)")

    def kill(self):
        self.db.close()
DB = Database()

if __name__ == "__main__":
    #DB.make_db()
    print(DB.get_tables())
    DB.delete("npc",("id", 0))
    DB.delete("npc",("id", 1))
    DB.delete("dialogue",("npc", 0))
    DB.delete("dialogue",("npc", 1))
      #DB.insert("npc", "(0,\'test_npc\',100,0,0,0,0)")
    DB.insert("npc", "(0, \"empty\", 0, 0, \"[{\"\"min\"\" : 0, \"\"max\"\" : 99, \"\"entry_point\"\" : 0},{\"\"min\"\" : 99, \"\"max\"\" : 100, \"\"entry_point\"\" : 0}]\", \"[{\"\"name\"\" : \"\"empty\"\"}]\", \"data/npc_profiles/empty\")")
    DB.insert("npc", "(1, \"chesire\", 50, 0, \"[{\"\"min\"\" : 0, \"\"max\"\" : 99, \"\"entry_point\"\" : 0},{\"\"min\"\" : 99, \"\"max\"\" : 100, \"\"entry_point\"\" : 0}]\", \"[{\"\"name\"\" : \"\"chesire cat\"\", \"\"race\"\" : \"\"cat\"\", \"\"humanoid\"\" : false}]\", \"data/npc_profiles/chesire\")")
    DB.insert("dialogue","(0,\"You awaken in a field of light. You find yourself blind. Your vision is blurry, out of focus. The world around you is abstract undefined, pure visual noise.\", 0, \"The Void\", \"data/npc_profiles/backgrounds/empty.png\", 1, \"[{\"\"prereq\"\" : [], \"\"set\"\" : [{\"\"type\"\" : \"\"sentiment\"\", \"\"value\"\" : 100}], \"\"goto\"\" : 1, \"\"body\"\" : \"\"* Something is here with you. Strain your eyes and try to see it.*\"\"}]\")")
    DB.insert("dialogue","(1,\"A face peers back from the sea of static. It is a small creature, roughly the size and shape of a house cat. Its face carries a blank expression and a docile smile. \", 1, \"The Cat\", \"data/npc_profiles/backgrounds/cat.png\", 0, \"[{\"\"prereq\"\" : [], \"\"set\"\" : [{\"\"type\"\" : \"\"sentiment\"\", \"\"value\"\" : -100}], \"\"goto\"\" : 2, \"\"body\"\" : \"\"Psst. Psst. Psst.\"\"},{\"\"prereq\"\" : [], \"\"set\"\" : [{\"\"type\"\" : \"\"sentiment\"\", \"\"value\"\" : 50}], \"\"goto\"\" : 3, \"\"body\"\" : \"\"Hail stranger, it appears I am lost\"\"},{\"\"prereq\"\" : [], \"\"set\"\" : [{\"\"type\"\" : \"\"sentiment\"\", \"\"value\"\" : -100}], \"\"goto\"\" : 2, \"\"body\"\" : \"\"Here kitty kitty kitty\"\"},{\"\"prereq\"\" : [], \"\"set\"\" : [], \"\"goto\"\" : -1, \"\"body\"\" : \"\"* Ignore it *\"\"}]\")")
    DB.insert("dialogue","(2,\"The cat ignores you. \", 1, \"The Cat\", \"data/npc_profiles/backgrounds/wall.png\", 1, \"[{\"\"prereq\"\" : [], \"\"set\"\" : [], \"\"goto\"\" : 2, \"\"body\"\" : \"\"Psst. Psst. Psst.\"\"},{\"\"prereq\"\" : [], \"\"set\"\" : [{\"\"type\"\" : \"\"sentiment\"\", \"\"value\"\" : 50}], \"\"goto\"\" : 3, \"\"body\"\" : \"\"DO. YOU. HEAR. ME.\"\"},{\"\"prereq\"\" : [], \"\"set\"\" : [], \"\"goto\"\" : 2, \"\"body\"\" : \"\"Here kitty kitty kitty\"\"},{\"\"prereq\"\" : [], \"\"set\"\" : [], \"\"goto\"\" : -1, \"\"body\"\" : \"\"* Give up *\"\"}]\")")
    DB.insert("dialogue","(3,\"The cat blinks, then opens its mouth: \n  And who might you be? \", 1, \"The Cat\", \"data/npc_profiles/backgrounds/wall.png\", 1, \"[{\"\"prereq\"\" : [], \"\"set\"\" : [], \"\"goto\"\" : -1, \"\"body\"\" : \"\"A friend.\"\"},{\"\"prereq\"\" : [], \"\"set\"\" : [], \"\"goto\"\" : -1, \"\"body\"\" : \"\"A travler.\"\"},{\"\"prereq\"\" : [], \"\"set\"\" : [], \"\"goto\"\" : -1, \"\"body\"\" : \"\"Nobody.\"\"},{\"\"prereq\"\" : [], \"\"set\"\" : [], \"\"goto\"\" : -1, \"\"body\"\" : \"\"It talks!\"\"},{\"\"prereq\"\" : [], \"\"set\"\" : [], \"\"goto\"\" : -1, \"\"body\"\" : \"\"* refuse to speak *\"\"}]\")")
      #print(DB.get_tables())
      #print(DB.get("*","npc",("name","\'test_npc\'")))
      #print(DB.get("*", "npc"))
      #DB.update("\'name\'", "npc", "\'name_2\'",("name","\'test_npc\'"))
      #DB.delete( "npc",("name","\'name_2\'"))
      #print(DB.get("*", "npc"))