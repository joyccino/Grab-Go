from ftplib import FTP

ftp = FTP()
ftp.connect("112.169.196.210",50001)
# ftp.connect("112.169.196.210")
# ftp = FTP('ftp://112.169.196.210:50001')
# ftp = FTP('ftp://112.169.196.210:50001/')
ftp.login('ftpuser', '1234')
# ftp.login()
ftp.cwd('./files')  # 업로드할 FTP 폴더로 이동
myfile = open('/home/moon/Desktop/chosenones/1/customers/175.jpg','rb')  # 로컬 파일 열기
ftp.storbinary('STOR 175.jpg', myfile )  # 파일을 FTP로 업로드
myfile.close()  # 파일 닫기
ftp.quit()