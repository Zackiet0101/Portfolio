from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


IELTS_SCORE_CHOICES = [
    (Decimal(i) / Decimal('2'), f"{Decimal(i) / Decimal('2'):.1f}")
    for i in range(0, 19)
]


class Profile(models.Model):
    """Hồ sơ cá nhân"""
    full_name = models.CharField(max_length=120, verbose_name='Họ và tên')
    title = models.CharField(max_length=120, verbose_name='Chức danh')
    about = models.TextField(verbose_name='Giới thiệu')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=50, blank=True, verbose_name='Số điện thoại')
    location = models.CharField(max_length=120, blank=True, verbose_name='Vị trí')
    photo = models.ImageField(upload_to='profile/', blank=True, null=True, verbose_name='Ảnh hồ sơ')

    birth_date = models.DateField(blank=True, null=True, verbose_name='Ngày sinh')
    interests = models.TextField(blank=True, verbose_name='Sở thích')

    def clean(self):
        from django.core.exceptions import ValidationError
        from django.utils import timezone

        super().clean()
        if self.birth_date and self.birth_date > timezone.now().date():
            raise ValidationError({'birth_date': 'Ngày sinh phải trước ngày hiện tại.'})


    class Meta:
        verbose_name = 'Hồ sơ'

        verbose_name_plural = 'Hồ sơ'

    def __str__(self):
        return self.full_name


class Skill(models.Model):
    """Kỹ năng chuyên môn"""
    name = models.CharField(max_length=100, verbose_name='Tên kỹ năng')
    level = models.CharField(
        max_length=50, 
        blank=True,
        verbose_name='Trình độ',
        help_text='VD: Beginner, Intermediate, Advanced, Expert'
    )
    description = models.TextField(blank=True, verbose_name='Mô tả')

    class Meta:
        verbose_name = 'Kỹ năng'
        verbose_name_plural = 'Kỹ năng'

    def __str__(self):
        return self.name


class IeltsScore(models.Model):
    """Điểm IELTS do admin quản lý trong site quản trị"""
    listening = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        choices=IELTS_SCORE_CHOICES,
        default=Decimal('5.0'),
        verbose_name='Listening',
        help_text='Điểm từ 0.0 đến 9.0, bước 0.5',
        validators=[MinValueValidator(Decimal('0.0')), MaxValueValidator(Decimal('9.0'))]
    )
    reading = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        choices=IELTS_SCORE_CHOICES,
        default=Decimal('5.0'),
        verbose_name='Reading',
        help_text='Điểm từ 0.0 đến 9.0, bước 0.5',
        validators=[MinValueValidator(Decimal('0.0')), MaxValueValidator(Decimal('9.0'))]
    )
    writing = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        choices=IELTS_SCORE_CHOICES,
        default=Decimal('5.0'),
        verbose_name='Writing',
        help_text='Điểm từ 0.0 đến 9.0, bước 0.5',
        validators=[MinValueValidator(Decimal('0.0')), MaxValueValidator(Decimal('9.0'))]
    )
    speaking = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        choices=IELTS_SCORE_CHOICES,
        default=Decimal('5.0'),
        verbose_name='Speaking',
        help_text='Điểm từ 0.0 đến 9.0, bước 0.5',
        validators=[MinValueValidator(Decimal('0.0')), MaxValueValidator(Decimal('9.0'))]
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Cập nhật lần cuối')

    class Meta:
        verbose_name = 'Điểm IELTS'
        verbose_name_plural = 'Điểm IELTS'

    def __str__(self):
        return f'IELTS ({self.average_score:.1f})'

    @property
    def average_score(self):
        """Band score trung bình, làm tròn về bội 0.5 (x.0 hoặc x.5)."""
        total = self.listening + self.reading + self.writing + self.speaking
        avg = total / Decimal('4')

        # Quy đổi sang "nửa điểm" rồi làm tròn HALF_UP để ra các bước .0/.5.
        # Ví dụ: 6.25 -> 6.5 ; 6.75 -> 7.0
        from decimal import ROUND_HALF_UP

        half_points = (avg * Decimal('2')).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        return half_points / Decimal('2')


class Project(models.Model):

    """Dự án đã thực hiện"""
    title = models.CharField(max_length=150, verbose_name='Tiêu đề dự án')
    description = models.TextField(verbose_name='Mô tả')
    technologies = models.CharField(
        max_length=200, 
        blank=True,
        verbose_name='Công nghệ sử dụng',
        help_text='VD: Django, React, PostgreSQL'
    )
    link = models.URLField(blank=True, verbose_name='Link (GitHub/Demo)')

    class Meta:
        verbose_name = 'Dự án'
        verbose_name_plural = 'Dự án'

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    """Bài viết blog"""
    title = models.CharField(max_length=150, verbose_name='Tiêu đề')
    excerpt = models.TextField(blank=True, verbose_name='Tóm tắt')
    content = models.TextField(verbose_name='Nội dung')
    published_date = models.DateField(auto_now_add=True, verbose_name='Ngày đăng')

    def clean(self):
        from django.core.exceptions import ValidationError
        from django.utils import timezone

        super().clean()
        if self.title:
            qs = BlogPost.objects.filter(title__iexact=self.title)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError({'title': 'Tiêu đề bài viết không được trùng lặp.'})
        if self.published_date and self.published_date > timezone.now().date():
            raise ValidationError({'published_date': 'Ngày đăng phải trước ngày hiện tại.'})


    class Meta:
        verbose_name = 'Bài viết'
        verbose_name_plural = 'Bài viết'
        ordering = ['-published_date']

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    """Tin nhắn từ khách truy cập"""
    name = models.CharField(max_length=120, verbose_name='Họ tên')
    email = models.EmailField(verbose_name='Email')
    subject = models.CharField(max_length=150, verbose_name='Tiêu đề')
    message = models.TextField(verbose_name='Nội dung')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Thời gian')

    class Meta:
        verbose_name = 'Tin nhắn liên hệ'
        verbose_name_plural = 'Tin nhắn liên hệ'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.subject}'
