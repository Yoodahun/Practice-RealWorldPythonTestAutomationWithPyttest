from django.contrib import admin

from api.coronavstech.companies.models  import Company


# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass
