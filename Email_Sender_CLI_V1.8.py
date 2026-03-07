# INA WORK VI FITY THOUGH RELAY NOT TASTED 

import smtplib
import msvcrt
import sys
import os
import time
from email.message import EmailMessage
from email.utils import formataddr
from mimetypes import guess_type

print("""
                                                                           
                                                                                         
                                      -%*-...                                            
                                      :@@@@@@@*:.                                        
                                       +@@*%@@@@@@@%+:.                                  
                                       :@@@%-#@@@@@@@@@@@#+:.                            
                                       .=@@@@=.+@@@@@@@@@@@#.                            
                                         #@@@@%..=@@@@@@@*..                             
                .....    .... ...        -@@@@@@-...%@@-.                                
              .@@%=*@@-  .*#. #%.        .*@@@@@@#.....                                  
             .%+.    :@-  +*. #%:###:     .%@@@@@@@:       .+##*.   *-=##*.              
             =@           *%. #@+. .%*.    =@@@@@@@=      -@-..:@+  %@:..*%.             
             =@   .###@#. *%. #%.   :@:    .%@@@@@@@.    .@=    -@. %=   .@.             
             .@+.    .@-  *%. #%.   -@.    .+@@@@@@@*.   .%+    =@  %=   .@.             
              .@@%-+@@=   *%. #@@-.*@=.     .=@@@@@@@-    .%%:.%@:  %=   .@.             
                ..::.     ... ....:..  .*@@+...#@@@@@#     ..::..   ..   ...             
                                    .:#@@@@@@*..-@@@@@=.                                 
                                   -@@@@@@@@@@@%-.#@@@@:                                 
                                   .-*%@@@@@@@@@@@==@@@+.                                
                                         .-#@@@@@@@@#%@@:.                               
                                             ...-#@@@@@@#.                               
                                                  ...:=#%:                               
                                                                                         


""")

def get_input_until_escape(prompt):
    print(f"{prompt} (Press 'ESC' to finish writing):")
    content = ""
    while True:
        if msvcrt.kbhit():
            char = msvcrt.getch()
            if ord(char) == 27: # ESC
                print("\n[Message Captured]")
                break
            elif ord(char) == 13: # Enter
                content += "\n"
                sys.stdout.write("\n")
            elif ord(char) == 8: # Backspace
                content = content[:-1]
                sys.stdout.write("\b \b")
            else:
                try:
                    letter = char.decode('utf-8')
                    content += letter
                    sys.stdout.write(letter)
                except: pass
            sys.stdout.flush()
    return content

def send_bulk_email():
    print("\n\n--- Python Bulk Mailer 1.8  ---")


    mode = input("Select Mode: (1) Personal (Gmail) or (2) External Relay: ")

    # 1. Configuration
    if mode == "1":
        smtp_server, smtp_port = "smtp.gmail.com", 465
        user_email = input("Your Email: ")
        password = input("App Password: ")
    else:
        smtp_server = input("Relay SMTP Server: ")
        smtp_port = int(input("Relay Port: "))
        user_email = input("Username/API Key: ")
        password = input("Password/API Secret: ")

    # 2. Recipient List Loading
    list_path = input("\nEnter path to .txt file with emails: ").strip('"')
    if not os.path.exists(list_path):
        print("Error: Email list file not found!")
        return
    
    with open(list_path, 'r') as f:
        # Removes whitespace and empty lines
        recipients = [line.strip() for line in f if line.strip()]
    
    print(f"Loaded {len(recipients)} recipients.")

    # 3. Message Details
    display_name = input("\nCustom Sender Name: ")
    subject = input("Subject: ")
    is_html = input("Send as HTML? (y/n): ").lower() == 'y'
    body_content = get_input_until_escape("\nEnter Email Body")

    # 4. Global Message Setup (Headers & Attachments)
    # We create a template message here
    template_msg = EmailMessage()
    template_msg['Subject'] = subject
    template_msg['From'] = formataddr((display_name, user_email))
    
    if is_html:
        template_msg.set_content("HTML Content - Please use a compatible client.")
        template_msg.add_alternative(body_content, subtype='html')
    else:
        template_msg.set_content(body_content)

    # Attachments (Added once to the template)
    while True:
        f_path = input("\nAttach a file? (Path or Enter to skip): ").strip('"')
        if not f_path: break
        if os.path.isfile(f_path):
            ctype, _ = guess_type(f_path)
            maintype, subtype = (ctype or 'application/octet-stream').split('/', 1)
            with open(f_path, 'rb') as f:
                template_msg.add_attachment(f.read(), maintype=maintype, subtype=subtype, filename=os.path.basename(f_path))
            print(f"Attached {os.path.basename(f_path)}")

    # 5. Sending Loop
    try:
        print("\nConnecting to server...")
        Mailer = smtplib.SMTP_SSL if smtp_port == 465 else smtplib.SMTP
        
        with Mailer(smtp_server, smtp_port) as server:
            if smtp_port != 465: server.starttls()
            server.login(user_email, password)
            
            for target in recipients:
                # Update the 'To' header for each person
                del template_msg['To']
                template_msg['To'] = target
                
                server.send_message(template_msg)
                print(f"Email sent to - {target} -")
                time.sleep(1) # Small delay to prevent spam triggers
                
        print("\nBulk delivery complete!")
    except Exception as e:
        print(f"Critical Error: {e}")

if __name__ == "__main__":
    send_bulk_email()