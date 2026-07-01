from scapy.all import IP, TCP, Raw, wrpcap
import time
import random
import base64

def generate_mixed_pcap():
    packets = []
    src_ip = "172.16.0.10"
    dst_ip = "198.51.100.50" # Malicious Target Destination
    
    timestamp = time.time()
    sport = 5555
    dport = 443
    seq_num = 3000
    ack_num = 7000
    
    print("[+] Generating Dataset C: Mixed Exfiltration / Covert Timing Channel...")
    
    # 1. TRAFICO DE FONDO (Baseline normal - 120 paquetes cada 40ms)
    for i in range(120):
        tls_header = b'\x17\x03\x03\x01\x00' # Estructura TLS estandar
        dummy_data = bytes([random.randint(0, 255) for _ in range(251)])
        payload = tls_header + dummy_data
        
        pkt = IP(src=src_ip, dst=dst_ip) / \
              TCP(sport=sport, dport=dport, seq=seq_num, ack=ack_num, flags="PA") / \
              Raw(load=payload)
              
        pkt.time = timestamp
        packets.append(pkt)
        
        timestamp += 0.040 # Flujo continuo regular de 40ms
        seq_num += len(payload)
        
    # 2. RAFAGA DE EXFILTRACION (Covert Timing Channel - 40 paquetes cada 5ms)
    print("[!] Injecting highly aggressive micro-burst data exfiltration leakage...")
    for j in range(40):
        tls_header = b'\x17\x03\x03\x02\x00'
        # Simula datos sensibles pre-cifrados o codificados en Base64 de alta densidad
        leak_data = base64.b64encode(bytes([random.randint(0, 255) for _ in range(180)]))
        payload = tls_header + leak_data
        
        pkt = IP(src=src_ip, dst=dst_ip) / \
              TCP(sport=sport, dport=dport, seq=seq_num, ack=ack_num, flags="PA") / \
              Raw(load=payload)
              
        pkt.time = timestamp
        packets.append(pkt)
        
        timestamp += 0.005 # Micro-rafagas agresivas a baja escala temporal (5ms)
        seq_num += len(payload)

    output_path = "datasets/synthetic_mixed_leak_llm.pcap"
    wrpcap(output_path, packets)
    print(f"[✓] Dataset C successfully saved to: {output_path}")

if __name__ == "__main__":
    generate_mixed_pcap()