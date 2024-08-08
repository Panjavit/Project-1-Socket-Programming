import socket
import threading
import time

PROTOCOL_NAME = "CHATTProtocol"

def print_status(status_code, status_phrase):
    print(f"Status code: {status_code} , Status phrase: {status_phrase}")

def handle_client_connection(conn, addr, clients):
    conn.setblocking(False)  
    print(f"Client {addr} connected.")  #แสดงข้อความหลังจากclientเชื่อมต่อ
    while True:
        try:
            data = conn.recv(1024).decode().strip()  #รับข้อมูลจากclientและลบช่องว่าง
            if data:
                if data == "DISCONNECT":
                    status_code = "200"
                    status_phrase = "Success"
                    response = f"STATUS {status_code} {status_phrase}"
                    conn.sendall(response.encode())  #ส่งสถานะกลับไปยังclient
                    print_status(status_code, status_phrase)
                    break
                elif data.startswith("MESSAGE"):
                    message = data.split(" ", 1)[1]  #แยกข้อความที่ได้รับ
                    print(f"Client {addr}: {message}")  #แสดงข้อความจากclient
                    for client in clients:
                        if client != conn:
                            client.sendall(f"Client {addr}: {message}".encode())  #ส่งข้อความไปยังclientอื่น
                    status_code = "200"
                    status_phrase = "Success"
                    print_status(status_code, status_phrase)
        except BlockingIOError:
            time.sleep(0.1)  #หยุดสั้นๆ พื่อหลีกเลี่ยงการรอ
    conn.close()  #ปิดการเชื่อมต่อ
    clients.remove(conn)  #เอาclientออกจากรายการ
    print(f"Client {addr} disconnected.")  #แสดงข้อความเมื่อclient DISCONNECT

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))  # ผูกซ็อกเก็ตกับที่อยู่และพอร์ต
server_socket.listen(5) 

clients = []

print("Server is listening on port 12345...")  #แสดงข้อความเมื่อเซิร์ฟเวอร์เริ่มทำงาน

while True:
    conn, addr = server_socket.accept()  #ยอมรับการเชื่อมต่อจากclient
    clients.append(conn)  #เพิ่มclientลงในรายการ
    threading.Thread(target=handle_client_connection, args=(conn, addr, clients)).start()  #สร้างเธรดใหม่เพื่อจัดการการเชื่อมต่อ
