from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.forms import formset_factory
import secrets
from .forms import RegistrationForm, ConvidadoForm
from .models import Instrumento, HorarioDisponivel, Matricula, Cliente, VagaAulaExperimental, Configuracao
from .cart import Cart

def home(request):
    request.session['enrollment_mode'] = 'group'
    instrumentos = Instrumento.objects.all()
    contexto = {'instrumentos': instrumentos}
    return render(request, 'agendamento/home.html', contexto)

@login_required
def lista_horarios(request, instrumento_id):
    if request.GET.get('fluxo') == 'individual':
        request.session['enrollment_mode'] = 'individual'
    elif 'enrollment_mode' not in request.session:
        request.session['enrollment_mode'] = 'individual'
    instrumento = get_object_or_404(Instrumento, pk=instrumento_id)
    todos_horarios = HorarioDisponivel.objects.filter(instrumento=instrumento)
    horarios_com_vagas = []
    cart = Cart(request)
    for horario in todos_horarios:
        matriculas_ativas = Matricula.objects.filter(horario=horario, ativo=True).count()
        slots_no_carrinho = 0
        for item in cart:
            if item['horario'].id == horario.id:
                slots_no_carrinho += 1
        vagas_restantes = horario.capacidade - matriculas_ativas - slots_no_carrinho
        if vagas_restantes > 0:
            horario.vagas_restantes = vagas_restantes
            horarios_com_vagas.append(horario)
    contexto = {'instrumento': instrumento, 'horarios': horarios_com_vagas}
    return render(request, 'agendamento/lista_horarios.html', contexto)

@login_required
def adicionar_ao_carrinho(request, horario_id):
    cart = Cart(request)
    horario = get_object_or_404(HorarioDisponivel, id=horario_id)
    matriculas_oficiais = Matricula.objects.filter(horario=horario, ativo=True).count()
    slots_no_carrinho = 0
    for item in cart:
        if item['horario'].id == horario.id:
            slots_no_carrinho += 1
    vagas_reais_disponiveis = horario.capacidade - matriculas_oficiais - slots_no_carrinho
    if vagas_reais_disponiveis > 0:
        cart.add(horario=horario)
        mode = request.session.get('enrollment_mode', 'individual')
        if mode == 'group':
            return redirect('agendamento:sucesso_adicao_carrinho')
        else:
            return redirect('agendamento:checkout')
    else:
        messages.error(request, 'Não foi possível adicionar. Este horário não possui mais vagas disponíveis!')
        return redirect('agendamento:lista_horarios', instrumento_id=horario.instrumento.id)

@login_required
def remover_do_carrinho(request, item_id):
    cart = Cart(request)
    cart.remove(item_id)
    return redirect('agendamento:ver_carrinho')

@login_required
def ver_carrinho(request):
    cart = Cart(request)
    return render(request, 'agendamento/carrinho.html', {'cart': cart})

def pagina_cadastro(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            new_user = User.objects.create_user(
                username=dados['email'], email=dados['email'], password=dados['password'],
                first_name=dados['first_name'], last_name=dados['last_name']
            )
            Cliente.objects.create(
                user=new_user, celular=dados['celular'], data_nascimento=dados.get('data_nascimento')
            )
            return redirect('agendamento:login')
    else:
        form = RegistrationForm()
    contexto = {'form': form}
    return render(request, 'agendamento/cadastro.html', contexto)

@login_required
def minha_area(request):
    cliente = None
    matriculas = []
    aulas_experimentais = []
    try:
        cliente = Cliente.objects.get(user=request.user)
        matriculas = Matricula.objects.filter(aluno=cliente, ativo=True)
        aulas_experimentais = VagaAulaExperimental.objects.filter(aluno=cliente, status='AGENDADA')
    except Cliente.DoesNotExist:
        pass
    contexto = {
        'cliente': cliente, 'matriculas': matriculas, 'aulas_experimentais': aulas_experimentais
    }
    return render(request, 'agendamento/minha_area.html', contexto)

@login_required
def checkout(request):
    cart = Cart(request)
    cliente = get_object_or_404(Cliente, user=request.user)
    convidados = [item for item in cart if item['tipo'] == 'convidado']
    num_convidados = len(convidados)
    ConvidadoFormSet = formset_factory(ConvidadoForm, extra=num_convidados)
    formset = ConvidadoFormSet()
    taxa_matricula = 0
    config = Configuracao.objects.first()
    if not cliente.pagou_taxa_matricula:
        taxa_matricula = config.valor_taxa_matricula if config else 0
    total_mensalidades = cart.get_total_price()
    total_final = total_mensalidades + taxa_matricula
    contexto = {
        'cart': cart, 'taxa_matricula': taxa_matricula, 'total_final': total_final,
        'formset': formset, 'convidados': convidados,
    }
    return render(request, 'agendamento/checkout.html', contexto)

@login_required
def confirmar_pagamento(request):
    if request.method != 'POST':
        return redirect('agendamento:checkout')

    cart = Cart(request)
    organizador = get_object_or_404(Cliente, user=request.user)
    
    item_organizador = next((item for item in cart if item['tipo'] == 'organizador'), None)
    convidados_itens = [item for item in cart if item['tipo'] == 'convidado']
    num_convidados = len(convidados_itens)

    # Lógica do formset só é executada se houver convidados
    if num_convidados > 0:
        ConvidadoFormSet = formset_factory(ConvidadoForm, extra=num_convidados)
        formset = ConvidadoFormSet(request.POST)
        if not formset.is_valid():
            messages.error(request, "Por favor, corrija os erros no formulário dos convidados.")
            # No futuro, podemos renderizar o checkout com os erros. Por enquanto, um redirect simples.
            return redirect('agendamento:checkout')
        
        # Se o formset for válido, cria os usuários e matrículas para os convidados
        for i, form in enumerate(formset):
            dados_convidado = form.cleaned_data
            item_convidado = convidados_itens[i]
            
            novo_usuario_convidado = User.objects.create_user(
                username=dados_convidado['email'], email=dados_convidado['email'], password=dados_convidado['password'],
                first_name=dados_convidado['first_name'], last_name=dados_convidado['last_name']
            )
            novo_cliente_convidado = Cliente.objects.create(
                user=novo_usuario_convidado, celular=dados_convidado['celular'],
                data_nascimento=dados_convidado.get('data_nascimento')
            )
            Matricula.objects.create(aluno=novo_cliente_convidado, horario=item_convidado['horario'], status_pagamento_mes_atual='PAGO', ativo=True)

    # A matrícula do organizador é criada independentemente de haver convidados
    if item_organizador:
        Matricula.objects.create(aluno=organizador, horario=item_organizador['horario'], status_pagamento_mes_atual='PAGO', ativo=True)

    # Lógica final de pagamento e limpeza
    if not organizador.pagou_taxa_matricula:
        organizador.pagou_taxa_matricula = True
        organizador.save()
    
    cart.clear()
    if 'enrollment_mode' in request.session:
        del request.session['enrollment_mode']
        
    return redirect('agendamento:pagamento_sucesso')


def pagamento_sucesso(request):
    return render(request, 'agendamento/pagamento_sucesso.html')

@login_required
def agendar_aula_experimental(request):
    vagas_disponiveis = VagaAulaExperimental.objects.filter(status='DISPONIVEL')
    contexto = {'vagas': vagas_disponiveis}
    return render(request, 'agendamento/aula_experimental.html', contexto)

@login_required
def detalhe_aula_experimental(request, pk):
    vaga = get_object_or_404(VagaAulaExperimental, pk=pk)
    contexto = {'vaga': vaga}
    return render(request, 'agendamento/detalhe_aula_experimental.html', contexto)

@login_required
def confirmar_aula_experimental(request, pk):
    vaga = get_object_or_404(VagaAulaExperimental, pk=pk)
    cliente = get_object_or_404(Cliente, user=request.user)
    vaga.status = 'AGENDADA'
    vaga.aluno = cliente
    vaga.save()
    if not cliente.realizou_aula_experimental:
        cliente.realizou_aula_experimental = True
        cliente.save()
    return redirect('agendamento:sucesso_aula_experimental')

def sucesso_aula_experimental(request):
    return render(request, 'agendamento/sucesso_aula_experimental.html')

@login_required
def sucesso_adicao_carrinho(request):
    return render(request, 'agendamento/sucesso_adicao_carrinho.html')