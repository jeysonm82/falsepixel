from django.http import HttpResponse
from django.template import RequestContext, Context
from django.template.loader import get_template
from blog.models import Entry
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def test(request):
    """ Test view """
    t = get_template("test.htm")

    return HttpResponse(t.render(Context({})))

def get_entries(request, cat='all', page=1):
    """ Generates entry list of index page """

    page = int(page)
    if(cat == 'all'):
        entry_list = Entry.objects.order_by('-id').filter(published=True)
    p = Paginator(entry_list, 3)
    try:
        entries = p.page(page)
    except EmptyPage:
        entries = p.page(p.num_pages)
    except PageNotAnInteger:
        entries = p.page(1)


    t = get_template("entry_list.htm")
    c = RequestContext(request, {'entries': entries, 'cur_page': page , 'has_prev': entries.has_previous(), 'has_next': entries.has_next() ,'next_page': page+1, 'prev_page': page-1 }
)
    return HttpResponse(t.render(c))


def view_entry(request, e_id):
    """ View Entry """
    #TODO generic view
    entry = Entry.objects.get(id=e_id)

    t = get_template("entry.htm")
    c = RequestContext(request, {'entry': entry})
    return HttpResponse(t.render(c))
