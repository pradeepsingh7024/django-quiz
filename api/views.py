from django.shortcuts import redirect,render
from .models import Signup
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.db.models import Q
def signupform(request):
    if request.method=='POST':
        u=request.POST.get('username')
        e=request.POST.get('email')
        p=request.POST.get('password')
        p1=request.POST.get('password1')
        print()
        print('conti.......')
        if p==p1:
            user=Signup(name=u,gmail=e,password=p)
            user.save()
            return render(request,'api/login.html',{'mes':'succussfully registration'})
        else:
            return render(request,'api/signup.html',{'mes':'password not same'})
    else:
        return render(request,'api/signup.html',{'mes':'first register now'})
   

def Login(request):
    if request.method=='POST':
        u=request.POST.get('username')
        p=request.POST.get('password')
        print(u,p)
        user = Signup.objects.filter( Q(gmail=u, password=p) | Q(name=u, password=p)).first()
        print(user)
        if user:    
            u=Signup.objects.get(gmail=u)
            id = u.id
            print(id)
            # id = Signup.objects.get()
          
           
            print('login sucussfully')
            # return render(request,'api/paper2.html',{'user':u,'mes':'login successfully'})
            return redirect(f'/paper/{id}')
            # return redirect('paper', pk =id)
      
            # return render(request,'login.html',{'mes':"please try again"})
    return render(request,'api/login.html',{'mes':"Signup successfully...."})
        
        


def paper(request, pk):
    if pk is not None:
        obj1 = Signup.objects.get(id = pk)
        print(obj1.id)
        print(obj1.name)
        print(type(obj1))
    
    
    paper={ '1':{'q':'Django is a Python-based ____.',"option":['web framework','video creating tool','analysis tool','desktop development platform']},
              
    '2':{'q': ' Django is maintained by which organization/company?','option':['Oracle',
'Microsoft Corporation','Python Software Foundation',
'Django Software Foundation']},
    '3':{'q': 'Who is/are the original author(s) of Django?','option':['Pearu Peterson, Robert Kern, and Travis Oliphant',
'Adrian Holovaty and Simon Willison',
'Adrian Hallet and Simon Willison',
'Larry Ellison, Bob Miner, and Ed Oates']},
    '4':{'q': 'What is Django used for?','option':['Machine learning','Game development','Web development','Data analysis']},
    '5':{'q': 'What is Django in python?','option':['A framework','A library','A function','Ascript']},
    '6':{'q': 'What is the base principle of MVT in Django?','option':['Model, Template, View','Model, View, Template','Template, Model, View','Template, View, Model']},

    '7':{'q': 'How does Django handle URL routing?','option':['By using functions','By using a fixed path','By using classes','By using regular expressions']},
    '8':{'q': 'What is the default database used in Django?','option':['Oracle','SQLite','PostgreSQL','MySQL']},

    '9':{'q': 'Which command is used to create an app in Django?','option':['py admin.py startapp-c app_name',
'py manage.py startapp app_name',
'py manage.py djangoapp app_name',
'py manage.py createapp app_name']},
    
    '10':{'q': ' Which file is not a part of the Django project content?','option':['settings.py',
'manage.py',
'templates.py',
'py manage.py runserver']},
    
    '11':{'q': 'Django is written in which language?','option':['C++',
'Python',
'AngularJS',
'Asp.Net']},
    
    '12':{'q': 'Which Django functions are used to take http requests and return http responses?','option':['Django views',
'Django request() and response()',
'Django templates',
'Both A and B']},
    
    '13':{'q': 'In Django, data is created in ____.','option':['tables',
'views',
'templates',
'objects']},
    
    '14':{'q': 'In Django, data is created in objects, what are these objects called ____.','option':['models',
'views',
'templates',
'database']},
    
    }
    ans={
        '1':'web framework',
        '2':'Django Software Foundation',
        '3':'Adrian Holovaty and Simon Willison',
        '4':'Web development',
        '5':'A framework',
        '6':'Model, View, Template',
        '7':'By using regular expressions',
        '8':'SQLite',
        '9':'py manage.py startapp app_name',
        '10':'templates.py',
        '11':'Python',
        '12':'Django views',
        '13':'objects',
        '14':'models',

        
        }

    if request.method=='POST':
        a={}
        for key in paper.keys():
            a[key]=request.POST.get(key)
        
        check = {}
        t=0
        f=0
        q=0
        unattempted=0
        for key, value in a.items():
            q+=1
            if key in ans and ans[key] == value:
                check[key] = value +' ✔'
                t+=1
            else:
                if value==None:
                    value='not select'
                    check[key] = value+' 🔷'
                    unattempted+=1
                else:
                    check[key] = value+' ❌'
                    f+=1

        return render(request,'api/result.html',{'result':check,'right':t,'wrong':f,"q":q,'paper':paper,'a':unattempted})

    print('all done')
    return render(request,'api/paper2.html',{'paper':paper,"mes":"not login", 'obj1' : obj1})  


def logout(request,pk):
    user=Signup.objects.get(id=pk)
    if user:
        return redirect('/login/')


