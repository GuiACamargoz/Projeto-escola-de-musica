from django.contrib import admin
from .models import (
    Configuracao, Professor, Instrumento, Cliente, HorarioDisponivel,
    Matricula, VagaAulaExperimental
)

# Registra o novo modelo de configurações
@admin.register(Configuracao)
class ConfiguracaoAdmin(admin.ModelAdmin):
    list_display = ('valor_taxa_matricula',)

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(Instrumento)
class InstrumentoAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    # Adicionamos o novo campo para ver quem já pagou a taxa
    list_display = ('__str__', 'celular', 'pagou_taxa_matricula')
    search_fields = ('user__first_name', 'user__last_name', 'celular')

@admin.register(HorarioDisponivel)
class HorarioDisponivelAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'preco_mensal', 'capacidade')
    list_filter = ('instrumento', 'professor', 'dia_da_semana')

@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'horario', 'status_pagamento_mes_atual', 'ativo')
    list_filter = ('horario', 'status_pagamento_mes_atual', 'ativo')

@admin.register(VagaAulaExperimental)
class VagaAulaExperimentalAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status', 'aluno')
    list_filter = ('status', 'instrumento', 'professor')
