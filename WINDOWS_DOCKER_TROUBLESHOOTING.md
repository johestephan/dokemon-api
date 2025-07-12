# Windows Docker Troubleshooting Guide

## Common Issue: "Protocol not available" Error

If you're getting `"error": "Failed to initialize: protocol not available"` when accessing the Dokemon API on Windows, this is a Docker socket connectivity issue.

## Quick Fixes

### 1. Verify Docker Desktop Setup
```cmd
# Check if Docker Desktop is running
docker --version
docker info
```

**Requirements:**
- Docker Desktop must be running
- Use **Linux containers** (not Windows containers)
- Docker Desktop should be in "normal" mode (not experimental)

### 2. Use the Debug Endpoint
After starting the container, visit:
```
http://localhost:9090/docker-debug
```

This will show detailed diagnostics about Docker connectivity.

### 3. Try Different Container Start Methods

**Method A: Root User with Standard Socket Mount (Recommended)**
```cmd
docker run -d ^
    --name dokemon-api ^
    -p 9090:9090 ^
    -u root ^
    -v "/var/run/docker.sock:/var/run/docker.sock" ^
    -v dokemon_data:/app/data ^
    javastraat/dokemon-api:latest
```

**Method B: Privileged Mode**
```cmd
docker run -d ^
    --name dokemon-api ^
    -p 9090:9090 ^
    --privileged ^
    -v "/var/run/docker.sock:/var/run/docker.sock" ^
    -v dokemon_data:/app/data ^
    javastraat/dokemon-api:latest
```

**Method C: Docker-in-Docker (TCP)**
```cmd
docker run -d ^
    --name dokemon-api ^
    -p 9090:9090 ^
    -v dokemon_data:/app/data ^
    -e DOCKER_HOST=tcp://host.docker.internal:2375 ^
    javastraat/dokemon-api:latest
```

### 4. Enable Docker API (If needed)
If Method C above doesn't work, enable Docker daemon API:

1. Open Docker Desktop
2. Go to Settings → General
3. Check "Expose daemon on tcp://localhost:2375 without TLS"
4. Click "Apply & Restart"
5. Use Method C above

⚠️ **Security Note**: Only enable TCP API for development/testing!

### 5. Windows-Specific Docker Desktop Settings

**File Sharing:**
1. Docker Desktop → Settings → Resources → File Sharing
2. Add your project drive (usually C:)
3. Apply & Restart

**WSL 2 Backend (Recommended):**
1. Docker Desktop → Settings → General
2. Enable "Use the WSL 2 based engine"
3. Apply & Restart

### 6. Check Docker Desktop Logs
If issues persist:
1. Docker Desktop → Troubleshoot → Show Logs
2. Look for socket or daemon errors

## Testing Your Fix

After applying any fix:

1. **Test Docker Access:**
   ```cmd
   docker ps
   docker images
   ```

2. **Test API Health:**
   ```cmd
   curl http://localhost:9090/health
   ```

3. **Test API Docker Debug:**
   ```cmd
   curl http://localhost:9090/docker-debug
   ```

4. **Test Container Management:**
   ```cmd
   curl http://localhost:9090/api/v1/containers
   ```

## Alternative: Run on Host Instead of Container

If container-based Docker access continues to fail, you can run Dokemon API directly on Windows:

```cmd
# Setup
setup_windows.bat

# Activate environment
venv\Scripts\activate.bat

# Run directly on Windows
python app.py
```

This bypasses Docker socket mounting issues entirely.

## Still Having Issues?

1. **Check Windows Version**: Ensure you're on Windows 10/11 with latest updates
2. **Restart Everything**: Restart Docker Desktop, then restart your computer
3. **Clean Install**: Uninstall/reinstall Docker Desktop
4. **Use WSL**: Install Dokemon API in WSL 2 environment instead
5. **Use VM**: Run in a Linux VM if Windows compatibility issues persist

## Support Information

When reporting issues, include:
- Windows version (`winver`)
- Docker Desktop version
- Output from `docker-debug` endpoint
- Container logs (`docker logs dokemon-api`)
- Docker Desktop logs (from Troubleshoot menu)
