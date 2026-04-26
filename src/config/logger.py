import datetime
import sys

COLORS = {
    "RESET": "\033[0m",
    "INFO": "\033[96m",     # Cyan
    "SUCCESS": "\033[92m",  # Green
    "WARNING": "\033[93m",  # Yellow
    "ERROR": "\033[91m",    # Red
    "DEBUG": "\033[90m",    # Gray
    "TIME": "\033[37m"      # White
}

def log(level: str, message: str, **kwargs):
    level_upper = level.upper()
    color = COLORS.get(level_upper, COLORS["RESET"])
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    info_str = " ".join([f"{k}={v}" for k, v in kwargs.items()])
    if info_str:
        info_str = f" | {info_str}"
        
    type_formatted = f"[{level_upper}]"
    time_formatted = f"{COLORS['TIME']}[{timestamp}]{COLORS['RESET']}"
    
    output = f"{time_formatted} {color}{type_formatted.ljust(9)}{COLORS['RESET']} {message}{color}{info_str}{COLORS['RESET']}"
    print(output)
    
    sys.stdout.flush()

def info(message: str, **kwargs):
    log("INFO", message, **kwargs)

def success(message: str, **kwargs):
    log("SUCCESS", message, **kwargs)

def warning(message: str, **kwargs):
    log("WARNING", message, **kwargs)

def error(message: str, **kwargs):
    log("ERROR", message, **kwargs)

def debug(message: str, **kwargs):
    log("DEBUG", message, **kwargs)
