from django.contrib import admin
from .models import WimHofSession, BreathingRound, WimHofStats

class BreathingRoundInline(admin.TabularInline):
    model = BreathingRound
    extra = 1

class WimHofSessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_global', 'created_at')
    list_filter = ('is_global', 'created_at')
    search_fields = ('name', 'user__username')
    inlines = [BreathingRoundInline]

class WimHofStatsAdmin(admin.ModelAdmin):
    list_display = ('user', 'session', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('user__username',)
    readonly_fields = ('round_data',)

admin.site.register(WimHofSession, WimHofSessionAdmin)
admin.site.register(WimHofStats, WimHofStatsAdmin)