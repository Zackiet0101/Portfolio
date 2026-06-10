from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Skill, IeltsScore, Project, BlogPost, ContactMessage





def front(request):
    """Trang home (front)."""
    return render(request, 'portfolio_app/front.html')


def profile(request):

    """Profile (trang chủ) - hiển thị tóm tắt hồ sơ, kỹ năng, dự án, blog"""
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    projects = Project.objects.all()[:3]
    blogs = BlogPost.objects.order_by('-published_date')[:3]
    sent = request.GET.get('sent', False)

    return render(request, 'portfolio_app/profile.html', {
        'profile': profile,
        'skills': skills,
        'projects': projects,
        'blogs': blogs,
        'sent': sent,
    })


def skill_ielts(request):
    """Trang riêng cho kỹ năng với điểm IELTS"""
    skills = Skill.objects.all()
    ielts = IeltsScore.objects.first()
    return render(request, 'portfolio_app/skill_ielts.html', {
        'skills': skills,
        'ielts': ielts,
    })


def project_list(request):
    """Trang danh sách tất cả dự án"""
    projects = Project.objects.all()
    search_query = request.GET.get('q', '').strip()
    
    if search_query:
        from django.db.models import Q
        projects = projects.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(technologies__icontains=search_query)
        )
    
    return render(request, 'portfolio_app/project_list.html', {
        'projects': projects,
        'search_query': search_query
    })


def blog_list(request):
    """Trang blog - danh sách tất cả bài viết"""
    blogs = BlogPost.objects.order_by('-published_date')

    return render(request, 'portfolio_app/blog_list.html', {
        'blogs': blogs
    })


def blog_detail(request, pk):
    """Trang chi tiết bài viết blog"""
    blog = BlogPost.objects.get(pk=pk)
    return render(request, 'portfolio_app/blog_detail.html', {
        'blog': blog
    })


def contact(request):
    """Trang liên hệ - form gửi tin nhắn"""
    sent = False
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()
        
        if name and email and subject and message_text:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message_text
            )
            messages.success(request, 'Tin nhắn của bạn đã được gửi thành công! Cảm ơn bạn đã liên hệ.')
            return redirect('/?sent=true')
        else:
            messages.error(request, 'Vui lòng điền đầy đủ tất cả các trường.')
    
    sent = request.GET.get('sent', False)
    return render(request, 'portfolio_app/contact.html', {
        'sent': sent
    })
