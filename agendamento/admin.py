from django.contrib import admin
from .models import Professor, Instrumento, Aula, Cliente, Agendamento

# O @admin.register é uma forma elegante de registrar os modelos
@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'instrumento_principal')

@admin.register(Instrumento)
class InstrumentoAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ('instrumento', 'professor', 'nivel', 'preco', 'is_experimental')
    list_filter = ('instrumento', 'nivel', 'is_experimental')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'whatsapp', 'data_criacao')
    search_fields = ('nome_completo', 'whatsapp')

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'aula', 'data_hora', 'status', 'pagamento_status')
    list_filter = ('status', 'data_hora', 'aula', 'pagamento_status')