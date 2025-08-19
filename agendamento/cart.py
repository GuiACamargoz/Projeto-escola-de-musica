from decimal import Decimal
import uuid
from .models import HorarioDisponivel

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, horario):
        item_id = str(uuid.uuid4())

        # --- NOVA LÓGICA DE IDENTIFICAÇÃO ---
        # Verifica se este é o primeiro item a ser adicionado no carrinho.
        if len(self.cart) == 0:
            aluno_tipo = 'organizador' # O primeiro é sempre o organizador.
        else:
            aluno_tipo = 'convidado' # Os demais são convidados.

        self.cart[item_id] = {
            'horario_id': str(horario.id),
            'preco': str(horario.preco_mensal),
            'tipo': aluno_tipo # Guarda o tipo de aluno no item do carrinho
        }
        self.save()

    def save(self):
        self.session.modified = True
    
    def remove(self, item_id):
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def __iter__(self):
        cart = self.cart.copy()
        horario_ids = [item['horario_id'] for item in cart.values()]
        horarios = HorarioDisponivel.objects.filter(id__in=horario_ids)
        horarios_map = {str(h.id): h for h in horarios}

        for item_id, item_data in cart.items():
            horario_obj = horarios_map.get(item_data['horario_id'])
            if horario_obj:
                yield {
                    'item_id': item_id,
                    'horario': horario_obj,
                    'preco': Decimal(item_data['preco']),
                    'tipo': item_data.get('tipo', 'convidado') # Passa o tipo para o template
                }
            
    def __len__(self):
        return len(self.cart)

    def get_total_price(self):
        return sum(Decimal(item['preco']) for item in self.cart.values())

    def clear(self):
        if 'cart' in self.session:
            del self.session['cart']
            self.save()