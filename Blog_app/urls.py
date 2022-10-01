from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('About', views.About, name='About'),
    path('Blogs', views.Blogs, name='Blogs'),
    path('Contact', views.Contact, name='Contact'),
    path('Dashboard', views.Dashboard, name='Dashboard'),
    path('View_blog', views.View_blog, name='Blog'),
    path('Edit_Blog/<int:blog_id>', views.Blogcontent.Edit_Blog, name='Edit_Blog'),
    path('delete_blog/<int:blog_id>', views.Blogcontent.delete_blog, name='Delete Blog'),
    path('Write_Blog', views.Blogcontent.Write_Blog, name='Edit_Blog'),
    path('UpdatePic/<int:blog_id>', views.Blogcontent.UpdatePic, name='UpdatePic'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('send_message', views.sendmail, name='send_message'),
    path('Read_Blog/<int:blog_id>', views.Read_Blog, name='Read_Blog'),
    # path('register', views.register, name='register'),
    path('changeprofile/<int:User_id>', views.UpdateProfile.changedata, name='register'),
    path('UpdateProPic/<int:User_id>', views.UpdateProfile.changeprofilepic, name='register'),

]