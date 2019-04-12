from django.dispatch import Signal

chech_status = Signal(providing_args=['status','task_id'])
