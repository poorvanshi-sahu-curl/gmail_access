import subprocess
import sys
import time
import signal

processes = []

def shutdown(sig=None, frame=None):
    print("\n🛑 Shutting down all services...")
    for p in processes:
        p.terminate()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)

def run_background(cmd):
    p = subprocess.Popen(cmd)
    processes.append(p)
    return p

def run_foreground(cmd):
    subprocess.run(cmd, check=True)

print("🚀 Starting Gemma Gmail App...\n")

# Step 1 — Install dependencies
print("📦 Installing dependencies...")
subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)

# Step 2 — Pull Gemma model
print("\n🤖 Pulling Gemma 3 4B model...")
subprocess.run(["ollama", "pull", "gemma3:4b"], check=True)

# Step 3 — Start Ollama in background
print("\n⚙️  Starting Ollama server...")
run_background(["ollama", "serve"])
time.sleep(3)
print("   ✅ Ollama running")

# Step 4 — Start FastAPI backend in background
print("\n🔧 Starting FastAPI backend on port 8000...")
run_background(["uvicorn", "backend.main:app", "--reload", "--port", "8000"])
time.sleep(6)
print("   ✅ Backend running at http://localhost:8000")

# Step 5 — Start Streamlit frontend
print("\n🌐 Starting Streamlit frontend...")
print("   ✅ App will open at http://localhost:8501")
print("\n   Press Ctrl+C to stop everything\n")
run_foreground(["streamlit", "run", "frontend/app.py"])

# shutdown()