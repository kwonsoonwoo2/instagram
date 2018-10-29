import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import CommentForm, PostForm
from .models import Post


def post_list(request):
    # 1. Post모델에
    #  created_at (생성시간 저장)
    #       auto_now_add=True
    #  modified_at (수정시간 저장)
    #       auto_now=True
    #   두 필드를 추가

    # 2. Post모델이 기본적으로 pk내림차순으로 정렬되도록 설정
    #     class Meta:
    #         ordering = ['-pk']

    # 3. 모든 Post객체에 대한 QuerySet을
    #    render의 context인수로 전달 (키: posts)
    #      context = {'posts': Post.objects.all()}

    # 4. posts/post_list.html을 Template으로 사용
    #     템플릿에서는 posts값을 순회하며
    #     각 Post의 photo정보를 출력

    # 5. url은 posts.urls모듈을 사용
    #    config.urls에서 해당 모듈을 include
    #    posts.urls.app_name = 'posts'를 사용
    #     include할 URL은 'posts/'
    #     view의 URL은 비워둔다
    #      결과: localhost:8000/posts/ 로 접근시
    #            이 view가 처리하도록 함
    posts = Post.objects.all()
    # 적절히 CommentCreateForm을 전달
    context = {
        'posts': posts,
        'comment_form': CommentForm(),
    }
    return render(request, 'posts/post_list.html', context)


@login_required
def post_create(request):
    context = {}
    if request.method == 'POST':
        # request.FILES에 form에서 보낸 파일객체가 들어있음
        # 새로운 Post를 생성한다.
        #  author는 User.objects.first()
        #  photo는 request.FILES에 있는 내용을 적절히 꺼내서 쓴다
        # 완료된 후 posts:post-list로 redirect
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # PostForm에 'comment'값이 전달되었다면
            # 위에서 만든 Post와 연결되는 Comment를 생성
            comment_content = form.cleaned_data['comment']
            if comment_content:
                post.comments.create(
                    author=request.user,
                    content=comment_content,
                )
            return redirect('posts:post-list')
    else:
        # GET요청의 경우, 빈 Form인스턴스를 context에 담아서 전달
        # Template에서는 'form'키로 해당 Form인스턴스 속성을 사용 가능
        form = PostForm()

    context['form'] = form
    return render(request, 'posts/post_create.html', context)


def comment_create(request, post_pk):
    """
    post_pk에 해당하는 Post에 댓글을 생성하는 view
    'POST'메서드 요청만 처리
    'content'키로 들어온 값을 사용해 댓글 생성. 작성자는 요청한 User
    URL: /posts/<post_pk>/comments/create/
    댓글 생성 완료 후에는 posts:post-list로 redirect
    :param request:
    :param post_pk:
    :return:
    """
    # 1. post_pk에 해당하는 Post객체를 가져와 post변수에 할당
    # 2. request.POST에 전달된 'content'키의 값을 content변수에 할당
    # 3. Comment생성
    #     author: 현재 요청의 User
    #     post: post_pk에 해당하는 Post객체
    #     content: request.POST로 전달된 'content'키의 값
    # 4. posts:post-list로 redirect하기
    if request.method == 'POST':
        post = Post.objects.get(pk=post_pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('posts:post-list')


def tag_post_list(request, tag_name):
    # Post중, 자신에게 속한 Comment가 가진 HashTag목록 중 tag_name이 name인 HashTag가 포함된
    #  Post목록을 posts변수에 할당
    #  context에 담아서 리턴 render
    # HTML: /posts/tag_post_list.html
    posts = Post.objects.filter(
        comments__tags__name=tag_name).distinct()
    context = {
        'posts': posts,
    }
    return render(request, 'posts/tag_post_list.html', context)


def tag_search(request):
    # request.GET으로 전달된
    #  search_keyword값을 적절히 활용해서
    #  위의 tag_post_list view로 redirect
    # URL: '/posts/tag-search/'
    # URL Name: 'posts:tag-search'
    # Template: 없음
    search_keyword = request.GET.get('search_keyword')
    substituted_keyword = re.sub(r'#|\s+', '', search_keyword)
    return redirect('tag-post-list', substituted_keyword)


def post_like_toggle(request, post_pk):
    # URL: '/posts/<post_pk>/like-toggle/
    # URL Name: 'posts:post-like-toggle'
    # POST method에 대해서만 처리

    # request.user가 post_pk에 해당하는 Post에
    #  Like Toggle처리
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        post.like_toggle(request.user)
        url = reverse('posts:post-list')
        return redirect(url + f'#post-{post_pk}')