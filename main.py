import psutil
from requests import post, exceptions
from datetime import datetime

url = "https://api.privatbank.ua/"


def conversion(num):
    num /= 1000000000
    num = "%.1f" % num
    return num


def ram():
    physical_memory_percent = psutil.virtual_memory().percent
    physical_memory = psutil.virtual_memory().used
    total_physical_memory = psutil.virtual_memory().total
    time = datetime.now().strftime("%H:%M:%S %d-%m-%Y")
    info = f"RAM: {physical_memory_percent}% ({conversion(physical_memory)}/{conversion(total_physical_memory)} GB) is used at {time}"
    return physical_memory_percent, info


def posting():
    try:
        memory_percent, info = ram()
        dict_info = {"Alert": info}
        if memory_percent > 45:
            post(url=url, data= dict_info)
            print(f"Request sent ({info})")
    except exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except exceptions.Timeout as errt:
        print(f"Timeout Error:", errt)
    except exceptions.RequestException as err:
        print(f"OOps, Something Went Wrong: ", err)


if __name__ == '__main__':
    posting()
