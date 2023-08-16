from django.shortcuts import get_object_or_404
from django.views import generic as views


class UserProfileDetailsMixin(views.DetailView):
    profile = None

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        try:
            user_id = pk if pk == self.request.user.pk else self.request.user.pk
            return get_object_or_404(self.profile, user_id=user_id)
        except:
            return get_object_or_404(self.profile, user_id=pk)
