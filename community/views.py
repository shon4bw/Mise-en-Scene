from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .models import Review, Comment
from .forms import ReviewForm, CommentForm
from django.core.paginator import Paginator
from accounts.models import User
from django.contrib.auth.forms import AuthenticationForm

@login_required
@require_GET
def index(request):
    # # 일반 로그인과 소셜 로그인 분리
    # if request.user.is_authenticated:
    #     user = User.objects.get(id=request.user.id)
    #     try:
    #         profile = User.objects.get(user_id=user.id)
    #     except:
    #         User.objects.create(user=user)

    
    reviews = Review.objects.order_by('-pk')

    page = int(request.GET.get('p', 1)) #없으면 1로 지정
    paginator = Paginator(reviews, 10) #한 페이지 당 몇개 씩 보여줄 지 지정 
    
    boards = paginator.get_page(page)
    form = AuthenticationForm()

    context = {
        'reviews': boards,
        'form': form,
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
        form1 = AuthenticationForm()
        context = {
            'form': form,
            'form1':form1,
        }
    return render(request, 'community/create.html', context)


@login_required
@require_GET
def detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comments = review.comment_set.all()
    comment_form = CommentForm()
    form = AuthenticationForm()
    context = {
        'review': review,
        'comment_form': comment_form,
        'comments': comments,
        'form':form,
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
        return redirect('community:index')
    context = {
        'review': review,
        'form': form,
    }
    return render(request, 'community/update.html', context)


@require_POST
def review_delete(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user.is_authenticated:
        if request.user == review.user:
            review.delete()
            return redirect('community:index')
    return redirect(request.META.get('HTTP_REFERER'))

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

@login_required
@require_POST
def comment_delete(request, review_pk, comment_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@require_POST
def like(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        if review.like_users.filter(pk=request.user.pk).exists():
            # 좋아요 취소
            review.like_users.remove(request.user)
            liked = False
        else:
            # 좋아요 하기
            review.like_users.add(request.user)
            liked = True

        like_count = review.like_users.count()
        context = {
            'liked' : liked,
            'like_count' : like_count,
        }
        return JsonResponse(context)

# def search(request):
#     users = User.objects.all()
#     reviews = Review.objects.order_by('-pk')
#     q = request.POST.get('q', "")

#     if q[0] == '#':
#         reviews = reviews.filter(content__contains=q[1:])
#         context = {
#             'reviews': reviews,
#             'q': q,
#         }
#         return render(request, 'community/search.html', context)
#     elif q:
#         users = users.filter(username__icontains=q)
#         context = {
#             'users': users,
#             'q': q,
#         }
#         return render(request, 'community/search.html', context)
#     else:
#         return render(request, 'community/search.html')

