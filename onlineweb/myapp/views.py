from django.shortcuts import render,redirect
from django.http import HttpResponse
from myapp.models import register,donorregister,requests,bloodcamp
from django.contrib import messages
from myapp.forms import Updatepro
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import BadHeaderError, send_mail
from django.conf import settings
from datetime import date
from .utils import getplot,getplot1


# Create your views here.
def Login(request):
	if request.method=="POST":
		username=request.POST['username']
		pass1=request.POST['Password']
		
		if User.objects.filter(username=username, password=pass1).exists():
			user=User.objects.get(username=username)
			login(request, user)
			request.session['username']=username
			messages.success(request,('Youre logged in'))

			return redirect('base') #routes to 'home' on successful login  
		else:
			messages.success(request,('Error logging in'))
			return redirect('login') #re routes to login page upon unsucessful login
	else:
		return render(request, 'myapp/login.html', {})



	

def Registration(request):
	if request.method=="POST":
		regname=request.POST['Registeredname']
		email=request.POST['Email']
		password1=request.POST['Password1']
		password2=request.POST['Password2']
		mobile=request.POST['Mobile']
		if password1==password2:
			if User.objects.filter(username=regname).exists():
				messages.info(request,"Username already taken!!")
			
			if User.objects.filter(email=email).exists():
				messages.info(request,"Email already taken!!")
			
			else:
				user=User(username=regname,email=email,password=password1)
				messages.info(request,"Successfully registered-->Login now!!")
				'''subject="Blood donation"
				message=f"hii {user.username}, you have been succesfully registered for www.onlineblooddonation.com!"
				from_email=settings.EMAIL_HOST_USER
				to=[user.email,]
				if subject and message and from_email:
					try:
						send_mail(subject, message, from_email,to)
						print("sent mail")
					except:
						return HttpResponse('Invalid header found.')'''

				user.save()

				return redirect('login')
		else:
			messages.info(request,"Check password Fields properly!!")
		
	return render(request,'myapp/Registration.html')

def Home(request):
	return render(request,'myapp/home.html')
	
@login_required(login_url='login')
def Donorreg(request):
	if request.method=="POST":
		username=request.POST['person_name']
		age=request.POST['age']
		gender=request.POST['sex']
		city=request.POST['city']
		address=request.POST['address']
		contact=request.POST['contact_number']
		email=request.POST['email']
		donatetype=request.POST['donatetype']
		servicetype=request.POST['servicetype']

		bloodgroup=request.POST.get('blood_group')
		date=request.POST['last_donated_date']
		ill=request.POST['major_illness']
		if not User.objects.filter(username=username).exists():
			messages.info(request,"Username must be same as your registered name!!")
		#if username!=request.session.get('username'):
			#messages.info(request,"Only you can register by your registeredname don't use other names!")'''

		else:
			result1=donorregister(username=username,age=age,gender=gender,city=city,address=address,contact=contact,email=email,servicetype=servicetype,donortype=donatetype,bloodgroup=bloodgroup,date=date,ill=ill)
			result1.save()
			messages.info(request,"Successfully registered as Donor")

			return redirect('base')
		

	return render(request,'myapp/donorreg.html')

@login_required(login_url='login')
def Base(request):
	return render(request,'myapp/base.html')

def Contactus(request):
	return render(request,'myapp/contactus.html')

def Faq(request):
	return render(request,'myapp/faq.html')


@login_required(login_url='login')	
def Donorinf(request):
	return render(request,'myapp/donorinf.html')

@login_required(login_url='login')
def Searchdonor(request):
	if request.method=="POST":
		#try:
		city=request.POST['search_city']
		grp=request.POST['blood_group']
		donortype=request.POST['donortype']
		#servicetype=request.POST['servicetype']
		request.session['searchedcity']=city
		request.session['searchedgroup']=grp
		request.session['searchedtype']=donortype
		#request.session['searchtype']=servicetype

		user=request.session.get('username')
		userdata=User.objects.get(username=user)
		
		
		if donorregister.objects.filter(city=city,donortype=donortype,bloodgroup=grp).exists():
			donordata=donorregister.objects.filter(city=city,donortype=donortype,bloodgroup=grp)
			today=date.today()
			d1=str(today)
			a,b,c=d1[0:4],d1[5:7],d1[8:]
			if d1[5]=='0':
				b=d1[6:7]
			if d1[8]=='0':
				c=d1[9]
				
			print(a,b,c)
			print("today:",d1)
				
			for i in donordata:
				if i.date:
					ldate=str(i.date)
					print(ldate)
					a1,b1,c1=ldate[0:4],ldate[5:7],ldate[8:]
					if ldate[5]=='0':
						b1=ldate[6:7]
					if ldate[8]=='0':
						c1=ldate[9]
					print(a1,b1,c1)
					print("regdate:",ldate)
					delta=date(int(a),int(b),int(c))-date(int(a1),int(b1),int(c1))
					diff=delta.days
					print(diff)
					if diff<=30:
						donorregister.objects.filter(username=i.username).update(lastdonation_eligibility='NotEligible')
					elif diff>30:
						donorregister.objects.filter(username=i.username).update(lastdonation_eligibility='Eligible')
			#donordata=donorregister.objects.filter(city=city,donortype=donortype,bloodgroup=grp).order_by('lastdonation_eligibility')

			donordata=donordata.filter(city=city,donortype=donortype,bloodgroup=grp).order_by('-date')
			donordata=donordata.filter(city=city,donortype=donortype,bloodgroup=grp).order_by('age')
			#donordata=donordata.filter(city=city,donortype=donortype,bloodgroup=grp).order_by('servicetype')




			context={'donordata':donordata,'userdata':userdata}
			return render(request,'myapp/donorinf.html',context)
		else:
			
			messages.info(request,"OOPS!! NO DONOR EXITS FOR YOUR REQUIREMENTS")
			return redirect('searchdonor')
			
		#except:
			#return redirect('searchdonor')
		
		
	return render(request,'myapp/searchdonor.html')

@login_required(login_url='login')
def Updatedonor(request):
	udonordata=donorregister.objects.get(username=request.session.get('username'))
	userdata=User.objects.get(username=request.session.get('username'))
	if request.method=="POST":
		username=request.POST.get('u_person_name')
		age=request.POST['u_age']
		gender=request.POST['u_gender']
		city=request.POST['u_city']
		address=request.POST['u_address']
		contact=request.POST['u_contact_number']
		email=request.POST['u_email']
		bloodgroup=request.POST['u_bloodgroup']
		date=request.POST['u_last_donated_date']
		print(date)
		ill=request.POST['u_major_illness']
		

		request.session['username']=username
		donorregister.objects.filter(username=udonordata.username).update(username=username,age=age,gender=gender,city=city,address=address,contact=contact,email=email,bloodgroup=bloodgroup,date=date,ill=ill)
		User.objects.filter(username=userdata.username).update(username=username)
		
		return redirect('profile')
	
	return render(request,'myapp/updatedonor.html',{'udonordata':udonordata})

@login_required(login_url='login')
def Profile(request):
	name=request.session.get('username')
	
	try:
		if donorregister.objects.get(username=name) is not None:
			prodata=donorregister.objects.get(username=name)
			return render(request,'myapp/profile.html',{'prodata':prodata})
	except:
		pass
	return render(request,'myapp/profile.html')

@login_required(login_url='login')
def Donorprofile(request,donorname):
	
	try:
		if donorregister.objects.get(username=donorname) is not None:
			donordata=donorregister.objects.get(username=donorname)
			return render(request,'myapp/donorprofile.html',{'donordata':donordata})
	except:
		pass
	return render(request,'myapp/donorprofile.html')


def Logout(request):
	user=request.session.get('username')
	logout(request)
	request.session.flush()
	messages.info(request,"You have been Logged Out!!")
	
	return redirect('login')

@login_required(login_url='login')
def Requests(request):
	
	if requests.objects.filter(donorname=request.session.get('username')) is not None:
		requestdata=requests.objects.filter(donorname=request.session.get('username'))

		return render(request,'myapp/requests.html',{'requestdata':requestdata})
	else:
		messages.info(request,"NO Requests!")


	return render(request,'myapp/requests.html')


@login_required(login_url='login')
def Myrequests(request):
	
	if requests.objects.filter(recievername=request.session.get('username')) is not None:
		requestdata=requests.objects.filter(recievername=request.session.get('username'))
		return render(request,'myapp/myrequests.html',{'requestdata':requestdata})
	else:
		messages.info(request,"NO Requests!")


	return render(request,'myapp/myrequests.html')


def Addrequest(request,donorname,donortype):
	user=request.session.get('username')
	userdata=User.objects.get(username=user)

	city=request.session.get('searchedcity')
	grp=request.session.get('searchedgroup')
	donortype=request.session.get('searchedtype')

	donordata=donorregister.objects.filter(city=city,donortype=donortype,bloodgroup=grp)
	context={'donordata':donordata,'userdata':userdata}
	if user==donorname:
		messages.info(request,"You Can Not Request Yourself!")
		return render(request,'myapp/donorinf.html',context)

	elif requests.objects.filter(donorname=donorname,recievername=userdata.username,requiredservice=donortype).exists():
		messages.info(request,"ALREADY REQUESTED THIS USER!")
		return render(request,'myapp/donorinf.html',context)
		
	else:
		addreq=requests(donorname=donorname,recievername=userdata.username,requiredservice=donortype)
		addreq.save()
		messages.info(request,"Successfully Requested!")
		return render(request,'myapp/donorinf.html',context)
	return render(request,'myapp/searchdonor.html')

def Barchart(request):
	citydict={}
	cities=[]
	ds=donorregister.objects.all()
	for i in ds:
		if i.city not in cities:
			cities.append(i.city)
		if i.city not in citydict.keys():
			citydict[i.city]=1
		else:
			citydict[i.city]=citydict[i.city]+1
	
	
	bloodcount=[]
	bloodlist=['O Positive','O Negative','A Positive','A Negative','B Positive','B Negative','AB Positive','AB Negative',]
	for i in bloodlist:
		qs=donorregister.objects.filter(bloodgroup=i).count()
		bloodcount.append(qs)
	
	chart1=getplot(bloodlist,bloodcount)
	chart2=getplot1(cities,list(citydict.values()))
	context={'chart1':chart1,'chart2':chart2}
		
	return render(request,'myapp/barchart.html',context)
	

def Deletereq(request,dname,rname,rservice,mode):
	deldata=requests.objects.get(donorname=dname,recievername=rname,requiredservice=rservice)
	print(deldata.status)
	if mode=='my':
		requests.objects.get(donorname=dname,recievername=rname,requiredservice=rservice).delete()
		messages.info(request,"Request Deleted Successfully!")

		return redirect('myrequests')
	elif mode=='out':
		if deldata.status=='Pending':
			print(deldata.status)
			requests.objects.filter(donorname=dname,recievername=rname,requiredservice=rservice).update(status='Rejected')

			messages.info(request,"Request was Rejeceted!")
		elif deldata.status=='Rejected':
			messages.info(request,"Already Rejeceted!")
		elif deldata.status=='Accepted':
			requests.objects.filter(donorname=dname,recievername=rname,requiredservice=rservice).update(status='Rejected')
			messages.info(request,"Request was Rejeceted!")



		return redirect('requests')

def Acceptreq(request,dname,rname,rservice):
	if donorregister.objects.get(username=rname):
		recieverdata=donorregister.objects.get(username=rname)
	else:
		recieverdata=User.objects.get(username=rname)
	reqdata=requests.objects.get(donorname=dname,recievername=rname,requiredservice=rservice)
	if reqdata is not None:
		if reqdata.status=="Accepted":
			messages.info(request,"Already Accepted!")
		else:
			requests.objects.filter(donorname=dname,recievername=rname,requiredservice=rservice).update(status="Accepted")
			'''messages.info(request,"Request Accepted!")
			subject="Blood donation"
			message=f"GoodNews! {rname}, some of your requests  are accepted on www.onlineblooddonation.comm plz visit website to view."
			from_email=settings.EMAIL_HOST_USER
			to=[recieverdata.email,]
			if subject and message and from_email:
				try:
					send_mail(subject, message, from_email,to)
					
				except:
					return HttpResponse('Invalid header found.')'''
	return redirect('requests')
	
def Bloodcamp(request):
	campdata=bloodcamp.objects.all()
	return render(request,'myapp/bloodcamp.html',{'campdata':campdata})