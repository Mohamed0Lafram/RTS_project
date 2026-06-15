# RTS_project – Sécurisation des Communications ROS2

**Team Secure Swarm**  
Université Ibn Tofail – Kénitra | Master IA & IoT | 2025-2026  
Module : Systèmes en Temps Réel | Encadrante : Mme Khaoula Boukir

---

## Vue d'ensemble

Ce projet implémente une architecture de communication sécurisée sous ROS2 combinant :

| Couche | Mécanisme | Fichier |
|--------|-----------|---------|
| Confidentialité | AES-256-GCM | `encrypt.py` |
| Authentification | HMAC-SHA256 | `authentication.py` |
| Intégrité | RSA-2048-PSS | `integrity.py` |
| Gestion des clés | AES par topic + RSA pair | `generate_key.py` |
| Détection d'intrusion | IDS (flooding, spoofing…) | `ids_node.py` |

--- 

## Structure

```
RTS_project/
├── src/
│   ├── my_robot_controller/     # Nœuds publisher/subscriber + attaquant
│   └── secure_connection/       # Primitives cryptographiques + IDS
├── build/   (généré par colcon)
├── install/ (généré par colcon)
└── log/     (généré par colcon)
```

---

## Démarrage rapide

1. Prérequis

bashsudo apt install python3-cryptography

2. Générer les clés

bashcd RTS_project
source /opt/ros/jazzy/setup.bash
colcon build
source install/setup.bash
ros2 run secure_connection generate_key

3. Lancer les nœuds sécurisés

Terminal 1 – IDS

bashros2 run secure_connection ids_node \
  --ros-args -p hmac_secret:=my_secret \
             -p aes_key_hex:=<hex_from_topic_keys.json> \
             -p public_key_path:=src/secure_connection/secure_connection/certificates/public.pem

Terminal 2 – Talker sécurisé

bashros2 run my_robot_controller talker_secure \
  --ros-args -p aes_key_hex:=<hex_from_topic_keys.json> \
             -p hmac_secret:=my_secret \
             -p private_key_path:=src/secure_connection/secure_connection/certificates/private.pem

Terminal 3 – Listener sécurisé

bashros2 run my_robot_controller listener_secure \
  --ros-args -p aes_key_hex:=<hex_from_topic_keys.json> \
             -p hmac_secret:=my_secret \
             -p public_key_path:=src/secure_connection/secure_connection/certificates/public.pem

4. Tester les primitives (sans ROS 2)

bashpython3 src/secure_connection/secure_connection/test.py

5. Simuler une attaque

bash# Mode normal
ros2 run my_robot_controller attacker_node

# Mode flood
ros2 run my_robot_controller attacker_node --ros-args -p flood_mode:=true


## Membres de l'équipe

- Amina El Mansouri  
- Hajar Ait-ouarab  
- Hamza Kenzi  
- Cherkaoui Meryem  
- Mohamed Lafram  
