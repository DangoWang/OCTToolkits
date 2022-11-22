# -*- coding: utf-8 -*-

import sqlite3

def project():
    return ["", "dsf"]

def flat(list_):
    res = []
    for i in list_:
        if isinstance(i, list) or isinstance(i, tuple):
            res.extend(flat(i))
        else:
            res.append(i)
    return res
        
class taskInfo:
    def __init__(self, project):
        self.project = project
        self.db = '//192.168.15.253/projects/Daily_DB/'+project+'/DATA.s3db'
  
    def searchTaskInfoDict(self, name_en):
        result = {}
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(tasks)")
        column = cursor.fetchall()
        l_column_name = []
        column_names = ""
        for col in column:
            l_column_name.append(col[1])
            column_names = column_names + "'" + col[1] + "',"
        #print l_column_name
        #print column_names[:-1]
        cursor.execute("SELECT * from tasks where [name_en]='"+name_en+"' order by [name] asc;")
        data = cursor.fetchall()
        #print data
        if len(data) == 1:
            for i in range(0, len(l_column_name)):
                result[l_column_name[i]] = data[0][i]
        pass
        cursor.close()
        conn.close()
        return result

    def searchTaskInfoDict_ng(self, name, group):
        result = {}
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(tasks)")
        column = cursor.fetchall()
        l_column_name = []
        column_names = ""
        for col in column:
            l_column_name.append(col[1])
            column_names = column_names + "'" + col[1] + "',"
        #print l_column_name
        #print column_names[:-1]
        cursor.execute("SELECT * from tasks where [name]='"+name+"' AND [group]='"+group+"' order by [name] asc;")
        data = cursor.fetchall()
        #print data
        if len(data) == 1:
            for i in range(0, len(l_column_name)):
                result[l_column_name[i]] = data[0][i]
        pass
        cursor.close()
        conn.close()
        return result

    def searchUserTaskInfoList(self, user):
        result = []
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(tasks)")
        column = cursor.fetchall()
        l_column_name = []
        column_names = ""
        for col in column:
            l_column_name.append(col[1])
            column_names = column_names + "'" + col[1] + "',"
        cursor.execute("SELECT * from tasks where [user]='"+user+"' order by [name] asc;")
        # cursor.execute("%s" % s)
        l_data = cursor.fetchall()
        #print data
        for data in l_data:
            rlt = {}
            for i in range(0, len(l_column_name)):
                rlt[l_column_name[i]] = data[i]
            result.append(rlt)
        pass
        cursor.close()
        conn.close()
        return result

    def now(self):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("select strftime('%Y%m%d_%H%M','now','localtime')")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data[0][0]
        
    def searchShotNameList(self, scene):
        result = []
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("select DISTINCT [name] from tasks where [scene]='"+scene+"' order by [name] asc;")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return flat(result)
        
    def searchAssetNameList(self, classify):
        result = []
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("select DISTINCT [name] from tasks where [classify]='"+classify+"' order by [name] asc;")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return flat(result)

    def searchTaskInfoList(self, column_str, column_val, column_ord="name"):
        result = []
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(tasks)")
        column = cursor.fetchall()
        l_column_name = []
        column_names = ""
        for col in column:
            l_column_name.append(col[1])
            column_names = column_names + "'" + col[1] + "',"
        cursor.execute("SELECT * from tasks where ["+column_str+"]='"+column_val+"' order by ["+column_ord+"] asc")
        l_data = cursor.fetchall()
        for data in l_data:
            rlt = {}
            for i in range(0, len(l_column_name)):
                rlt[l_column_name[i]] = data[i]
            #print rlt
            result.append(rlt)
        pass
        cursor.close()
        conn.close()
        return result

    def searchUserSubmitsInfoList(self, user):
        result = []
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(submits)")
        column = cursor.fetchall()
        l_column_name = []
        column_names = ""
        for col in column:
            l_column_name.append(col[1])
            column_names = column_names + "'" + col[1] + "',"
        cursor.execute("SELECT * from submits where [user]='"+user+"' order by [task] asc;")
        # cursor.execute("%s" % s)
        l_data = cursor.fetchall()
        #print data
        for data in l_data:
            rlt = {}
            for i in range(0, len(l_column_name)):
                rlt[l_column_name[i]] = data[i]
            result.append(rlt)
        pass
        cursor.close()
        conn.close()
        return result

    def searchShotTaskInfoList(self, scene):
        return self.searchTaskInfoList("scene", scene)

    def searchAssetTaskInfoList(self, classify):
        return self.searchTaskInfoList("classify", classify)
        
    def searchBigList(self):
        result = []
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("select DISTINCT [big] from tasks order by [big] asc;")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return flat(result)
        
    def searchGroupList(self, big=''):
        result = []
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        if big == '':
            cursor.execute("select DISTINCT [group] from tasks order by [group] asc;")
        else:
            cursor.execute("select DISTINCT [group] from tasks where [big] = '"+big+"' order by [group] asc;")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return flat(result)
        
    def searchClassifyList(self):
        result = []
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("select DISTINCT [classify] from tasks order by [classify] asc;")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return flat(result)
        
    def searchSceneList(self):
        result = []
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("select DISTINCT [scene] from tasks order by [scene] asc;")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return flat(result)

    def searchCacheInfoDict(self, name_en):
        result = []
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(caches)")
        column = cursor.fetchall()
        l_column_name = []
        column_names = ""
        for col in column:
            l_column_name.append(col[1])
            column_names = column_names + "'" + col[1] + "',"
        #print l_column_name
        #print column_names[:-1]
        cursor.execute("SELECT * from caches where [name_en]='"+name_en+"' order by [name_en] asc;")
        l_data = cursor.fetchall()
        #print data
        for data in l_data:
            rlt = {}
            for i in range(0, len(l_column_name)):
                rlt[l_column_name[i]] = data[i]
            result.append(rlt)
        pass
        cursor.close()
        conn.close()
        return result

    def submitTaskFiles(self, data = {}, db = None):
        conn = None
        if db == None:
            conn = sqlite3.connect( self.db )
        else:
            conn = sqlite3.connect( db )

        cursor = conn.cursor()

        taskId = data["taskId"]
        task = data["task"]
        version = data["version"]
        user = data["user"]
        path = data["path"]
        projectf = data["projectf"]
        previewf = data["previewf"]
        software = data["software"]
        describe = data["describe"]
        hasAD = data["hasAD"]
        
        #print "1"
        sql_submits = "INSERT INTO [submits] ([taskId], [task], [projectf], [previewf], [version], [software], [user], [path], [describe], [hasAD], [subtime]) VALUES ("+taskId+","+"'"+task+"',"+"'"+projectf+"',"+"'"+previewf+"',"+version+","+"'"+software+"',"+"'"+user+"',"+"'"+path+"',"+"'"+describe+"',"+hasAD+","+"datetime('now','localtime'))"
        #print sql_submits
        cursor.execute(sql_submits)

        #print "2"
        sql_notes = "INSERT INTO [notes] ([taskId], [version], [user], [describe], [time]) VALUES ("+taskId+","+version+","+"'"+user+"',"+"'Submit Task In The Maya',"+"datetime('now','localtime'))"
        #print sql_notes
        cursor.execute(sql_notes)

        #print "3"
        sql_tasks = "UPDATE [tasks] SET [version] = "+version+", [projectf] = '"+projectf+"', [previewf] = '"+previewf+"', [hasAD] = "+hasAD+" WHERE [id] = "+taskId
        #print sql_tasks
        cursor.execute(sql_tasks)

        #print "4"
        conn.commit()
        conn.close()

    def createTask(self, data = {}, db = None):
        conn = None
        if db == None:
            conn = sqlite3.connect( self.db )
        else:
            conn = sqlite3.connect( db )

        cursor = conn.cursor()

        id = data["taskId"]
        Project = data["Project"]
        task_code = data["task_code"]
        name  = data["name"]
        chinese = data["chinese"]
        big = data["big"]
        act = data["act"]
        seq = data["seq"]
        classify = data["classify"]
        group = data["group"]
        assigned = data["assigned"]
        name_en = data["name_en"]

        sql_tasks = "INSERT INTO [tasks] ([id], [project], [code], [name], [name_zn], [big], [act], [scene], [classify], [group], [user], [name_en] ) VALUES ("+id+","+"'"+Project+"',"+"'"+task_code+"',"+"'"+name+"',"+"'"+chinese+"',"+"'"+big+"',"+"'"+act+"',"+"'"+seq+"',"+"'"+classify+"',"+"'"+group+"',"+"'"+assigned+"',"+"'"+name_en+"')"
        print sql_tasks
        cursor.execute(sql_tasks)  

        #print "2"
        sql_notes = "INSERT INTO [notes] ([taskId], [version], [user], [describe], [time]) VALUES ("+id+","+version+","+"'"+user+"',"+"'Create Task In The Maya',"+"datetime('now','localtime'))"
        print sql_notes
        cursor.execute(sql_notes)

        #print "4"
        conn.commit()
        conn.close()
