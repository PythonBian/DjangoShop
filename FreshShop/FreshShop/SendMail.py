
import smtplib #登陆邮件服务器，进行邮件发送
from email.mime.text import MIMEText #负责构建邮件格式

subject = "老边的学习邮件"
content = "孩子不学习，多半是欠的，抄五遍就好了"
sender = "3392279511@qq.com"
recver = """3392279511@qq.com,
215558997@qq.com,
773733859@qq.com,
912575770@qq.com,
1529825704@qq.com,
1307128051@qq.com,
721788741@qq.com,
3303236612@qq.com,
710731910@qq.com,
329688391@qq.com,
626978318@qq.com,
419538402@qq.com,
1637805820@qq.com,
738389368@qq.com,
329688391@qq.com,
1225858108@qq.com,
329688391@qq.com,
1225858108@qq.com"""

password = "svhbjrvepdoqdbfi"

message = MIMEText(content,"plain","utf-8")
message["Subject"] = subject
message["To"] = recver
message["From"] = sender

smtp = smtplib.SMTP_SSL("smtp.qq.com",465)
smtp.login(sender,password)
smtp.sendmail(sender,recver.split(",\n"),message.as_string())
smtp.close()

