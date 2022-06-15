
class HelthBar:
    def __init__(self) -> None:
        pass

    @staticmethod
    def healthbar(is_health:int,max_health:int,length=10)->str:
        full = is_health/(max_health/length)
        r = ""
        r+="▄"*int(full)
        if full <0:
            r="▁"*length
            return r
        rest=length-int(full)
        r+="▁"*rest
        return r  

if __name__ == '__main__':
    print(HelthBar.healthbar(334,-100))