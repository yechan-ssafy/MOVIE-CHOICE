from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .models import Review, Comment
from .forms import ReviewForm, CommentForm
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


@require_GET
def index(request):
    reviews = Review.objects.all()
    total_len = len(reviews)
    paginator = Paginator(reviews, 3)
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
