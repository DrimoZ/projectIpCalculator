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
        self.netMask: str = Reseau.defineMask(self, netMask)
        self.netAddress: str = Reseau.defineAddress(self, netAddress)
        self.netBroadcast: str = Reseau.defineBroadcast(self)
        
        self.maxNetHosts: int = 0
        self.subnets = Reseau.defineSubnets(self, wantedSubnets, wantedHosts, isSubnetFromHosts)


        self.str()


    
    def str(self) -> None:
        print(self.subnets is None)
        print(
            "Reseau : \n\tIp : " + self.ip 
               + "\n\tMasque : " +  self.netMask 
               + "\n\tRéseau : " +  self.netAddress 
               + "\n\tBroadcast : " +  self.netBroadcast
               + "\n\tHotes max : " +  str(self.maxNetHosts)
               + "\n\tSR voulus : " +  self.subnets
            #    + "\n\tHotes voulus par SR : " +  str(self.wantedHosts)
            #    + "\n\tDefinition des SR par le nombre d'hotes : " +  str(self.isSubnetFromHosts)
              
              )

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
            octets = ip.strip().lower().split('.')
            if(int(octets[0])==127 or int(octets[0])==0):
                return False
            return True
        except ValueError:
            return False

    @staticmethod
    def defineMask(self, mask: str) -> str:
        octetsIp = self.ip.strip().lower().split('.')

        # Si le masque n'est pas donné, on le défini en fonction de l'ip
        if(mask==""):
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
            print(1)
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
                        if not (val_octet in [0, 128, 192, 224, 240, 248, 252, 254, 255])  :
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
            net = ipaddress.IPv4Network(self.ip + '/' + self.netMask, False)
            return f'{net.broadcast_address:s}'
        else:
            return DEFAULT_NET_IP
        
    @staticmethod
    def defineSubnets(self, nbHosts, nbSubnets, fromHosts):
        if (self.netAddress != DEFAULT_NET_IP and self.netAddress != "-1" and self.netMask != DEFAULT_NET_IP):
            net = ipaddress.IPv4Network(self.netAddress + '/' + self.netMask, False)
            self.maxNetHosts = net.num_addresses - 2

            minHostPerSubnet = 2

            while (True):
                if (nbHosts + 2 <= minHostPerSubnet):
                    break
                else :
                    minHostPerSubnet *= 2


            #Check if we can generate subnets with the given number of hosts and subnets
            if (self.maxNetHosts > minHostPerSubnet * nbSubnets):
                # Ici gen les subnets avec le nombre d'hotes et de sr 
                pass

            else:
                #ici mettre en fonction de fromHosts (boolean) une gen en fonction du nb de subnet ou de hossts
                pass
        else:
            return []

