from django.forms import ModelForm
from blog.models import Post,Comment

class PostCreationForm(ModelForm):
    
    class Meta:
        model = Post
        fields = ['title','content','category']