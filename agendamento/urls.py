from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'agendamento'

urlpatterns = [
    path('', views.home, name='home'),
    path('horarios/<int:instrumento_id>/', views.lista_horarios, name='lista_horarios'),
    path('minha-area/', views.minha_area, name='minha_area'),

    # Rotas do Carrinho
    path('carrinho/', views.ver_carrinho, name='ver_carrinho'),
    path('carrinho/adicionar/<int:horario_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/remover/<str:item_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('carrinho/item-adicionado/', views.sucesso_adicao_carrinho, name='sucesso_adicao_carrinho'),

    # Rotas de Matrícula
    path('checkout/', views.checkout, name='checkout'),
    path('confirmar-pagamento/', views.confirmar_pagamento, name='confirmar_pagamento'),
    
    # ROTA ANTIGA REMOVIDA E NOVA ADICIONADA
    path('pagamento-sucesso/', views.pagamento_sucesso, name='pagamento_sucesso'),

    # Rotas de Aula Experimental
    path('aula-experimental/', views.agendar_aula_experimental, name='agendar_aula_experimental'),
    path('aula-experimental/detalhe/<int:pk>/', views.detalhe_aula_experimental, name='detalhe_aula_experimental'),
    path('aula-experimental/confirmar/<int:pk>/', views.confirmar_aula_experimental, name='confirmar_aula_experimental'),
    path('aula-experimental/sucesso/', views.sucesso_aula_experimental, name='sucesso_aula_experimental'),

    # Rotas de Autenticação
    path('cadastro/', views.pagina_cadastro, name='pagina_cadastro'),
    path('login/', auth_views.LoginView.as_view(template_name='agendamento/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]