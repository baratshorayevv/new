
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import PermissionDenied
from .bad_words import BAD_WORDS

class BlockBadWordsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            for word in BAD_WORDS:
                if word in request.POST.get('content', '').lower():
                    raise PermissionDenied("You are blocked for using inappropriate language.")
