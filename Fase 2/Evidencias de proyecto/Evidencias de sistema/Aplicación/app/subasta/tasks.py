# app/tasks.py
import time
from celery import shared_task
from django.utils import timezone
from subasta.views import cerrar_subasta
from .models import Subasta, Puja

@shared_task
def cerrar_subasta_automaticamente(subasta_id):
    subasta = Subasta.objects.get(id=subasta_id)
    while subasta.estado == "Activa":
        ultima_puja = Puja.objects.filter(subasta=subasta).order_by("-created_at").first()

        # Verificar si han pasado 15 segundos desde la última puja
        if ultima_puja and (timezone.now() - ultima_puja.created_at).seconds >= 15:
            # Llamar a la función que cierra la subasta
            cerrar_subasta(subasta_id)
            break
        time.sleep(5)  # Verifica cada 5 segundos


