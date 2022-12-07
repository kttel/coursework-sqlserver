from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

from . import models


class RedirectIfNotStuff(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return redirect('posts')
        return super(RedirectIfNotStuff, self).dispatch(request, *args, **kwargs)


class RedirectIfNotOwnReview(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        review = models.Review.objects.get(pk=self.kwargs.get('pk'))
        if not self.request.user.is_anonymous:
            profile = models.Profile.objects.get(user=self.request.user)
            if review.profile != profile and not profile.user.is_staff:
                return redirect('book', pk=review.book.id)
        else:
            return redirect('book', pk=review.book.id)
        return super(RedirectIfNotOwnReview, self).dispatch(request, *args, **kwargs)
