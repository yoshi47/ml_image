import torch
import torch.nn.functional as F
from PIL import Image
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from model.model import Model, transform
from .forms import ImageForm, LoginForm, SignUpForm
from .models import ModelFile

# Create your views here.

weight_path = 'model/model_weights.pth'

model = Model()
model.load_state_dict(torch.load(weight_path))

classnames = [
  'ゴリラ',
  'ゾウ',
  'パンダ',
  'ホッキョクグマ'
]


def trans(img):
  img = Image.open(img)
  input = transform(img)
  input = input.unsqueeze(0)

  model.eval()
  outputs = model(input)
  probs = F.softmax(outputs, dim=1)
  proba, y = probs.sort(dim=1, descending=True)
  y = int(y[0][0])
  proba = f'{proba[0][0]:.2%}'

  return classnames[y], proba


@login_required
def image_upload(request):
  if request.method == "POST":
    form = ImageForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      image_name = request.FILES['image']
      image_url = 'media/documents/{}'.format(image_name)
      y, proba = trans(image_url)
      img = ModelFile.objects.order_by('id').reverse()[0]
      img.label = y
      img.ploba = proba
      img.save()

      return render(request, 'image.html', {'image_url': image_url, 'y': y, 'prob': proba})
  else:
    form = ImageForm()
    return render(request, 'index.html', {'form': form})


class Login(LoginView):
  form_class = LoginForm
  template_name = 'login.html'
  success_url = reverse_lazy('imageupload')


class Logout(LogoutView):
  template_name = 'base.html'


class SignUp(CreateView):
  form_class = SignUpForm
  template_name = 'signup.html'
  success_url = reverse_lazy('imageupload')

  def form_valid(self, form):
    user = form.save()
    login(self.request, user)
    self.object = user
    return HttpResponseRedirect(self.get_success_url())
