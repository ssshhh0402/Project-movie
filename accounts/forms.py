from django.contrib.auth import get_user_model
from django.contribauth.forms impor tUserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username','password','email','preferences')
        
