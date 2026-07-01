from scapy.all import IP, TCP, Raw, wrpcap
import time
import random
import math

def generate_remote_pcap():
    packets = []
    src_ip = "192.168.1.10"
    dst_ip = "142.250.190.46" # Cloud Service IP
    
    # Parametros iniciales
    timestamp = time.time()
    sport = 54321
    dport = 443
    seq_num = 1000
    ack_num = 5000
    
    print("[+] Generating Dataset A: Remote Cloud Inference (30ms continuous streaming)...")
    
    for i in range(200):
        # Generacion de bytes pseudo-aleatorios emulando registros de datos TLS 1.3 (Alta entropia)
        # ContentType: 0x17 (Application Data), Version: 0x0303 (TLS 1.2/1.3 legacy compatibility), Length: 512
        tls_header = b'\x17\x03\x03\x02\x00' 
        encrypted_payload = bytes([random.randint(0, 255) for _ in range(507)])
        payload = tls_header + encrypted_payload
        
        # Construccion del paquete de red
        pkt = IP(src=src_ip, dst=dst_ip) / \
              TCP(sport=sport, dport=dport, seq=seq_num, ack=ack_num, flags="PA") / \
              Raw(load=payload)
              
        # Asignacion del timestamp con variacion estocastica menor (Red normal sin congestion severa)
        pkt.time = timestamp
        packets.append(pkt)
        
        # Acumulacion secuencial monotona para evitar inversiones cronologicas (IPT ~30ms)
        jitter = random.normalvariate(0, 0.002) # Desviacion minima
        timestamp += 0.030 + jitter 
        seq_num += len(payload)

    # Exportacion directa del dataset binario PCAP
    output_path = "datasets/synthetic_remote_llm.pcap"
    wrpcap(output_path, packets)
    print(f"[✓] Dataset A successfully saved to: {output_path}")

if __name__ == "__main__":
    generate_remote_pcap()