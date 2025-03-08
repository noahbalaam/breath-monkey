from django.contrib import admin
from .models import BreathingTechnique, BreathingPhase

class BreathingPhaseInline(admin.TabularInline):
    model = BreathingPhase
    extra = 1

class BreathingTechniqueAdmin(admin.ModelAdmin):
    inlines = [BreathingPhaseInline]

admin.site.register(BreathingTechnique, BreathingTechniqueAdmin)