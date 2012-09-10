from django.http import HttpResponse
import random
import cv2
import numpy as np
import smtplib
from email.mime.text import MIMEText

def create_captcha():
    #TODO define parameters
    im = np.zeros((30,90,3),dtype=np.uint8)+40
    rn = random.randint
    #random noise
    for r in range(75):
        x, y = int(rn(0,im.shape[1]-1)), int(rn(0,im.shape[0]-1))
        cv2.circle(im, (x,y),1,[rn(rn(75,105),255) for x in range(3)])

    code = [chr(65+rn(0,25)).upper() for x in range(4)]
    print_code = ' '.join(code)
    
    cv2.putText(im,print_code,(5,20),cv2.FONT_HERSHEY_PLAIN, 1.2,tuple([rn(rn(75,105),255) for x in range(3)]), thickness=2)

    im=cv2.blur(im,(3,3))
    
    response = HttpResponse(cv2.imencode('.jpg', im)[1].tostring(),mimetype='image/jpeg')
    return (code, response)


def send_email(From, to, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] =  From
    msg['To'] =  to
    try:
        s = smtplib.SMTP('localhost')
        s.sendmail(msg['From'], [msg['To']], msg.as_string())
        s.quit()
        return True
    except:
        print "Error sending email"
        return False

    
