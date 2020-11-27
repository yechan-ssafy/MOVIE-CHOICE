from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .models import Review, Comment
from .forms import ReviewForm, CommentForm
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.db.models import Q


@login_required
@require_GET
def index(request):
    reviews = Review.objects.all()

    # 검색 기능
    search_keyword = request.GET.get('q', '')
    search_type = request.GET.get('type', '')
    notice_list = Review.objects.order_by('-id') 
    
    search_notice_list = []
    if search_keyword :
        if len(search_keyword) >= 2 :
            if search_type == 'all':
                search_notice_list = notice_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword) | Q (user__username__icontains=search_keyword) | Q (movie__icontains=search_keyword))
            elif search_type == 'title_content':
                search_notice_list = notice_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword))
            elif search_type == 'title':
                search_notice_list = notice_list.filter(title__icontains=search_keyword)    
            elif search_type == 'content':
                search_notice_list = notice_list.filter(content__icontains=search_keyword)    
            elif search_type == 'movie':
                search_notice_list = notice_list.filter(movie__icontains=search_keyword)    
            elif search_type == 'writer':
                search_notice_list = notice_list.filter(user__username__icontains=search_keyword)

        reviews = search_notice_list

    # pagination
    total_len = len(reviews)
    paginator = Paginator(reviews, 10)
    page = request.GET.get('page', 1)
    
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    index = users.number - 1
    max_index = len(paginator.page_range)
    if index == 2:
        start_index = index - 2
    elif index == 3:
        start_index = index - 3
    elif index == max_index - 1:
        start_index = max_index - 3
    elif index >= 1:
        start_index = index - 1
    else:
        start_index = 0
    
    if index < 1:
        end_index = 3 - start_index
    else:
        if index < max_index - 4:
            end_index = index + 2
        else:
            end_index = max_index
    page_range = list(paginator.page_range[start_index:end_index])

    context = {
        'users': users,
        'page_range': page_range,
        'total_len': total_len,
        'prev_max_index': max_index - 3,
        'max_index': max_index - 1,
    }
    return render(request, 'community/index.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST) 
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('community:detail', review.pk)
    else:
        form = ReviewForm()
    context = {
        'form': form,
    }
    return render(request, 'community/create.html', context)


@login_required
@require_GET
def detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comments = review.comment_set.all()
    comment_form = CommentForm()
    context = {
        'review': review,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'community/detail.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user == review.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                return redirect('community:detail', review.pk)
        else:
            form = ReviewForm(instance=review)
    else:
        return redirect('reviews:index')
    context = {
        'form': form,
        'review': review,
    }
    return render(request, 'community/update.html', context)


@require_POST
def delete(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        if request.user == review.user:
            review.delete()
            return redirect('community:index')
    return redirect('community:detail', review.pk)


@require_POST
def create_comment(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
        return redirect('community:detail', review.pk)
    context = {
        'comment_form': comment_form,
        'review': review,
        'comments': review.comment_set.all(),
    }
    return render(request, 'community/detail.html', context)


@require_POST
def comments_delete(request, review_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('community:detail', review_pk)


@require_POST
def like(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        user = request.user

        if review.like_users.filter(pk=user.pk).exists():
            review.like_users.remove(user)
            is_like = False
        else:
            review.like_users.add(user)
            is_like = True
        data = {
            'is_like' : is_like,
            'like_count': review.like_users.count()
        }
        return JsonResponse(data)
    return redirect('accounts:login')
