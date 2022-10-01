from email.message import Message
from django.http import request
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.utils.html import strip_tags
from Blog_app.models import Blog, Profile
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required

# Create your views here.


def About(request):
    try:
        user_info = User.objects.filter(is_staff=1, is_superuser=0)[0]
        profile_info = Profile.objects.get(user_id=user_info.id)
        return render(request, "About.html", {"user_data": user_info, "profile": profile_info})
    except:
        messages.info(request, f"Some Error occured!")
        return redirect('/')


def Blogs(request):
    blog_con = Blog.objects.all()[::-1]
    return render(request, "blogs.html", {"blogs": blog_con})


def Contact(request):
    return render(request, "Contact.html")


@login_required(login_url='/login')
def Dashboard(request):
    profile_id = Profile.objects.get(user_id=request.user)
    blog = Blog.objects.all()[::-1]
    return render(request, "Dashboard.html", {"profile": profile_id, "blog_con": blog})


def View_blog(request):
    return render(request, "New_BLog.html")


def index(request):
    blog_con = Blog.objects.all()[::-1]
    return render(request, "index.html", {"blogs": blog_con})


def login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else: 
        if request.method == 'POST':
            USER_ID = request.POST['inputemail']
            password = request.POST['Password']
            user = auth.authenticate(username=USER_ID, password=password)
            if user is not None and user.is_staff == 1:
                auth.login(request, user)
                return redirect("Dashboard")
            else:
                messages.info(request, 'Invalid Username or Password')
                return redirect('/login')
        else:
            return render(request, 'Login.html')


@login_required(login_url='/login')
def logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['fname'].capitalize()
        last_name = request.POST['lname'].capitalize()
        user_name = request.POST['username']
        user_email = request.POST['inputemail']
        user_password1 = request.POST['Password']
        user_password2 = request.POST['conPassword']
        if user_password1 == user_password2:
            if User.objects.filter(email=user_email).exists():
                messages.alert(request, "User Name alredy registerd")
                return redirect("/Registration")
            elif User.objects.filter(username=user_name).exists():
                messages.alert(request, "User Name alredy registerd")
                return redirect("/register")
            else:
                user = User.objects.create_user(
                    username=user_name, first_name=first_name, last_name=last_name, email=user_email, password=user_password1)
                user.save()
                user1 = User.objects.get(username=user_name)
                user_profile = Profile(user_id=user1.id, )
                user_profile.save()
                messages.success(request, 'Yor are registerd Succesfully')
                return redirect("/login")
        else:
            messages.warning(request, "Password is not matching")
            return redirect("/register")
    else:
        return render(request, "register.html")


@login_required(login_url='/login')
class UpdateProfile():
    @login_required(login_url='/login')
    def changedata(request, User_id):
        if request.method == 'POST':
            fname = request.POST['fname']
            lname = request.POST['lname']
            u_email = request.POST['email']
            bio = request.POST['bio']
            fblink = request.POST['fb']
            inlink = request.POST['in']
            twkink = request.POST['tw']
            gmlink = request.POST['gm']
            contact = request.POST['contact']
            # updating user tabel
            user_data = User.objects.get(id=User_id)
            user_data.first_name = fname
            user_data.last_name = lname
            user_data.email = u_email
            user_data.save()
            # Updating Profile data
            prof_data = Profile.objects.get(user_id=User_id)
            prof_data.bio = bio
            prof_data.fblink = fblink
            prof_data.twlink = twkink
            prof_data.inlink = inlink
            prof_data.gmlink = gmlink
            prof_data.contect = contact
            prof_data.save()
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.info(request, 'Your Changes are saved succesfully')
            return redirect("/")

    @login_required(login_url='/login')
    def changeprofilepic(request, User_id):
        if request.method == "POST":
            pro_img = request.FILES['image']
            prof_data = Profile.objects.get(user_id=User_id)
            prof_data.profile_img = pro_img
            prof_data.save()
            messages.info(request, 'Profle picture is updated succefully')
            return redirect(request.META['HTTP_REFERER'])


def Read_Blog(request, blog_id):
    blog_con = Blog.objects.get(id=blog_id)
    return render(request, "Read_Blog.html", {"content": blog_con})


class Blogcontent():
    # Function For Addin new Blog
    @login_required(login_url='/login')
    def Write_Blog(request):
        if request.method == "POST":
            blog_title = request.POST['blog_title']
            blog_description = request.POST['blog_description']
            blog_content = request.POST['blog_content']
            blog_image = request.FILES['image']
            userid = request.POST['userid']
            save_blog = Blog(blog_title=blog_title, short_desc=blog_description,
                                 main_content=blog_content, b_image=blog_image, user_id=userid)
            save_blog.save()
            messages.info(request, "Blog Is Saved Successfully")
            return redirect("/Dashboard")
        else:
            return render(request, "Write_Blog.html")
        # Function For Editing The Blog

    @login_required(login_url='/login')
    def Edit_Blog(request, blog_id):
        if request.method == "POST":
            Blog_title = request.POST['blog_title']
            blog_description = request.POST['blog_description']
            blog_content = request.POST['blog_content']
            edit_blog = Blog.objects.get(id=blog_id)
            edit_blog.blog_title = Blog_title
            edit_blog.short_desc = blog_description
            edit_blog.main_content = blog_content
            edit_blog.save()
            messages.info(request, f"Blog - '{edit_blog.blog_title}' is eddited Successfully!")
            return redirect('/Dashboard')
        else:
            retrive_blog = Blog.objects.get(id=blog_id)
            return render(request, "Edit_Blog.html", {"retrive_block": retrive_blog})

        # Function For changing the Blog Pic
    @login_required(login_url='/login')
    def UpdatePic(request, blog_id):
        if request.method == "POST":
            blog_image = request.FILES['image']
            blog_imageget = Blog.objects.get(id=blog_id)
            blog_imageget.b_image = blog_image
            blog_imageget.save()
            messages.info(request, f"Image  '{blog_image}' of blog - '{blog_imageget.blog_title}' is changed Successfully")
            return render(request, "Edit_Blog.html", {"retrive_block": blog_imageget})
        else:
            retrive_blog = Blog.objects.get(id=blog_id)
            return render(request, "Edit_Blog.html", {"retrive_block": retrive_blog})

    @login_required(login_url='/login')
    def delete_blog(request, blog_id):
        blog = Blog.objects.get(id=blog_id)
        blog_title = blog.blog_title
        blog.delete()
        messages.info(request, f"Blog '{blog_title}' is deleted Successfully")
        return redirect('/Dashboard')


def sendmail(request):
    if request.method == 'POST':
        user_name = request.POST['name']
        user_email = request.POST['email']
        user_message = request.POST['message']
        html_content = render_to_string('About.html', {'email': user_email, 'name': user_name, 'message': user_message, 'time': timezone.now()})
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives('Message from user', settings.EMAIL_HOST_USER, user_email)
        email.attach_alternative(text_content, 'text/html')
        email.send()
        return render(request, "About.html")
