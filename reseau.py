from constants import DEFAULT_NET_IP
import ipaddress


# Classe Reseau - OOP
class Reseau():
    """
    Reprend toutes les informations et méthodes de verification/recherche/etc de réseau ou ip. 
    - Adresse Ip
    - Masque du Réseau
    - Adresse du Réseau
    - Adresse de Broadcast
    - Adresse du Sous Réseau
    """

    def __init__(self, ip: str, netMask: str, netAddress: str = DEFAULT_NET_IP, isSubnetFromHosts: bool = False, wantedSubnets: int = 0, wantedHosts: int = 0) -> None:
        self.ip: str = Reseau.defineIp(self, ip)
        self.netMask: str = Reseau.defineMask(self, netMask, netAddress)
        self.netAddress: str = Reseau.defineAddress(self, netAddress)
        self.netBroadcast: str = Reseau.defineBroadcast(self)

        self.canCreateFromSubnets: bool = False
        self.canCreateFromHosts: bool = False

        self.createdSubnet: int = -1
        self.maxNetHosts: int = 0
        self.subnets = Reseau.defineSubnets(self, wantedSubnets, wantedHosts, isSubnetFromHosts)


        self.str(wantedSubnets,wantedHosts,isSubnetFromHosts)
        

        # Tous les deux faisables: retourner une liste de sous-réseau
        # Aucun faisable: retourner une liste vide + canCreateFromHosts & canCreateFromSubnets a False
        # Un seul faisable: retourner une liste vide + canCreateFromHosts ou canCreateFromSubnets a True
        # fonction defineSubnets() 1 arg en plus initialisé a 0 par defaut 
        #   => 0 -> gen que si les 2 sont faisables + modif params
        #   => 1 -> gen que en fonction du nombre de sous-réseau
        #   => 2 -> gen que en fonction du nombre d'hôtes




        #  POUR LA VALEUR DU RETURN SAVOIR QUEL COMMANDE UTILISER POUR AFFICHAGE

            
        # Dans une boucle for listant les subnet, tu peux retrouver les ip/masque pour l'affichage
        # for i, sub in enumerate(self.subnets):

            # Pour obtenir l'ip (exemple : 192.168.33.0) -> sub.network_address
            # Pour obtenir le / après (exemple /26) -> sub.prefixlen

    
    def str(self,wantedSubnets,wantedHosts,isSubnetFromHosts) -> None:
        print(
            "Reseau : \n\tIp : " + self.ip 
               + "\n\tMasque : " +  self.netMask 
               + "\n\tRéseau : " +  self.netAddress 
               + "\n\tBroadcast : " +  self.netBroadcast
               + "\n\tHotes max : " +  str(self.maxNetHosts)
               + "\n\tSR voulus : " +  str(wantedSubnets)
               + "\n\tHotes voulus par SR : " +  str(wantedHosts)
               + "\n\tDefinition des SR par le nombre d'hotes : " +  str(isSubnetFromHosts)
               + "\n\tType de découpe : " +  str(self.createdSubnet)
              )
        if(self.netAddress!="-1"):
            for i, sub in enumerate(self.subnets):
                print(f"Sous-réseau {i+1} : | Adresse : {sub.network_address}/{sub.prefixlen} | 1erIP : {sub.network_address+1} | \
                    DernIP : {sub.network_address+self.maxNetHosts} | Broadcast : {sub.network_address+self.maxNetHosts+1}")



    @staticmethod
    def defineIp(self, ip: str) -> str:
        if (Reseau.isValidIp(ip)):
            return ip
        else:
            return DEFAULT_NET_IP

    @staticmethod
    def isValidIp(ip: str) -> bool:
        try:
            ip_object = ipaddress.ip_address(ip) 
            ipV4 = ipaddress.IPv4Address(ip)
            return not (ipV4.is_reserved or ipV4.is_link_local or ipV4.is_multicast or ipV4.is_unspecified or ipV4.is_loopback)
            # octets = ip.strip().lower().split('.')
            # if(int(octets[0])==127 or int(octets[0])==0):
                # return False
            # return True
        except ValueError:
            return False

    @staticmethod
    def defineMask(self, mask: str, netAdress: str) -> str:
        # Si le masque n'est pas donné, on le défini en fonction de l'ip
        octetsIp = self.ip.strip().lower().split('.')
        if (self.ip == DEFAULT_NET_IP):
            if not hasattr(self, 'netAddress'):
                self.netAddress = Reseau.defineAddress(self, netAdress)
                octetsIp = self.netAddress.strip().lower().split('.')

        if(mask==""):
            if(len(octetsIp)!=4):
                return DEFAULT_NET_IP
            
            if(int(octetsIp[0])<127):
                    return "255.0.0.0"
            elif(int(octetsIp[0])<192):
                return "255.255.0.0"
            else:
                return "255.255.255.0"
        else:
            # Si le masque est valide, on verifie qu'il est compatible avec l'ip
            if (Reseau.isValidMask(mask)):
                octetsMasque = mask.strip().lower().split('.')

                if(int(octetsIp[0])<127 and int(octetsMasque[0])==255):
                    return mask
                elif(int(octetsIp[0])<192 and int(octetsMasque[1])==255):
                    return mask
                elif(int(octetsMasque[2])==255):
                    return mask
                else:
                    return DEFAULT_NET_IP
            else:
                return DEFAULT_NET_IP

    @staticmethod
    def isValidMask(mask: str) -> bool:
        octets = mask.strip().lower().split('.')

        # Vérification du nombre d'octets
        if len(octets) != 4:
            return False
        
        # Initialisation d'un booleen pour verifier si on a des 1 contigus // Définition de l'octet précédent
        est_contigu = True

        for octet in octets:
            try:
                val_octet = int(octet)

                # Si l'octet n'est pas compris entre 0 et 255, retourner False
                if val_octet < 0 or val_octet > 255:
                    return False

                # vérifier que l'octet est contigu
                if est_contigu:
                    if val_octet != 255:
                        # Si l'octet qui n'est pas a 255 n'est pas un des octets contigus, retourner False
                        if not (val_octet in [0, 128, 192, 224, 240, 248, 252, 254])  :
                            return False
                        
                        est_contigu = False
                else:
                    # Si n'est pas contigu et l'octet n'est pas 0, retourner False
                    if val_octet != 0:
                        return False
            
            # Si un octet n'est pas un entier, retourner False
            except ValueError:
                return False
            
        # Si le masque fini par des 1, retourner False
        if est_contigu:
            return False
                   
        return True

    @staticmethod
    def defineAddress(self, netAddress: str) -> str:
        if (self.ip == DEFAULT_NET_IP):
            if (Reseau.isValidAddress(netAddress)):
                return netAddress
            else:
                return DEFAULT_NET_IP
        else:   
            net = ipaddress.IPv4Network(self.ip + '/' + self.netMask, False)

            # Si pas de réseau donné, on le défini en fonction de l'ip et du masque
            if (netAddress == DEFAULT_NET_IP):
                return f'{net.network_address:s}'
        
            # Si un réseau est donné, on vérifie qu'il est valide et qu'il correspond à l'ip et au masque
            if (Reseau.isValidAddress(netAddress)):
                if(netAddress==f'{net.network_address:s}'):
                    return netAddress
                else:
                    # Return -1 pour l'application 2
                    return "-1"
            else:
                return DEFAULT_NET_IP
    
    @staticmethod
    def isValidAddress(netAddress: str) -> bool:
        try:
            ip_object = ipaddress.ip_address(netAddress) 
            octets = netAddress.strip().lower().split('.')
            if(int(octets[0])==127 or int(octets[0])==0):
                return False
            return True
        except ValueError:
            return False

    @staticmethod
    def defineBroadcast(self) -> str:
        if (self.netAddress != DEFAULT_NET_IP and self.netAddress != "-1"):
            net = ipaddress.IPv4Network(self.netAddress + '/' + self.netMask, False)
            return f'{net.broadcast_address:s}'
        else:
            return DEFAULT_NET_IP

    @staticmethod
    def defineSubnets(self, nbSubnets, nbHosts, fromHosts, gen: int = 0) -> list[ipaddress.IPv4Network]:
        if (self.netAddress != DEFAULT_NET_IP and self.netAddress != "-1" and self.netMask != DEFAULT_NET_IP and nbHosts != 0 and nbSubnets != 0):
            
            # Renvoye un network tel que -> 192.168.33.21/24
            network = ipaddress.IPv4Network(self.netAddress + '/' + self.netMask, strict=False)
            # Calcul taille masque max -> /..
            subnet_mask_length = network.prefixlen + nbSubnets.bit_length() - 1

            # Si au dessus de 32 on se base que sur le nbr d'hôte et nn de sous-réseau
            if subnet_mask_length > 32:

                # Calcul du subnet par rapport au nbr d'hôte
                subnet = network.subnets(new_prefix=network.prefixlen)
                subnets_list = list(subnet)
                self.maxNetHosts = subnets_list[0].num_addresses-2

                # Impossible de mettre le nbr d'hôte dans la découpe
                if self.maxNetHosts<nbHosts:
                    return list()

                # Possible de mettre le nbr d'hôte dans la découpe
                else:
                    # Découpe seulement en hote
                    subnet_mask_addition=128
                    subnet_mask=0
                    while subnet_mask_addition-2>=nbHosts:
                        subnet_mask+=1
                        subnet_mask_addition/=2

                    # Pas touche :D les info sont envoyer dans les variables voulues et return la liste
                    subnet = network.subnets(new_prefix=network.prefixlen+subnet_mask)
                    subnets_list = list(subnet)
                    self.maxNetHosts = subnets_list[0].num_addresses-2

                    self.createdSubnet = 2 # SR IMPOSSIBLE -> HOSTS
                    return subnets_list
                      
            else:

                subnet = network.subnets(new_prefix=subnet_mask_length+1)
                subnets_list = list(subnet)
                self.maxNetHosts =subnets_list[0].num_addresses-2

                if self.maxNetHosts<nbHosts:
                    # seulement en SR
                    self.createdSubnet = 1 # HOSTS IMPOSSIBLE -> SR
                    return subnets_list

                else:
                    if(fromHosts):
                        # Découpe seulement en hote
                        subnet_mask_addition=128
                        subnet_mask=1
                        while subnet_mask_addition-2>nbHosts:
                            subnet_mask+=1
                            subnet_mask_addition/=2
                        subnet_mask-=1

                        # Pas touche :D les info sont envoyer dans les variables voulues et return la liste
                        subnet = network.subnets(new_prefix=network.prefixlen+subnet_mask)
                        subnets_list = list(subnet)
                        self.maxNetHosts = subnets_list[0].num_addresses-2

                        self.createdSubnet = 2
                        return subnets_list                    
                    self.createdSubnet = 0
                    return subnets_list
        else:
            return list()


