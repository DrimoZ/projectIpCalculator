
import ipaddress

# Saisie de l'adresse IP et du masque de sous-réseau au format CIDR (par exemple, 192.168.1.0/24)
ip_cidr = input("Entrez l'adresse IP et le masque CIDR (ex: 192.168.1.0/24) : ")

# Convertir l'entrée en objet IPNetwork
network = ipaddress.ip_network(ip_cidr, strict=False)
print(network)

# Demander le nombre de sous-réseaux souhaité
num_subnets = int(input("Entrez le nombre de sous-réseaux souhaité : "))

# Calculer le masque de sous-réseau approprié pour le nombre de sous-réseaux
subnet_mask_length = network.prefixlen + num_subnets.bit_length() - 1
print(network.prefixlen)
print(subnet_mask_length)

if subnet_mask_length > 32:
    print("Nombre de sous-réseaux souhaité trop élevé pour l'adresse IP donnée.")
else:
    subnet = network.subnets(new_prefix=subnet_mask_length)
    subnets_list = list(subnet)
    
    # Afficher les informations sur les sous-réseaux créés
    print(f"Adresse IP d'origine : {network.network_address}/{network.prefixlen}")
    print(f"Masque de sous-réseau pour {num_subnets} sous-réseaux : /{subnet_mask_length}")

    for i, sub in enumerate(subnets_list):
        print(f"Sous-réseau {i+1} : {sub.network_address}/{subnet_mask_length}")