import ftplib as ftp
import os
import io
import pandas as pd

class FTP:
    def __init__(self,host,username,password,port=21):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.server = ftp.FTP(host=host)
        self.server.login(username,password)
        print(self.server.getwelcome())

    def change_path(self,path:str):
        self.server.cwd(path)

    def list_files(self,path=None):
        if(path != None):
            self.server.cwd(path)
        files = self.server.nlst()
        return files

    def get_file_content(self, filename: str, path: str, local_filename=None):
        if local_filename is None:
            local_filename = filename

        content = None
        with io.BytesIO() as file:
            # Command for retrieving file contents "RETR filename"
            self.server.retrbinary(f"RETR {filename}", file.write)
            content = file.getvalue()

        if content:
            # Read the content as CSV into a Pandas DataFrame
            df = pd.read_csv(io.BytesIO(content),dtype={'lat':str,'lon':str})
            df["vrn"] = df["vrn"].apply(lambda x:x.split("_")[0])

            df = df.drop_duplicates(subset="vrn", keep="first")
            return df

        return None

    def download_file(self,filename:str,path:str,local_filename=None):
        if(local_filename == None):
            local_filename = filename
        with open(os.path.join(path,local_filename), "wb") as file:
            # Command for Downloading the file "RETR filename"
            self.server.retrbinary(f"RETR {filename}", file.write)

    def download_files(self,filenames:list,path:str,local_filename=None):
        if(local_filename == None):
            local_filename = filename
        for filename in filenames:
            with open(path+local_filename, "wb") as file:
                # Command for Downloading the file "RETR filename"
                self.server.retrbinary(f"RETR {filename}", file.write)

    def upload_file(self,path:str):
        with open(path, "rb") as file:
            # Command for Uploading the file "STOR filename"
            self.server.storbinary(f"STOR {os.path.basename(path)}", file)

    def upload_files(self,paths:list):
        for filename in paths:
            with open(filename, "wb") as file:
                # Command for uploading the file "STOR filename"
                self.server.storbinary(f"STOR {os.path.basename(filename)}", file)

    def delete_file(self,file:str):
        self.server.delete(file)

    def delete_files(self,files:list):
        for file in files:
            self.server.delete(file)

    def close(self):
        self.server.quit()


if(__name__ == "__main__"):
    ftp_obj = FTP("192.168.56.1","sagun","sagun")
    ftp_obj.change_path("/Udemy - PyTorch for Deep Learning in 2023 Zero to Mastery 2022-11/1. Introduction/")
    print(ftp_obj.list_files())
    files = ftp_obj.list_files()
    ftp_obj.change_path("/Udemy - PyTorch for Deep Learning in 2023 Zero to Mastery 2022-11/10. PyTorch Paper Replicating/")
    # ftp_obj.download_file('1. PyTorch for Deep Learning.mp4',"temp//")
    # ftp_obj.download_files(files,"temp//")
    ftp_obj.upload_file("C:\\Users\\Dell\\Downloads\\Compressed\\chromedriver_win32\\chromedriver.exe")
    ftp_obj.close()