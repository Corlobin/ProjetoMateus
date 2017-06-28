#lembrar de não recomendar dependencias!!!!
from Model import Process
def main():
    #entrada = ["d(a,b,c,d)", "<(c;d)", "o(a;b)", "o(a,b;c,d)"]
    #entrada = ["d(a,b,c,d,e)", "o(a,b;c,d)", "<(d;e)"]
    #entrada = ["d(a,b,c,d,e)", "o(a,b;c,d)"]
    entrada = ["d(a,b,c,d,e,f,g,h)", "x(a;b)", "<(c;b)", "<(d;c)", "x(f;g,h)"]
    try:
        processo = Process.Process(entrada)
        processo.carregar()
        processo.step_2()


    except Exception as ex:
        print(ex)

main()