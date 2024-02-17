import sqlite3
import os
import re
import shutil

# Create the database and table
conn = sqlite3.connect('tsh.db')
cursor = conn.cursor()

# Create the categories and articles tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS topics (
        id INTEGER PRIMARY KEY,
        title TEXT,
        level INTEGER,
        parent INTEGER,
        path TEXT,
        draft TEXT
    )
''')

# Create the articles table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY,
        type TEXT,
        title TEXT,
        parent INTEGER,
        description TEXT,
        path TEXT,
        keywords TEXT,
        date TEXT,
        date_modified TEXT,
        draft TEXT,
        weight INTEGER,
        author TEXT,
        content TEXT
    )
''')
               
# Create the contributors table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS contributors (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description_short TEXT,
        description_long TEXT,
        skills TEXT,
        linkedin TEXT,
        facebook TEXT,
        twitter TEXT,
        email TEXT,
        image TEXT,
        status TEXT,
        path TEXT,
        content TEXT
    )
''')
               
# Create the blogs table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS blogs (
        id INTEGER PRIMARY KEY,
        title TEXT,
        description TEXT,
        path TEXT,
        date TEXT,
        date_modified TEXT,
        draft TEXT,
        content TEXT
    )
''')

# Commit the creation of tables
conn.commit()

# Define the content directory
script_directory = os.path.dirname(os.path.realpath(__file__))
content_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "content")
topic_folder = os.path.join(content_directory, 'topics')

def insert_topic_into_db(title, level, parent, path, draft):
    cursor.execute("INSERT INTO topics (title, level, parent, path, draft) VALUES (?, ?, ?, ?, ?)", (title, level, parent, path, draft))
    return cursor.lastrowid

def insert_article_into_db(type, title, parent, description, path, keywords, date, date_modified, draft, weight, author, content):
    cursor.execute("INSERT INTO articles (type, title, parent, description, path, keywords, date, date_modified, draft, weight, author, content) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                   (type, title, parent, description, path, keywords, date, date_modified, draft, weight, author, content))

def parse_md_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        title = re.search(r'title: "(.*?)"', content)
        description = re.search(r'description: "(.*?)"', content)
        draft = re.search(r'draft: (.*?)\n', content)

        # Extract values, return None if not found
        title_value = title.group(1) if title else None
        description_value = description.group(1) if description else None
        draft_value = draft.group(1) if draft else None

        return title_value, description_value, draft_value

def process_article(md_file_path, parent_id):
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        content = md_file.read()
        title = re.search(r'title: "(.*?)"', content)
        description = re.search(r'description: "(.*?)"', content)
        draft = re.search(r'draft: (.*?)\n', content)
        keywords = re.search(r'keywords: "(.*?)"', content)
        date = re.search(r'date: (\d{4}-\d{2}-\d{2})', content)
        date_modified = re.search(r'date_modified: (\d{4}-\d{2}-\d{2})', content)
        weight = re.search(r'weight: (\d+)', content)
        author = re.search(r'author: "(.*?)"', content)

        # Extract article content
        match = re.search(r'---(.*?)---(.*)', content, re.DOTALL)
        if match:
            file_content = match.group(2).strip()

        # Insert data into articles table
        insert_article_into_db('topic', title.group(1) if title else None, parent_id,
                               description.group(1) if description else None, os.path.basename(md_file_path).replace('.md', ''),
                               keywords.group(1) if keywords else None, date.group(1) if date else None,
                               date_modified.group(1) if date_modified else None, draft.group(1) if draft else None,
                               int(weight.group(1)) if weight else None, author.group(1) if author else None, file_content)

def fill_database(root_path):
    exclude = {'img', 'images', 'data'}
    path_to_id = {}

    for path, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in exclude]
        level = path.count(os.sep) - root_path.count(os.sep)
        parent_path = os.path.dirname(path)
        parent_id = path_to_id.get(parent_path, None)
        folder_name = os.path.basename(path)

        index_file = os.path.join(path, '_index.md')
        if os.path.exists(index_file):
            title, description, draft = parse_md_file(index_file)
            folder_id = insert_topic_into_db(title, level, parent_id, folder_name, draft)
            path_to_id[path] = folder_id

            for file in os.listdir(path):  # Veranderd naar os.listdir(path)
                if file != '_index.md' and file.endswith('.md'):
                    md_file_path = os.path.join(path, file)
                    process_article(md_file_path, folder_id)

fill_database(topic_folder)

# Fetch Examples
examples_root_folder = os.path.join(content_directory, 'examples')
for md_file_name in os.listdir(examples_root_folder):
    if md_file_name != '_index.md' and md_file_name.endswith('.md'):
        # Construct the full path of the Markdown file
        md_file_path = os.path.join(examples_root_folder, md_file_name)

        path = md_file_name.replace('.md', '').lower()

        #Init Vars
        description = None
        title = None
        keywords = None
        date = None
        date_modified = None
        draft = None
        author = None
        content = None 

        # Read the contents of the Markdown file
        with open(md_file_path, 'r', encoding='utf-8') as md_file:

            # YAML
            for line in md_file:
                
                if line.startswith('description:'):
                    description = line.strip().replace('description:', '', 1).replace('"','').strip()
                elif line.startswith('title:'):
                    title = line.strip().replace('title:', '', 1).replace('"','').strip()
                elif line.startswith('keywords:'):
                    keywords = line.strip().replace('keywords:', '', 1).replace('"','').strip()
                elif line.startswith('date:'):
                    date = line.strip().replace('date:', '', 1).strip()
                elif line.startswith('date_modified:'):
                    date_modified = line.strip().replace('date_modified:', '', 1).strip()
                elif line.startswith('draft:'):
                    draft = line.strip().replace('draft:', '', 1).strip()
                elif line.startswith('author:'):
                    author = line.strip().replace('author:', '', 1).replace('"','').strip()
        
        with open(md_file_path, 'r', encoding='utf-8') as md_file:
            
            # Fetch Content
            md_file_content = md_file.read()
            match = re.match(r'---(.*?)---(.*)', md_file_content, re.DOTALL)
            if match:
                file_content = match.group(2)
                content = file_content

        # Execute an SQL INSERT statement to add data to the 'articles' table
        cursor.execute('''
            INSERT INTO articles (type, title, description, path, keywords, date, date_modified, draft, author, content)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', ('examples', title, description, path, keywords, date, date_modified, draft, author, content))

# Fetch Contributors
contributors_root_folder = os.path.join(content_directory, 'contributors')
for md_file_name in os.listdir(contributors_root_folder):
    if md_file_name != '_index.md' and md_file_name.endswith('.md'):
        # Construct the full path of the Markdown file
        md_file_path = os.path.join(contributors_root_folder, md_file_name)

        #Init Vars
        name = None
        description_short = None
        description_long = None
        skills_list = []
        skills = None
        skills_started = False
        skills_ended = False
        linkedin = None
        facebook = None
        twitter = None
        email = None
        image = None
        status = None
        content = None
        path = None
        

        # Read the contents of the Markdown file
        with open(md_file_path, 'r', encoding='utf-8') as md_file:

            # YAML
            for line in md_file:
                
                if line.startswith('name:'):
                    name = line.strip().replace('name:', '', 1).replace('"','').strip()
                    path = name.replace(' ','-').lower()
                elif line.startswith('description_short:'):
                    description_short = line.strip().replace('description_short:', '', 1).replace('"','').strip()
                elif line.startswith('description_long:'):
                    description_long = line.strip().replace('description_long:', '', 1).replace('"','').strip()
                elif 'linkedin' in line.strip().lower() and line.strip().startswith('link:'):
                    linkedin = line.strip().replace('link:', '', 1).strip()
                elif 'facebook' in line.strip().lower() and line.strip().startswith('link:'):
                    facebook = line.strip().replace('link:', '', 1).strip()
                elif 'twitter' in line.strip().lower() and line.strip().startswith('link:'):
                    twitter = line.strip().replace('link:', '', 1).strip()
                elif line.startswith('email:'):
                    email = line.strip().replace('email:', '', 1).replace('"','').strip()
                elif line.startswith('image:'):
                    image = line.strip().replace('image:', '', 1).replace('"','').strip()
                elif line.startswith('status:'):
                    status = line.strip().replace('status:', '', 1).replace('"','').strip()
                elif line.strip().startswith('skills:'):
                    skills_started = True
                elif skills_started and line.strip().startswith('-'):
                    skill = line.strip().lstrip('-').strip()
                    skills_list.append(skill)
                elif skills_started and not line.strip().startswith('-') and not line.strip().startswith('skills:'):
                    skills_started = False
                
        skills = ', '.join(skills_list)
        
        with open(md_file_path, 'r', encoding='utf-8') as md_file:
            
            # Fetch Content
            md_file_content = md_file.read()
            match = re.match(r'---(.*?)---(.*)', md_file_content, re.DOTALL)
            if match:
                content = match.group(2)

        # Execute an SQL INSERT statement to add data to the 'articles' table
        cursor.execute('''
            INSERT INTO contributors (name, description_short, description_long, skills, linkedin, facebook, twitter, email, image, status, path, content)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, description_short, description_long, skills, linkedin, facebook, twitter, email, image, status, path, content))

# Fetch Blogs
blog_root_folder = os.path.join(content_directory, 'blog')
for md_file_name in os.listdir(blog_root_folder):
    if md_file_name != '_index.md' and md_file_name.endswith('.md'):
        # Construct the full path of the Markdown file
        md_file_path = os.path.join(blog_root_folder, md_file_name)

        path = md_file_name.replace('.md', '').lower()

        #Init Vars
        description = None
        title = None
        date = None
        date_modified = None
        draft = None
        content = None 

        # Read the contents of the Markdown file
        with open(md_file_path, 'r', encoding='utf-8') as md_file:

            # YAML
            for line in md_file:
                
                if line.startswith('description:'):
                    description = line.strip().replace('description:', '', 1).replace('"','').strip()
                elif line.startswith('title:'):
                    title = line.strip().replace('title:', '', 1).replace('"','').strip()
                elif line.startswith('date:'):
                    date = line.strip().replace('date:', '', 1).strip()
                elif line.startswith('date_modified:'):
                    date_modified = line.strip().replace('date_modified:', '', 1).strip()
                elif line.startswith('draft:'):
                    draft = line.strip().replace('draft:', '', 1).strip()
        
        with open(md_file_path, 'r', encoding='utf-8') as md_file:
            
            # Fetch Content
            md_file_content = md_file.read()
            match = re.match(r'---(.*?)---(.*)', md_file_content, re.DOTALL)
            if match:
                file_content = match.group(2)
                content = file_content

        # Execute an SQL INSERT statement to add data to the 'articles' table
        cursor.execute('''
            INSERT INTO blogs (title, description, path, date, date_modified, draft, content)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, description, path, date, date_modified, draft, content))

# Submit to Database
conn.commit()
conn.close()

## Copy All images to img folder
img_directory = os.path.join(script_directory, "static/img")

## IMAGES AND VIDS
if not os.path.exists(img_directory):
    os.makedirs(img_directory)

image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.mov']

def is_image(filename):
    _, ext = os.path.splitext(filename)
    return ext.lower() in image_extensions

# Loop door de bestanden in de bronmap (content_directory) en submappen
for root, _, files in os.walk(content_directory):
    for filename in files:
        src_filepath = os.path.join(root, filename)
        
        # Controleer of het bestand een afbeelding is op basis van de extensie
        if is_image(filename):
            dst_filepath = os.path.join(img_directory, filename)
            
            # Kopieer het afbeeldingsbestand van de bronmap naar de doelmap en vervang indien nodig
            shutil.copy(src_filepath, dst_filepath)