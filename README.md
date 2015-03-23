# PythonMailer

Recently I was on an engagement where I needed to perform an email phishing attack. I threw together a python script to automate the attack and decided to take out the hardcoded data and add more features for future phishing engagements.

Features Include

Specify multiple mail servers

Loadbalance mail servers with RoundRobin or Random
Read email addresses from a file or from the commandline
Randomize the order of email addresses when sending
Specify multiple from addresses from a file or from the command line
Randomize the order of the usage of from addresses
Group emails and specify a sleep time to wait between groups
Read the email body from a file
Replace instances of $image$ with a specified URL
Replace instances of $link$ with a specified URL

Future Features 

Send commands to the script remotely over an encrypted connection
Add attachments to the email
Enhance the grouping to allow specifying which email source and mail server to use for which group



usage: PythonMailer.py [-h] [-l] [--agent-server-ip AGENT_SERVER_IP]
                       [--agent-server-port AGENT_SERVER_PORT]
                       [-m MAIL_SERVER]
                       [--load-balance-type {RoundRobin,Random}]
                       [-t TO_EMAIL_ADDRESS_FILE] [--to-email TO_EMAIL]
                       [-s {List,Random}] [-f FROM_EMAIL_ADDRESSES]
                       [--from-email-address-file FROM_EMAIL_ADDRESS_FILE]
                       [--from-email-balance {RoundRobin,Random}] [-d DELAY]
                       [-g GROUP_SIZE] [-b EMAIL_BODY] [-u SUBJECT]
                       [-a ATTACHMENT] [--replace-link REPLACE_LINK]
                       [--replace-image REPLACE_IMAGE]

For all of your evil email needs

optional arguments:
  -h, --help            show this help message and exit
  -l, --listen          Run as an agent listening for commands. Default False
  --agent-server-ip AGENT_SERVER_IP
                        IP Address to listen on. Default 0.0.0.0
  --agent-server-port AGENT_SERVER_PORT
                        Port number to use for the listening agent. Default
                        333
  -m MAIL_SERVER, --mail-server MAIL_SERVER
                        Mailserver to use. You can specify a port number with
                        the colon. Default port number is 25. You can add this
                        option multiple times. Default localhost:25.
  --load-balance-type {RoundRobin,Random}
                        Mail server load balance type. RoundRobin or Random.
                        Default is RoundRobin.
  -t TO_EMAIL_ADDRESS_FILE, --to-email-address-file TO_EMAIL_ADDRESS_FILE
                        File name with the to email addresses. One address per
                        line in the file.
  --to-email TO_EMAIL   Specify to emails from the commandline by calling this
                        argument multiple times.
  -s {List,Random}, --send-method {List,Random}
                        Method of sending emails. List will start at the first
                        email in the file and go one by one. Random will pop
                        emails out of the list randomly. Default is List
  -f FROM_EMAIL_ADDRESSES, --from-email-addresses FROM_EMAIL_ADDRESSES
                        The email address to send from. This can be specified
                        more than once.
  --from-email-address-file FROM_EMAIL_ADDRESS_FILE
                        File of from email addresses to use.
  --from-email-balance {RoundRobin,Random}
                        The method of balancing the from email addresses.
                        RoundRobin or Random. Default RoundRobin.
  -d DELAY, --delay DELAY
                        The amount of time to delay in seconds between sending
                        emails. Default is 0.
  -g GROUP_SIZE, --group-size GROUP_SIZE
                        The number of emails in a group. Groups will be sent
                        in rapid succession and with the same server. For
                        example if the group size is five, the delay is 10 and
                        there are two servers then five emails will be sent to
                        the first server then a delay of ten seconds then five
                        emails sent to the second server then a delay of ten
                        seconds and so on until all emails have been sent.
  -b EMAIL_BODY, --email-body EMAIL_BODY
                        The file containing the body of the email.
  -u SUBJECT, --subject SUBJECT
                        The subject of the email to send.
  -a ATTACHMENT, --attachment ATTACHMENT
                        File name of an attachment to add. This argument can
                        be specified more than once.
  --replace-link REPLACE_LINK
                        Replaces all instances of $link$ in the email body
                        with the provided link.
  --replace-image REPLACE_IMAGE
                        Replaces all instances of $image$ in the email body
                        with the provided url.
