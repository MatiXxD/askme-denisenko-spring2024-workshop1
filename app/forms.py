from django import forms
from app.models import Profile, Tag, Question, Answer
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


MAX_USERNAME_LENGTH = 24
MAX_PASSWORD_LENGTH = 24
MAX_EMAIL_LENGTH = 48
MAX_TITLE_LENGTH = 100
MAX_TEXT_LENGTH = 2048
MAX_TAG_LENGTH = 24


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    
    def clean_username(self):
        if len(self.cleaned_data["username"]) > MAX_USERNAME_LENGTH:
            raise ValidationError("Username is too long")
        return self.cleaned_data["username"]
    
    def clean_password(self):
        if len(self.cleaned_data["password"]) > MAX_PASSWORD_LENGTH:
            raise ValidationError("Password is too long")
        return self.cleaned_data["password"]
    

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Enter username"}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={"placeholder": "Enter email"}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={"placeholder": "Enter password"}))
    password_check = forms.CharField(required=True, widget=forms.PasswordInput(attrs={"placeholder": "Enter password one more time"}))
    
    class Meta:
        model = Profile
        fields = ["username", "email", "password", "password_check", "avatar"]
        
    def clean_email(self):
        email = self.cleaned_data["email"]
        if Profile.objects.filter(user__email=email).exists():
            raise ValidationError("Email already exists")
        if len(email) > MAX_EMAIL_LENGTH:
            raise ValidationError("Email is too long")
        
        emailPart = email[email.find("@"):]        
        if len(emailPart[emailPart.find("."):]) <= 0:
            raise ValidationError("Wrong email")
        
        return self.cleaned_data["email"]
    
    def clean_username(self):
        username = self.cleaned_data["username"]

        if len(username) > MAX_USERNAME_LENGTH:
            raise ValidationError("Username is too long")
        if Profile.objects.filter(user__username=username).exists():
            raise ValidationError("Username already exists")

        return username
    
    def clean_password(self):
        if len(self.cleaned_data["password"]) > MAX_PASSWORD_LENGTH:
            raise ValidationError("One of the passwords is too long")
        return self.cleaned_data["password"]
    
    def clean_password_check(self):
        if len(self.cleaned_data["password"]) > MAX_PASSWORD_LENGTH:
            raise ValidationError("One of the passwords is too long")
        return self.cleaned_data["password_check"]
        
    def clean(self):
        password = self.cleaned_data["password"]
        password_check = self.cleaned_data["password_check"]
                
        if password != password_check:
            self.fields["password"].widget.attrs.update({"class": "form-control is-invalid"})
            self.fields["password_check"].widget.attrs.update({"class": "form-control is-invalid"})
            raise ValidationError("Passwords don't match")
    
    def save(self, **kwargs):
        profile = Profile.objects.create(
            user = User.objects.create_user(self.cleaned_data["username"], 
                                            self.cleaned_data["email"], 
                                            self.cleaned_data["password"]),
            avatar=self.cleaned_data["avatar"]
        )
        
        return profile


class SettingsForm(forms.Form):
    username = forms.CharField(required=False)
    email = forms.CharField(required=False)
    avatar = forms.FileField(required=False)
    
    def clean_username(self):
        username = self.cleaned_data["username"]
        if username != "":
            if len(username) > MAX_USERNAME_LENGTH:
                raise ValidationError("Username is too long")
            if Profile.objects.filter(user__username=username).exists():
                raise ValidationError("Username already exists")

        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if email != "":
            if Profile.objects.filter(user__email=email).exists():
                raise ValidationError("Email already exists")
            if len(email) > MAX_EMAIL_LENGTH:
                raise ValidationError("Email is too long")
            
            emailPart = email[email.find("@"):]        
            if len(emailPart[emailPart.find("."):]) <= 0:
                raise ValidationError("Wrong email")
        
        return email

    
    def save(self, user):
        data = self.cleaned_data
        profile = Profile.objects.get(user=user)
        
        if "username" in data and data["username"] != "":
            user.username = data["username"]
        if "email" in data and data["email"] != "":
            user.email = data["email"]
        if "avatar" in data and data["avatar"] != None:
            profile.avatar = data["avatar"]
        
        profile.save()
        user.save()


class QuestionForm(forms.ModelForm):
    tags = forms.CharField(required=True, max_length=255)
    
    class Meta:
        model = Question
        fields = ["title", "tags", "text"]
        
    def clean_title(self):
        if len(self.cleaned_data["title"]) > MAX_TITLE_LENGTH:
            raise ValidationError("Title is too long")
        return self.clean_data["title"]

    def clean_text(self):
        if len(self.cleaned_data["text"]) > MAX_TEXT_LENGTH:
            raise ValidationError("Text is too long")
        return self.cleaned_data["text"]

    def clean_tags(self):
        if len(self.cleaned_data["tags"].split(' ')) > 3 or \
           len(self.cleaned_data["tags"].split(' ')) <= 0:
            for field in self.fields:
                self.fields[field].widget.attrs.update({'class': 'form-control is-invalid'})   
            raise ValidationError("Number of tags should be in [1; 3]")

        for tag in self.cleaned_data["tags"].split(' '):
            if len(tag) > MAX_TAG_LENGTH:
                raise ValidationError("On or more tags are too long")
        return self.cleaned_data["tags"]
    
        
    def save(self, user):
        data = self.cleaned_data
        profile = Profile.objects.get(user=user)
        
        if len(data["tags"].split(' ')) > 3 or \
           len(data["tags"].split(' ')) <= 0:
            raise ValidationError("Number of tags should be in [1; 3]")
                
        tags = list()
        for tag in data["tags"].split(' '):
            try: 
                find_tag = Tag.objects.get(name=tag)
                find_tag.score += 1
                find_tag.save()
                tags.append(find_tag)
            except:
                tags.append(Tag.objects.create(name=tag, score=1))
                    
        question = Question.objects.create(
            author=profile,
            title=data["title"],
            text=data["text"]
        )
        question.tags.set(tags)
        question.save()
        
        return question


class AnswerForm(forms.ModelForm):
    
    class Meta:
        model = Answer
        fields = ["text"]
        
    def clean_text(self):
        if self.cleaned_data["text"] >= MAX_TEXT_LENGTH:
            raise ValidationError("Text is too long")
        return self.clean_data["text"]

        
    def save(self, user, question):
        text = self.cleaned_data["text"]
        profile = Profile.objects.get(user=user)
        
        answer = Answer.objects.create(
            text = text,
            is_correct = False,
            question = question,
            author = profile,
        )
        
        question.answers_count += 1
        question.save()

        return answer