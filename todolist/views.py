
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import smtplib
import os
from email.mime.text import MIMEText
from .forms import TaskForm, RegisterForm, EditTaskForm, ContactForm
from .models import AddItem
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.shortcuts import render, redirect



def register_form(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})



def login_form(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            error_message = "Invalid username or password."
            return render(request, "login.html", {"error_message": error_message})

    return render(request, "login.html")


@login_required(login_url='login')
def task_form(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = AddItem(
                text=form.cleaned_data['name'],
                due_date=form.cleaned_data['date'],
                picture=form.cleaned_data.get('image'),
                user=request.user
            )
            task.save()
            return redirect('index')
    else:
        form = TaskForm()

    return render(request, "todolist/edit.html", {"form": form})


def edit_task(request,part_id=None):
    if part_id is None:
        return redirect('index')

    _object = AddItem.objects.get(pk=part_id)
    if request.method == "POST":
         form = EditTaskForm(request.POST,request.FILES, instance=_object)
         if form.is_valid():
             form.save()
             return redirect('index')

    else:
        form = EditTaskForm(instance=_object)

    return render(request, "todolist/edit_task.html", {"form": form,"part_id": part_id})

@login_required(login_url='login')
def delete_view(request,part_id=None):
    if part_id is None:
        return redirect("index")

    _object=AddItem.objects.get(pk=part_id)
    _object.delete()
    render(request,'todolist/index.html')
    return redirect('index')


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return render(request, 'todolist/logout.html')

def change_confirmation_view(request,part_id=None):
    if part_id is None:
        return redirect("index")

    _object=AddItem.objects.get(pk=part_id)
    _object.completed = not _object.completed
    _object.save()
    render(request,'todolist/index.html')
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required(login_url='login')
def about_view(request):
    form = ContactForm(request.POST)

    if request.method == "POST":
        if request.user.is_authenticated:
            # Get authenticated user's email and username
            email_name = request.user.email
            name = request.user.username
        else:
            # Handle case when the user is not authenticated
            email_name = "Anonymous"
            name = "Guest"

        if form.is_valid():
            print("Valid form")

            # Get cleaned data from the form
            message = form.cleaned_data['message']
            print("Form data retrieved")

            email_user = "chiras.to.do.list@gmail.com"
            email_password = os.getenv('EMAIL_HOST_PASSWORD')  # Ensure the App Password is set


                # Create the SMTP connection
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()  # Encrypt connection
                server.login(email_user, email_password)

                # Create email message
                msg = MIMEText(message)
                msg["Subject"] = f"New contact from {name} ({email_name})"
                msg["From"] = email_user
                msg["To"] = email_user  # Send to your email address

                redirect("index")

                server.sendmail(email_user, email_user, msg.as_string())

                # Redirect or render a success page
                return redirect("index")



    # Render the contact form page
    return render(request, 'todolist/about.html', {"form": form})


class all_to_do(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = AddItem
    template_name = "todolist/index.html"

    def get_queryset(self):
        return AddItem.objects.filter(user=self.request.user).order_by('due_date')


class completed_view(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = AddItem
    template_name = "todolist/completed.html"

    def get_queryset(self):
        return AddItem.objects.filter(user=self.request.user)


class incomplete_view(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = AddItem
    template_name = "todolist/incomplete.html"

    def get_queryset(self):
        return AddItem.objects.filter(user=self.request.user)


class home_view( TemplateView):
    template_name = "todolist/home.html"



