from django.shortcuts import render, redirect

from .models import Post

from .forms import PostCreateForm


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
    }
    return render(request, 'posts/post_list.html', context)


def post_create(request):
    if request.method == 'POST':
        post = Post(
            author=request.user,
            photo=request.FILES['photo'],
        )
        post.save()
        return redirect('posts:post-list')
    else:
        form = PostCreateForm()
        context = {
            'form': form,
        }
        return render(request, 'posts/post_create.html', context)
