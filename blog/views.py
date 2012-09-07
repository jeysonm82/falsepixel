from django.http import HttpResponse
from django.template import RequestContext, Context
from django.template.loader import get_template
from blog.models import Entry
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from blog.forms import CommentForm, ContactForm
import random

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
    print "ENTERINNG"
    msg = ''
    if(request.method == 'POST'):
        #check captcha
        code = request.session['captcha_code']
        print "session code", ''.join(code), 'user code', request.POST['captcha'].upper()
        if(''.join(code) == str.strip(str(request.POST['captcha'].upper()))):
            msg = 'Comment posted succesfully. Thanks.!'
        else:
            msg = 'Wrong Captcha. Please Try Again'
        #save comment
        request.session['comment_posted_msg'] = msg
        return redirect('/blog/article/%s'%(e_id))#TODO put marker here to go to specific part of the html

    entry = Entry.objects.get(id=e_id)
    if('comment_posted_msg' in request.session):
        msg= request.session['comment_posted_msg']
        del request.session['comment_posted_msg']

    cf = CommentForm()

    t = get_template("entry.htm")
    c = RequestContext(request, {'entry': entry, 'cform': cf, 'rn': random.randint(1,999999), 'msg': msg})
    return HttpResponse(t.render(c))

def contact(request):
    msg = ''
    if(request.method == 'POST'):
        #TODO send email
        msg = 'Message sent. Thanks.!'
        pass

    t = get_template("contact.htm")
    cf = ContactForm()
    c = RequestContext(request, {'form': cf, 'msg': msg})
    return HttpResponse(t.render(c))


def serve_captcha(request):
    import cv2
    import numpy as np
    im = np.zeros((30,90,3),dtype=np.uint8)+40
    rn = random.randint
    #random noise
    for r in range(75):
        x, y = int(rn(0,im.shape[1]-1)), int(rn(0,im.shape[0]-1))
        cv2.circle(im, (x,y),1,[rn(rn(75,105),255) for x in range(3)])

    code = [chr(65+rn(0,25)).upper() for x in range(4)]
    request.session['captcha_code'] = code
    print_code = ' '.join(code)
    
    cv2.putText(im,print_code,(5,20),cv2.FONT_HERSHEY_PLAIN, 1.2,tuple([rn(rn(75,105),255) for x in range(3)]), thickness=2)

    im=cv2.blur(im,(3,3))
    
    response = HttpResponse(cv2.imencode('.jpg', im)[1].tostring(),mimetype='image/jpeg')
    return response

