from django.shortcuts import render
from .forms import RegistrationForm,LoginForm,SearchForm,CheckForm,RegisForm,FindForm#,ExtendForm,ConfirmForm
from django.http import HttpResponseRedirect 
from django.http import HttpResponse
from datetime import date,timedelta
import psycopg2
#import itertools
#from itertools import izip
current_user = ''
conn = psycopg2.connect(database ="loli_isp",  
                            user = "postgres",  
                            password = "lolislayer",  
                            host = "localhost",  
                            port = "5432") #ket noi  toi database
cur = conn.cursor()
t1 = timedelta(days = 30)
t2 = timedelta(days = 90)
t3 = timedelta(days = 180)

# Create your views here.
def index(request): #tao view home
    return render(request, 'pages/home.html')
def contact(request):
   return render(request, 'pages/contact.html')
def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    return render(request, 'pages/register.html', {'form': form})

    
def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            #current_user = form.clean_username()
            if form.clean_username() != 'admin':
                return render(request,'pages/userlog.html', {'form': form,'username':form.clean_username})
            else:
                return render(request, 'pages/admin.html', {'form': form})
    return render(request, 'pages/login.html',{'form': form})
def userlog(request,username):
    context={
        'username' : username
    }
    return render(request, 'pages/userlog.html',context)

def admin(request,username):
    context={
        'username' : username
    }
    return render(request, 'pages/admin.html',context)

def check(request,username):
    cur.execute("select * from customer where username = '%s'" % username)
    data = cur.fetchall()
    username = data[0][1]
    name = data[0][3] + ' ' + data[0][4]
    dob = data[0][5]
    sdt = data[0][6]
    reg = data[0][7]
    add = data[0][8]
    city = data[0][9]
    pid = data[0][10]
    exd = data[0][11]
    cmt = data[0][12]
    if data[0][13] == 'F':
        gen = 'Nữ'
    else:
        gen = 'Nam'
    
    if pid != None:
        cur.execute("select package_name,speed from package where package_id = '%s'" % pid)
        pack = cur.fetchall()
        if pack[0][0] != None:
            pname = pack[0][0]
            ps = pack[0][1]
        else:
            pname = 'Chưa đăng ký'
            ps = ''
            exd = ''
    else:
        pname = 'Chưa đăng ký'
        ps = ''
    context = {
        'username' : username,
        'name' : name,
        'dob' : dob,
        'sdt' : sdt,
        'reg' : reg,
        'add' : add,
        'city' : city,
        'exd' : exd,
        'cmt' : cmt,
        'gen' : gen,
        'pname' : pname,
        'ps' : ps
    }
    return render(request, 'pages/setting.html',context)
def family(request):
    cur.execute("select package_name,speed,rate,cost from package where lower(package_name) like '%net%'")
    data= cur.fetchall()
    pname = []
    ps = []
    r = []
    c = []
    for row in data:
        pname.append(row[0])
        ps.append(row[1])
        r.append(round(row[2],1))
        c.append(row[3])
    
    cur.execute("select count(*) from package where lower(package_name) like '%net%'")
    data1 = cur.fetchall()
    num = data1[0][0]
    nu = []
    for i in range(int(num)):
        nu.append(i)
    context={
        'pname' : pname,
        'ps' : ps,
        'r' : r,
        'num' : nu,
        'c' :c,
        'infor': zip(pname,ps,r,c)
    }
    return render(request, 'pages/family.html',context)
def compa(request):
    cur.execute("select package_name,speed,rate,cost from package where lower(package_name) like '%fast%'")
    data= cur.fetchall()
    pname = []
    ps = []
    r = []
    c = []
    for row in data:
        pname.append(row[0])
        ps.append(row[1])
        r.append(round(row[2],1))
        c.append(row[3])
    
    cur.execute("select count(*) from package where lower(package_name) like '%fast%'")
    data1 = cur.fetchall()
    num = data1[0][0]
    nu = []
    for i in range(int(num)):
        nu.append(i)
    context={
        'pname' : pname,
        'ps' : ps,
        'r' : r,
        'num' : nu,
        'c' :c,
        'infor': zip(pname,ps,r,c)
    }
    return render(request, 'pages/compa.html',context)
def spec(request):
    cur.execute("select package_name,speed,rate,cost from package where lower(package_name) not like '%net%' and lower(package_name) not like '%fast%'")
    data= cur.fetchall()
    pname = []
    ps = []
    r = []
    c = []
    for row in data:
        pname.append(row[0])
        ps.append(row[1])
        r.append(round(row[2],1))
        c.append(row[3])
    
    cur.execute("select count(*) from package where lower(package_name) not like '%net%' and lower(package_name) not like '%fast%'")
    data1 = cur.fetchall()
    num = data1[0][0]
    nu = []
    for i in range(int(num)):
        nu.append(i)
    context={
        'pname' : pname,
        'ps' : ps,
        'r' : r,
        'num' : nu,
        'c' :c,
        'infor': zip(pname,ps,r,c)
    }
    return render(request, 'pages/spec.html',context)
def searchcity(request):
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            #current_user = form.clean_username()
            return render(request, 'pages/ctresult.html', {'form': form})
    return render(request, 'pages/searchct.html',{'form': form})
def ctresult(request):
    return render(request, 'pages/ctresult.html')
def loginrequire(request):
    return render(request, 'pages/loginrequire.html')
def cancelpack(request,username):
    form = CheckForm()
    cur.execute("select package_id,expire_day from customer where username = '%s'" % username)
    data = cur.fetchall()
    pack = data[0][0]
    warn1 = 'Bạn chưa đăng ký gói nào'
    if pack == None:
        return render(request, 'pages/huygoi.html',{'username' : username,'warn':warn1})
    else:
        cur.execute("select package_name from package where package_id = '%s'" %pack)
        da = cur.fetchall()
        pname = da[0][0]
        warn2 = 'Bạn đang sử dụng gói' + ' ' + pname
        if request.method == 'POST':
            warn3 = 'Bạn đã hủy gói thành công'
            form = CheckForm(request.POST)
            if form.is_valid():
                if form.checks() == 'Y':
                    cur.execute("update customer set package_id = NULL,expire_day =NULL where username = '%s'" % username)
                    conn.commit()
                    return render(request, 'pages/huygoi.html',{'username': username,'warn':warn3})
                else:
                    return render(request, 'pages/userlog.html',{'username' : username})
        return render(request, 'pages/huygoi.html',{'username': username,'warn':warn2,'form':form})
'''def extend(request,username):
    form1 = ExtendForm()
    form2 = ConfirmForm()
    cur.execute("select package_id,expire_day from customer where username = '%s'" % username)
    data = cur.fetchall()
    pack = data[0][0]
    warn1 = 'Bạn chưa đăng ký gói nào'
    if pack == None:
        return render(request, 'pages/extend.html',{'username' : username,'warn':warn1})
    else:
        cur.execute("select package_name from package where package_id = '%s'" %pack)
        da = cur.fetchall()
        pname = da[0][0]
        warn2 = 'Bạn đang sử dụng gói' + ' ' + pname
        if request.method == 'POST':
            warn3 = ''
            form1 = ExtendForm(request.POST)
            if form1.is_valid():
                return render(request, 'pages/extend.html',{'username': username,'form':form2,'m':form1.choices()})
        return render(request, 'pages/extend.html',{'username' : username,'form':form1,'warn':warn2})
def cfextend(request,username,m):
    form = ConfirmForm()
    cur.execute("select expire_day from customer where username = '%s'" % username)
    data = cur.fetchall()
    exp = data[0][0]'''
def packavai(request,username):
    cur.execute("select city from customer where username = '%s'" % username)
    data = cur.fetchall()
    city = data[0][0]
    cur.execute("select package_name,speed,rate,cost,package_id from package where package_id in (select package_id from address where address = '%s') order by package_id" % city)
    data1 = cur.fetchall()
    pname = []
    ps = []
    r = []
    c = []
    pid = []
    for row in data1:
        pname.append(row[0])
        ps.append(row[1])
        r.append(round(row[2],1))
        c.append(row[3])
        pid.append(row[4])
    context={
        'pname' : pname,
        'ps' : ps,
        'r' : r,
        'c' :c,
        'infor': zip(pname,ps,r,c,pid),
        'username':username,
    }
    return render(request, 'pages/avaipack.html',context)
def regispack(request,username,pid):
    cur.execute("select count(*) from transaction")
    data = cur.fetchall()
    id = data[0][0]
    id = id+1
    cur.execute("select cost from package where package_id = '%s'" % pid)
    data = cur.fetchall()
    cost = data[0][0]
    form = RegisForm()
    if request.method == 'POST':
        form = RegisForm(request.POST)
        if form.is_valid():
            if form.clean_time() == '1':
                total = cost*1
                reg = date.today()
                exp = reg + t1
                rate = form.clean_rate()
                cur.execute("insert into transaction values ('%s','%s','%s','%s','%s','%s','%s','%s')" % (id,username,pid,id,total,reg,exp,rate)) 
                conn.commit()
                method = form.clean_pay()
                cur.execute("update bill set pay_method='%s' where bill_id = '%s'" % (method,id))
                conn.commit()
                return render(request, 'pages/regispack.html',{'username' : username,'form': form,'tb':'Đăng ký thành công'})
            if form.clean_time() == '3':
                total = cost*3
                reg = date.today()
                exp = reg + t2
                rate = form.clean_rate()
                cur.execute("insert into transaction values ('%s','%s','%s','%s','%s','%s','%s','%s')" % (id,username,pid,id,total,reg,exp,rate)) 
                conn.commit()
                method = form.clean_pay()
                cur.execute("update bill set pay_method='%s' where bill_id = '%s'" % (method,id))
                conn.commit()
                return render(request, 'pages/regispack.html',{'username' : username,'form': form,'tb':'Đăng ký thành công'})
            if form.clean_time() == '6':
                total = cost*6
                reg = date.today()
                exp = reg + t3
                rate = form.clean_rate()
                cur.execute("insert into transaction values ('%s','%s','%s','%s','%s','%s','%s','%s')" % (id,username,pid,id,total,reg,exp,rate)) 
                conn.commit()
                method = form.clean_pay()
                cur.execute("update bill set pay_method='%s' where bill_id = '%s'" % (method,id))
                conn.commit()
                return render(request, 'pages/regispack.html',{'username' : username,'form': form,'tb':'Đăng ký thành công'})
    return render(request, 'pages/regispack.html',{'username' : username,'form':form})
def extend(request,username):
    cur.execute("select expire_day from customer where username = '%s'" % username)
    data = cur.fetchall()
    exp = data[0][0]
    cur.execute("select package_id from customer where username = '%s'" % username)
    data = cur.fetchall()
    pid = data[0][0]
    cur.execute("select count(*) from transaction")
    data = cur.fetchall()
    id = data[0][0]
    id = id+1
    if pid != None:
        cur.execute("select cost from package where package_id = '%s'" % pid)
        data = cur.fetchall()
        cost = data[0][0]
    form = RegisForm()
    if pid == None:
        return render(request, 'pages/extend.html',{'username' : username,'warn':'Bạn chưa đăng ký'})
    else:
        if request.method == 'POST':
            form = RegisForm(request.POST)
            if form.is_valid():
                if exp < date.today():
                    if form.clean_time() == '1':
                        total = cost*1
                        reg = date.today()
                        exp = reg + t1
                        rate = form.clean_rate()
                        cur.execute("insert into transaction values ('%s','%s','%s','%s','%s','%s','%s','%s')" % (id,username,pid,id,total,reg,exp,rate)) 
                        conn.commit()
                        method = form.clean_pay()
                        cur.execute("update bill set pay_method='%s' where bill_id = '%s'" % (method,id))
                        conn.commit()
                        return render(request, 'pages/extend.html',{'username' : username,'form': form,'tb':'Gia hạn thành công'})
                    if form.clean_time() == '3':
                        total = cost*3
                        reg = date.today()
                        exp = reg + t2
                        rate = form.clean_rate()
                        cur.execute("insert into transaction values ('%s','%s','%s','%s','%s','%s','%s','%s')" % (id,username,pid,id,total,reg,exp,rate)) 
                        conn.commit()
                        method = form.clean_pay()
                        cur.execute("update bill set pay_method='%s' where bill_id = '%s'" % (method,id))
                        conn.commit()
                        return render(request, 'pages/extend.html',{'username' : username,'form': form,'tb':'Gia hạn thành công'})
                    if form.clean_time() == '6':
                        total = cost*6
                        reg = date.today()
                        exp = reg + t3
                        rate = form.clean_rate()
                        cur.execute("insert into transaction values ('%s','%s','%s','%s','%s','%s','%s','%s')" % (id,username,pid,id,total,reg,exp,rate)) 
                        conn.commit()
                        method = form.clean_pay()
                        cur.execute("update bill set pay_method='%s' where bill_id = '%s'" % (method,id))
                        conn.commit()
                        return render(request, 'pages/extend.html',{'username' : username,'form': form,'tb':'Gia hạn thành công'})
                else:
                    if form.clean_time() == '1':
                        total = cost*1
                        reg = date.today()
                        exp = exp + t1
                        rate = form.clean_rate()
                        cur.execute("insert into transaction values ('%s','%s','%s','%s','%s','%s','%s','%s')" % (id,username,pid,id,total,reg,exp,rate)) 
                        conn.commit()
                        method = form.clean_pay()
                        cur.execute("update bill set pay_method='%s' where bill_id = '%s'" % (method,id))
                        conn.commit()
                        return render(request, 'pages/extend.html',{'username' : username,'form': form,'tb':'Gia hạn thành công'})
                    if form.clean_time() == '3':
                        total = cost*3
                        reg = date.today()
                        exp = exp + t2
                        rate = form.clean_rate()
                        cur.execute("insert into transaction values ('%s','%s','%s','%s','%s','%s','%s','%s')" % (id,username,pid,id,total,reg,exp,rate)) 
                        conn.commit()
                        method = form.clean_pay()
                        cur.execute("update bill set pay_method='%s' where bill_id = '%s'" % (method,id))
                        conn.commit()
                        return render(request, 'pages/extend.html',{'username' : username,'form': form,'tb':'Gia hạn thành công'})
                    if form.clean_time() == '6':
                        total = cost*6
                        reg = date.today()
                        exp = exp + t3
                        rate = form.clean_rate()
                        cur.execute("insert into transaction values ('%s','%s','%s','%s','%s','%s','%s','%s')" % (id,username,pid,id,total,reg,exp,rate)) 
                        conn.commit()
                        method = form.clean_pay()
                        cur.execute("update bill set pay_method='%s' where bill_id = '%s'" % (method,id))
                        conn.commit()
                        return render(request, 'pages/extend.html',{'username' : username,'form': form,'tb':'Gia hạn thành công'})
        return render(request, 'pages/extend.html',{'username' : username,'form':form})
def research(request,username):
    cur.execute("select count(*) from pay_history where username = '%s'" % username)
    data = cur.fetchall()
    number_tran = data[0][0]
    cur.execute("select sum(total) from bill where username = '%s'" % username)
    data = cur.fetchall()
    total = data[0][0]
    cur.execute("select register_day,total,pay_method from bill where username = '%s'" % username)
    data = cur.fetchall()
    reg = []
    to = []
    me = []
    for row in data:
        reg.append(row[0])
        to.append(row[1])
        me.append(row[2])
    count=[]
    for i in range(int(number_tran)):
        count.append(i+1)

    context={
        'username' : username,
        'infor' : zip(reg,to,me,count),
        'total' : total,
        'number_tran' : number_tran
    }
    return render(request, 'pages/tracuu.html',context)
def find(request):
    form = FindForm()
    if request.method == 'POST':
        form = FindForm(request.POST)
        if form.is_valid():
            content = form.clean_content()
            cur.execute("select package_name from package where lower(package_name) like '%%%s%%'" % content.lower())
            data = cur.fetchall()
            pack = []
            for row in data:
                pack.append(row[0])
            cur.execute("select address from address where lower(address) like '%%%s%%' group by address" % content.lower())
            data = cur.fetchall()
            add =[]
            for row in data:
                add.append(row[0])
            context = {
                'pack':pack,
                'add': add,
                'form':form
            }
            return render(request, 'pages/timkiem.html',context)
    return render(request, 'pages/timkiem.html',{'form' : form,})

            
        
        


    


