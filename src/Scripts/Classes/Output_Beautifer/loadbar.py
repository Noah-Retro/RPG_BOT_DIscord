import sys
class LoadBar:
    def __init__(self,width:int=40,c:str=u"\u2589",color:str='\033[95m',title:str="") -> None:
        self.width = width
        self.c = c
        self.color = color
        self.title = title
        self.o:int=0
        self.setup:bool=0

    def write(self,percent:float):
        if percent == 100:
            sys.stdout.write("|...Completed\n")
            sys.stdout.write('\033[92m')
            return

        w = int(self.width * (percent/100))

        if not self.setup:
            sys.stdout.write(self.color +self.title + "\n")
            sys.stdout.flush()
            sys.stdout.write("|%s|" % (" " * self.width))
            sys.stdout.flush()
            sys.stdout.write("\b" * (self.width+1))
            self.setup=1
        while self.o < w:
            self.o +=1
            # update the bar
            sys.stdout.write(self.color + self.c)
            sys.stdout.flush()