import paramiko
import sys

host = '112.169.196.210'
username = 'webdev'
# port= '50003'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=username, port=50003, password='1234')
sftp = ssh.open_sftp()
# sftp.get(filepath, localpath)  # 파일 다운로드

localpath = sys.argv[1]
# foldername = 'joy'
filepath='./public_html/onejotest' + sys.argv[1]

sftp.put(localpath, filepath)  # 파일 업로드

sftp.close()
ssh.close()
