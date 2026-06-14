from logging import FileHandler, StreamHandler, INFO, ERROR, Formatter, basicConfig, error as log_error, info as log_info
from os import path as ospath, environ
from subprocess import run as srun, PIPE
from dotenv import load_dotenv
from datetime import datetime
import pytz

# Define IST timezone
IST = pytz.timezone("Asia/Kolkata")

class ISTFormatter(Formatter):
    """Custom formatter to use IST timezone."""
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, IST)
        return dt.strftime(datefmt or "%d-%b-%y %I:%M:%S %p")

# Clear log file if it exists
log_file = "log.txt"
if ospath.exists(log_file):
    with open(log_file, "w") as f:
        f.truncate(0)

# Create handlers
file_handler = FileHandler(log_file)
stream_handler = StreamHandler()

# Create custom formatter with IST timezone
formatter = ISTFormatter("[%(asctime)s] [%(levelname)s] - %(message)s", "%d-%b-%y %I:%M:%S %p")
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Configure logging
basicConfig(handlers=[file_handler, stream_handler], level=INFO)

# Load environment variables
load_dotenv("config.env")
UPSTREAM_REPO = environ.get("UPSTREAM_REPO", "").strip() or None
UPSTREAM_BRANCH = environ.get("UPSTREAM_BRANCH", "").strip() or "main"

if UPSTREAM_REPO:
    # 1. Clean start
    if ospath.exists(".git"):
        srun(["rm", "-rf", ".git"])
        log_info("Removed existing .git directory.")

    srun(["git", "init", "-q"])
    
    # 2. Disable interactive prompts globally for this process
    env = environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"

    # 3. Use a credential helper to "save" the token immediately
    # This prevents Git from ever asking for a password
    srun(["git", "config", "credential.helper", "store"])
    
    # 4. Set identity
    srun(["git", "config", "user.email", "doc.adhikari@gmail.com"])
    srun(["git", "config", "user.name", "weebzone"])

    # 5. Add remote and Fetch
    srun(["git", "remote", "add", "origin", UPSTREAM_REPO])
    
    # Fetching with the custom environment to block prompts
    fetch = srun(["git", "fetch", "origin", UPSTREAM_BRANCH, "-q"], env=env)
    
#    if fetch.returncode == 0:
#        srun(["git", "reset", "--hard", f"origin/{UPSTREAM_BRANCH}", "-q"])
#        log_info("Successfully updated!!")
#    else:
        # log_error("Fetch failed. Your token might be expired or missing 'repo' permissions.")
        # log_error("Verify your token at: https://github.com")