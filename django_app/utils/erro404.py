from django.http import Http404

def page404(obj):
  if not obj:
    raise Http404
