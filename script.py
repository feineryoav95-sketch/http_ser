import socket
import platform
import os
import subprocess
SYSTEMNAME = platform.system()

def getURL(ans):
    """
    return the url from the client request
    :param ans: the request
    :return: the url
    """
    url = None
    line1 = ans.split('\r\n')[0]
    params = line1.split(' ')
    if len(params) == 3 and params[0] == 'GET' and params[2] == "HTTP/1.1":
        url = params[1]
    if url == "/":
        url = "/index.html"
    return url[1:]

def getData (url):
    """

    :param url:
    :return: length and data of the file
    """
    file_info = None
    file_len = None
    if os.path.isfile(url):
        with open(url, 'rb') as file:
            data = file.read()
            file_len = len(data)
            file_info = data

    return file_info,file_len

def calculate_next(url):
    """

    :param url:
    :return: length of number, number
    """
    num = 5
    len_num = 1
    if not url == "calculate-next":
        if url[:14:1] == "calculate-next":
            if url[14:19:1] == "?num=":
                len_num = len((url[19::1]))
                num = int(url[19::1])
                num+=1
                num = str(num)
    return num,len_num

def calculate_area(height,width):
    """

    :param height:
    :param width:
    :return: area of triangle, length of area
    """
    area = None
    len_area = None
    if height > 0 and width > 0:
        area = (height*width)/2
        area = str(area)
        len_area = len(area)
    return area,len_area
server_socket = socket.socket()
server_socket.bind(("0.0.0.0", 80)) #if 80 not work do 8080
server_socket.listen(3)


while True:
    client_socket, addr = server_socket.accept()
    print(f"{addr[0]} - connected")

    try:
        data = client_socket.recv(1024).decode()
    except Exception as e:
        print(f"error in receive {str(e)}")
    else:
        print(data)

    new_dict = {"C:/Users/feine/PycharmProjects/http_ser/secret.txt":"C:/Users/feine/PycharmProjects/http_ser/secret2.txt"}
    no_access = ["C:/Users/feine/PycharmProjects/http_ser/hapoel.png"]
    url = getURL(data)


    if url:
        if url in new_dict:
            url = new_dict[url]
        file_info,file_len = getData(url)

        if url not in no_access:
            ans = f"HTTP/1.1 200 OK\r\nContent-Length: {str(file_len)}\r\n\r\n"
        else:
            ans = f"HTTP/1.1 403 Not Allowed\r\nContent-Length: 0\r\n\r\n"

        if url.lower() == "server":
            ans = f"HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\n\r\n"

        elif url == "calculate-next" or (url[:19:1] == "calculate-next?num=" and url[19::1].isdigit()):#check if valid message for calculating next number
            num,len_num = calculate_next(url)
            ans = f"HTTP/1.1 200 OK\r\nContent-Length: {str(len_num)}\r\n\r\n"
            file_info = num.encode()

        elif url[0:22:1] == "calculate-area?height=" and url[22:url.find("&"):1].isdigit() and url[url.find("&"):url.find("&")+7:1] == "&width=" and url[url.find("&")+7::1].isdigit():#check if valid message for calculating area
            height, width = int(url[22:url.find("&"):1]), int(url[url.find("&")+7::1])
            area,len_area = calculate_area(height,width)
            ans = f"HTTP/1.1 200 OK\r\nContent-Length: {str(len_area)}\r\n\r\n"
            file_info = area.encode()

        elif not file_info:
            ans = f"HTTP/1.1 404 Not Found \r\nContent-Length: 0\r\n\r\n"
        try:
            client_socket.send(ans.encode())
            client_socket.send(file_info)
        except Exception as e:
            print(f"error in receive {str(e)}")
    client_socket.close()

server_socket.close()
