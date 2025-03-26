# Mikrotik-MASS (Advanced Setup Script)

## 🇬🇷 Ελληνικά

### Περιγραφή
Το **Mikrotik-MASS (Advanced Setup Script)** είναι ένα προηγμένο Python script που αυτοματοποιεί τη διαδικασία αρχικής παραμετροποίησης ενός router Mikrotik. Μέσω διαδραστικών ερωτήσεων προς το χρήστη, το script εκτελεί αυτόματα βασικές ρυθμίσεις όπως:

- Ρύθμιση του ονόματος (Identity) του router.
- Επιλογή και ρύθμιση interface για DHCP client.
- Δημιουργία Bridge και προσθήκη των επιλεγμένων interfaces.
- Ρύθμιση IP address στο Bridge.
- Ρύθμιση DHCP Server (με δυναμικές προεπιλεγμένες τιμές).
- Δημιουργία κανόνων NAT masquerade στο firewall.
- Ενεργοποίηση Mikrotik Cloud (DDNS).

### BETA
-  1. Δυνατότητα για Πολλαπλά Bridges
      Ο χρήστης μπορεί να δημιουργήσει περισσότερα από ένα bridges με interfaces.
      Κάθε bridge έχει τη δική του IP και interface list.
- 2. Δημιουργία Interface List “WAN” και “PCC”
      Αν ο χρήστης δημιουργήσει DHCP-client ή βάλει χειροκίνητα IP στο WAN, το script:
      Δημιουργεί την interface list WAN.
      Προσθέτει το αντίστοιχο interface σε αυτή.
      Δημιουργεί και την interface list PCC για μελλοντική χρήση.
      Επίσης, δημιουργείται αυτόματα κανόνας NAT με out-interface-list=WAN.
- 3. DHCP Server Setup με Custom Ρυθμίσεις
      DNS (προαιρετικά, μπορεί να μείνει και κενό)
      Αν ο χρήστης θέλει, ορίζεται και DNS server στο router (/ip dns set).
- 4. Επιλογή για Ρύθμιση Firewall
      Ρωτάει τον χρήστη αν θέλει να ρυθμίσει το firewall:
      Αν ναι:
      Εμφανίζει τα ενεργά services (/ip service print)
      Του επιτρέπει να απενεργοποιήσει όσα θέλει
      Αν αφήσει ανοιχτό το SSH, μπορεί να ενεργοποιηθεί προστασία SSH
      Αν κάποιος κάνει πάνω από 5 λάθος login → blacklist για 24 ώρες

### Προαπαιτούμενα
- Python 3.x
- Πακέτο `paramiko` (εγκαθίσταται αυτόματα από το script αν δεν υπάρχει)

### Χρήση
Απλώς τρέξτε το script και ακολουθήστε τις οδηγίες που εμφανίζονται στο τερματικό:

```bash
python mikrotik_mass.py
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
The **Mikrotik-MASS (Advanced Setup Script)** is an advanced Python script that automates the initial setup process for a Mikrotik router. Through interactive prompts, the script automatically performs essential configuration tasks, including:

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

### BETA
- 1. Multiple Bridges Ability
      The user can create more than one bridge with interfaces.
     Each bridge has its own IP and interface list.
- 2. Create Interface List “WAN” and “PCC”
      If the user creates a DHCP-client or manually sets IP on the WAN, the script:
      Creates the WAN interface list.
      Adds the corresponding interface to it.
      Creates the PCC interface list for future use.
      Also, a NAT rule is automatically created with out-interface-list=WAN.
- 3. DHCP Server Setup with Custom Settings
      DNS (optional, can be left blank)
      If the user wants, a DNS server is also defined on the router (/ip dns set).
- 4. Firewall Configuration Option
      Asks the user if they want to configure the firewall:
      If so:
      Displays the active services (/ip service print)
      Allows them to disable whatever they want
      If they leave SSH open, SSH protection can be enabled
      If someone makes more than 5 incorrect logins → blacklist for 24 hours

### Usage
Simply run the script and follow the prompts displayed in the terminal:

```bash
python mikrotik_mass.py
```

### Future Additions
- WAN aggregation using PCC with automatic creation of mangle rules based on the number of WAN connections.
- Automatic Wireguard server and client setup with automatic generation of configuration files.
- Automatic Site-to-Site VPN setup using Wireguard or IP Tunnel.
- Port Forwarding.
- Mikrotik security hardening.

