def verify_user_profile(modeladmin, request, queryset):
    for obj in queryset:
        obj.administrator_validated = True
        obj.save()
verify_user_profile.short_description = "Verify user profile"
