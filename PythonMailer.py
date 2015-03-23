import sys
import argparse
import io
import smtplib
import os
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class ServerEngine:
    def start_server():
        pass
    
class CoreEngine:
    def __init__(self,configuration):
        self.configuration = configuration
        self.load_balance_index = 0
        self.from_email_index = 0
        
    def get_next_email(self):
        if not self.configuration.to_email:
            return ''
        
        if self.configuration.send_method == 'List':
            return self.configuration.to_email.pop(0)
        elif self.configuration.send_method == 'Random':
            return self.configuration.to_email.pop(os.urandom(len(self.configuration.to_email_list) - 1))
        elif self.configuration.send_method == 'RuleBased':
            raise NotImplementedError
        return ''
    
    def get_next_server(self):
        if len(self.configuration.mail_server) <= 0:
            raise AttributeError
        
        if len(self.configuration.mail_server) == 1:
            return self.configuration.mail_server[0]

        if self.configuration.load_balance_type == 'RoundRobin':
            if self.load_balance_index >= len(self.configuration.mail_server):
                self.load_balance_index = 0
                
            current_server = self.configuration.mail_server[self.load_balance_index]
            self.load_balance_index += 1
            return current_server
        
        elif self.configuration.load_balance_type == 'Random':
            return self.configuration.mail_server[os.urandom(len(self.configuration.mail_server) - 1)]

        return ''
    
    def get_next_sending_address(self):
            if self.configuration.from_email_balance == 'RoundRobin':
                next_address = self.configuration.from_email_addresses[self.from_email_index]
                
                #Add one to the current index
                self.from_email_index += 1
                
                #If the current index is greater than or equal to the number of email addresses
                #Set the index to zero
                if self.from_email_index >= len(self.configuration.from_email_addresses) - 1:
                    self.from_email_index = 0
                
                #Return the address
                return next_address
    
            elif self.configuration.from_email_balance == 'Random':
                #Pick a random from email address
                return self.configuration.from_email_addresses[os.urandom(len(self.configuration.from_email_addresses) - 1)]
            return ''    
    
        
        
    def run(self):
        #Get the body from the file
        body_file = open(configuration.email_body,'r')
        html = body_file.read()
        body_file.close()
    
        #Replace the links
        if '$link$' in html and configuration.replace_link:
            html = html.replace('$link$',self.configuration.replace_link)
        #Replace the images
        if '$image$' in html and configuration.replace_image:
            html = html.replace('$image$',self.configuration.replace_image)
    
        #MIMEify the text
        mime_type = 'html'
    
        html_mime = MIMEText(html, mime_type) 
        
        #Get the first email address
        email_address = self.get_next_email().strip()
        
        #Initialize the group count
        group_count = 1
        
        #Get the next email server
        #NOTE: If there's only one mail server should move this outside of the loop
        #so there isn't a separate mail server instance for each email
        mail_server = self.get_next_server().split(':')        

        #Enter a loop until there are no more email addresses
        while email_address:
            #Get the next mail from address
            mail_from = self.get_next_sending_address().strip()
            
            #If there is no mail server raise an exception
            if not mail_server:
                raise ReferenceError
            
            #Create the email message
            msg = MIMEMultipart('alternative')
            msg['subject'] = self.configuration.subject
            msg['From'] = mail_from
            msg['To'] = email_address
            
            #Attach it to the message
            msg.attach(html_mime)
            
            #Create smtp client
            client = smtplib.SMTP(host=mail_server[0], port=str(mail_server[1]))
            
            #Send the email
            print '[*] Sending email'
            client.sendmail(mail_from,email_address,msg.as_string())
            
            #Close the client
            client.quit()
            
            print '[*] Email sent'
        
            #If there is a delay and the group count is greater than or equal to the group size
            #Sleep for the amount given in the delay variable then reset the group count
            #Otherwise add one to the group count
            if self.configuration.group_size <= group_count:
                time.sleep(self.configuration.delay)
                group_count = 0
                mail_server = self.get_next_server().split(':')  
            else:
                group_count += 1
            
            #Get the next email address to work with
            email_address = self.get_next_email().strip()
            
        

def main():
    global configuration
    
    #Read arguments from the command prompt
    parser = argparse.ArgumentParser(description='For all of your evil email needs')
    parser.add_argument('-l','--listen',action='store_true',default=False, help='Run as an agent listening for commands. Default False')
    parser.add_argument('--agent-server-ip',default='0.0.0.0',help='IP Address to listen on. Default 0.0.0.0')
    parser.add_argument('--agent-server-port',type=int,help='Port number to use for the listening agent. Default 333')
    parser.add_argument('-m','--mail-server',action='append',default=["localhost:25"],help='Mailserver to use. You can specify a port number with the colon. Default port number is 25. You can add this option multiple times. Default localhost:25.')
    parser.add_argument('--load-balance-type',choices=['RoundRobin','Random'],default='RoundRobin',help='Mail server load balance type. RoundRobin or Random. Default is RoundRobin.')
    parser.add_argument('-t','--to-email-address-file', help='File name with the to email addresses. One address per line in the file.')
    parser.add_argument('--to-email',action='append',default=[],help='Specify to emails from the commandline by calling this argument multiple times.')
    parser.add_argument('-s','--send-method',choices=['List','Random'],default='List',help='Method of sending emails. List will start at the first email in the file and go one by one. Random will pop emails out of the list randomly. Default is List')
    parser.add_argument('-f','--from-email-addresses',action='append', default=[],help='The email address to send from. This can be specified more than once.')
    parser.add_argument('--from-email-address-file', help='File of from email addresses to use.')
    parser.add_argument('--from-email-balance', choices=['RoundRobin','Random'],default='RoundRobin',help='The method of balancing the from email addresses. RoundRobin or Random. Default RoundRobin.')
    parser.add_argument('-d','--delay',type=int,default=0,help='The amount of time to delay in seconds between sending emails. Default is 0.')
    parser.add_argument('-g','--group-size',type=int,default=1,help='The number of emails in a group. Groups will be sent in rapid succession and with the same server. For example if the group size is five, the delay is 10 and there are two servers then five emails will be sent to the first server then a delay of ten seconds then five emails sent to the second server then a delay of ten seconds and so on until all emails have been sent.')
    parser.add_argument('-b','--email-body',help='The file containing the body of the email.')
    parser.add_argument('-u','--subject',help='The subject of the email to send.')
    parser.add_argument('-a','--attachment',action='append',default=[],help='File name of an attachment to add. This argument can be specified more than once.')
    parser.add_argument('--replace-link',help='Replaces all instances of $link$ in the email body with the provided link.')
    parser.add_argument('--replace-image', help='Replaces all instances of $image$ in the email body with the provided url.')
    configuration = parser.parse_args()
    
    if configuration.listen:
        #Start listening for connections
        pass
    
    else:
        #If an email address file was specified pull out the email addresses
        if configuration.to_email_address_file:
            email_address_file = open(configuration.to_email_address_file, 'r')
            configuration.to_email = email_address_file.readlines()
            email_address_file.close()
        #If a from email address was specified pull out the from email addresses
        if configuration.from_email_address_file:
            from_address_file = open(configuration.from_email_address_file,'r')
            configuration.from_email_addresses = from_address_file.readlines()
            from_address_file.close()
        
        #Create the engine and run it
        engine = CoreEngine(configuration)
        engine.run()
        
main()
