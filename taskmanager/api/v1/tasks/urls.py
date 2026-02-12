from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserTaskList, UpdateTaskStatus, TaskReportView

urlpatterns = [
    path('login/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('tasks/', UserTaskList.as_view()),
    path('tasks/<uuid:pk>/', UpdateTaskStatus.as_view()),
    path('tasks/<uuid:pk>/report', TaskReportView.as_view()),
]
