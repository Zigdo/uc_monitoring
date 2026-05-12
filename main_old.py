from dotenv import load_dotenv
from core.scheduler import run_scheduler

#Load env file to memory 
load_dotenv()

if __name__ == "__main__":
    run_scheduler()