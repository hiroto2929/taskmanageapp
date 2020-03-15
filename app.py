from flask import Flask, render_template,request,redirect,url_for,session,abort
import csv

app = Flask(__name__)
app.secret_key = 'hogehoge'

name_deadline_dict={}





@app.route('/login', methods=['POST'])
def do_admin_login():

    username=request.form['username']
    password=request.form['password']

    with open('member.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0]==username and row[1]==password:
                session['username'] = username
                session['password'] = password
                session['logged_in'] = True
                return redirect(url_for('index'))


        return render_template("login.html")


@app.route("/logout")
def logout():
   session['logged_in'] = False
   return redirect(url_for('index'))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/new_register")
def new_register():
    username= request.args.get('new_username','')
    password=request.args.get('new_password','')
    csv_path = 'data/'+ username+ '.csv'
    list_reg=[]
    list_reg.append(username)
    list_reg.append(password)
    list_reg.append(username)


    with open('member.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if username==row[0] and password==row[1]:
                return render_template("login.html",alr="already registered")
            elif username==row[0]:
                with open('member.csv','w') as q:
                    writer = csv.writer(q)
                    writer.writerow(list_reg)


        with open('member.csv','a') as q:
            writer = csv.writer(q)
            writer.writerow(list_reg)
        try:
            with open(csv_path, mode='x') as f:
                pass
        except FileExistsError:
            pass
        return render_template("login.html")

@app.route('/')
def index():

    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        data='none'
        with open('member.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                if session['username']==row[0] and session['password']==row[1]:
                    data=('data/'+row[2]+'.csv')
        name_deadline_dict={}


        with open(data,'r') as f:
            reader = csv.reader(f)
            for row in reader:
                list_index=[]
                list_index.append(row[1])
                list_index.append(row[2])
                name_deadline_dict[row[0]]=list_index

        return render_template('index.html',data=name_deadline_dict)

@app.route('/place')
def place():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('place.html')


@app.route('/n&d')
def nd():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:

        name_type_dict_nd={}
        data='none'
        with open('member.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                if session['username']==row[0] and session['password']==row[1]:
                    data=('data/'+row[2]+'.csv')


        with open(data) as f:
            reader = csv.reader(f)
            for row in reader:
                list_nd=[]
                list_nd.append(row[1])
                list_nd.append(row[2])
                name_type_dict_nd[row[0]]=list_nd

        list1=[]
        sorted_name_deadline_dict={}
        
        panfname = request.args.get('panfname','')
        panf_type = request.args.get('type','')
        place = request.args.get('place','')

        list2=[]
        list2.append(panf_type)
        list2.append(place)


        #要素を追加
        name_type_dict_nd[panfname] = list2
    
        #辞書からリストに戻してソートしてまた辞書に戻す
        for i,j in name_type_dict_nd.items():
            list2=[]
            list2.append(i)
            list2.append(j[0])
            list2.append(j[1])
            list1.append(list2)


        with open(data,'w') as q:
            writer = csv.writer(q,lineterminator='\n')
            for m in list1:
                writer.writerow(m)

        for k in list1:
            list3=[]
            list3.append(k[1])
            list3.append(k[2])
            sorted_name_deadline_dict[k[0]]=list3


        return render_template('index.html',data4=sorted_name_deadline_dict)


@app.route('/search')
def search_n():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        panfname_s = request.args.get('panfname_s','')
        search_dict={}
        name_deadline_dict_ser={}

        data='none'
        with open('member.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                if session['username']==row[0] and session['password']==row[1]:
                    data=('data/'+row[2]+'.csv')

        with open(data) as f:
            reader = csv.reader(f)
            for row in reader:
                name_deadline_dict_ser[row[0]]=row[1]
                if panfname_s in name_deadline_dict_ser:
                    list_s=[]
                    row[1]=row[1].replace('-','/')
                    list_s.append(row[1])
                    list_s.append(row[2])
                    search_dict[panfname_s]=list_s
        if len(search_dict)==0:
            list_non=[]
            list_non.append(' ')
            list_non.append('検索に該当する情報がありません')
            search_dict[' ']=list_non


        return render_template('index.html',data2=search_dict)
      
                
@app.route('/search_t')
def search_t():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        panftype= request.args.get('type','')
        searcht_dict={}
        name_type_dict={}

        data='none'
        with open('member.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                if session['username']==row[0] and session['password']==row[1]:
                    data=('data/'+row[2]+'.csv')
        with open(data) as f:
            reader = csv.reader(f)
            for row in reader:
                name_type_dict[row[0]]=row[1]
                if panftype == row[1]:
                    list_t=[]
                    list_t.append(row[1])
                    list_t.append(row[2])
                    searcht_dict[row[0]]=list_t

        
        if len(searcht_dict)==0:
            list_non=[]
            list_non.append(' ')
            list_non.append('検索に該当する情報がありません')
            searcht_dict[' ']=list_non

        return render_template('index.html',data3=searcht_dict)




@app.route('/search_p')
def search_p():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        panfname_pl = request.args.get('search_p','')
        searchp_dict={}
        name_deadline_dict_pl={}

        data='none'
        with open('member.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                if session['username']==row[0] and session['password']==row[1]:
                    data=('data/'+row[2]+'.csv')

        with open(data) as f:
            reader = csv.reader(f)
            for row in reader:
                name_deadline_dict_pl[row[0]]=row[1]
                if panfname_pl == row[2]:
                    list_f=[]
                    row[1]=row[1].replace('-','/')
                    list_f.append(row[1])
                    list_f.append(row[2])
                    searchp_dict[row[0]]=list_f
        
        if len(searchp_dict)==0:
            list_non=[]
            list_non.append(' ')
            list_non.append('検索に該当する情報がありません')
            searchp_dict[' ']=list_non

        return render_template('index.html',data6=searchp_dict)

                    

@app.route('/delete')
def delete():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:

        panf_name = request.args.get('delete','')
        list1=[]
        l_name_deadline_dict={}

        data='none'
        with open('member.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                if session['username']==row[0] and session['password']==row[1]:
                    data=('data/'+row[2]+'.csv')

        with open(data) as f:
            reader = csv.reader(f)
            for row in reader:
                lista=[]
                if panf_name == row[0]:
                    continue
                else:
                    lista.append(row[1])
                    lista.append(row[2])
                    l_name_deadline_dict[row[0]]=lista

 
                

        for i,j in l_name_deadline_dict.items():
            list2=[]
            list2.append(i)
            list2.append(j[0])
            list2.append(j[1])
            list1.append(list2)

        with open(data,'w') as q:
            writer = csv.writer(q,lineterminator='\n')
            for m in list1:
                writer.writerow(m)

        for k in list1:
            listb=[]
            k[1]=k[1].replace('-','/')
            listb.append(k[1])
            listb.append(k[2])
            l_name_deadline_dict[k[0]]=listb


        
        return render_template('index.html',data5=l_name_deadline_dict)



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
