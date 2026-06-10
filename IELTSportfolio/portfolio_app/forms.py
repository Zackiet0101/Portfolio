from django import forms
from django.core.exceptions import ValidationError
from .models import Profile, Skill, IeltsScore, Project, BlogPost, ContactMessage
from decimal import Decimal


class ProfileForm(forms.ModelForm):
    """Form nhập dữ liệu hồ sơ cá nhân"""
    
    class Meta:
        model = Profile
        fields = ['full_name', 'title', 'about', 'email', 'phone', 'location', 'photo', 'birth_date', 'interests']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập họ và tên',
                'maxlength': '120'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'VD: Full Stack Developer',
                'maxlength': '120'
            }),
            'about': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Giới thiệu về bản thân',
                'rows': 5,
                'maxlength': '5000'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(+84) 123 456 789'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Hà Nội, Việt Nam'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'interests': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập sở thích của bạn (cách nhau bằng dấu phẩy)',
                'rows': 3
            }),
        }
        labels = {
            'full_name': 'Họ và tên',
            'title': 'Chức danh',
            'about': 'Giới thiệu',
            'email': 'Email',
            'phone': 'Số điện thoại',
            'location': 'Vị trí',
            'photo': 'Ảnh hồ sơ',
            'birth_date': 'Ngày sinh',
            'interests': 'Sở thích',
        }


class SkillForm(forms.ModelForm):
    """Form nhập dữ liệu kỹ năng"""
    
    LEVEL_CHOICES = [
        ('', '-- Chọn trình độ --'),
        ('Beginner', 'Beginner (Người mới bắt đầu)'),
        ('Intermediate', 'Intermediate (Trung cấp)'),
        ('Advanced', 'Advanced (Nâng cao)'),
        ('Expert', 'Expert (Chuyên gia)'),
    ]
    
    level = forms.ChoiceField(
        choices=LEVEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        label='Trình độ'
    )
    
    class Meta:
        model = Skill
        fields = ['name', 'level', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'VD: Python, JavaScript, Django',
                'maxlength': '100'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Mô tả chi tiết về kỹ năng này',
                'rows': 4
            }),
        }
        labels = {
            'name': 'Tên kỹ năng',
            'level': 'Trình độ',
            'description': 'Mô tả',
        }


class IeltsScoreForm(forms.ModelForm):
    """Form nhập dữ liệu điểm IELTS"""
    
    class Meta:
        model = IeltsScore
        fields = ['listening', 'reading', 'writing', 'speaking']
        widgets = {
            'listening': forms.Select(attrs={'class': 'form-control'}),
            'reading': forms.Select(attrs={'class': 'form-control'}),
            'writing': forms.Select(attrs={'class': 'form-control'}),
            'speaking': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'listening': 'Listening (Nghe)',
            'reading': 'Reading (Đọc)',
            'writing': 'Writing (Viết)',
            'speaking': 'Speaking (Nói)',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        # Kiểm tra tính hợp lệ của điểm
        for field in ['listening', 'reading', 'writing', 'speaking']:
            score = cleaned_data.get(field)
            if score:
                if score < Decimal('0.0') or score > Decimal('9.0'):
                    self.add_error(field, 'Điểm phải nằm trong khoảng 0.0 đến 9.0')
        return cleaned_data


class ProjectForm(forms.ModelForm):
    """Form nhập dữ liệu dự án"""
    
    class Meta:
        model = Project
        fields = ['title', 'description', 'technologies', 'link']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập tiêu đề dự án',
                'maxlength': '150'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Mô tả chi tiết về dự án',
                'rows': 5
            }),
            'technologies': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'VD: Django, React, PostgreSQL, Docker',
                'maxlength': '200'
            }),
            'link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/username/project hoặc demo link'
            }),
        }
        labels = {
            'title': 'Tiêu đề dự án',
            'description': 'Mô tả',
            'technologies': 'Công nghệ sử dụng',
            'link': 'Link (GitHub/Demo)',
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title:
            qs = Project.objects.filter(title__iexact=title)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError('Tiêu đề dự án không được trùng lặp.')
        return title


class BlogPostForm(forms.ModelForm):
    """Form nhập dữ liệu bài viết blog"""
    
    class Meta:
        model = BlogPost
        fields = ['title', 'excerpt', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập tiêu đề bài viết',
                'maxlength': '150'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tóm tắt ngắn gọn về bài viết (tùy chọn)',
                'rows': 3
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Nội dung chi tiết của bài viết. Hỗ trợ HTML và Markdown',
                'rows': 10
            }),
        }
        labels = {
            'title': 'Tiêu đề',
            'excerpt': 'Tóm tắt (tùy chọn)',
            'content': 'Nội dung',
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title:
            qs = BlogPost.objects.filter(title__iexact=title)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError('Tiêu đề bài viết không được trùng lặp.')
        return title


class ContactMessageForm(forms.ModelForm):
    """Form nhập dữ liệu tin nhắn liên hệ"""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập họ và tên của bạn',
                'maxlength': '120',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập email của bạn',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tiêu đề tin nhắn',
                'maxlength': '150',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Nội dung tin nhắn của bạn',
                'rows': 6,
                'required': True
            }),
        }
        labels = {
            'name': 'Họ và tên',
            'email': 'Email',
            'subject': 'Tiêu đề',
            'message': 'Nội dung',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        # Kiểm tra các trường bắt buộc
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            value = cleaned_data.get(field, '').strip()
            if not value:
                self.add_error(field, f'{self._meta.labels[field]} không được để trống.')
        return cleaned_data
