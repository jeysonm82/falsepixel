from django.http import HttpResponse
from django.template import RequestContext, Context
from django.template.loader import get_template
from blog.models import Entry, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from blog.forms import CommentForm, ContactForm
import bbcode
import random
from blog.util import create_captcha, send_email
from django.utils.safestring import mark_safe 

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
    entry = Entry.objects.get(id=e_id)
    entry.parsed_content = mark_safe(entry.content) #bbcode.render_html(entry.content) 
    msg = ''
    if(request.method == 'POST'):
        cf = CommentForm(request.POST)
        #check captcha
        code = request.session['captcha_code']
        if(cf.is_valid()):
            #Check Captcha
            if(''.join(code) == str.strip(str(request.POST['captcha'].upper()))):
                #save comment
                com = Comment()
                com.author = cf.cleaned_data['author']
                com.content = cf.cleaned_data['message']
                com.entry = entry
                try: 
                    com.save()
                    msg = 'Comment posted succesfully. Thanks.!'
                except:
                    msg = 'Error processing your comment. Please try again.' 
            else:
                msg = 'Wrong Captcha code. Please Try Again'
            
        else:
            msg = 'Error processing your comment. Please Try Again.'

        request.session['comment_posted_msg'] = msg
        return redirect('/blog/article/%s'%(e_id))#TODO put marker here to go to specific part of the html

    if('comment_posted_msg' in request.session):
        msg= request.session['comment_posted_msg']
        del request.session['comment_posted_msg']
    comments = entry.comment_set.filter(status=True)
    cf = CommentForm()

    t = get_template("entry.htm")
    c = RequestContext(request, {'entry': entry,'comments': comments, 'cform': cf, 'rn': random.randint(1,999999), 'msg': msg})
    return HttpResponse(t.render(c))

def contact(request):
    msg = ''
    if(request.method == 'POST'):
        #TODO send email
        cf = ContactForm(request.POST)
        if(cf.is_valid()):
            send_email('test@falsepixel.net', 'jjmc82@gmail.com', 'Falsepixel: '+ cf.cleaned_data['name'] + ' wrote to you.', cf.cleaned_data['email'] +'<br>' +cf.cleaned_data['message'])
        msg = 'Message sent. Thanks.!'
        

    t = get_template("contact.htm")
    cf = ContactForm()
    c = RequestContext(request, {'form': cf, 'msg': msg})
    return HttpResponse(t.render(c))


def serve_captcha(request):
   request.session['captcha_code'], response = create_captcha()   
   return response

def index(request):
    t = get_template("index.htm")
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))
