from django.contrib import admin

# Register your models here.
from app.models import *

class SubmissionAdmin(admin.ModelAdmin):
	model = Submission
	list_display = ('ques_ID', 'user_ID', 'status', 'source_code_URL')
	list_filter = ['status']


admin.site.register(UserProfile)
admin.site.register(Question)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Announcement)