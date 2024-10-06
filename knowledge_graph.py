#!/usr/bin/env python3

import os
import subprocess  # For Git interactions
from bs4 import BeautifulSoup
import networkx as nx
from pyvis.network import Network
from urllib.parse import urlparse
import argparse
import sys

# ----------------------------
# Default Output File
# ----------------------------

OUTPUT_FILE_DEFAULT = 'static/garden_map.html'

# ----------------------------
# Exclusion Sets
# ----------------------------

# Exclude specific files by their filenames
EXCLUDE_FILES = set([
    'output_graph.html',
    'animation_template.html',
    'sub.html',
    'index-head.html',
    'template.html',
])

# Exclude pages based on their <h1> titles
EXCLUDE_TITLES = set([
    '@tailwindcss/forms examples',
    '@tailwindcss/forms-examples',
    'injected',
    '{{this imitates some kind of template fragment}}',
    'kitchen-sink',
    '~{linked-path}',
    'Hello world.',
    'private',
    'directory',
    'index-caps',
    'fragment',
])

# ----------------------------
# Git Helper Functions
# ----------------------------

def get_git_root(root_dir):
    """
    Returns the Git repository root directory if root_dir is inside a Git repo.
    Otherwise, returns None.
    """
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            cwd=root_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        git_root = result.stdout.strip()
        return git_root
    except subprocess.CalledProcessError:
        return None

def get_untracked_files(git_root):
    """
    Returns a set of untracked file paths relative to the Git root directory.
    """
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd=git_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        lines = result.stdout.splitlines()
        untracked = set()
        for line in lines:
            if line.startswith('??'):
                # Line format: '?? path/to/file'
                file_path = line[3:].strip()
                untracked.add(os.path.normpath(file_path))
        return untracked
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving untracked files: {e.stderr}", file=sys.stderr)
        return set()

# ----------------------------
# Core Functions
# ----------------------------

def find_html_files(root_dir, exclude_untracked=False):
    """
    Scans the root directory and its subdirectories for HTML files,
    excluding those in EXCLUDE_FILES and optionally untracked Git files.
    """
    html_files = []
    git_root = get_git_root(root_dir) if exclude_untracked else None
    untracked_files = get_untracked_files(git_root) if git_root else set()

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.html') or filename.lower().endswith('.htm'):
                if filename in EXCLUDE_FILES:
                    continue
                filepath = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(filepath, root_dir)
                rel_path_norm = os.path.normpath(rel_path)
                if exclude_untracked and rel_path_norm in untracked_files:
                    # Skip untracked files
                    continue
                html_files.append(rel_path_norm)
    return html_files

def get_page_title(file_path):
    """
    Extracts the text from the first <h1> tag in the HTML file.
    Returns the title or the filename without extension as a fallback.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        h1_tag = soup.find('h1')
        if h1_tag:
            return h1_tag.get_text(strip=True)
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
    return os.path.splitext(os.path.basename(file_path))[0]  # Fallback to filename without extension

def extract_links(html_file, root_dir, html_files_set):
    """
    Extracts internal links from an HTML file, resolving them to relative paths.
    """
    file_dir = os.path.dirname(os.path.join(root_dir, html_file))
    try:
        with open(os.path.join(root_dir, html_file), 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {html_file}: {e}", file=sys.stderr)
        return set()

    soup = BeautifulSoup(content, 'html.parser')
    links = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        # Ignore external links and mailto links
        if href.startswith('mailto:'):
            continue
        parsed_href = urlparse(href)
        if href.startswith('#'):
            # Process hash links
            hash_value = href[1:]  # Remove the '#' character
            if not hash_value:
                # Empty hash, map to 'home.html' in root_dir
                target = os.path.normpath(os.path.join(root_dir, 'src', 'pages', 'home.html'))
                href_rel_path = os.path.relpath(target, root_dir)
                href_rel_path = os.path.normpath(href_rel_path)
                if href_rel_path in html_files_set:
                    links.add(href_rel_path)
                continue
            # Replicate your JavaScript logic
            last_slash_index = hash_value.rfind('/')
            page_name = hash_value if last_slash_index == -1 else hash_value[last_slash_index + 1:]
            indexPath = os.path.normpath(os.path.join(root_dir, 'src', 'pages', hash_value, f'{page_name}.html'))
            hashPath = os.path.normpath(os.path.join(root_dir, 'src', 'pages', f'{hash_value}.html'))
            # Check if these files exist
            indexPath_rel = os.path.relpath(indexPath, root_dir)
            indexPath_rel = os.path.normpath(indexPath_rel)
            hashPath_rel = os.path.relpath(hashPath, root_dir)
            hashPath_rel = os.path.normpath(hashPath_rel)
            if indexPath_rel in html_files_set:
                links.add(indexPath_rel)
            elif hashPath_rel in html_files_set:
                links.add(hashPath_rel)
            else:
                # Also check for files with the same name as the directory
                dir_name = os.path.basename(hash_value)
                dirPath = os.path.normpath(os.path.join(root_dir, 'src', 'pages', hash_value, f'{dir_name}.html'))
                dirPath_rel = os.path.relpath(dirPath, root_dir)
                dirPath_rel = os.path.normpath(dirPath_rel)
                if dirPath_rel in html_files_set:
                    links.add(dirPath_rel)
                else:
                    # File not found, ignore or handle accordingly
                    pass
        else:
            # Process normal links
            if parsed_href.scheme != '' or parsed_href.netloc != '':
                continue
            # Remove query and fragment
            href_no_frag = parsed_href._replace(query='', fragment='').geturl()
            href_path = os.path.normpath(os.path.join(file_dir, href_no_frag))
            # Get path relative to root_dir
            href_rel_path = os.path.relpath(href_path, root_dir)
            href_rel_path = os.path.normpath(href_rel_path)
            if href_rel_path in html_files_set:
                links.add(href_rel_path)
            else:
                # If href_path is a directory, look for file with same name as directory
                if os.path.isdir(href_path):
                    dir_name = os.path.basename(href_path)
                    file_same_name = os.path.join(href_path, dir_name + '.html')
                    file_same_name_rel = os.path.relpath(file_same_name, root_dir)
                    file_same_name_rel = os.path.normpath(file_same_name_rel)
                    if file_same_name_rel in html_files_set:
                        links.add(file_same_name_rel)
                    else:
                        # Check for index.html in the directory
                        index_file = os.path.join(href_path, 'index.html')
                        index_file_rel = os.path.relpath(index_file, root_dir)
                        index_file_rel = os.path.normpath(index_file_rel)
                        if index_file_rel in html_files_set:
                            links.add(index_file_rel)
                        else:
                            # Directory does not contain expected file, ignore or handle accordingly
                            pass
    return links

def build_graph(root_dir, exclude_untracked=False):
    """
    Builds a directed graph from HTML files, excluding files based on filenames and titles.
    Additionally, adds edges from parent pages to their children based on directory structure.
    Also removes edges from index.html to these children to prevent redundancy.
    """
    html_files = find_html_files(root_dir, exclude_untracked=exclude_untracked)
    html_files_set = set(html_files)

    # Mapping from file to title
    file_to_title = {}
    excluded_files = set()

    # First pass: Get titles and exclude based on EXCLUDE_TITLES
    for html_file in html_files:
        file_path = os.path.join(root_dir, html_file)
        title = get_page_title(file_path)
        file_to_title[html_file] = title
        if title in EXCLUDE_TITLES:
            print(f"Excluding {html_file} based on title: {title}")
            excluded_files.add(html_file)
        # Debugging output
        # Uncomment the following line if you want to see all titles
        # print(f"Title: {title} for {html_file}")

    # Remove excluded files from the set
    html_files_set -= excluded_files

    # Initialize the directed graph
    G = nx.DiGraph()

    # Add nodes for remaining files
    for html_file in html_files_set:
        G.add_node(html_file)

    # Add edges based on links
    for html_file in html_files_set:
        links = extract_links(html_file, root_dir, html_files_set)
        # Only consider links to files in html_files_set
        for link in links:
            if link in html_files_set:
                G.add_edge(html_file, link)

    # ----------------------------
    # Add Parent-to-Children Edges
    # ----------------------------

    children_of_parents = set()  # To keep track of children nodes connected via parent pages

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Get relative path of the current directory
        dir_rel_path = os.path.relpath(dirpath, root_dir)
        dir_rel_path = os.path.normpath(dir_rel_path)

        # Get the directory name
        dir_name = os.path.basename(dirpath)

        # Define the expected parent filename (same as directory name)
        parent_filename = f"{dir_name}.html"

        # Check if the parent file exists in this directory
        if parent_filename in filenames:
            parent_rel_path = os.path.normpath(os.path.join(dir_rel_path, parent_filename))
            if parent_rel_path in html_files_set:
                # Iterate through all HTML files in this directory
                for child_filename in filenames:
                    if child_filename.lower().endswith('.html') or child_filename.lower().endswith('.htm'):
                        if child_filename == parent_filename:
                            continue  # Skip the parent itself
                        child_rel_path = os.path.normpath(os.path.join(dir_rel_path, child_filename))
                        if child_rel_path in html_files_set:
                            G.add_edge(parent_rel_path, child_rel_path)
                            children_of_parents.add(child_rel_path)
                #print(f"Added parent-to-children edges for: {parent_rel_path}")

    # ----------------------------
    # Remove Edges from index.html to Children of Parent Pages
    # ----------------------------

    index_node = 'index.html'  # Adjust if index.html is located elsewhere

    if index_node in G:
        for child in children_of_parents:
            if G.has_edge(index_node, child):
                G.remove_edge(index_node, child)
                #print(f"Removed edge from {index_node} to {child}")
    else:
        print(f"No node found for {index_node}; skipping edge removal.")

    # ----------------------------
    # Add labels and URLs for visualization
    # ----------------------------

    for node in G.nodes():
        title = file_to_title.get(node, os.path.splitext(os.path.basename(node))[0])
        G.nodes[node]['title'] = node  # The relative path
        G.nodes[node]['label'] = title
        # Generate relative URL for the node
        # Assuming the output HTML is in root_dir, the relative URL can be the node's relative path
        G.nodes[node]['url'] = node.replace("\\", "/")  # Replace backslashes on Windows

    return G

def visualize_graph(G, output_file=OUTPUT_FILE_DEFAULT):
    """
    Visualizes the directed graph using PyVis with dark mode and clickable nodes.
    """
    net = Network(height='500px', width='100%', directed=True, notebook=False, bgcolor='#2B2B2B', font_color='white')

    # Customize physics to prevent overlapping labels
    net.set_options("""
    var options = {
      "nodes": {
        "font": {
          "size": 14,
          "color": "white"
        },
        "color": {
          "background": "#4A90E2",
          "border": "#1C1C1C",
          "highlight": {
            "background": "#50E3C2",
            "border": "#1C1C1C"
          }
        },
        "shape": "dot",
        "size": 20
      },
      "edges": {
        "color": {
          "color": "#AAAAAA",
          "highlight": "#FFFFFF"
        },
        "arrows": {
          "to": {
            "enabled": true,
            "scaleFactor": 0.5,
            "type": "arrow"
          }
        },
        "smooth": {
          "enabled": true,
          "type": "dynamic"
        }
      },
      "physics": {
        "enabled": true,
        "barnesHut": {
          "gravitationalConstant": -2000,
          "centralGravity": 0.4,
          "springLength": 100,
          "springConstant": 0.04,
          "damping": 0.09,
          "avoidOverlap": 1
        },
        "minVelocity": 0.5,
        "solver": "barnesHut"
      },
      "interaction": {
        "hover": true,
        "navigationButtons": false,
        "keyboard": false
      }
    }
    """)

    net.from_nx(G)

    # Add URLs to nodes for clicking
    for node in net.nodes:
        node['href'] = node['url']
        node['title'] = node['label']  # Tooltip

    # Display the graph
    net.write_html(output_file)

    # After writing the HTML file, append the site's CSS to the <head> section
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add custom CSS to remove the border of the graph container
    custom_css = """
    <style>
        body {
            overflow: hidden;
        }
        #mynetwork {
            border: none !important;
        }
    </style>
    """
    content = content.replace('</head>', f'{custom_css}\n</head>')

    # Insert the CSS link before </head>
    content = content.replace('</head>', '  <link rel="stylesheet" href="static/stylesheet.css">\n</head>')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

# ----------------------------
# Main Execution
# ----------------------------

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build and visualize a knowledge graph from HTML files.')
    parser.add_argument('root_dir', help='Root directory to search for HTML files.')
    parser.add_argument('--output', default=OUTPUT_FILE_DEFAULT, help='Output HTML file for the graph visualization.')
    parser.add_argument('--exclude-untracked', action='store_true', help='Exclude untracked Git files from the graph.')
    args = parser.parse_args()

    # Update the default output file if specified
    if args.output:
        OUTPUT_FILE_DEFAULT = args.output

    # Verify if --exclude-untracked is set and root_dir is a Git repository
    if args.exclude_untracked:
        git_root = get_git_root(args.root_dir)
        if not git_root:
            print("Warning: The specified root directory is not a Git repository. Proceeding without excluding untracked files.", file=sys.stderr)

    # Build the graph
    G = build_graph(args.root_dir, exclude_untracked=args.exclude_untracked)
    visualize_graph(G, args.output)

    print(f"Knowledge graph generated at {args.output}")
