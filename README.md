# DeceptaNet – AI-Driven Adaptive Honeypot Framework

DeceptaNet is a next-generation cybersecurity deception framework that leverages Artificial Intelligence (AI), Machine Learning (ML), and Reinforcement Learning (RL) to dynamically deceive cyber attackers, analyze their behavior, and generate actionable threat intelligence in real time.

Unlike traditional static honeypots, DeceptaNet continuously adapts its responses based on attacker actions, escalates interaction intelligently, and maps attacker techniques to the MITRE ATT&CK framework.

This project was developed as a Major Academic Project in Cyber Security & Forensics.



## Key Features

- AI-driven adaptive honeypot architecture  
- Dynamic escalation from low-interaction to high-interaction honeypots  
- Reinforcement Learning–based deception strategy selection  
- Real-time attacker behavior profiling and anomaly detection  
- Automated log collection and threat intelligence generation  
- MITRE ATT&CK mapping and IOC extraction  
- Secure, isolated environment using virtualization  



## System Architecture

The system consists of an AI core that monitors attacker behavior, decides deception strategies, and dynamically modifies the honeypot environment to maximize intelligence gathering while remaining undetected.



## Technology Stack

**Programming Languages**
- Python

**AI / Machine Learning**
- Scikit-learn  
- TensorFlow / PyTorch  

**Honeypot Technologies**
- Cowrie (SSH)
- Honeyd
- Dionaea
- Custom honeypot scripts

**Virtualization & Isolation**
- Docker
- Virtual Machines

**Logging & Monitoring**
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Wireshark

**Threat Intelligence**
- MITRE ATT&CK
- MISP



## How It Works

1. Suspicious network traffic is redirected to the honeypot environment  
2. Incoming actions are monitored and logged  
3. AI models classify behavior as normal or malicious  
4. Reinforcement Learning selects optimal deception strategies  
5. Honeypot behavior adapts dynamically (fake files, ports, services)  
6. Attacker actions are logged and mapped to known attack techniques  
7. Actionable threat intelligence is generated for security analysis  



## System Demonstration

### Enterprise-Grade SOC Dashboard
Real-time visualization of attack detection, AI classification, deception responses, and system health.

![SOC Dashboard](screenshots/01_dashboard.png)

---

### MITRE ATT&CK Mapping
Observed attacker behaviors are mapped to MITRE ATT&CK tactics to generate structured and actionable threat intelligence.

![MITRE ATT&CK Heatmap](screenshots/02_mitre_attack.png)

---

### Reinforcement Learning for Adaptive Deception
The Reinforcement Learning agent dynamically learns optimal deception strategies using Q-learning by assigning higher Q-values to effective responses.

![Reinforcement Learning](screenshots/03_rl-learning.png)

---

### Real Attack Simulation
Live attacker commands executed against the honeypot with corresponding adaptive deception and security responses.

![Real Attack Simulation](screenshots/04_real-attack-simulation.png)

Additional analytics, live logs, and deployment modes are available in the `screenshots/` directory.



## Objectives

- Design and develop an AI-driven adaptive honeypot framework  
- Improve realism and engagement of deception systems  
- Collect and analyze attacker behavior automatically  
- Generate actionable cybersecurity intelligence  
- Enhance detection of unknown and zero-day attacks  



## Future Scope

- Integration of deep reinforcement learning models  
- Cloud and IoT honeypot deployment  
- Automatic attack prevention and isolation  
- Advanced visualization and analytics dashboard  
- Continuous learning without manual retraining  
- Threat intelligence sharing across platforms  



## Contributors

Made By Diya Kharb  



## License

This project is licensed under the MIT License.
