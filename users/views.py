import hashlib
from datetime import datetime
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from .models import *
from django.contrib import messages
from django.contrib.auth  import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, admin_only
from django.views import generic
from django.core.mail import send_mail
from django.contrib.messages.views import SuccessMessageMixin

from .forms import UserForm, ProfileForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .my_captcha import FormWithCaptcha



host = 'http://127.0.0.1:8000/'
admin_email = "muzahid.ccn@gmail.com"


# Create your views here.


def FeedBack(request):
    return render(request, 'feedback.html')


def profile(request):
    return render(request, 'profile.html')



class UserRegisterView(SuccessMessageMixin, generic.CreateView):
    template_name = "register.html"
    form_class = UserForm
    success_message = "Registered successfully !!!"
    error_message = "OOPS some error occurred !!!"

    def get_success_url(self):
        # messages.info(self, 'Registered Successfully :)')
        return reverse("users:login")

    def form_invalid(self, form):

        err=form.errors
        messages.error(self.request, err)
        return redirect('users:register')


    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user_email = user.email
        user.save()
        Profile.objects.create(
            user=user
        )

        new_msg = """
        <h4 class='m-0'>Congratulations!!
            CEO<br>
            Pfaccounts.com<br>
        <p>"""
        
        email_subject = "Your account is successfully crteated "
        from_email = admin_email
        to_email = user_email
        
        send_mail(
            email_subject,
            new_msg,
            from_email,
            [to_email],
            fail_silently=False,
            html_message=new_msg,
        )

        messages.success(self.request, 'Your account is created successfully and pending for activation on CCN Head')
        return HttpResponseRedirect(self.request.path_info)




@login_required
def accountSettings(request):
	user = request.user.profile
	form = ProfileForm(instance=user)

	if request.method == 'POST':
		form = ProfileForm(request.POST, request.FILES,instance=user)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'admin/account_settings.html', context)




#  WORKING PERFECTLY

# def update_profile(request):
#     division_list = Division.objects.all().order_by('division_name')
#     if request.method == 'POST':
#         user_form = UserForm(request.POST)
#         if user_form.is_valid():
#             user_form.save()
#             messages.info(request, 'Registered Successfully :)')
#             return redirect('users:login')
#         else:
#             messages.info(request, 'Error, Something went wrong !!')
#     else:
#         user_form = UserForm()
#     return render(request, 'register.html', {
#         'user_form': user_form,
#         'division_list':division_list,
#     })




# def registration_view(request):

#     division_list = Division.objects.all().order_by('division_name')
#     if request.method == 'POST':
#         username = request.POST['username']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         email = request.POST['email']
#         division_nameId = int(request.POST['division_name'])

#         division_name = Division.objects.get(id=division_nameId)

#         #encripted_pass = hashlib.md5(user_password.encode())
#         #password = encripted_pass.hexdigest() 
#         username_check = User.objects.filter(username =username ) 
#         email_check = User.objects.filter(email =email) 
#         if username_check.exists():
#             messages.error(request, "Username already exists")
#         elif email_check.exists():
#             messages.error(request, "Email already exists")
#         else:
#             messages.error(request, "Email already exists")
#             user = User.objects.create(username=username, password1=password1, password2=password2, first_name=first_name,last_name=last_name, email= email)
#             messages.success(request, "Signup Completed. Please check your email to Activate your account.")
#             return redirect('users:login')
            
#     context = {
#         'division_list':division_list
#     }
#     return render(request,'register.html',context)



# class register(CreateView):
#     model = User
#     form_class = CustomerSignUpForm
#     template_name = 'register.html'
    

#     def get_context_data(self, **kwargs):
#         context = super(register, self).get_context_data(**kwargs)
#         context['division'] = Division.objects.all()
#         return context


#     def form_valid(self, form):
#         user = form.save()
#         return redirect('/login/')

# class employee_register(CreateView):
#     model = User
#     form_class = EmployeeSignUpForm
#     template_name = 'mytemplates/employee_register.html'

#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('/')









@unauthenticated_user
def UserLogin(request):
    #context = RequestContext(request)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
                
        user = authenticate(request, username=username, password=password)
            
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/dashboard/')
            else:
                messages.error(request, 'Your account is not activated by CCN Head !!')
                return HttpResponse("You're account is disabled.")

        else:
            messages.error(request, 'Username or Password is incorrect !!')

    context = {
        "captcha": FormWithCaptcha,
    }
    return render(request, 'login.html', context)

def UserLogOut(request):
    logout(request)
    return redirect('/login/')    

def MyCustomer(request):
    return render(request, 'customer.html')


# @unauthenticated_user
# def UserRegistration(request):
#     form = CreateUserForm()
#     if request.method =='POST':
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             user = form.save()
            
#             username = form.cleaned_data.get('username')
#             messages.success(request, 'Registered Successfully ! ' + username)
#             return redirect('/login/')
    
#     context = {'form':form}
#     return render(request, 'registration.html', context)

@admin_only
def home(request):
    return render(request, 'index.html')

@login_required
def Dashboard(request):
    return render(request, 'dashboard.html')




@login_required
def UsersList(request):
    user_list = User.objects.all().order_by('first_name')
    context = {
        'user_list':user_list
    }
    return render(request, 'admin/user_list.html',context)




@login_required
def UserActive(request, id):
    user_ob = User.objects.get(id = id)
    user_ob.status = True
    user_ob.save() 
    messages.success(request, "User status changed uccessfully")
    return redirect("users:users-list") 


@login_required
def UserDeactive(request, id):
    user_ob = User.objects.get(id = id)
    user_ob.status = False
    user_ob.save() 
    messages.success(request, "User status changed uccessfully")
    return redirect("users:users-list")















@login_required
def add_division(request):
    if request.method == 'POST':
        division = request.POST['division'] 
        Division.objects.create(division_name=division)
        messages.success(request, "division Added Successfully")
    return render(request,'admin/add_division.html')


@login_required
def division_list(request):
    division_list = Division.objects.all().order_by('division_name')
    context = {
        'division_list':division_list
    }
    return render(request, 'admin/division_list.html',context)

@login_required
def division_edit(request, id):
    division = Division.objects.filter(id = id) 
    old_name = division[0].division_name
    if request.method == 'POST':
        division_name = request.POST['division']
        division.update(division_name = division_name)  
        messages.success(request, "Division updated successfully")
        return redirect("users:division_list") 
    context = {
        'division_name':old_name
    }
    return render(request,'admin/edit_division.html',context)

@login_required
def division_active(request, id):
    division = Division.objects.get(id = id)
    division.status = True
    division.save() 
    messages.success(request, "Division status changed successfully")
    return redirect("users:division_list") 


@login_required
def division_deactive(request, id):
    division = Division.objects.get(id = id)
    division.status = False
    division.save() 
    messages.success(request, "division status changed uccessfully")
    return redirect("users:division_list")







@login_required
def add_jobcard(request):
    problem_category = ProblemCategory.objects.filter(status=True)
    if request.method == 'POST':
        problemcategory = request.POST['problemcategory']
        user_no = request.user.username
        division_name = request.user.division
        problem = request.POST['problem']

        print(problemcategory)
        print(problem)

        if problemcategory == '2':
            issue_in = request.POST['issue_in']
            problem = request.POST['problem']
            ccn_jobb = CcnJobCard.objects.create(user_no=user_no, problemcategory=problemcategory, division=division_name)
            InternetJobCard.objects.create(ccn_internet=ccn_jobb, issue_in=issue_in, problem=problem)
            messages.success(request, "Internet JobCard Added Successfully")
            
        elif problemcategory == '3':
            printer_make = request.POST['printer_make']
            model_no = request.POST['model_no']
            problem = request.POST['problem']
            ccn_job = CcnJobCard.objects.create(user_no=user_no, problemcategory=problemcategory, division=division_name)
            PrinterJobCard.objects.create(ccn_job_card=ccn_job, printer_make=printer_make, model_no=model_no, problem=problem)
            messages.success(request, "Printer JobCard Added Successfully")

            

        else:
            messages.success(request, "else block")



    context = {
        'problem_category':problem_category,
    }    
    return render(request,'jobcard/add_jobcard.html', context)


@login_required
def TraceJobCard(request, id):
    jb_cr = CcnJobCard.objects.filter(id=id)
    context = {
        'jb_cr':jb_cr,
    }

    return render(request, 'jobcard-tracking.html', context)



def load_printers(request):
    programming_id = request.GET.get('programming')
    printer_list = Printer.objects.filter(printer_id=programming_id)
    return render(request, 'printers-name-list.html', {'printer_list': printer_list})




@login_required
def CcnJobCardList(request):
    jobcard_list = CcnJobCard.objects.order_by("-id") & CcnJobCard.objects.filter(job_on="Engineer") | CcnJobCard.objects.filter(job_on="CCN Head")
    p = Paginator(jobcard_list, 10)

    page_num = request.GET.get('page', 1)

    try:
        page = p.page(page_num)
    except:
        page = p.page(1)

    context = {
        'jobcard_list':page
    }
    return render(request, 'jobcard/jobcard_list-of-head-ccn.html',context)

# @login_required
# def jobcard_edit(request, id):
#     jobcard = CcnJobCard.objects.filter(id = id) 
#     old_name = jobcard[0].jobcard_name
#     if request.method == 'POST':
#         division_name = request.POST['division']
#         division.update(division_name = division_name)  
#         messages.success(request, "jobcard updated uccessfully")
#         return redirect("users:jobcard_list") 
#     context = {
#         'jobcard_name':old_name
#     }
#     return render(request,'admin/edit_jobcard.html',context)


@login_required
def jobcard_active(request, id):
    jobcard = CcnJobCard.objects.get(id = id)
    jobcard.status = True
    jobcard.save() 
    messages.success(request, "jobcard status changed uccessfully")
    return redirect("users:jobcard_list") 


@login_required
def jobcard_deactive(request, id):
    jobcard = CcnJobCard.objects.get(id = id)
    jobcard.status = False
    jobcard.save() 
    messages.success(request, "jobcard status changed uccessfully")
    return redirect("users:jobcard_list")    



@login_required
def add_jobcard_problem(request):
    if request.method == 'POST':
        problem_name = request.POST['problem_name']
        ProblemCategory.objects.create(problem_name=problem_name)
        messages.success(request, "Type of Problem Added Successfully")
        return redirect("users:jobcard-problem-list") 
    return render(request,'admin/add_jobcard_problem.html')


@login_required
def jobcard_problem_list(request):
    p_list = ProblemCategory.objects.all()
    context = {
        'p_list':p_list
    }
    return render(request, 'admin/jobcard_problem_list.html',context)

@login_required
def jobcard_problem_edit(request, id):
    jobcard = ProblemCategory.objects.filter(id = id) 
    old_name = jobcard[0].jobcard_name
    if request.method == 'POST':
        division_name = request.POST['division']
        division.update(division_name = division_name)  
        messages.success(request, "jobcard updated uccessfully")
        return redirect("users:jobcard_list") 
    context = {
        'jobcard_name':old_name
    }
    return render(request,'admin/jobcard_problem_edit.html',context)



@login_required
def jobcard_problem_active(request, id):
    jobcard = ProblemCategory.objects.get(id = id)
    jobcard.status = True
    jobcard.save() 
    messages.success(request, "Type of Problem status changed successfully")
    return redirect("users:jobcard-problem-list") 


@login_required
def jobcard_problem_deactive(request, id):
    jobcard = ProblemCategory.objects.get(id = id)
    jobcard.status = False
    jobcard.save() 
    messages.success(request, "Type of Problem status changed successfully")
    return redirect("users:jobcard-problem-list")







@login_required
def job_card_on_user_head(request):
    division_jobcards = CcnJobCard.objects.filter(division=request.user.division).order_by('-id') & CcnJobCard.objects.filter(job_on="User Head").order_by('-id')

    pp = Paginator(division_jobcards, 15)

    page_numm = request.GET.get('page', 1)

    try:
        page = pp.page(page_numm)
    except:
        page = pp.page(1)

    
    context = {
        'j_list':page
    }
    return render(request,'jobcard/job-card-on-user-head.html',context) 




@login_required
def jobcard_approved(request, id):
    job = CcnJobCard.objects.get(id = id)
    job.job_on = 'CCN Head'
    job.forwareded_to_ccn_head_date = timezone.now()
    job.save() 
    messages.success(request, "Jobcard Approved & forwarded to CCN HEAD successfully !!")
    return redirect("users:job-card-on-user-head")


@login_required
def jobcard_rejected(request, id):
    job = CcnJobCard.objects.get(id = id)
    job.status = True
    job.save() 
    messages.success(request, "Jobcard rejected !!")
    return redirect("users:job-card-on-user-head")
    
@login_required
def JobForarded(request):
    division_jobcards = CcnJobCard.objects.filter(division=request.user.division)
    approved_list = CcnJobCard.objects.filter()
    context = {
        'division_jobcards':division_jobcards
        }
    return render(request, 'jobcard/jobcard_approved_list.html', context)


@login_required
def jobcard_view(request, id):
    job_view = CcnJobCard.objects.get(id=id)
    context = {
        'job_view':job_view
    }    
    return render(request, 'jobcard/jobcard-view.html',context)




# User Jobcard views

@login_required
def user_submitted_jobcard(request):

    user_jobcard_list = CcnJobCard.objects.filter(user_no=request.user.username).order_by('-id')

    pp = Paginator(user_jobcard_list, 10)

    page_numm = request.GET.get('page', 1)

    try:
        page = pp.page(page_numm)
    except:
        page = pp.page(1)

    context = {
        'user_jobcard_list':page
    }
    return render(request,'jobcard/user-submitted-jobcard.html',context) 




# CCN Head 


@login_required
def jobcard_pending_ccn_head(request):
    engineer_list = User.objects.filter(is_engineer=True)
    user_jobcard_list = CcnJobCard.objects.filter(job_on="CCN Head").order_by('-id')
    if request.method == "POST":
        job_id = request.POST['job_id']
        jobc = CcnJobCard.objects.get(id=job_id)
        jobc.assigned_to = request.POST['assigned_to']
        jobc.job_on = 'Engineer'
        jobc.ccn_head_to_engg_date = timezone.now()
        jobc.save() 
        messages.success(request, "Jobcard forwarded to an engineer !!")
    context = {
        'engineer_list':engineer_list,
        'p_ccn_jobcard_list':user_jobcard_list
    }
    return render(request,'jobcard/jobcard-pending-ccn-head.html',context) 





# Engineer    


@login_required
def jobcard_pending_on_engineer(request):
    pending_to_engineer = CcnJobCard.objects.order_by('-id') & CcnJobCard.objects.filter(status=False) & CcnJobCard.objects.filter(assigned_to=request.user.username) & CcnJobCard.objects.filter(job_on="Engineer")

    pp = Paginator(pending_to_engineer, 10)

    page_numm = request.GET.get('page', 1)

    try:
        page = pp.page(page_numm)
    except:
        page = pp.page(1)

    context = {
        'pending_to_engineer':page
    }
    return render(request,'jobcard/jobcard-pending-on-engineer.html',context) 



@login_required
def EngineerCommentsOnJobcard(request, id):

    engg_update = CcnJobCard.objects.filter(id = id)
    context = {
        'engg_update':engg_update
    }
    return render(request, 'jobcard/engineer-comments-on-jobcard.html', context)

@login_required
def EngineerCommentsOnJobcardForm(request):
    if request.method == "POST":
        jobb_id = request.POST['jobb_id']
        engg_comment = request.POST['engg_comment']
        jobc = CcnJobCard.objects.get(id=jobb_id)
        jobc.status = True
        jobc.engg_comment = engg_comment
        jobc.engg_task_complete_date = timezone.now()
        jobc.save() 
        messages.success(request, "Task Completed !!")
        return redirect("users:jobcard_pending_on_engineer")



@login_required
def AllJobCardsEngineer(request):
    engg_all = CcnJobCard.objects.filter(assigned_to=request.user.username).order_by('-id')

    pp = Paginator(engg_all, 10)

    page_numm = request.GET.get('page', 1)

    try:
        page = pp.page(page_numm)
    except:
        page = pp.page(1)

    context = {
        'engg_all':page
    }
    return render(request,'jobcard/all-jobcards-of-engineer.html',context) 





