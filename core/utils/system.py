import psutil

def get_system_status():
    cpu_usage = psutil.cpu_percent(interval=0.2)
    ram_usage = psutil.virtual_memory().percent
    return cpu_usage, ram_usage