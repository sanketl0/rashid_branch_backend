from django.contrib import admin
from .models import ManualJournal, JournalTransaction, RecJournal, BulkUpdate, Budget

# Register your models here.
admin.site.register(ManualJournal)
admin.site.register(RecJournal)
admin.site.register(BulkUpdate)
admin.site.register(Budget)
admin.site.register(JournalTransaction)

