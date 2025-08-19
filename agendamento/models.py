from django.db import models
from django.contrib.auth.models import User

class Configuracao(models.Model):
    valor_taxa_matricula = models.DecimalField(max_digits=7, decimal_places=2, default=150.00, help_text="Valor da taxa de matrícula única para novos alunos.")
    class Meta:
        verbose_name = "Configuração da Escola"
        verbose_name_plural = "Configurações da Escola"
    def __str__(self):
        return "Configurações Gerais"

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100)
    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professores"
    def __str__(self):
        return self.nome

class Instrumento(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    class Meta:
        verbose_name = "Instrumento"
        verbose_name_plural = "Instrumentos"
    def __str__(self):
        return self.nome

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    celular = models.CharField(max_length=15, unique=True)
    # --- NOVO CAMPO ADICIONADO AQUI ---
    data_nascimento = models.DateField(null=True, blank=True) # Permitimos que seja opcional por enquanto
    pagou_taxa_matricula = models.BooleanField(default=False)
    realizou_aula_experimental = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"
    def __str__(self):
        return self.user.get_full_name() or self.user.username

class HorarioDisponivel(models.Model):
    DIAS_SEMANA_CHOICES = [
        (0, 'Segunda-feira'), (1, 'Terça-feira'), (2, 'Quarta-feira'),
        (3, 'Quinta-feira'), (4, 'Sexta-feira'), (5, 'Sábado'), (6, 'Domingo')
    ]
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    instrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE)
    dia_da_semana = models.IntegerField(choices=DIAS_SEMANA_CHOICES)
    horario = models.TimeField()
    preco_mensal = models.DecimalField(max_digits=7, decimal_places=2)
    capacidade = models.PositiveIntegerField(default=1)
    class Meta:
        verbose_name = "Horário Fixo para Matrícula"
        verbose_name_plural = "Horários Fixos para Matrícula"
    def __str__(self):
        return f"{self.instrumento.nome} com {self.professor.nome} - {self.get_dia_da_semana_display()} às {self.horario}"

class Matricula(models.Model):
    STATUS_PAGAMENTO_CHOICES = [('PENDENTE', 'Pendente'), ('PAGO', 'Pago')]
    aluno = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    horario = models.ForeignKey(HorarioDisponivel, on_delete=models.CASCADE)
    data_matricula = models.DateField(auto_now_add=True)
    status_pagamento_mes_atual = models.CharField(max_length=10, choices=STATUS_PAGAMENTO_CHOICES, default='PENDENTE')
    ativo = models.BooleanField(default=True)
    class Meta:
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"
    def __str__(self):
        return f"{self.aluno} matriculado em {self.horario}"

class VagaAulaExperimental(models.Model):
    STATUS_CHOICES = [('DISPONIVEL', 'Disponível'), ('AGENDADA', 'Agendada')]
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    instrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(unique=True)
    aluno = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DISPONIVEL')
    valor = models.DecimalField(max_digits=7, decimal_places=2, default=150.00)
    class Meta:
        verbose_name = "Vaga para Aula Experimental"
        verbose_name_plural = "Vagas para Aulas Experimentais"
    def __str__(self):
        return f"Vaga de {self.instrumento.nome} em {self.data_hora.strftime('%d/%m/%Y às %H:%M')}"