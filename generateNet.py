#!./pyenv/bin/python3
import sys
import pydot
import re
import os

def verify_node(s):
    pattern = r'^(n\d+|g0|v\d+)$'
    return bool(re.match(pattern,s))

def convert_name(node):
    if node == "g0":
        return "genesis0"
    if node[0] == 'v':
        return "validator"+node[1:]
    if node[0] == 'n':
        return "node"+node[1:]

def get_node_peers(graph, node):
    PEERS=""
    for edge in graph[0].get_edges():
        if(edge.get_source() == node or \
                edge.get_destination() == node):
            if(edge.get_source() == node):
                peer_name = convert_name(edge.get_destination())
                PEERS+=f"{peer_name} "
            else:
                peer_name = convert_name(edge.get_source())
                PEERS+=f"{peer_name} "
    if PEERS[-1] == " ":
        PEERS=PEERS[:-1]
    return PEERS

def generate_networks(graph):
    network_string="networks:\n"
    for edge in graph[0].get_edges():
        source = convert_name(edge.get_source())
        dest = convert_name(edge.get_destination())
        link_name = f"net_{source}_{dest}"
        network_string += f"  {link_name}:\n"
        network_string += "    driver: bridge\n"
        network_string += f"    name: {link_name}\n"
    return network_string

def generate_validator_keygen(graph,nodes):
    keygen_string = ""
    for node in nodes:
        if(node[0] == 'v'):
            val_name = convert_name(node)
            service_name = val_name+"_keygen"
            keygen_string += f"  {service_name}:\n"
            keygen_string += f"    build: .\n"
            keygen_string += f"    image: atomone:latest\n"
            keygen_string += f"    container_name: {service_name}\n"
            keygen_string += f"    environment:\n"
            keygen_string += f"      - NODEID={node[1:]}\n"
            keygen_string += f"      - ADDRESS={val_name}\n"
            keygen_string += f"    volumes:\n"
            keygen_string += f"      - ./{val_name}_data:/root/atomone_data\n"
            keygen_string += f"      - ./shared_data:/root/shared_data\n"
            keygen_string += f"      - ./scripts/validator_keygen.sh:/root/validator_keygen.sh\n"
            keygen_string += f"    command: /root/validator_keygen.sh\n"
            keygen_string += f"    networks:\n"
            for edge in graph[0].get_edges():
                if(edge.get_source() == node or \
                        edge.get_destination() == node):
                    source = convert_name(edge.get_source())
                    dest = convert_name(edge.get_destination())
                    link_name = f"net_{source}_{dest}\n"
                    keygen_string += f"      - {link_name}"
    return keygen_string

def generate_genesis_build(graph,nodes):
    keygen_string = ""
    for node in nodes:
        if node == 'g0':
            val_name = convert_name(node)
            service_name = val_name+"_build"
            keygen_string += f"  {service_name}:\n"
            keygen_string += f"    build: .\n"
            keygen_string += f"    image: atomone:latest\n"
            keygen_string += f"    container_name: {service_name}\n"
            keygen_string += f"    environment:\n"
            keygen_string += f"      - NODEID={node[1:]}\n"
            keygen_string += f"      - ADDRESS={val_name}\n"
            keygen_string += f"    volumes:\n"
            keygen_string += f"      - ./{val_name}_data:/root/atomone_data\n"
            keygen_string += f"      - ./shared_data:/root/shared_data\n"
            keygen_string += f"      - ./scripts/genesis_build.sh:/root/genesis_build.sh\n"
            keygen_string += f"    command: /root/genesis_build.sh\n"
            keygen_string += f"    networks:\n"
            for edge in graph[0].get_edges():
                if edge.get_source() == node or \
                        edge.get_destination() == node:
                    source = convert_name(edge.get_source())
                    dest = convert_name(edge.get_destination())
                    link_name = f"net_{source}_{dest}"
                    keygen_string += f"      - {link_name}\n"
            keygen_string += f"    depends_on:\n"
            for node in nodes:
                if node[0] == 'v':
                    val_name = convert_name(node)
                    keygen_string += f"      {val_name}_keygen:\n"
                    keygen_string += f"        condition: service_completed_successfully\n"
    return keygen_string

def generate_genesis(graph,nodes):
    keygen_string = ""
    for node in nodes:
        if node == 'g0':
            val_name = convert_name(node)
            service_name = val_name
            keygen_string += f"  {service_name}:\n"
            keygen_string += f"    build: .\n"
            keygen_string += f"    image: atomone:latest\n"
            keygen_string += f"    container_name: {service_name}\n"
            keygen_string += f"    environment:\n"
            keygen_string += f"      - NODEID={node[1:]}\n"
            keygen_string += f"      - ADDRESS={val_name}\n"
            keygen_string += f"    volumes:\n"
            keygen_string += f"      - ./{val_name}_data:/root/atomone_data\n"
            keygen_string += f"      - ./shared_data:/root/shared_data\n"
            keygen_string += f"      - ./scripts/genesis.sh:/root/genesis.sh\n"
            keygen_string += f"    command: /root/genesis.sh\n"
            keygen_string += f"    networks:\n"
            for edge in graph[0].get_edges():
                if edge.get_source() == node or \
                        edge.get_destination() == node:
                    source = convert_name(edge.get_source())
                    dest = convert_name(edge.get_destination())
                    link_name = f"net_{source}_{dest}"
                    keygen_string += f"      - {link_name}\n"
            keygen_string += f"    depends_on:\n"
            keygen_string += f"      genesis0_build:\n"
            keygen_string += f"        condition: service_completed_successfully\n"
    return keygen_string

def generate_validator(graph,nodes):
    keygen_string = ""
    for node in nodes:
        if(node[0] == 'v'):
            PEERS=get_node_peers(graph, node)
            val_name = convert_name(node)
            service_name = val_name
            keygen_string += f"  {service_name}:\n"
            keygen_string += f"    build: .\n"
            keygen_string += f"    image: atomone:latest\n"
            keygen_string += f"    container_name: {service_name}\n"
            keygen_string += f"    environment:\n"
            keygen_string += f"      - NODEID={node[1:]}\n"
            keygen_string += f"      - ADDRESS={val_name}\n"
            keygen_string += f"      - PEERS={PEERS}\n"
            keygen_string += f"    volumes:\n"
            keygen_string += f"      - ./{val_name}_data:/root/atomone_data\n"
            keygen_string += f"      - ./shared_data:/root/shared_data\n"
            keygen_string += f"      - ./scripts/validator.sh:/root/validator.sh\n"
            keygen_string += f"    command: /root/validator.sh\n"
            keygen_string += f"    networks:\n"
            for edge in graph[0].get_edges():
                if(edge.get_source() == node or \
                        edge.get_destination() == node):
                    source = convert_name(edge.get_source())
                    dest = convert_name(edge.get_destination())
                    link_name = f"net_{source}_{dest}"
                    keygen_string += f"      - {link_name}\n"
            keygen_string += f"    depends_on:\n"
            keygen_string += f"      genesis0_build:\n"
            keygen_string += f"        condition: service_completed_successfully\n"
    return keygen_string

def generate_node(graph,nodes):
    keygen_string = ""
    for node in nodes:
        if(node[0] == 'n'):
            PEERS=get_node_peers(graph, node)
            val_name = convert_name(node)
            service_name = val_name
            keygen_string += f"  {service_name}:\n"
            keygen_string += f"    build: .\n"
            keygen_string += f"    image: atomone:latest\n"
            keygen_string += f"    container_name: {service_name}\n"
            keygen_string += f"    environment:\n"
            keygen_string += f"      - NODEID={node[1:]}\n"
            keygen_string += f"      - ADDRESS={val_name}\n"
            keygen_string += f"      - PEERS={PEERS}\n"
            keygen_string += f"    volumes:\n"
            keygen_string += f"      - ./{val_name}_data:/root/atomone_data\n"
            keygen_string += f"      - ./shared_data:/root/shared_data\n"
            keygen_string += f"      - ./scripts/node.sh:/root/node.sh\n"
            keygen_string += f"    command: /root/node.sh\n"
            keygen_string += f"    networks:\n"
            for edge in graph[0].get_edges():
                if(edge.get_source() == node or \
                        edge.get_destination() == node):
                    source = convert_name(edge.get_source())
                    dest = convert_name(edge.get_destination())
                    link_name = f"net_{source}_{dest}"
                    keygen_string += f"      - {link_name}\n"
            keygen_string += f"    depends_on:\n"
            keygen_string += f"      genesis0_build:\n"
            keygen_string += f"        condition: service_completed_successfully\n"
    return keygen_string

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: expected one command-line argument, having the name of the network file")
        sys.exit(1)
    filename = sys.argv[1]
    if not filename.endswith('.dot'):
        print(f"Error: '{filename}' does not end with '.dot'")
        sys.exit(1)
    graph = pydot.graph_from_dot_file(filename)
    # print(graph[0])

    nodes = set()
    for edge in graph[0].get_edges():
        # print(edge.get_source() + "--" + edge.get_destination())
        nodes.add(edge.get_source())
        nodes.add(edge.get_destination())

    for node in nodes:
        if not verify_node(node):
            print("Error: node break specification "+node)
            sys.exit(1)

    if not "g0" in nodes:
        print("Error: each network needs to have a genesis node 'g0'")
        sys.exit(1)

    for node in nodes:
        val_name = convert_name(node)
        if not os.path.isdir(f"{val_name}_data"):
            os.mkdir(f"{val_name}_data")

    compose = "services:\n"
    compose += generate_validator_keygen(graph,nodes)
    compose += "\n"
    compose += generate_genesis_build(graph,nodes)
    compose += "\n"
    compose += generate_genesis(graph,nodes)
    compose += "\n"
    compose += generate_validator(graph,nodes)
    compose += "\n"
    compose += generate_node(graph,nodes)
    compose += "\n"
    compose += generate_networks(graph)
    compose += "\n"
    print(compose)
    


    

