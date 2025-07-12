# Docker API Server - Windows Installation Guide

## Quick Start

1. **Download the files** to a folder (e.g., `C:\Users\einstein\Software\docker-api\`)

2. **Install Python** (if not already installed):
   - Download from https://python.org
   - Make sure to check "Add Python to PATH" during installation

3. **Install Docker Desktop** (if not already installed):
   - Download from https://docker.com/products/docker-desktop

4. **Run the setup script**:
   - Open Command Prompt or PowerShell
   - Navigate to the docker-api folder
   - Run: `setup_windows.bat`

5. **Start the server**:
   - Run: `start_windows.bat`
   - Or manually: 
     ```cmd
     venv\Scripts\activate.bat
     python app.py
     ```

6. **Test the API**:
   - Open browser: http://localhost:9090
   - Or test with curl: `curl http://localhost:9090/health`

## Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
- Run `setup_windows.bat` to install Flask
- Make sure you're using the virtual environment: `venv\Scripts\activate.bat`

### "Docker is not accessible"
- Make sure Docker Desktop is running
- Check if Docker works: `docker --version`

### "Python is not recognized"
- Install Python from python.org
- Make sure "Add Python to PATH" was checked during installation
- Restart Command Prompt after installation

## API Endpoints

Once running, the API will be available at http://localhost:9090

- Health check: `GET /health`
- List containers: `GET /api/v1/containers`
- Start container: `POST /api/v1/containers/{id}/start`
- Stop container: `POST /api/v1/containers/{id}/stop`
- And many more... (see full documentation at http://localhost:9090)

## Example Usage

```cmd
# Check if API is running
curl http://localhost:9090/health

# List all containers
curl http://localhost:9090/api/v1/containers

# Run a new container
curl -X POST http://localhost:9090/api/v1/containers/run ^
  -H "Content-Type: application/json" ^
  -d "{\"image\": \"nginx\", \"name\": \"my-nginx\", \"ports\": [\"8080:80\"]}"
```
