import multiprocessing as mp
from imagesearch import imagesearch_loop

def foo():
    print("hola")
    if  imagesearch_loop("images\initiateLink.jpg", 2, 0.8) != -1:
            print("1280*1024 detected")

if __name__ == '__main__':
    mp.set_start_method('spawn')
    p = mp.Process(target=foo)
    p.start()
    p.join()