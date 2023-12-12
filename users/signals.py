from django.db.models.signals import post_save
from .models import User
from django.contrib.auth.models import Group


from .models import Employee

def employee_profile(sender, instance, created, **kwargs):
	if created:
		Employee.objects.create(
			user=instance,
            name=instance.first_name,
            email=instance.email,
			)

post_save.connect(employee_profile, sender=User)


# def job_card_details(sender, instance, created, **kwargs):
# 	if created:
# 		CcnJobCard.objects.create(
# 			user=instance,
#             name=instance.first_name,
# 			)

# post_save.connect(job_card_details, sender=CcnJobCard())