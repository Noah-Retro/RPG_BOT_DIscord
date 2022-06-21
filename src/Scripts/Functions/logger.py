import logging
import platform

def log(num,*args):
    if platform.system() == "Windows":
        logging.basicConfig(encoding="utf-8",level=logging.INFO,filename=r"src\Log\log.txt")
    else:
        logging.basicConfig(encoding="utf-8",level=logging.INFO,filename="src/Log/log.txt")
    """
    log(num,*args)

    loggs args with level num 0-4
    0:Debug
    1:Info
    2:Warning
    3:Error
    4:Critical Error
    """
    if num == 0:
        logging.debug(args)
    elif num==1:
        logging.info(args)
    elif num==2:
        logging.warning(args)
    elif num==3:
        logging.error(args)
    elif num==4:
        logging.critical(args)
    else:
        return logging.critical("logglevel hase wrong level 0-4")
        

if __name__ == '__main__':
    log(0,"Test Logg info level")