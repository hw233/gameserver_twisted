import sqlite3


class BPObjectDB(object):
    def __init__(self, connect, bpobject_table_name="BackpackObjects"):
        super(BPObjectDB, self).__init__()
        self.connect = connect
        self.bpobject_table_name = bpobject_table_name

    def check_and_create_user_table(self):
        c = self.connect.cursor()
        try:
            # try to create the BPObject table
            sqlcmd = "CREATE TABLE " + self.bpobject_table_name + \
                     " (ID INTEGER PRIMARY KEY, name TEXT)"
            c.execute(sqlcmd)
            self.connect.commit()

        except sqlite3.OperationalError:
            pass