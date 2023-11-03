from django.urls import path, include
from .views import NewViews,FeedBackView,NewsByTagView

urlpatterns = [
    path('news',NewViews.getall,name='getAll'),
    path('news/post',NewViews.post,name='createnew'),
    path('new/<int:id>',NewViews.getone,name='getonenew'),
    path('delete/new/<int:id>',NewViews.delete,name='deletenew'),
    path('update/new/<int:id>',NewViews.update,name='updatenew'),
    path('feedback/create',FeedBackView.feedupdateorcreate,name='createfeedback'),
    path('views/add',FeedBackView.viewsupdate, name='viewscontroll'),
    path('newbytag/<int:id>', NewsByTagView.get, name='newsbytagsearch')
]