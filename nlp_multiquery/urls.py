from django.contrib import admin
from django.urls import path,include
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mahasiswa_operation/<int:id>', views.mahasiswaOperation),
    path('mahasiswa_add', views.mahasiswaAdd),
    path('mahasiswa_all', views.mahasiswaAll),
    path('freq_operation/<int:id>', views.freqOperation),
    path('freq_add', views.freqAdd),
    path('freq_all', views.freqAll),
    path('nilai_operation/<int:id>', views.nilaiOperation),
    path('nilai_add', views.nilaiAdd),
    path('nilai_all', views.nilaiAll),
    path('preprocessing', views.preprocessingProses),
    path('parsing', views.parsingWordProses),
    path('translator', views.translatorProses),
    path('evaluator', views.pragmatikProses),
    path('eksekusiQuery',views.eksekusiQuery),
    path('main', views.mainProses)
]
