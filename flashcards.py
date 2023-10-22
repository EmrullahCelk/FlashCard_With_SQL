import sys
import psycopg2
import hashlib

from sympy import false
from loginscreen import Ui_MainWindow
from mainscreen import Main_Ui_Class
from gamescreen import Game_Ui_Class
from statscreen import Ui_Stat
from showscreen import Ui_Show
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox



class Login(QMainWindow):
    def __init__(self):
        super(Login,self).__init__()
        self.login_screen = Ui_MainWindow()
        self.login_screen.setupUi(self)
        #self.convert_data()
        self.login_screen.login_btn_signup.clicked.connect(self.SignUp)
        self.login_screen.login_btn_login.clicked.connect(self.Login)
       ########################
        self.s = 0
        self.user=""
        

    def go_main(self):
        main_s = Main(self.user)
        widget.addWidget(main_s)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def Login(self):
        self.user = self.login_screen.login_edt_username.text()
        self.password = self.login_screen.login_edt_password.text()
        self.hashpassword = hashlib.md5()
        self.hashpassword.update(self.password.encode("utf-8"))
        self.hashresult = self.hashpassword.hexdigest()
        
        user_l=[]
        if self.user == "" or self.password == "":
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/icons/flash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.messagebox=QtWidgets.QMessageBox()
            self.messagebox.critical(self,'WARNING','Please Enter Username and Password')
            self.messagebox.setWindowIcon(icon)
        else:
            conn1 = psycopg2.connect("dbname=flashcard user=postgres password=4408")
            cur1 = conn1.cursor()
            cur2 = conn1.cursor()
            cur1.execute("select username from users")
            cur2.execute(f"select password from users where username = '{self.user}'")
            self.pass_db = cur2.fetchone() 
            self.usrlst = cur1.fetchall()
            
            if self.pass_db != None: # db de girilen kullanıcı yoksa none dönüyor
                for i in self.pass_db:
                    self.user_password = i
            cur1.close()
            conn1.commit()
            conn1.close()
            self.l_user = []
            for i in self.usrlst:
                for j in i:
                    self.l_user.append(j)
            if self.user in self.l_user and self.hashresult == self.user_password:
                self.go_main()
            elif self.user in self.l_user and self.hashresult != self.user_password: 
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(":/icons/flash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.messagebox=QtWidgets.QMessageBox()
                self.messagebox.critical(self,'WARNING','Invalid password')
                self.messagebox.setWindowIcon(icon)                       
            else:
               
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(":/icons/flash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.messagebox=QtWidgets.QMessageBox()
                self.messagebox.critical(self,'WARNING','Invalid User Name, Please Sign Up!!!')
                self.messagebox.setWindowIcon(icon)


    def SignUp(self):
        self.user = self.login_screen.login_edt_username.text()
        self.password = self.login_screen.login_edt_password.text()
        self.hashpassword = hashlib.md5()
        self.hashpassword.update(self.password.encode("utf-8"))
        self.hashresult = self.hashpassword.hexdigest()
        user_list=[]
        self.user = self.login_screen.login_edt_username.text()
        self.password = self.login_screen.login_edt_password.text()
       
        if self.user == "" or self.password == "":
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/icons/flash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.messagebox=QtWidgets.QMessageBox()
            self.messagebox.critical(self,'WARNING','Please Enter Username and Password')
            self.messagebox.setWindowIcon(icon)
        else:
            conn1 = psycopg2.connect("dbname=flashcard user=postgres password=4408")
            cur1 = conn1.cursor()
            cur2 = conn1.cursor()
            cur1.execute("select username from users")
            cur2.execute(f"select password from users where username = '{self.user}'")
            self.pass_db = cur2.fetchone() 
            self.usrlst = cur1.fetchall()
            
            if self.pass_db != None: # db de girilen kullanıcı yoksa none dönüyor
                for i in self.pass_db:
                    self.user_password = i
            cur1.close()
            conn1.commit()
            conn1.close()
            self.l_user = []
            for i in self.usrlst:
                for j in i:
                    self.l_user.append(j)
                    
            if self.user in self.l_user :
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(":/icons/flash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.messagebox=QtWidgets.QMessageBox()
                self.messagebox.critical(self,'WARNING','Username is already exist')
                self.messagebox.setWindowIcon(icon) 
                # self.go_main()
                
            else:
                conn1 = psycopg2.connect("dbname=flashcard user=postgres password=4408")
                cur1 = conn1.cursor()
                cur2 = conn1.cursor()
                cur1.execute(f"insert into users (username,password,level) values ('{self.user}','{self.hashresult}', 1)")
                cur1.execute(f"ALTER TABLE words ADD COLUMN {self.user} character varying(40) default 0")
                cur1.close()
                cur2.close()
                conn1.commit()
                conn1.close()
                self.go_main() 

        
class Main(QMainWindow):
    def __init__(self,user):
        super(Main,self).__init__()
        self.user = user
        self.main_screen = Main_Ui_Class()
        self.main_screen.setupUi(self)
        self.main_screen.main_btn_play.clicked.connect(self.go_game)
        self.main_screen.main_btn_quit.clicked.connect(self.Quit)
        self.main_screen.main_btn_stat.clicked.connect(self.go_statistic)
        self.main_screen.main_btn_show.clicked.connect(self.go_show)
        self.main_screen.main_txt_player.setText("Player : "+self.user)

        conn1 = psycopg2.connect("dbname=flashcard user=postgres password=4408")
        cur1 = conn1.cursor()
        cur1.execute("select level from words order by level desc limit 1")
        max_level=cur1.fetchone()   
        # conn1.commit()
        
        cur1.execute(f"select level from users where username = '{self.user}'")
        user_level_db = cur1.fetchone()
        cur1.close()
        conn1.commit()
        conn1.close()
        self.user_level = user_level_db[0]
        self.total_level = max_level[0]
        
        # self.main_screen.comboBox_2
        
        
    # CUSTOM LEVEL EKLENDİ
        conn1 = psycopg2.connect("dbname=flashcard user=postgres password=4408")
        cur1 = conn1.cursor()
        cur1.execute(f"select {self.user} from words where {self.user}='1' limit 1")
        cust_db = cur1.fetchone()
        conn1.commit()
        cur1.close()
        conn1.close()
        self.main_screen.comboBox.addItem("")
        self.main_screen.comboBox.setItemText(0,f"select")
        
        self.choose = "select"
        if cust_db != None: # custom level varsa/yoksa
            self.isCustom = cust_db[0]
                
        for i in range(self.user_level): # level seçimi
            self.main_screen.comboBox.addItem("")
            self.main_screen.comboBox.setItemText(i+1,f"{i+1}")
            
        if cust_db != None:
            self.main_screen.comboBox.addItem("")
            self.main_screen.comboBox.setItemText(self.user_level+1, "Custom")
        
        self.main_screen.progressBar.setMaximum(self.total_level)
        self.main_screen.progressBar.setProperty("value", self.user_level)
        # self.main_screen.main_txt_level.setText(f"4/{self.total_level}")
        self.main_screen.main_txt_level.setText(f"{self.user_level}/{self.total_level}")
        

    def go_statistic(self):
        stat_s = Statistic(self.user)
        widget.addWidget(stat_s)
        widget.setCurrentIndex(widget.currentIndex() + 1)
          
    def go_show(self):
        show_s = Show(self.user)
        widget.addWidget(show_s)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def go_game(self):
        self.choose = str(self.main_screen.comboBox.currentText())
        self.lang = str(self.main_screen.comboBox_2.currentText())
        game_s = Game(self.user,self.choose,self.lang)
        widget.addWidget(game_s)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def Quit(self):
        sys.exit(app.exec())













#------------------------------------------------------------------------

















class Statistic(QMainWindow):
    def __init__(self, user):
        super(Statistic,self).__init__()
        self.user = user
        self.stat_screen = Ui_Stat()
        self.stat_screen.setupUi(self)
        self.stat_screen.pushButton.clicked.connect(self.go_main)
        
        conn1 = psycopg2.connect("dbname=flashcard user=postgres password=4408")
        cur1 = conn1.cursor()
        cur1.execute(f"select user_id from users where username = '{self.user}'")
        u_id = cur1.fetchone()
        self.user_id = u_id[0]
        cur1.execute("select count(*) from users")
        n_users = cur1.fetchone()
        self.num_of_user = n_users[0]
        cur1.execute(f"select level from users where username = '{self.user}'")
        l_users = cur1.fetchone() 
        self.level_user = l_users[0]      
        
        self.stat_screen.stat_txt_userlevel.setText(str(self.level_user))
        self.stat_screen.stat_txt_numofuser.setText(str(self.num_of_user))
        self.stat_screen.stat_txt_username.setText(str(self.user))
       
        cur1.execute(f"select level, success_per from success where user_id = (select user_id from users where username = '{self.user}')")
        self.db_success=cur1.fetchall()
        
        # if db_suc != None:
        #     self.db_success = db_suc
        
        cur1.execute("select username, level from users order by level desc")
        self.h_level = cur1.fetchall()
        
        cur1.execute(f"select user_id, level, success_per from success ")
        self.success_data = cur1.fetchall()
        
        # cur1.close()
        # conn1.commit()
        # conn1.close()
        
        self.personal_success()
        self.level_rank()
        self.success_table()
        # self.stat_screen.stat_txt_levelrank.setText(str(self.user_rank))
        # self.stat_screen.stat_txt_levelrank.setHidden(True)
        # self.stat_screen.stat_txt_successrank.setHidden(True)

    def success_table(self):
        
        self.stat_screen.stat_table_suc.setRowCount(6)
        self.stat_screen.stat_table_suc.setColumnCount(3)
        self.stat_screen.stat_table_suc.setColumnWidth(0,5)
        self.stat_screen.stat_table_suc.setColumnWidth(1,136)
        self.stat_screen.stat_table_suc.setColumnWidth(2,76)
        self.stat_screen.stat_table_suc.verticalHeader().setHidden(True)
        self.stat_screen.stat_table_suc.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.stat_screen.stat_table_suc.setHorizontalHeaderLabels(("","Username","Success(%)"))
        
        
        if len(self.success_data) != 0:
            r = self.success_data
            b = float(r[0][2])
            lis=[]
            for i in self.success_data:
                lis.append(i[0])
            a=set(lis)
            b=list(a)
            y=0
            t=0
            # for i in range(len(self.success_data)):
            dic_s = {}
            
            for j in b:
                conn1 = psycopg2.connect("dbname=flashcard user=postgres password=4408")
                cur1 = conn1.cursor()
                cur1.execute(f"select username from users where user_id ={j} ")
                us_name=cur1.fetchone()
                for k in range(len(self.success_data)):
                    p = self.success_data[k][0]
                    if j == self.success_data[k][0]:
                        t+=1
                        y += float(self.success_data[k][2])
                        dic_s.update({us_name[0] : round((y/t),2)})
                y=0
                t=0
            # print(dic_s)    
            dic_sort=dict(sorted(dic_s.items(), key=lambda item: item[1],reverse=True))
            # print(a)
            i=0
            for k, l in dic_sort.items():
                if i < 5:
                    for j in range(3):
                        if j == 0 :
                            self.stat_screen.stat_table_suc.setItem(i,j,QTableWidgetItem(str(i+1)))
                        elif j== 1:
                            self.stat_screen.stat_table_suc.setItem(i,j,QTableWidgetItem(str(k)))
                        else:
                            self.stat_screen.stat_table_suc.setItem(i,j,QTableWidgetItem(str(l)))
                    if k == self.user: # kullanıcın arka planın boya
                        for k in range(3):
                            self.stat_screen.stat_table_suc.item(i,k).setBackground(QtGui.QColor(205,255,0))
                i+=1
            m=0
            for k, l in dic_sort.items():
                m += 1
                if k == self.user:
                    self.user_success_rank = m
            
            # self.stat_screen.stat_txt_successrank.setText(str(self.user_success_rank))
            # user rankı
            if self.level_user !=1: # hiçbir level bitmediyse hata almasın
                if self.user_success_rank > 5:  
                    self.stat_screen.stat_table_suc.setItem(5,0,QTableWidgetItem(str(self.user_success_rank)))
                    self.stat_screen.stat_table_suc.setItem(5,1,QTableWidgetItem(self.user))
                    self.stat_screen.stat_table_suc.setItem(5,2,QTableWidgetItem(str(self.totalsuccess)))
                    for i in range(3): # kullanıcın arka planın boya
                        self.stat_screen.stat_table_suc.item(5,i).setBackground(QtGui.QColor(205,255,0))

    def level_rank(self):
        self.stat_screen.stat_table_highlevel.setRowCount(6)
        self.stat_screen.stat_table_highlevel.setColumnCount(3)
        self.stat_screen.stat_table_highlevel.setColumnWidth(0,5)
        self.stat_screen.stat_table_highlevel.setColumnWidth(1,145)
        self.stat_screen.stat_table_highlevel.setColumnWidth(2,66)
        self.stat_screen.stat_table_highlevel.verticalHeader().setHidden(True)
        self.stat_screen.stat_table_highlevel.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.stat_screen.stat_table_highlevel.setHorizontalHeaderLabels((" ","Username","Level"))
        
        if len(self.h_level) != 0:
            for i in range(len(self.h_level)):
                if self.h_level[i][0] == self.user:
                    self.user_rank = i+1
            
            if self.user_rank>5:
               
                self.stat_screen.stat_table_highlevel.setItem(5,0,QTableWidgetItem(str(self.user_rank)))
                self.stat_screen.stat_table_highlevel.setItem(5,1,QTableWidgetItem(str(self.user)))
                self.stat_screen.stat_table_highlevel.setItem(5,2,QTableWidgetItem(str(self.level_user)))
                for i in range(3): # kullanıcın arka planın boya
                    self.stat_screen.stat_table_highlevel.item(5,i).setBackground(QtGui.QColor(205,255,0))
                    
            for i in range (len(self.h_level)):
                for j in range(3):
                    if j == 0: # satır numarası için
                        self.stat_screen.stat_table_highlevel.setItem(i,0,QTableWidgetItem(str(i+1)))
                    else:    
                        self.stat_screen.stat_table_highlevel.setItem(i,j,QTableWidgetItem(str(self.h_level[i][j-1])))
                        
                if self.h_level[i][0] == self.user : # kullanıcın arka planın boya
                    for k in range(3):
                        self.stat_screen.stat_table_highlevel.item(i,k).setBackground(QtGui.QColor(205,255,0))
                if i == 4:
                    break
    def personal_success(self):
        
        self.stat_screen.stat_table_pers.setRowCount(len(self.db_success))
        self.stat_screen.stat_table_pers.setColumnCount(3)
        self.stat_screen.stat_table_pers.setColumnWidth(0,5)
        self.stat_screen.stat_table_pers.setColumnWidth(1,100)
        self.stat_screen.stat_table_pers.setColumnWidth(2,110)
        self.stat_screen.stat_table_pers.verticalHeader().setHidden(True)
        # self.stat_screen.stat_table_pers.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.stat_screen.stat_table_pers.setHorizontalHeaderLabels(("","Level","Success(%)"))
        
        
        # self.stat_screen.stat_table_pers.setRowCount(len(self.db_success))
        # self.stat_screen.stat_table_pers.setColumnCount(2)
        
        # self.stat_screen.stat_table_pers.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # listeyi ortalaadık
        
        

        x=0
        if len(self.db_success) != 0:
            for i in range (len(self.db_success)):
                x +=  self.db_success[i][1]
                for j in range(3):
                    if j == 0:
                        self.stat_screen.stat_table_pers.setItem(i,0,QTableWidgetItem(str(i+1)))
                    else:
                        # a = self.db_success[i][j]
                        self.stat_screen.stat_table_pers.setItem(i,j,QTableWidgetItem(str(self.db_success[i][j-1])))
                
            self.totalsuccess = x / len(self.db_success)
            self.stat_screen.stat_txt_total.setText(str(round(self.totalsuccess, 2)))

    def go_main(self):
        main_s = Main(self.user)
        widget.addWidget(main_s)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        























class Show(QMainWindow):
    def __init__(self, user):
        super(Show,self).__init__()
        self.user = user
        self.show_screen = Ui_Show()
        self.show_screen.setupUi(self)
        self.show_screen.show_btn_main.clicked.connect(self.go_main)
        self.show_screen.show_btn_add.clicked.connect(self.add_db)
        self.show_screen.show_btn_show.clicked.connect(self.show_db)
        
        conn1 = psycopg2.connect("dbname=flashcard user=postgres password=4408")
        cur1 = conn1.cursor()
        cur1.execute("select level from words order by level desc limit 1")
        max_level=cur1.fetchone()  
        cur1.execute(f"select user_id from users where username = '{self.user}'")
        u_id = cur1.fetchone()
        self.user_id = u_id[0]
        cur1.close()
        conn1.commit()
        conn1.close()
        
        self.total_level = max_level[0]
        
        for i in range(self.total_level): # level seçimi
            self.show_screen.show_combo_level.addItem("")
            self.show_screen.show_combo_level.setItemText(i,f"{i+1}")
            
        self.show_screen.show_combo_level.addItem("")
        self.show_screen.show_combo_level.setItemText(self.total_level, "Custom")
            
    def show_db(self):
        self.s_level = str(self.show_screen.show_combo_level.currentText())
        conn = psycopg2.connect("dbname=flashcard user=postgres password=4408")
        cur=conn.cursor()
        if self.s_level == "Custom":
            cur.execute(f"select count(*) from words where {self.user} = '1' ")
        else:
            cur.execute(f"select count(*) from words where level = {int(self.s_level)} ")
        c_word=cur.fetchone()
        
        self.len_list = c_word[0]
        
        x=c_word[0]
        
        self.show_screen.tableWidget.setRowCount(self.len_list)
        self.show_screen.tableWidget.setColumnCount(2)
        self.show_screen.tableWidget.setHorizontalHeaderLabels(("Dutch","English"))
        self.show_screen.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # listeyi ortalaadık

        
        if self.s_level == "Custom":
            cur.execute(f"select dutch,english from words where {self.user} = '1' ")
        else:
            cur.execute(f"select dutch,english from words where level = {int(self.s_level)} or user_id = {self.user_id} ")
        
        db_all=cur.fetchall()  
        
        for i in range (self.len_list):
            for j in range(2):
                a = db_all[i][j]
                self.show_screen.tableWidget.setItem(i,j,QTableWidgetItem(str(db_all[i][j])))
                
        cur.close()
        conn.commit()
        conn.close()

        
        
    def add_db(self):
        
        self.new_d = self.show_screen.show_edt_dutch.text()
        self.new_eng = self.show_screen.show_edt_english.text()   
        self.s_level = str(self.show_screen.show_combo_level.currentText())
        
        if self.new_d == "" or self.new_eng == "":
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/icons/flash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.messagebox=QtWidgets.QMessageBox()
            self.messagebox.critical(self,'WARNING','Please enter the words')
            self.messagebox.setWindowIcon(icon)
        else:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/icons/flash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.messagebox=QtWidgets.QMessageBox()
            self.messagebox.information(self,"INFORMATION","    Word Added    ")
            self.messagebox.setWindowIcon(icon)
            conn1 = psycopg2.connect("dbname=flashcard user=postgres password=4408")
            cur1 = conn1.cursor()
            cur1.execute(f"select user_id from users where username = '{self.user}'")
            u_id = cur1.fetchone()
            self.user_id = u_id[0]
            if  self.s_level == "Custom":
                cur1.execute(f"insert into words (user_id,dutch,english,level,{self.user}) values ({int(self.user_id)} ,'{self.new_d}','{self.new_eng}',0,1)") 
            
            else:
                cur1.execute(f"insert into words (user_id,dutch,english,level) values ({int(self.user_id)} ,'{self.new_d}','{self.new_eng}',{int(self.s_level)})") 
            
            cur1.close()
            conn1.commit()
            conn1.close()
            self.show_screen.show_edt_dutch.setText("")
            self.new_eng = self.show_screen.show_edt_english.setText("")
    def go_main(self):
        main_s = Main(self.user)
        widget.addWidget(main_s)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # QMessageBox.information(self, "Kayıt Hakkında", "Kayıt Başarılı !")
    #             else:
    #                 QMessageBox.warning(self,"Kayıt Tekrarı !","Girdiğiniz eposta başka bir kullanıcı tarafından kullanılmaktadır.")
    #         else:
    #             QMessageBox.warning(self,"Hata !","Girişleri Kontrol ederek yeniden deneyiniz !")
    # def Calistir(self):
    #         ad = self.pencere.txtAdi.text()
    #         soyadi = self.pencere.txtSoyadi.text()
    #         unv = self.pencere.cmbUnvan.currentIndex()
    #         uzm = self.pencere.cmbUzmanlik.currentIndex()
    #         ID = self.pencere.lblDokID.text()
    #         if self.veriTabani.doktorEkleGuncelle(ad,soyadi,unv,uzm,ID):
    #             QMessageBox.information(self,"Bilgi","Kayıt Başarılı",QMessageBox.Ok,QMessageBox.Ok)
    #             self.doldurma()

















#       G   A   M   E















class Game(QMainWindow):
    def __init__(self,user,choose,lang):
        super(Game,self).__init__()
        self.user = user
        self.choose = choose
        self.lang = lang
        self.game_screen = Game_Ui_Class()
        self.game_screen.setupUi(self)
        
        conn = psycopg2.connect("dbname=flashcard user=postgres password=4408")
        cur = conn.cursor()
        cur.execute(f"select user_id from users where username = '{self.user}'")
        u_id = cur.fetchone()
        self.user_id = u_id[0]
        if self.choose =="select":
            self.level_find()
            cur.execute(f"select count(*) from words where level = '{self.user_level}' and {self.user} = '0' and user_id is null  or level = {self.user_level} and user_id = {self.user_id}")
            conn.commit()
        elif self.choose =="Custom":    
            cur.execute(f"SELECT COUNT(*) FROM words WHERE {self.user} = '1'")
        else:
            cur.execute(f"select count(*) from words where level = {int(self.choose)} and {self.user} = '0' and user_id is null  or level = {int(self.choose)} and user_id = {self.user_id} ")
        qw = cur.fetchone()
        
     
        
        for i in qw:
            self.len_list = i
        
        if self.choose == "Custom":
            self.game_screen.game_btn_custom.setEnabled(False)
        
        self.game_screen.game_btn_back.clicked.connect(self.go_main)
        self.game_screen.game_btn_custom.clicked.connect(self.customLevel) #custom level için
        self.wordCounter=0
        self.totalCounter=self.len_list
        self.levelCounter=0
        
        self.game_screen.game_progres_bar.setProperty("value", 0)
        self.game_screen.game_progres_bar.setMaximum(self.len_list)
        self.game_screen.game_txt_skor.setText(f"{self.wordCounter}/{self.len_list}")
    
        self.s = 0
        self.custom_click = 0
        self.false_click = 0
        #self.s = (self.level-1)*20
        self.word = True
        
        self.game_screen.game_btn_yes.setEnabled(False)
        self.game_screen.game_btn_no.setEnabled(False)
        x=1
        if self.lang == "Dutch / English":
            self.DutchWord()
        else:
            self.EngWord()
        
        self.wrong_list = {}
        self.game_screen.game_btn_yes.clicked.connect(self.PressTrue)
        self.game_screen.game_btn_no.clicked.connect(self.PressFalse)
        
        
        
        self.timer_select()
####################### TIMER #####################################
         
     
        self.count = self.timer_begin_second
        self.start = True
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)
        self.game_screen.game_time_txt.setText(str(self.count))

    def timer_select(self):
        self.spin_timer = self.game_screen.game_timer.value()
        self.timer_begin_second = self.spin_timer 
        
    
    def level_find(self):
        conn = psycopg2.connect("dbname=flashcard user=postgres password=4408")
        cur = conn.cursor()
        cur.execute(f"select level from users where username = '{self.user}'")
        user_level_db = cur.fetchone()
        for i in user_level_db:
            self.user_level = i

    def showTime(self):
        if self.start==True:
            self.count -= 1
            if self.count < 0:
                self.start = False
                self.count = self.timer_begin_second
  
        if self.start==True:
            self.game_screen.game_time_txt.setText(str(self.count)) # label a sayac ı yaz
    
        if str(self.count) == "0":  # sayac 0 olursa english word yazdır
           
            self.game_screen.game_btn_yes.setEnabled(True)
            self.game_screen.game_btn_no.setEnabled(True)
            if self.lang == "Dutch / English":          
                self.game_screen.game_txt_language.setText("English")
            else:
                self.game_screen.game_txt_language.setText("Dutch")
            
            
            if self.levelCounter >= self.totalCounter:
                if len(self.wrong_list) != 0:
                    if self.lang == "Dutch / English":
                        self.game_screen.game_txt_word.setText(f"{self.eng_y}")
                    else:
                        self.game_screen.game_txt_word.setText(f"{self.dutch_x}")
            else:
                if self.lang == "Dutch / English":
                    self.EngWord()
                else:
                    self.DutchWord()   
                
                
            self.game_screen.verticalFrame.setStyleSheet("#verticalFrame{\n"
    "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(168, 255, 120, 255), stop:1 rgba(120, 255, 214, 255));\n"
    "\n"
    "border-radius: 25px;\n"
    "}") 
####################### TIMER ###########################################
    def customLevel(self):
        conn = psycopg2.connect("dbname=flashcard user=postgres password=4408")
        cur = conn.cursor()
        cur.execute(f"update words set {self.user} = 1 where dutch = '{self.word_list_dutch[self.s]}' ") 
        cur.execute("select * from words order by id")
        cur.close()
        conn.commit()
        conn.close()  
        self.custom_click +=1
        #TODO istatistik tutulurken customa basma sayısı çıkarılmalı
        self.PressTrue()
        
    def PressTrue(self):
        if self.lang == "Dutch / English":          
            self.game_screen.game_txt_language.setText("Dutch")
        else:
            self.game_screen.game_txt_language.setText("English")
    
        self.game_screen.game_btn_yes.setEnabled(False)
        self.game_screen.game_btn_no.setEnabled(False)
        self.game_screen.verticalFrame.setStyleSheet("#verticalFrame{\n"
    "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.423, y2:0.570652, stop:0 rgba(0, 255, 255, 255), stop:1 rgba(170, 255, 255, 255));\n"
"\n"
    "border-radius: 25px;\n"
    "}")
        self.timer_select()
        self.count = self.timer_begin_second+1
        self.start = True
        self.showTime()
        
        self.s += 1
        self.levelCounter+=1
        self.game_screen.game_progres_bar.setMaximum(self.len_list)
        self.game_screen.game_txt_skor.setText(f"{self.wordCounter + 1}/{self.len_list}")
        self.wordCounter += 1
        self.game_screen.game_progres_bar.setProperty("value", f"{self.wordCounter}")
        
        if self.wordCounter == self.totalCounter:
            if self.choose == "select":
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(":/icons/flash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.messagebox=QtWidgets.QMessageBox()
                result=self.messagebox.question(self,'WARNINIG','Do you want to play next level ?',
                                            self.messagebox.Yes|self.messagebox.No)
                
                if result==QMessageBox.Yes:
                    # self.level+=1
                    # self.s = (self.level-1)*20
                    self.level_up()
                    self.statistic_calculate()
                    
                    self.s = 0
                    self.wordCounter -= 1
                    if self.lang == "Dutch / English":
                        self.DutchWord()
                    else:
                        self.EngWord()
                    
                    # self.s -= 1
                    self.levelCounter=-1
                    if self.wordCounter == self.totalCounter:
                        self.wordCounter=0
                        self.game_screen.game_progres_bar.setMaximum(self.len_list)
                        self.game_screen.game_txt_skor.setText(f"{self.wordCounter}/{self.len_list}")
                        self.game_screen.game_progres_bar.setProperty("value", 0)
                        self.wordCounter=-1
                    self.wrong_list.clear()
                    self.word_list_dutch.clear()
                    self.word_list_eng.clear()
                    # self.level_up()
                    self.s = -1
                    self.PressTrue()
    
                if result == QMessageBox.No:
                    self.level_up()
                    self.statistic_calculate()
                    
                    main_s = Main(self.user)
                    widget.addWidget(main_s)
                    widget.setCurrentIndex(widget.currentIndex() + 1)
                    self.go_main()
                # DB YE KAYDET

            else:
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(":/icons/flash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.messagebox=QtWidgets.QMessageBox()
                self.messagebox.information(self,"INFORMATION","    Level Completed. Go to Main Menu    ")
                self.messagebox.setWindowIcon(icon)
                
                self.go_main()    
        
        if self.levelCounter >= self.totalCounter:
            
            if len(self.wrong_list) == 0:             
                self.levelCounter = 1
                self.totalCounter = self.len_list
            else:
                self.s -= 1
      
                if self.levelCounter > self.totalCounter:
                    self.wrong_list.pop(self.dutch_x)
                 
                for x,y in self.wrong_list.items():
                    self.dutch_x=x
                    self.eng_y=y
                    
                    if self.lang == "Dutch / English":
                        self.game_screen.game_txt_word.setText(f"{self.dutch_x}")
                    else:
                        self.game_screen.game_txt_word.setText(f"{self.eng_y}")
                    
                    break
            print(self.wrong_list)      
        else:        
            if self.lang == "Dutch / English":
                self.DutchWord()
            else:
                self.EngWord()
            
    def statistic_calculate(self):
        
        conn = psycopg2.connect("dbname=flashcard user=postgres password=4408")
        cur = conn.cursor()
        self.success_per = round((self.list_length / (self.list_length + self.false_click))*100,2)
        cur.execute(f"insert into success (user_id,level,success_per) values ({self.user_id},{self.user_level},{self.success_per})") 
        cur.execute("select * from words order by id")
        cur.close()
        conn.commit()
        conn.close()
        self.false_click = 0     
        self.wordCounter = 0
        self.totalCounter = self.len_list  
            
    def level_up(self):
        if self.choose == "select": 
            conn = psycopg2.connect("dbname=flashcard user=postgres password=4408")
            cur = conn.cursor()
            cur.execute(f"update users set level={self.user_level+1} where username ='{self.user}'") 
            conn.commit()
            cur.close()
            conn.close()
        
    def PressFalse(self):
        if self.lang == "Dutch / English":
            self.game_screen.game_txt_language.setText("Dutch")
        else:
            self.game_screen.game_txt_language.setText("English")   
        # self.DutchWord()
        
        self.false_click +=1
        self.game_screen.game_btn_yes.setEnabled(False)
        self.game_screen.game_btn_no.setEnabled(False)
        self.game_screen.verticalFrame.setStyleSheet("#verticalFrame{\n"
    "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.423, y2:0.570652, stop:0 rgba(0, 255, 255, 255), stop:1 rgba(170, 255, 255, 255));\n"
"\n"
    "border-radius: 25px;\n"
    "}")
        self.timer_select()
        self.count = self.timer_begin_second+1
        self.start = True
        self.showTime()
        
        
        self.s += 1
        self.levelCounter+=1
        
        if self.levelCounter >= self.totalCounter:
            
            pass

        else:
            self.s -= 1 ######################################
            self.wrong_list.update({self.word_list_dutch[self.s] : self.word_list_eng[self.s] })
            self.s += 1 ###################################
           
        if self.levelCounter >= self.totalCounter:
            if len(self.wrong_list) == 0:            
                self.levelCounter = 1
                self.totalCounter = self.len_list
            else:
                self.s -= 1
                self.wrong_list.pop(self.dutch_x)
                self.wrong_list.update({self.dutch_x : self.eng_y})
                for x,y in self.wrong_list.items():
                    self.dutch_x=x
                    self.eng_y=y
                    if self.lang == "Dutch / English":
                        self.game_screen.game_txt_word.setText(f"{self.dutch_x}")
                    else:
                        self.game_screen.game_txt_word.setText(f"{self.eng_y}") 
                        
                    break
                
                self.wrong_list.pop(self.dutch_x)
            self.wrong_list.update({self.dutch_x : self.eng_y})
            print(self.wrong_list)          
        else:
            if self.lang == "Dutch / English":
                self.DutchWord()
            else:
                self.EngWord()
                
    def go_main(self):
        main_s = Main(self.user)
        widget.addWidget(main_s)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
    def DutchWord(self):
        
            conn = psycopg2.connect("dbname=flashcard user=postgres password=4408")
            cur = conn.cursor()
            
            self.level_find()
         
            if self.choose == "select":
                # cur.execute(f"select dutch from words where level = {self.user_level} and {self.user} = '0' or user_id = '{self.user_id}' order by id")
                cur.execute(f"select dutch from words where level = {self.user_level} and {self.user} = '0' and user_id is null  or level = {self.user_level} and user_id = {self.user_id} order by id")
            elif self.choose == "Custom":
                cur.execute(f"select dutch from words where {self.user} = '1' ")
            else:
                cur.execute(f"select dutch from words where level = {int(self.choose)} and {self.user} = '0' or level = {int(self.choose)} and user_id = {self.user_id} order by id")   
                
            word_l = cur.fetchall()
            self.word_list_dutch=[]
            for i in word_l:
                for j in i:
                    self.word_list_dutch.append(j)
            self.list_length = len (self.word_list_dutch) 
            cur.close()
            conn.close()
            aa = self.word_list_dutch[self.s]
            if self.s < self.list_length:
                self.game_screen.game_txt_word.setText(f"{self.word_list_dutch[self.s]}") 
            if self.s == self.list_length:
                self.s = 0
                
            
    def EngWord(self):
        
            conn = psycopg2.connect("dbname=flashcard user=postgres password=4408")
            cur = conn.cursor()
            self.level_find()
            if self.choose == "select":
                cur.execute(f"select english from words where level = {self.user_level} and {self.user} = '0' and user_id is null  or level = {self.user_level} and user_id = {self.user_id} order by id")
            elif self.choose == "Custom":
                cur.execute(f"select english from words where {self.user} = '1'")      
            else:
                cur.execute(f"select english from words where level = {int(self.choose)} and {self.user} = '0' or level = {int(self.choose)} and user_id = {self.user_id} order by id")
                
            word_l = cur.fetchall()
            conn.commit()
            cur.close()
            conn.close()
        
            self.word_list_eng=[]
            for i in word_l:
                for j in i:
                    self.word_list_eng.append(j)
            self.list_length = len (self.word_list_eng)
            bb = self.word_list_eng[self.s]
            if self.s < self.list_length:
                self.game_screen.game_txt_word.setText(f"{self.word_list_eng[self.s]}")
                
            if self.s == self.list_length:
                self.s = 0
    
app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setWindowTitle("FLASHCARDS")
icon = QtGui.QIcon()
icon.addPixmap(QtGui.QPixmap(":/icons/flash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
widget.setWindowIcon(icon)
widget.setFixedHeight(600)
widget.setFixedWidth(900)
widget.show()
sys.exit(app.exec())