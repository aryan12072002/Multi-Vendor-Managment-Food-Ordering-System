from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import User,UserProfile
@receiver(post_save,sender=User)
def post_save_create_profile_receiver(sender,instance,created,**kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            UserProfile.objects.get(user=instance)
            #print("User profile is created")
            
        except:
            profile=UserProfile.objects.create(user=instance)
            profile.save()
            #print("User was not exists so I created a new one")
        #print("User is updated")
@receiver(pre_save,sender=User)
def pre_save_create_profile_receiver(sender,instance,**kwargs):
    pass
    #print(instance.username,"is being saved")    
    