from django.contrib import admin
from django.urls import reverse
from .models import Profile, Skill, IeltsScore, Project, BlogPost, ContactMessage


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'title', 'email')
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('full_name', 'title', 'about', 'birth_date', 'interests', 'email', 'phone', 'location')
        }),
      
        

    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')
    search_fields = ('name',)


@admin.register(IeltsScore)
class IeltsScoreAdmin(admin.ModelAdmin):
    list_display = ('updated_at',)
    list_display_links = None
    readonly_fields = ('average_score',)
    change_list_template = 'admin/portfolio_app/ieltsscore/change_list.html'

    def average_score(self, obj):
        return f'{obj.average_score:.1f}'
    average_score.short_description = 'Trung bình'

    def has_add_permission(self, request):
        return not IeltsScore.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return True

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        ielts = IeltsScore.objects.first()
        if ielts:
            extra_context['ielts_change_url'] = reverse(
                'admin:portfolio_app_ieltsscore_change',
                args=(ielts.pk,)
            )
            extra_context['ielts_delete_url'] = reverse(
                'admin:portfolio_app_ieltsscore_delete',
                args=(ielts.pk,)
            )
        else:
            extra_context['ielts_add_url'] = reverse('admin:portfolio_app_ieltsscore_add')
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'technologies')
    search_fields = ('title', 'technologies')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'technologies', 'link')
        }),
    )


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date')
    search_fields = ('title', 'excerpt', 'content')
    exclude = ('published_date',)

 


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
