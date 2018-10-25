from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import PostCreateForm, CommentCreateForm, CommentForm
from .models import Post, Comment


def post_list(request):
    # Post모델에
    #   created_at (생성시간 저장)
    #   modified_at (수정시간 저장)
    #       두 필드를 추가

    # 2. Post모델이 기본적으로 pk 내림차순으로 정렬되도록 설정

    # 3. 모든 Post객체에 대한 QuerySet을
    #   render의 context인수로 전달

    # 4. posts/post_list.html을 Template으로 사용
    #   템플릿에서는 posts값을 순회하며
    #   각 Post의 photo정보를 출력
    posts = Post.objects.all()
    context = {
        'posts': posts,
        'comment_form': CommentForm(),
    }
    return render(request, 'posts/post_list.html', context)


@login_required
def post_create(request):
    context = {}
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(author=request.user)
            return redirect('posts:post-list')
    else:
        form = PostCreateForm()

    context['form'] = form
    return render(request, 'posts/post_create.html', context)


def comment_create(request, post_pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('posts:post-list')
        # content = request.POST['content']
        # Comment.objects.create(
        #     author=request.user,
        #     post=post,
        #     content=content,
        # )
