from django.urls import path
from enroll import views

urlpatterns = [
    path('add', views.add, name="add"),
    path('show', views.show, name="show"),
    path('delete/<int:id>/', views.delete_data, name="deletedata"),
    path('<int:id>/', views.update_data, name="updatedata"),
    path('complete/<task_id>', views.complete_task, name='complete_task'),
    path('pending/<task_id>', views.pending_task, name='pending_task'),
    path('dash', views.dashboard, name="dashboard"),


]