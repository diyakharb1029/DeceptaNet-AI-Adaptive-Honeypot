# config.py
"""
Global configuration for DeceptaNet deployment.

MODE:
    "LOCAL"      -> Local Self-Defense Mode (your own system / lab env)
    "ENTERPRISE" -> Enterprise Decoy Mode (simulated Flipkart-like infra)

NOTE: Both modes are still local & safe; ENTERPRISE is a simulation for demo.
"""

MODE = "LOCAL"  # change to "ENTERPRISE" for enterprise demo mode

# Only used when MODE == "ENTERPRISE"
ENTERPRISE_NAME = "E-Commerce (Flipkart-like) Simulation"
