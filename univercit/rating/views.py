from django.shortcuts import render
from django.views import View


# Create your views here.
class RatingView(View):
    template_name = "rating.html"
    def get(self, request):
        return render(request, self.template_name)
