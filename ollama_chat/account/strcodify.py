import base64


def str_codify(x:str):
    return base64.urlsafe_b64encode(x.encode()).decode()
    
    # 
    # g = (f"{ord(c):03}" for c in x)
    # return "".join(g)


def str_decodify(x:str):
    return base64.urlsafe_b64decode(x.encode()).decode()
    
    #
    # g = (chr(int(x[3*n:((3*n)+3)])) for n in range(0, int(len(x)/3)))
    # return "".join(g)

