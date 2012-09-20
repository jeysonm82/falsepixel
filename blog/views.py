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
from django.contrib.auth import logout
from django.template import Template

def test(request):
    """ Test view """
    t = get_template("test.htm")
    print request.user
    print "SEssion captcha ", 'captcha_code' in request.session.keys()
    print request.session['captcha_code']
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
        user_data= {'author': request.POST['author'] , 'email': request.POST['email'], 'message': request.POST['message'],'captcha': request.POST['captcha'] }

        #check captcha
        code = request.session['captcha_code']

        if(request.user.is_authenticated()):
            #user auth witrh external account
            user_data['author'] = '%s %s '%(request.user.first_name, request.user.last_name ) 
            
            if(request.session['backend'] == 'twitter'):
                user_data['author'] += '(@%s)'%(request.user.username)
            else:
                user_data['author'] +='(%s)'%(request.session['backend'])

            if(request.user.email == ''):
               user_data['email'] = 'mail@nomail.com'#request.user.email
            else:
               user_data['email'] = request.user.email
            logout(request)

        cf = CommentForm(user_data)
            
        if(cf.is_valid()):
            #Check Captcha
            if(''.join(code) == str.strip(str(request.POST['captcha'].upper()))):
                #save comment
                com = Comment()
                com.author = cf.cleaned_data['author']
                com.content = cf.cleaned_data['message']
                com.email = cf.cleaned_data['email']
                com.entry = entry
                try: 
                    com.save()
                    msg = 'Comment posted succesfully. Thanks.!'
                except:
                    msg = 'Error saving your comment. Please try again.' 
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
    cf = ContactForm()
    if(request.method == 'POST'):
        #TODO send email
        cf = ContactForm(request.POST)
        if(cf.is_valid()):
            try:
                send_email('test@falsepixel.net', 'jjmc82@gmail.com', 'Falsepixel: '+ cf.cleaned_data['name'] + ' wrote to you.', cf.cleaned_data['email'] +'<br>' +cf.cleaned_data['message'])
                msg = 'Message sent. Thanks.!'
            except:
                msg = 'Error sending msg. Try again please.'
        else:
            msg = 'Error sendin msg. Please verify fields.'

    t = get_template("contact.htm")
    c = RequestContext(request, {'form': cf, 'msg': msg})
    return HttpResponse(t.render(c))


def serve_captcha(request):
   request.session['captcha_code'], response = create_captcha()   
   print "Saving captcha code", request.session['captcha_code']
   return response

def index(request):
    t = get_template("index.htm")
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))

def login_conf(request):
    msg = ''
    if(request.user.is_authenticated()):
        msg = 'Logged in! %s from %s'%(request.user.username, request.session['social_auth_last_login_backend'])
        request.session['backend'] = request.session['social_auth_last_login_backend']
        t = get_template('login_success.htm')
        c = RequestContext(request, {'msg': msg})
        return HttpResponse(t.render(c))

def logout_view(request):
    captcha_code = request.session['captcha_code']
    logout(request)
    request.session['captcha_code'] = captcha_code
    return HttpResponse("Logout Done.!")
def log_error(request):
    return HttpResponse("Couldn't log, try again")
