from django.views.generic import ListView, DetailView, ArchiveIndexView, YearArchiveView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Post    # models의 Post 클래스를 import 해옴
from .forms import PostForm
from django.contrib import messages

# @login_required
# def post_list(request):
#     qs = Post.objects.all()
#     # q : 검색어
#     q = request.GET.get('q', '')
#     if q:
#         qs = qs.filter(message__icontains = q)
#     # instagram/templates/instagram/post_list.html 에 만든다(템플릿을)
#     return render(request, 'instagram/post_list.html',{'post_list':qs, 'q':q})    
#     # render 설명       1번째 인자 : view 함수의 request 인자를 그대로 넣는다
#     #                   2번째 인자 : 앱이름/원하는 html 템플릿 명
#     #                   3번째 인자 : html 템플릿내에서 qs라는 값을 참조할때 쓸 이름 넣기
# # 아래 코드가 위의 함수를 다 포함하고 있음
# post_list = login_required(ListView.as_view(model=Post, paginate_by=10))
# # 아래 코드가 위의 함수를 다 포함하고 있음
@method_decorator(login_required, name='dispatch')
class PostListView(ListView):
    model = Post
    paginate_by = 10
post_list = PostListView.as_view()


# def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
#     post = get_object_or_404(Post, pk=pk)   # DoesNotExist 예외 처리
#     # try:
#     #     post = Post.objects.get(pk=pk)
#     # except Post.DoesNotExist:
#     #     raise Http404
#     return render(request, 'instagram/post_detail.html',{'post':post,})

# 아래 코드가 위에 post_detail 함수의 기능을 다 포함하고 있다
# post_detail = DetailView.as_view(model=Post, queryset=Post.objects.filter(is_public=True))

# 아래 코드가 위의 post_detail의 기능을 다 포함하고 있다
class PostDetailView(DetailView):
    model = Post
    # queryset=Post.objects.filter(is_public=True)
    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_authenticated:   # 유저가 인증이 되어 있는지 확인하는 코드(로그인 여부)
            qs = qs.filter(is_public=True)          # 로그인이 안되어 있으면 공개되어 있는 것만 볼수 있다
        return qs

post_detail = PostDetailView.as_view()



# def archives_year(request, year):
#     return HttpResponse(f"{year}년 archives")

post_archive =ArchiveIndexView.as_view(model=Post, date_field='created_at', paginate_by=10)

post_archive_year = YearArchiveView.as_view(model=Post, date_field='created_at', make_object_list=True)

# @login_required
# def post_new(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user  # 현재 로그인 User Instance, 새글을 작성할때 작성 유저를 선택하지 않고 내가 작성자가 되게 하기 위함
#             post.save()
#             messages.success(request, '포스팅을 저장했습니다')
#             # post = form.save(commit=True) # 이 코드로 실행하면 글을 작성할때 어떤 유저로 작성할지 선택할수있게하는 사태가 발생함
#             return redirect(post)
#     else:
#         form = PostForm()

#     return render(request, 'instagram/post_form.html', {
#         'form':form,
#         'post':None,
#     })
# 밑에 부터 클래스 기반 뷰를 작성 위의 post_new와 같은 기능
class PostCreateView(LoginRequiredMixin, CreateView):
    model=Post
    form_class=PostForm

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.auther = self.request.user
        messages.success(self.request, '포스팅을 저장했습니다')
        return super().form_valid(form)

post_new = PostCreateView.as_view()


# @login_required
# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)

#     # 작성자와 로그인 한 유저가 같은지 체크!
#     if post.author != request.user:
#         messages.error(request, '작성자만 수정할 수 있습니다.')
#         return redirect(post)

#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES, instance=post)
#         if form.is_valid():
#             post = form.save(commit=True)
#             messages.success(request, '포스팅을 수정했습니다')
#             return redirect(post)
#     else:
#         form = PostForm(instance=post)

#     return render(request, 'instagram/post_form.html', {
#         'form':form,
#         'post':post,
#     })
# 밑에 부터 클래스 기반 뷰를 작성 위의 post_edit와 같은 기능
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model=Post
    form_class=PostForm

    def form_valid(self,form):
        messages.success(self.request, '포스팅을 수정했습니다.')
        return super().form_valid(form)

post_edit = PostUpdateView.as_view()


# @login_required
# def post_delete(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == 'POST':
#         post.delete()
#         messages.success(request, '포스팅을 삭제했습니다')
#         return redirect('instagram:post_list')  # 삭제했으면 post가 사라진거니까 리다이렉트를 시켜줘야한다
#     return render(request, 'instagram/post_confirm_delete.html', {
#         'post':post,
#     })
# 밑에 부터 클래스 기반 뷰를 작성 위의 post_delete와 같은 기능
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post

    def get_success_url(self):
        return reverse('instagram:post_list')
    # 이렇게 하거나 아래처럼 해주면 된다
    # success_url = reverse_lazy('instagram:post_list')


post_delete = PostDeleteView.as_view()