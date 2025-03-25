# Mikrotik-ASS (Advance Setup Script)

## 🇬🇷 Ελληνικά

### Περιγραφή
Το **Mikrotik-ASS (Advance Setup Script)** είναι ένα προηγμένο Python script που αυτοματοποιεί τη διαδικασία αρχικής παραμετροποίησης ενός router Mikrotik. Μέσω διαδραστικών ερωτήσεων προς το χρήστη, το script εκτελεί αυτόματα βασικές ρυθμίσεις όπως:

- Ρύθμιση του ονόματος (Identity) του router.
- Επιλογή και ρύθμιση interface για DHCP client.
- Δημιουργία Bridge και προσθήκη των επιλεγμένων interfaces.
- Ρύθμιση IP address στο Bridge.
- Ρύθμιση DHCP Server (με δυναμικές προεπιλεγμένες τιμές).
- Δημιουργία κανόνων NAT masquerade στο firewall.
- Ενεργοποίηση Mikrotik Cloud (DDNS).

### Προαπαιτούμενα
- Python 3.x
- Πακέτο `paramiko` (εγκαθίσταται αυτόματα από το script αν δεν υπάρχει)

### Χρήση
Απλώς τρέξτε το script και ακολουθήστε τις οδηγίες που εμφανίζονται στο τερματικό:

```bash
python mikrotik_ass.py
```

### Μελλοντικές Προσθήκες
- Ενοποίηση γραμμών με PCC και αυτόματη δημιουργία κανόνων mangle βάσει του αριθμού των WAN.
- Αυτόματη δημιουργία Wireguard server και client με αυτόματο generation του αρχείου config.
- Αυτόματο Site-to-Site VPN με Wireguard ή IP Tunnel.
- Port Forwarding.
- Θωράκιση ασφαλείας Mikrotik.

---

## 🇬🇧 English

### Description
The **Mikrotik-ASS (Advance Setup Script)** is an advanced Python script that automates the initial setup process for a Mikrotik router. Through interactive prompts, the script automatically performs essential configuration tasks, including:

- Setting the router identity.
- Selecting and configuring an interface for DHCP client.
- Creating a Bridge and adding selected interfaces to it.
- Assigning an IP address to the Bridge.
- Configuring a DHCP Server (with dynamic default values).
- Creating NAT masquerade rules in the firewall.
- Enabling Mikrotik Cloud (DDNS).

### Prerequisites
- Python 3.x
- `paramiko` package (installed automatically by the script if not present)

### Usage
Simply run the script and follow the prompts displayed in the terminal:

```bash
python mikrotik_ass.py
```

### Future Additions
- WAN aggregation using PCC with automatic creation of mangle rules based on the number of WAN connections.
- Automatic Wireguard server and client setup with automatic generation of configuration files.
- Automatic Site-to-Site VPN setup using Wireguard or IP Tunnel.
- Port Forwarding.
- Mikrotik security hardening.
