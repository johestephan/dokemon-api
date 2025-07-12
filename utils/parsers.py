#!/usr/bin/env python3

def parse_container_list(output):
    """Parse docker ps output into structured data"""
    if not output:
        return []
    
    lines = output.split('\n')
    if len(lines) < 2:
        return []
    
    # Get header line to understand column positions
    header = lines[0]
    if not header:
        return []
    
    # Find column positions based on header
    container_id_pos = header.find('CONTAINER ID')
    image_pos = header.find('IMAGE')
    command_pos = header.find('COMMAND')
    created_pos = header.find('CREATED')
    status_pos = header.find('STATUS')
    ports_pos = header.find('PORTS')
    names_pos = header.find('NAMES')
    
    containers = []
    for line in lines[1:]:  # Skip header
        if line.strip():
            # Extract fields based on column positions
            container = {}
            
            # Container ID
            if image_pos > container_id_pos:
                container["container_id"] = line[container_id_pos:image_pos].strip()
            else:
                container["container_id"] = line[:12].strip()  # fallback to first 12 chars
            
            # Image
            if command_pos > image_pos:
                container["image"] = line[image_pos:command_pos].strip()
            else:
                # Fallback: try to extract image name
                parts = line.split()
                container["image"] = parts[1] if len(parts) > 1 else ""
            
            # Command
            if created_pos > command_pos:
                container["command"] = line[command_pos:created_pos].strip()
            else:
                parts = line.split()
                container["command"] = parts[2] if len(parts) > 2 else ""
            
            # Created
            if status_pos > created_pos:
                container["created"] = line[created_pos:status_pos].strip()
            else:
                parts = line.split()
                container["created"] = parts[3] if len(parts) > 3 else ""
            
            # Status
            if ports_pos > status_pos:
                container["status"] = line[status_pos:ports_pos].strip()
            else:
                # Try to find status in the line
                parts = line.split()
                for i, part in enumerate(parts):
                    if 'Up' in part or 'Exited' in part or 'Created' in part:
                        # Get status including time info
                        status_parts = []
                        for j in range(i, min(i+4, len(parts))):
                            if parts[j].startswith('0.0.0.0') or '->' in parts[j]:
                                break
                            status_parts.append(parts[j])
                        container["status"] = ' '.join(status_parts)
                        break
                else:
                    container["status"] = ""
            
            # Ports
            if names_pos > ports_pos:
                container["ports"] = line[ports_pos:names_pos].strip()
            else:
                # Extract ports by looking for port mapping patterns
                parts = line.split()
                port_parts = []
                for part in parts:
                    if '->' in part or ':' in part and ('tcp' in part or 'udp' in part):
                        port_parts.append(part)
                container["ports"] = ', '.join(port_parts)
            
            # Names (last column)
            if names_pos >= 0:
                container["names"] = line[names_pos:].strip()
            else:
                # Fallback: use last part
                parts = line.split()
                container["names"] = parts[-1] if parts else ""
            
            containers.append(container)
    
    return containers

def parse_image_list(output):
    """Parse docker images output into structured data"""
    if not output:
        return []
    
    lines = output.split('\n')
    if len(lines) < 2:
        return []
    
    # Get header line to understand column positions
    header = lines[0]
    if not header:
        return []
    
    # Find column positions based on header
    repository_pos = header.find('REPOSITORY')
    tag_pos = header.find('TAG')
    image_id_pos = header.find('IMAGE ID')
    created_pos = header.find('CREATED')
    size_pos = header.find('SIZE')
    
    images = []
    for line in lines[1:]:  # Skip header
        if line.strip():
            # Extract fields based on column positions
            image = {}
            
            # Repository
            if tag_pos > repository_pos:
                image["repository"] = line[repository_pos:tag_pos].strip()
            else:
                parts = line.split()
                image["repository"] = parts[0] if len(parts) > 0 else ""
            
            # Tag
            if image_id_pos > tag_pos:
                image["tag"] = line[tag_pos:image_id_pos].strip()
            else:
                parts = line.split()
                image["tag"] = parts[1] if len(parts) > 1 else ""
            
            # Image ID
            if created_pos > image_id_pos:
                image["image_id"] = line[image_id_pos:created_pos].strip()
            else:
                parts = line.split()
                image["image_id"] = parts[2] if len(parts) > 2 else ""
            
            # Created
            if size_pos > created_pos:
                image["created"] = line[created_pos:size_pos].strip()
            else:
                parts = line.split()
                # Created might be multiple words, so take everything except the last part (size)
                if len(parts) >= 4:
                    image["created"] = ' '.join(parts[3:-1])
                else:
                    image["created"] = parts[3] if len(parts) > 3 else ""
            
            # Size (last column)
            if size_pos >= 0:
                image["size"] = line[size_pos:].strip()
            else:
                parts = line.split()
                image["size"] = parts[-1] if parts else ""
            
            images.append(image)
    
    return images

def parse_network_list(output):
    """Parse docker network ls output into structured data"""
    if not output:
        return []
    
    lines = output.split('\n')
    if len(lines) < 2:
        return []
    
    # Get header line to understand column positions
    header = lines[0]
    if not header:
        return []
    
    # Find column positions based on header
    network_id_pos = header.find('NETWORK ID')
    name_pos = header.find('NAME')
    driver_pos = header.find('DRIVER')
    scope_pos = header.find('SCOPE')
    
    networks = []
    for line in lines[1:]:  # Skip header
        if line.strip():
            # Extract fields based on column positions
            network = {}
            
            # Network ID
            if name_pos > network_id_pos:
                network["network_id"] = line[network_id_pos:name_pos].strip()
            else:
                parts = line.split()
                network["network_id"] = parts[0] if len(parts) > 0 else ""
            
            # Name
            if driver_pos > name_pos:
                network["name"] = line[name_pos:driver_pos].strip()
            else:
                parts = line.split()
                network["name"] = parts[1] if len(parts) > 1 else ""
            
            # Driver
            if scope_pos > driver_pos:
                network["driver"] = line[driver_pos:scope_pos].strip()
            else:
                parts = line.split()
                network["driver"] = parts[2] if len(parts) > 2 else ""
            
            # Scope (last column)
            if scope_pos >= 0:
                network["scope"] = line[scope_pos:].strip()
            else:
                parts = line.split()
                network["scope"] = parts[3] if len(parts) > 3 else ""
            
            networks.append(network)
    
    return networks

def parse_volume_list(output):
    """Parse docker volume ls output into structured data"""
    if not output:
        return []
    
    lines = output.split('\n')
    if len(lines) < 2:
        return []
    
    # Get header line to understand column positions
    header = lines[0]
    if not header:
        return []
    
    # Find column positions based on header
    driver_pos = header.find('DRIVER')
    volume_name_pos = header.find('VOLUME NAME')
    
    volumes = []
    for line in lines[1:]:  # Skip header
        if line.strip():
            # Extract fields based on column positions
            volume = {}
            
            # Driver
            if volume_name_pos > driver_pos:
                volume["driver"] = line[driver_pos:volume_name_pos].strip()
            else:
                parts = line.split()
                volume["driver"] = parts[0] if len(parts) > 0 else ""
            
            # Volume Name (last column)
            if volume_name_pos >= 0:
                volume["volume_name"] = line[volume_name_pos:].strip()
            else:
                parts = line.split()
                volume["volume_name"] = parts[1] if len(parts) > 1 else ""
            
            volumes.append(volume)
    
    return volumes

def parse_docker_info(output):
    """Parse docker info output into structured data"""
    if not output:
        return {}
    
    info = {}
    current_section = None
    current_subsection = None
    
    lines = output.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for main sections (no leading space)
        if not line.startswith(' ') and ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            if key in ['Client', 'Server']:
                current_section = key
                info[current_section] = {}
                if value:
                    info[current_section]['type'] = value
            else:
                if current_section:
                    info[current_section][key] = value
                else:
                    info[key] = value
        
        # Check for subsections (single space indent)
        elif line.startswith(' ') and not line.startswith('  ') and ':' in line:
            if current_section:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                if key in ['Plugins', 'Security Options']:
                    current_subsection = key
                    info[current_section][current_subsection] = {}
                    if value:
                        info[current_section][current_subsection]['details'] = value
                else:
                    # Convert numeric values
                    if value.isdigit():
                        value = int(value)
                    elif value.replace('.', '').replace('GiB', '').replace('MiB', '').replace('KB', '').isdigit():
                        # Keep memory sizes as strings for now
                        pass
                    
                    info[current_section][key] = value
        
        # Check for sub-subsections (double space indent)
        elif line.startswith('  ') and ':' in line:
            if current_section and current_subsection:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                if current_subsection not in info[current_section]:
                    info[current_section][current_subsection] = {}
                
                info[current_section][current_subsection][key] = value
        
        # Handle list items (single space, no colon)
        elif line.startswith(' ') and not line.startswith('  ') and ':' not in line:
            if current_section and current_subsection:
                if 'items' not in info[current_section][current_subsection]:
                    info[current_section][current_subsection]['items'] = []
                info[current_section][current_subsection]['items'].append(line.strip())
    
    return info
