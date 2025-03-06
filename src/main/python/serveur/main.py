from app import app
# import netifaces
#
# def get_ipv4():
#     for interface in netifaces.interfaces():
#         addrs = netifaces.ifaddresses(interface)
#         if netifaces.AF_INET in addrs:
#             for addr in addrs[netifaces.AF_INET]:
#                 if addr["addr"] != "127.0.0.1":  # Exclure localhost
#                     return addr["addr"]
#     return "127.0.0.1"
#
# ip_server = get_ipv4()

import views

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000")