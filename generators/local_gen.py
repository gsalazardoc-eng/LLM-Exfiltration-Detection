from scapy.all import IP, TCP, Raw, wrpcap
import random
import time

def generate_local_pcap():
    packets = []
    src_ip = "127.0.0.1"
    dst_ip = "127.0.0.1" # Local Host Loopback Interface
    
    timestamp = time.time()
    sport = 40000
    dport = 9000 # Local model port (e.g., Ollama / Local API)
    seq_num = 2000
    ack_num = 6000
    
    print("[+] Generating Dataset B: Local Inference (Variable timing, Plaintext ASCII)...")
    
    for i in range(150):
        # Carga util basada en strings estandar de ejecucion (Baja entropia controlada)
        payload_text = f"LOCAL_LLM_INFERENCE_RESPONSE_NODE_{i:04d}_TOKEN_CHUNKING_RAW_ASCII_DATA_VALIDATION"
        payload = payload_text.encode('ascii')
        
        pkt = IP(src=src_ip, dst=dst_ip) / \
              TCP(sport=sport, dport=dport, seq=seq_num, ack=ack_num, flags="PA") / \
              Raw(load=payload)
              
        pkt.time = timestamp
        packets.append(pkt)
        
        # Modelo stocastico intermitente: tiempos de espera representativos del procesamiento de hardware local
        interval = random.choice([0.02, 0.05, 0.15, 0.25, 0.45])
        timestamp += interval
        seq_num += len(payload)

    output_path = "datasets/synthetic_local_llm.pcap"
    wrpcap(output_path, packets)
    print(f"[✓] Dataset B successfully saved to: {output_path}")

if __name__ == "__main__":
    generate_local_pcap()