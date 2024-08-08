import socket
import threading
import time

PROTOCOL_NAME = "CHATTProtocol"

def print_status(status_code, status_phrase):
    print(f"Status code: {status_code} , Status phrase: {status_phrase}")

def send_msg(client_socket):
    while True:
        msg = input()
        if msg == "DISCONNECT":
            client_socket.sendall("DISCONNECT".encode())
            #แสดงสถานะหลังจากDISCONNECT
            print_status("200", "Success")
            break
        client_socket.sendall(f"MESSAGE {msg}".encode())
        #แสดงสถานะหลังจากส่งข้อความ
        print_status("200", "Success")
        time.sleep(0.1)  #หยุดเวลาสั้นๆเพื่อให้เซิร์ฟเวอร์ได้มีเวลาประมวลผล

def receive_msg(client_socket):
    client_socket.setblocking(False)
    while True:
        try:
            response = client_socket.recv(1024).decode().strip() #ลบช่องว่างเพิ่มเติม
            if response:
                if response.startswith("200"):
                    break
                else:
                    print(f"Server: {response}")
                    status_code = "200"
                    status_phrase = "Success"   
                    print_status(status_code, status_phrase)
        except BlockingIOError:
            time.sleep(0.1)  #หยุดเวลาสั้นๆเพื่อหลีกเลี่ยงการรอ

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

#เริ่มเธรดสำหรับรับและส่งข้อความ
send_thread = threading.Thread(target=send_msg, args=(client_socket,))
receive_thread = threading.Thread(target=receive_msg, args=(client_socket,))

send_thread.start()
receive_thread.start()

send_thread.join()
receive_thread.join()

client_socket.close()
