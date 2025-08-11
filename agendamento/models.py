from django.db import models

# Modelo para os Professores da escola
class Professor(models.Model):
    nome = models.CharField(max_length=100)
    instrumento_principal = models.CharField(max_length=50)
    bio_curta = models.TextField(blank=True, help_text="Um breve resumo sobre o professor.")

    # NOVA CLASSE META para corrigir os nomes no painel
    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professores"

    def __str__(self):
        return self.nome

# Modelo para os Tipos de Instrumentos oferecidos
class Instrumento(models.Model):
    nome = models.CharField(max_length=50, unique=True, help_text="Ex: Violão, Piano, Canto")

    class Meta:
        verbose_name = "Instrumento"
        verbose_name_plural = "Instrumentos"

    def __str__(self):
        return self.nome

# Modelo para as Aulas oferecidas
class Aula(models.Model):
    NIVEL_CHOICES = [('IN', 'Iniciante'), ('IT', 'Intermediário'), ('AV', 'Avançado'), ('UN', 'Nível Único')]
    instrumento = models.ForeignKey(Instrumento, on_delete=models.PROTECT)
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True)
    nivel = models.CharField(max_length=2, choices=NIVEL_CHOICES, default='UN')
    duracao_min = models.IntegerField(default=50, help_text="Duração da aula em minutos")
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    is_experimental = models.BooleanField(default=False, help_text="Marque se for uma aula experimental.")

    class Meta:
        verbose_name = "Aula"
        verbose_name_plural = "Aulas"

    def __str__(self):
        return f"Aula de {self.instrumento.nome} ({self.get_nivel_display()})"

# Modelo para os Clientes (Alunos)
class Cliente(models.Model):
    nome_completo = models.CharField(max_length=100)
    whatsapp = models.CharField(max_length=15, unique=True, help_text="Use o formato (XX) XXXXX-XXXX")
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.nome_completo

# Modelo para os Agendamentos feitos
class Agendamento(models.Model):
    STATUS_CHOICES = [('AG', 'Agendado'), ('CA', 'Cancelado'), ('RE', 'Realizado')]
    PAGAMENTO_CHOICES = [('PE', 'Pendente'), ('AP', 'Aprovado'), ('RE', 'Recusado')]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='AG')
    pagamento_status = models.CharField(max_length=2, choices=PAGAMENTO_CHOICES, default='PE')

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"

    def __str__(self):
        return f"{self.cliente.nome_completo} - {self.aula.instrumento.nome} em {self.data_hora.strftime('%d/%m/%Y %H:%M')}"