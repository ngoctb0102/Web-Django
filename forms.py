from django import forms
import psycopg2
import re
from datetime import date,timedelta
conn = psycopg2.connect(database ="loli_isp",  
                            user = "postgres",  
                            password = "lolislayer",  
                            host = "localhost",  
                            port = "5432") #ket noi  toi database
cur = conn.cursor()
cur.execute("select address,address from address group by address")
data1 = cur.fetchall()
city1 = []
for row in data1:
    city1.append(row[0])

cur.execute("select count(*) from customer")
data2 = cur.fetchall()
id = data2[0][0] + 1
from datetime import date
today = date.today()
cur.execute("select username from customer")
data3 = cur.fetchall()
tk =[]
for row in data3:
    tk.append(row[0])
def check_pass(password,username):
    cur.execute("select password from customer where username = '%s'" % (username))
    passx = cur.fetchall()
    passcheck = passx[0][0]
    if password == passcheck:
        return True
    else:
        return False


def check_user(username):
    i = 0
    for user in tk:
        if username == user:
            i+=1
    if i == 0:
        return False
    else:
        return True


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Tài khoản', max_length=30)
    #email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Nhập lại mật khẩu', widget=forms.PasswordInput())
    fn = forms.CharField(label='Họ', max_length=50)
    ln = forms.CharField(label='Tên',max_length=20)
    dob = forms.DateField(label='Năm-Tháng-Ngày sinh',widget=forms.DateInput())
    phone = forms.CharField(label='Số điện thoại',max_length=15)
    add = forms.CharField(label='Địa chỉ')
    city = forms.ChoiceField(label='Thành Phố',choices = tuple(data1))
    cmt = forms.CharField(label='Số chứng minh thư',max_length=20)
    gen = forms.ChoiceField(label='Giới tính',choices = (('F','Nữ'),('M','Nam')))
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2 and password1:
                return password2
        raise forms.ValidationError("Onii-chan nhập sai mật khẩu rồi kìa :))")

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError("Tên tài khoản của onii-chan có kí tự đặc biệt")
        i = 0
        for acc in tk:
            if acc == username:
                i+=1
        if i == 0:
            return username
        else:
            raise forms.ValidationError("Onii-chan đã tồn tại!")
    def save(self):
        tk.append(self.cleaned_data['username'])
        cur.execute("insert into customer(customer_id,username,password,first_name,last_name,dob,phone,register_day,address,city,cmt,gender) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (id,self.cleaned_data['username'],self.cleaned_data['password1'],self.cleaned_data['fn'],self.cleaned_data['ln'],self.cleaned_data['dob'],self.cleaned_data['phone'],today,self.cleaned_data['add'],self.cleaned_data['city'],self.cleaned_data['cmt'],self.cleaned_data['gen']))
        conn.commit()

class LoginForm(forms.Form):
    username = forms.CharField(label='Tài khoản', max_length=30)
    password = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput())
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError("Tên tài khoản của onii-chan có kí tự đặc biệt")
        if check_user(username) == False:
            raise forms.ValidationError("Tài khoản không tồn tại !!")
        else:
            return username
    def clean_password(self):
        if 'username' in self.cleaned_data:
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if check_user(username) == False:
                raise forms.ValidationError("Tài khoản không tồn tại !!")
            else:
                if check_pass(password,username) is False:
                    raise forms.ValidationError("Onii-chan nhập sai mật khẩu rồi kìa :))")
                else:
                    return password
class SearchForm(forms.Form):
    city = forms.ChoiceField(label='Thành Phố',choices = tuple(data1))
    def takeid(self):
        city = self.cleaned_data['city']
        cur.execute("select package_name,speed,rate,cost from package where package_id in (select package_id from address where address = '%s')" % city)
        pack = cur.fetchall()
        pname = []
        ps = []
        r = []
        c = []
        for row in pack:
            pname.append(row[0])
            ps.append(row[1])
            r.append(round(row[2],1))
            c.append(row[3])
        return zip(pname,ps,r,c)
class CheckForm(forms.Form):
    check = forms.ChoiceField(label='Bạn có chắc chắn muốn hủy gói không ?',choices = (('Y','Có'),('N','Không')))
    def checks(self):
        check = self.cleaned_data['check']
        return check
class ExtendForm(forms.Form):
    choice = forms.ChoiceField(label='Số tháng bạn muốn gia hạn',choices=((1,'1 Tháng'),(3,'3 Tháng'),(6,'6 Tháng')) )
    def choices(self):
        choice = self.cleaned_data['choice']
        return choice
class ConfirmForm(forms.Form):
    check = forms.ChoiceField(label='Xác nhận gia hạn ?',choices = (('Y','Có'),('N','Không')))
    def confirm(self):
        check = self.cleaned_data['check']
        return check
class RegisForm(forms.Form):
    cur.execute("select pay_method,pay_method from paymethod")
    data = cur.fetchall()
    time = forms.ChoiceField(label='Số tháng đăng ký',choices=((1,'1 Tháng'),(3,'3 Tháng'),(6,'6 Tháng')))
    rate = forms.IntegerField(label='Đánh giá của bạn (0 đến 5)',min_value = 0,max_value = 5)
    pay = forms.ChoiceField(label='Phương thức thanh toán',choices=tuple(data))
    def clean_time(self):
        time = self.cleaned_data['time']
        return time
    def clean_rate(self):
        rate = self.cleaned_data['rate']
        return rate
    def clean_pay(self):
        pay = self.cleaned_data['pay']
        return pay
class FindForm(forms.Form):
    content = forms.CharField(label='Nội dung tìm kiếm',max_length=200)
    def clean_content(self):
        content = self.cleaned_data['content']
        return content



