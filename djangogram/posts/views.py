from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from djangogram.users.models import User as user_model

from . import models, serializers
from .forms import CreatePostForm

# Create your views here.
def index(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = get_object_or_404(user_model, pk=request.user.id)
            following = user.following.all()
            posts = models.Post.objects.filter(
                Q(author__in=following) | Q(author=user)
            )

            serializer = serializers.PostSerializer(posts, many=True) # 피드에 보여지는 포스트가 여러개일 수도 있으니 many=True 옵션 추가
            print(serializer.data)

            return render(request, 'posts/main.html', {"posts": serializer.data})
    
    return render(request, 'posts/main.html')


def post_create(request):
    if request.method == 'GET':
        form = CreatePostForm()
        return render(request, 'posts/post_create.html', {"form" : form})

    elif request.method == 'POST':
        if request.user.is_authenticated:
            user = get_object_or_404(user_model, pk=request.user.id)
            # image = request.FILES['image']
            # caption = request.POST['caption']

            # new_post = models.Post.objects.create(
            #     author = user,
            #     image = image,
            #     caption = caption
            # )
            # new_post.save()

            form = CreatePostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = user
                post.save()
            else:
                print(form.errors)

            return render(request, 'posts/main.html')

        else:
            return render(request, 'users/main.html')