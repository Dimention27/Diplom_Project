from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Permission
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import TemplateView, CreateView


from .forms import PostForm
from .models import New
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.views import View


#
# news = [
#     {
#         'title': 'Точное земледелие',
#         'text': 'Точное земледелие в сельском хозяйстве — это концепция управления производственным процессом, '
#                 'основанная на наблюдении, измерении и реагировании на изменчивость культур и условий их '
#                 'возделывания. В основе точного земледелия лежит использование точных карт полей. К каждому '
#                 'участку поля привязываются точные агротехнические характеристики — это данные о химическом составе '
#                 'почвы, уровне её влажности, количестве получаемой солнечной радиации и другие. На основе этих карт '
#                 'создаются точные инструкции для каждого участка поля по распашке, количеству удобрений, семян, '
#                 'поливу и прочей обработке. Эти инструкции контролируют и корректируют действия сельскохозяйственной '
#                 'техники.',
#         'date': '10 Мая 2020',
#         'author': 'Валерий'
#     },
#     {
#         'title': 'Искусственный интеллект',
#         'text': 'Искусственный интеллект в сельском хозяйстве предполагает использование передовых технологий, '
#                 'таких как машинное обучение, компьютерное зрение, робототехника и Интернет вещей (IoT), '
#                 'для улучшения различных методов ведения сельского хозяйства. Эти технологии позволяют фермерам '
#                 'собирать и анализировать данные, автоматизировать процессы и принимать обоснованные решения, '
#                 'тем самым повышая урожайность сельскохозяйственных культур и рациональное использование ресурсов. '
#                 'Сельское хозяйство входит в число приоритетных сфер для внедрения Искусственного Интеллекта (ИИ). '
#                 'Отечественные компании уже разработали нейросеть, которая анализирует полевые данные, видеоматериалы '
#                 'и изображения, полученные при помощи разных устройств. Затем она выдает план сельскохозяйственных '
#                 'операций по обработке, прополке, орошению. ИИ способен и сам передавать команды технике: такая '
#                 'система делает процесс выращивания урожая полностью автоматизированным.Попробовать ИИ можно уже '
#                 'сегодня: существуют приложения, которые оценивают внешний вид растений, определяют возможные '
#                 'заболевания, нехватку макро- и микроэлементов и предлагают схемы лечения. И все это – в вашем '
#                 'телефоне.',
#         'date': '19 Мая 2020',
#         'author': 'Егор'
#     },
#     {
#         'title': 'Новые системы обработки почвы и альтернативные виды топлива.',
#         'text': 'Интенсивное земледелие негативно сказывается на состоянии почв. Деградация почв – общемировая '
#                 'проблема, которая привела к пересмотру привычных подходов. Так, все чаще применяют более бережную '
#                 'обработку почвы: в частности, no-till и mini-till. Нулевая обработка исключает глубокую вспашку, '
#                 'благодаря чему сохраняется естественная структура почвы. Новые технологии позволяют сделать '
#                 'использование сельскохозяйственной техники более экологичным. В частности, с помощью альтернативных '
#                 'видов топлива. Вместо привычных бензина, дизеля и газа аграрии начинают использовать электричество, '
#                 'а также биотопливо: например, пеллеты из мискантуса или лузги подсолнечника.',
#         'date': '19 Мая 2020',
#         'author': 'Егор'
#     },
#     {
#         'title': 'Роботы, беспилотники, дроны и другие устройства.',
#         'text': 'Во многих странах разрабатывают устройства, которые автоматизируют разные сельскохозяйственные '
#                 'процессы. Например, в Швейцарии есть роботы для прополки сорняков: это позволяет избежать '
#                 'использования дорогостоящих гербицидов, которые оказывают угнетающее действие на почву и растения. А '
#                 'в США разработаны беспилотные тракторы, которые могут выполнять чизелевание, посев культур, '
#                 'а в процессе работы избавляться от сорняков. Россия также активно внедряет инновационные технологии: '
#                 'так, уже проводились эксперименты с использованием дронов для посева донника и горчицы, а также для '
#                 'обработки полей от вредителей.',
#         'date': '19 Мая 2020',
#         'author': 'Егор'
#     },
#     {
#         'title': 'Интернет вещей (IoT)',
#         'text': 'Концепция интернета вещей состоит в том, что технические устройства обмениваются информацией друг с '
#                 'другом, а человек получает уже готовые, обработанные данные или алгоритм действий. Мы пользуемся '
#                 'интернетом вещей практически каждый день. Простой пример: у многих есть смарт-часы, которые собирают '
#                 'данные о физических нагрузках, давлении, пульсе, глубине сна человека. Затем эти данные поступают в '
#                 'приложение, которое анализирует их и выдает общую информацию о состоянии здоровья, '
#                 'а также рекомендации – например, по улучшению качества сна или питания. В сельском хозяйстве '
#                 'интернет вещей также начал свое распространение. Так, уже существуют дроны, которые мониторят '
#                 'состояние полей и посевов, сверяются со сводками погоды и дают советы по поливу, обработке, '
#                 'внесению удобрений. Распространяется IoT и в животноводстве. Ниже –только 6 вариантов применения '
#                 'интернета вещей на практике:',
#         'date': '19 Мая 2020',
#         'author': 'Егор'
#
#     }
# ]


def home(request):
    data = {
        'news': New.objects.all(),
        'title': 'Агротехнологии'
    }
    return render(request, 'blog/home.html', data)


@login_required(login_url='/login/')
def contacts(request):
    return render(request, 'blog/contacts.html', {'title': 'Контакты'})


@login_required(login_url='/login/')
def add_post(request):
    return render(request, 'blog/post_edit.html', {'title': 'Добавить статью'})


def registration(request):
    form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'blog/home.html')


class RegisterView(TemplateView):
    template_name = "registration/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            if password == password2:
                User.objects.create_user(username, email, password)
                return redirect("login")

        return render(request, self.template_name)


def post_detail(request, pk):
    post = get_object_or_404(New, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('/', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(New, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user,
            post.published_date = timezone.now()
            post.save()
            return redirect('/', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
