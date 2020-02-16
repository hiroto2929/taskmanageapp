from flask import Flask, render_template,request
import csv

app = Flask(__name__)

name_deadline_dict={}


@app.route('/')
def index():

    name_deadline_dict={}

    with open('data.csv','r') as f:
        reader = csv.reader(f)
        for row in reader:
            list_index=[]
            row[1]=row[1].replace('-','/')
            list_index.append(row[1])
            list_index.append(row[2])
            name_deadline_dict[row[0]]=list_index

    return render_template('index.html',data=name_deadline_dict)
@app.route('/place')
def place():
    return render_template('place.html'


@app.route('/n&d')
def nd():

    name_deadline_dict_nd={}


    with open('data.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            list_nd=[]
            list_nd.append(row[1])
            list_nd.append(row[2])
            name_deadline_dict_nd[row[0]]=list_nd

    list1=[]
    sorted_name_deadline_dict={}
    panfname = request.args.get('panfname','')
    deadline = request.args.get('deadline','')
    place = request.args.get('place','')
    deadline=deadline.replace('/','-')
    list2=[]
    list2.append(deadline)
    list2.append(place)


    #要素を追加
    name_deadline_dict_nd[panfname] = list2
    
    #辞書からリストに戻してソートしてまた辞書に戻す
    for i,j in name_deadline_dict_nd.items():
        list2=[]
        list2.append(i)
        list2.append(j[0])
        list2.append(j[1])
        list1.append(list2)
    sorted_data = sorted(list1,key=lambda x:x[1])

    with open('data.csv','w') as q:
        writer = csv.writer(q,lineterminator='\n')
        for m in sorted_data:
            writer.writerow(m)

    for k in sorted_data:
        list3=[]
        k[1]=k[1].replace('-','/')
        list3.append(k[1])
        list3.append(k[2])
        sorted_name_deadline_dict[k[0]]=list3


    return render_template('index.html',data4=sorted_name_deadline_dict)


@app.route('/search')
def search_n():
    panfname_s = request.args.get('panfname_s','')
    search_dict={}
    name_deadline_dict_ser={}

    with open('data.csv') as f:
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
      
@app.route('/search_d')
def search_d():
    deadline_s = request.args.get('deadline_s','')
    search_dict2={}
    name_deadline_dict_serd={}

    with open('data.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            name_deadline_dict_serd[row[0]]=row[1]
            if deadline_s == name_deadline_dict_serd[row[0]]:
                list_d=[]
                row[1]=row[1].replace('-','/')
                list_d.append(row[1])
                list_d.append(row[2])
                
                search_dict2[row[0]]=list_d

    if len(search_dict2)==0:
        list_non=[]
        list_non.append(' ')
        list_non.append('検索に該当する情報がありません')
        search_dict2[' ']=list_non

    return render_template('index.html',data3=search_dict2)


@app.route('/search_p')
def search_p():
    panfname_pl = request.args.get('search_p','')
    searchp_dict={}
    name_deadline_dict_pl={}

    with open('data.csv') as f:
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

    panf_name = request.args.get('delete','')
    list1=[]
    l_name_deadline_dict={}

    with open('data.csv') as f:
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

    with open('data.csv','w') as q:
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
