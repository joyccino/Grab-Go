import os
import cx_Oracle
import cv2
from flask import Flask, Response, request, render_template, redirect, flash, session
# from forms import RegisterForm, LoginForm
import numpy as np
import time
import face_recognition
import ftplib 
import os
import os.path
import shutil
#file transfer
from ftplib import FTP
from models import db, Fcuser, Orders
from flask_bootstrap import Bootstrap

os.putenv('NLS_LANG', '.UTF8')

#연결에 필요한 기본 정보 (유저, 비밀번호, 데이터베이스 서버 주소)
connection = cx_Oracle.connect("Ai_team1","1234","192.168.0.12:1521/orcl")
connection.autocommit = True

app = Flask(__name__)
Bootstrap(app)


@app.route('/index', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/test', methods=['GET'])
def test():
   cursor = connection.cursor()
   cursor.execute("""
   select customer_name
   from customers where customer_id = 5
   """)
   temp0 = cursor.fetchone()
   name = str(temp0)[1:-2]
   return render_template("test.html", name = name)

@app.route('/mainreceipt', methods=['GET','POST'])
def mainreceipt():
    if request.method == 'GET':
        cursor = connection.cursor()
        print('is custumer still in session?',session)
        ses = session['customer']
    #if it is, select customer's id from db
        if ses != None:
            q = 'select customer_name from customers where email = '+"'"+ses+"'"
            cursor.execute(q)
            a = cursor.fetchone()
            name = str(a)[1:-2]

            q2 = 'select customer_id from customers where email = '+"'"+ses+"'"
            cursor.execute(q2)
            c = cursor.fetchone()
            customer_id = str(c)[1:-2]

            q3 = 'select order_date from orders where customer_id = '+"'"+customer_id+"'"
            cursor.execute(q3)
            dates = cursor.fetchall()
            print('original dates: ',dates)

            updates = []
            for i in range(len(dates)):
                yyyy = str(dates[i])[19:-21]
                print("printing yearssss: ",yyyy)
                mm = str (dates[i])[24:27]
                print("printing monthssss: ",mm)
                dd = str (dates[i])[28:-13]
                print("printing ddssss: ",dd)
                hh = str (dates[i])[32:-9]
                print("printing hhsss: ",hh)
                mins = str (dates[i])[36: -5]
                print("printing mins: ",mins)
                updates.append(yyyy+"년"+mm+"월"+dd+"일"+hh+"시"+mins+"분")
                print('updates: ',updates)

            q4 = 'select order_id from orders where customer_id = '+"'"+customer_id+"'"
            cursor.execute(q4)
            od = cursor.fetchall()
            
            order_id = []
            for i in range(len(od)):
                oid = str(od[i])[1:-2]
                order_id.append(oid)
            print("new generated order_id: ",order_id)
            
                # print("get one sample: ",order_id[3]," and the length: ",len(order_id[3]))
            print("temp is: ",dates," and the type is ",type(dates)," and the length: ",len(dates))

            return render_template("mainreceipt.html", name = name, len = len(updates), dates = updates, order_id = order_id)
    else:
        order_id = request.form['order_id']
        # return order_id
        cursor = connection.cursor()
        # select product_id by order id
        query = 'select product_id from order_details where order_id = '+"'"+order_id+"'"
        cursor.execute(query)
        a = cursor.fetchone()
        product_id = str(a)[1:-2] 
        # select product_name by order_id
        query2 = 'select product_name from products where product_id = '+"'"+product_id+"'"
        cursor.execute(query2)
        b = cursor.fetchone()
        print(b)
        product_name = str(b)[2:-3]
        # select price by product_id
        query3 = 'select product_price from products where product_id = '+"'"+product_id+"'"
        cursor.execute(query3)
        c = cursor.fetchone()
        price = str(c)[1:-2]
        #get total price by order id
        query4 = 'select total_price from orders where order_id = '+"'"+order_id+"'"
        cursor.execute(query4)
        d = cursor.fetchone()
        tprice = str(d)[1:-2]

        query5 = 'select cart_stock from order_details where order_id = '+"'"+order_id+"'"
        cursor.execute(query5)
        prestock = cursor.fetchall()
        cart_stock = str(prestock)[2:-3]

        print('order_id is: ',order_id)
        print('product id is,',product_id)
        print('product name is: ',product_name)
        print('product_price is: ',price)
        print('total price is: ',tprice)
        print('cart stock is ',cart_stock)
        return render_template("receipt2.html", order_id = order_id, product_id = product_id, product_name = product_name, price = price, tprice = tprice, cart_stock = cart_stock)

@app.route('/maincart', methods=['GET'])
def maincart():
   #check if customer info is still in session
    cursor = connection.cursor()
    print('is custumer still in session?',session)
    ses = session['customer']
    print('ses type: ',type(ses))
    print('ses is :',ses)

   #if it is, select customer's id from db
    if ses != None:
           q = 'select customer_id from customers where email = '+"'"+ses+"'"
           print('******************')
           print(q)
           print('******************')
         #   query = str(q)
           cursor.execute(q)
           c = cursor.fetchone()
           customer_id = str(c)[1:-2]
           print("customer id is: ",customer_id)

           q2 = 'select customer_name from customers where customer_id = '+"'"+customer_id+"'"
           que2 = str(q2) 
           print('******************')
           print(type(q2))
           print('******************')
           cursor.execute(que2)
           temp0 = cursor.fetchone()
           customer_name = str(temp0)[1:-2]

           q3 = 'select cart_stock from carts where customer_id = '+"'"+customer_id+"'"
        #    print('q3 is: ',q3)
           cursor.execute(q3)
           temp1 = cursor.fetchone()
           print("**************************************************")
           print('temp1 is: ',temp1)
           if temp1 == None:
               return render_template("maincart.html", name = customer_name)
           else:
               cart_stock = str(temp1)[1:-2]
               print('cart stock is',cart_stock,' and the type',type(cart_stock))
               icart_stock = int(cart_stock)
               print("23569837598275983275983275983275983250")
               print("is icart converted correctly?: ",type(icart_stock)," :: ",icart_stock)

               query4 = 'select product_id from carts where customer_id = '+"'"+customer_id+"'"
               cursor.execute(query4)
               temp2 = cursor.fetchone()
               product_id = str(temp2)[1:-2]
               iproduct_id = float(product_id)

        #    #following lines are for total price
               query5 = 'select product_name from products where product_id = '+"'"+product_id+"'"
               cursor.execute(query5)
               temp3 = cursor.fetchone()
               product_name = str(temp3)[2:-3]
           

               query6 = 'select product_price from products where product_name = '+"'"+product_name+"'"
               cursor.execute(query6)
               temp4 = cursor.fetchone()
               product_price = str(temp4)[1:-2]
               iproduct_price = float(product_price)
           
               query7 = 'select cart_stock from carts where customer_id = '+"'"+customer_id+"'"
               cursor.execute(query7)
               temp5 = cursor.fetchone()
               cart_stock = str(temp5)[1:-2]
               icart_stock = float(cart_stock)

               
               total_price = icart_stock * iproduct_price
               print("XXXXXXXXXXXXXXXXXXXXXxxxxx")
               print("XXXXXXXXXXXXXXXXXXXXXxxxxx")
               print("XXXXXXXXXXXXXXXXXXXXXxxxxx")
               print("XXXXXXXXXXXXXXXXXXXXXxxxxx")
               print("XXXXXXXXXXXXXXXXXXXXXxxxxx")
               print("XXXXXXXXXXXXXXXXXXXXXxxxxx")
               print("XXXXXXXXXXXXXXXXXXXXXxxxxx")
               print("before calculation")
               print('total price is :',total_price," and the type:: ",type(total_price) )
               q7 = 'select login_session from customers where customer_id = '+"'"+customer_id+"'"
               #is the customer active now?
               cursor.execute(q7)
               a = cursor.fetchone()
               active = str(a)[2:-3]
               print(active)
               if active == 'True' :
                   return render_template("maincart.html", name = customer_name, cart_stock = cart_stock, product_id = product_id, total_price=total_price, product_price = iproduct_price, product_name = product_name)
               else:
                   return render_template("maincart.html", name = customer_name)

@app.route('/')
def hello():
    # username = session.get('email', None)
    return render_template('hello.html')

@app.route('/logout', methods=['GET'])
def logout():
       session.pop('customer',None)
       return redirect('/')

@app.route('/glogin', methods=['GET', 'POST'])
def glogin():
    """Login Form"""
    if request.method == 'GET':
        return render_template('glogin.html')
    else:
        email1 = request.form['email']
        pass1 = request.form['customer_pass']
        print("---------------------------------------------------------------------------------------------------------")
        print("input email: "+email1) # 들어오나 확인해볼 수 있다. 
        print("input customer_pass: "+pass1) # 들어오나 확인해볼 수 있다.

        print("---------------------------------------------------------------------------------------------------------")
        if email1 and pass1 is not None:
            cursor = connection.cursor()
            cursor.execute("select customer_pass from customers where email = :email",
                {"email": email1})
            opass = cursor.fetchone()
            print("opass: "+str(opass[0]))

            if opass[0] == pass1:
                flash( "Correct. Welcome, "+email1)
                customer = email1
                session['customer'] = customer
                print('initial input in session: ',session)
                return redirect('/home')

                # q = 'select customer_name from customers where email = '+"'"+email1+"'"
                # print('******************')
                # print(q)
                # print('******************')
                # #   query = str(q)
                # cursor.execute(q)
                # c = cursor.fetchone()
                # name = str(c)[1:-2]
                # print("customer id is: ",name)
                # #to check if customer is active
                # q2 = 'select login_session from customers where email ='+"'"+email1+"'"
                # cursor.execute(q2)
                # a = cursor.fetchone()
                # active = str(a)[2:-3]
                # print(active,' and the type of',active,' is :',type(active))
                # if active == 'True':
                #     # add to check when the customer has been arrived
                #     return redirect('/home',name = name, time = 'exist')
                # else:
                #     return render_template('/home',name = name)
                
            else:
                flash("Wrong. Try again")
                return redirect('/login')
@app.route('/home', methods=['GET'])
def home():
    e = session['customer']
    email1 = str(e)[1:-2]
    q = 'select customer_name from customers where email = '+"'"+e+"'"
    #   query = str(q)
    cursor = connection.cursor()
    cursor.execute(q)
    c = cursor.fetchone()
    name = str(c)[1:-2]
    print("customer name is: ",name)
    #to check if customer is active
    q2 = 'select login_session from customers where email ='+"'"+e+"'"
    cursor.execute(q2)
    a = cursor.fetchone()
    active = str(a)[2:-3]
    print(active,' and the type of',active,' is :',type(active))
    if active == 'True':
        # add to check when the customer has been arrived
        return render_template('home.html',name = name, time = 'exist')
    else:
        return render_template('home.html',name = name)

#GET = 페이지가 나오도록 요청. POST = 버튼을 눌렀을때 데이터를 가지고오는 요청/ 요청정보확인하려면 request 임포트 필요
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        email = session['email']
        return render_template("register.html", email)
    else:
        #회원정보 생성
        verification = 0
        login_session = 'False'
        customer_name = request.form.get('customer_name') 
        email = session['email']
        customer_pass = request.form.get('customer_pass')
        repass = request.form.get('repass')
        print("---------------------------------------------------------------------------------------------------------")
        print("input customer_pass: ") # 들어오나 확인해볼 수 있다. 
        print(customer_pass) # 들어오나 확인해볼 수 있다. 
        print("---------------------------------------------------------------------------------------------------------")

        if not (email and customer_name and customer_pass and repass) :
            return "모두 입력해주세요"
        elif customer_pass != repass:
            return "비밀번호를 확인해주세요"
        else: #모두 입력이 정상적으로 되었다면 밑에명령실행(DB에 입력됨)
            fcuser = Fcuser()         
            fcuser.email = email           #models의 FCuser 클래스를 이용해 db에 입력한다.
            fcuser.customer_name = customer_name
            fcuser.customer_pass = customer_pass 
            fcuser.login_session = login_session
            fcuser.verification = verification
            
            cursor = connection.cursor()
            query = ("insert into customers"+"(customer_id, email, customer_name, customer_pass, login_session, verification) "+
            "values(customer_seq.currval,"+
            "'"+email+"', "+
            "'"+customer_name+"', "+
            "'"+customer_pass+"', "+
            "'"+"False', "+ "0)")
            print(query)
            cursor.execute(query)
            print("---------------------------------------------------------------------------------------------------------")
            print("insert query done.")
            
            return redirect('/')

@app.route('/pregi', methods=['GET','POST'])
def crop():
    if request.method == 'GET':
        return render_template("name.html")
    else:
        email = request.form.get('email')
        session['email'] = email
        print("**********************email: ",email)
        directory = email
        parent_dir = "/home/moon/Desktop/Ui_mix/chosenones/1/customers/"
        # Path 
        path = os.path.join(parent_dir, directory) 
        os.mkdir(path) 
        print("Directory '% s' created" % directory) 
        print("done, a directory has been generated for "+email)
        ########################3
        cursor = connection.cursor()
        query1 = ("SELECT customer_seq.nextval from customers")
        query = ("SELECT customer_seq.currval from customers")
        cursor.execute(query1)
        cursor.execute(query)
        temp = cursor.fetchone()
        picnum = str(temp)[1:-2]
        print("#################################################################")
        print("#################################################################")
        print("#################################################################")
        print("#################################################################")
        print('pic number is: ',picnum,' and the temp was ',temp)
        print('Your webcam is getting ready...')
        
        # cropData()
        webcam = cv2.VideoCapture(0)
        
        if not webcam.isOpened():
            print("Could not open webcam")
            exit()

        sample_num = 0    
        captured_num = 0
        start_time=time.time()
        counter = 0
        grabngo = 'customer'

        # loop through frames
        while webcam.isOpened():
    
        # read frame from webcam 
            status, frame = webcam.read()
            # sample_num = sample_num + 1
    
            if not status:
                break
 
            # display output
            cv2.imshow("captured frames", frame)

        # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Label the results
            for (top, right, bottom, left), name in zip(face_locations, grabngo):
                if not name:
                    continue

            # Draw a box around the face
                # cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                crop_img = frame[top:bottom, left:right]

                # captured_num = captured_num + 1
                cv2.imwrite('/home/moon/Desktop/chosenones/1/customers/'+picnum+'.jpg', crop_img)

            # press "Q" to stop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            end_time=time.time()
            elapsed = end_time - start_time
            if elapsed > 4:
                break
    
        # release resources
        webcam.release()
        cv2.destroyAllWindows()   

        prepath = '/home/moon/Desktop/Ui_mix/chosenones/1/customers/'
        path = prepath+email
        num_files = len([f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))])

        if num_files < 1:
            os.remove('/home/moon/Desktop/Ui_mix/chosenones/1/customers/'+email)
            shutil.rmtree(r'/home/moon/Desktop/Ui_mix/chosenones/1/customers/'+email)
            print('directory for '+email+' has been deleted...')
            return 'Your data size is less than 10... please inform your staff and try again.'
        
        else:
        # return "Welcome, "+email+". Please click a button below to proceed your registration.."
        #update ftp################3
        # ftp = FTP()
        # ftp.connect("192.168.0.69",21) #Moified on 16 Dec 2020 at home.
        # ftp.connect("112.169.196.210",50001)
        # ftp = FTP('ftp://112.169.196.210:50001')
        # ftp = FTP('ftp://112.169.196.210:50001/')
        # ftp.login('ftpuser', '1234')
        # # ftp.login()
        # ftp.cwd('./files')  # 업로드할 FTP 폴더로 이동
        # picname = picnum,'.jpg'
        # path = '/home/moon/Desktop/chosenones/1/customers/',picname
        # myfile = open(path,'rb')  # 로컬 파일 열기
        # f = 'STOR '+picname
        # ftp.storbinary(f, myfile)  # 파일을 FTP로 업로드
        # myfile.close()  # 파일 닫기

            return render_template('register.html', email = email)

        # print('for file transfer')
               

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='192.168.0.67', port=9843, debug=True) 

    # app.run(host='192.168.0.1', port=9842, debug=True) 
