import imaplib
import email
import rich
from rich.console import Console
from rich import print as p
import base64
from subprocess import run
#global variables :
console=Console()
app_pass:'str'='erza sdaw seik fiei'
imap_server :'str'='imap.gmail.com'
port:'int'=993
def main():
    #login , and Authentication
    mail=imaplib.IMAP4_SSL(host=imap_server,port=993) #this creates am imap session over ssl encryption
    mail.login(user="hussamcyber231@gmail.com",password=app_pass) #Authentication using app password
    mail.select() #For a certain reason , only inbox is available .
    #search : performs a search for email in the mail.select() , and returns ->data:space seperated string of email nums that match , we will
    #use it later to fetch the email .
    #choosing the filter :
    filtere=input("enter what you want to retrive , Available filters :[1.From ,src email, or ALL]\naccepted Form : From email adress   or ALL\n")
    data=None
    try:
        if filtere.split()[0]=='ALL':
            _,data=mail.search(None,'ALL')
        elif filtere.split()[0]=='From':
            _, data = mail.search(None, 'From',filtere.split()[1])
    except imaplib.IMAP4.error:
        raise SystemExit("unaccepted filter\n")
    mail_numbers_list:'list'=data[0].split()
    #setting the maximum numbers of messages to view :
    max_limit=int(input("enter how much messages you want to read , enter -1 to get everything\n"))
    for msg_num in mail_numbers_list:
        _,data=mail.fetch(msg_num,'(RFC822)') #fetching the matched email based on its number
        my_msg=email.message_from_bytes(data[0][1])
        console.print("_________________________________________________________________",style='yellow bold')
        console.print(f"From : {my_msg['From']}",style='yellow bold')
        console.print(f"To : {my_msg['To']}",style='yellow bold')
        console.print(f"Date : {my_msg['Date']}",style='yellow bold')
        console.print(f"Subject : {my_msg['Subject']}", style='yellow bold')
        console.print("Body :",sep='\n',style='yellow bold')
        for part in my_msg.walk():
                if  part.get_content_type()=='text/plain':
                        payload=part.as_string()
                        if payload.startswith('Content-Type:'):
                            validate=payload.split('\n',maxsplit=3)
                            try:
                                if validate[1].split(':')[1].strip()=='base64':
                                    payload=base64.b64decode(validate[3]).decode()
                                    console.print(payload,style='bright_green')
                                else:
                                    console.print(validate[3], style='bright_green')
                            except:
                                pass
        if max_limit==0:
            break
        max_limit-=1





if __name__=="__main__":
    main()


