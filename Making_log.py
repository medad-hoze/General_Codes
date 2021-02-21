from datetime import datetime
import inspect ,sys
import traceback

class General:
    def __init__(self, function): 
        self.function = function
    class GetMessages(object): 
        """
         @General.GetMessages(skipfailures=True , print_args=True)
         @General.GetMessages()
        """
        def __init__(self,  print_args = True, skipfailures = False): 
            # self.function = function 
            self.print_args = print_args 
            self.skipfailures = skipfailures 
        def __call__(self, function): 
            def aux(*args, **kwargs):
                print(f"Executing: {function.__name__ }")
                bound_args = inspect.signature(function).bind(*args, **kwargs)
                bound_args.apply_defaults()
                dict_args = dict(bound_args.arguments)
                if "kwargs" in   dict_args:
                    if not dict_args["kwargs"]:
                        del dict_args["kwargs"]
                if self.print_args:
                    print("Arguments:" ,dict_args)
                now = datetime.now()
                print(f"Function {function.__name__ }, Start Program: ", now.strftime("%d/%m/%Y %H:%M:%S"))
                # start_time = time.time()
                if self.skipfailures:
                    try:
                        result = function(*args, **kwargs) 
                    except Exception: #as e
                        # print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                        e = traceback.format_exc()
                        print(e)
                        result = None
                else:
                    result = function(*args, **kwargs) 
                now2 = datetime.now()
                print(f"Function {function.__name__ }, End Program:", now2.strftime("%d/%m/%Y %H:%M:%S"))
                seconds = str(now2-now)
                if "." in seconds:
                    seconds = seconds[:seconds.rindex(".")]
                # seconds = time.time() - start_time
                print(f"Function {function.__name__ }, Elapsed Time: {seconds}" )
                # print("Elapsed Time: " +time.strftime("%H:%M:%S",time.gmtime(seconds)))
                return result
            return aux

    class WaitTimeValue(object):
        def __init__(self,WaitTimeSeconds=2, SleepSeconds=2):
            self.WaitTimeSeconds = WaitTimeSeconds
            self.SleepSeconds = SleepSeconds
        def __call__(self, function):
            def aux(*args, **kwargs):
                out = None
                t_end = time.time() +self.WaitTimeSeconds # 60 * 
                while time.time() < t_end and out is None:
                    out = function(*args, **kwargs)
                    if out is None:
                        time.sleep(self.SleepSeconds)
                return  out 
            return aux
    


@General.WaitTimeValue(WaitTimeSeconds=10, SleepSeconds=0.5)
def bar(c):
    print(c)
    return c


bar(None)



@General.GetMessages(skipfailures=True , print_args=False)
def some2(): 
    from time import sleep
   
    # print(25525)
    # sleep(0.2)
    # 1/0
    return 5# a +t
    
t= 6
a = 1

aa=some2()



