from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, or_, not_
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from flask import request
import math

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Get reading time estimate
def calculate_reading_time(content):
    
    if (content != None):
        words = content.split()

        # Calculate the reading time (in minutes) assuming 200 words per minute
        reading_time = len(words) / 200

        # Round up the reading time to the nearest whole minute
        reading_time = math.ceil(reading_time)

        return reading_time
    
    else:

        return 0

def urlize(text):
    # Remove leading and trailing whitespace
    text = text.strip()

    # Replace hyphens and underscores with spaces
    text = text.replace('-', ' ').replace('_', ' ')

    # Split the text into words
    words = text.split()

    # Capitalize the first letter of each word, excluding common stop words
    words = [word.capitalize() if word.lower(
    ) not in stop_words else word for word in words]

    # Join the words back together with hyphens
    text = ' '.join(words)

    text = text[0].capitalize() + text[1:]

    return text

# Create a function to build the data_dict


def build_data_dict(categories, articles,):
    # Fetch categories, subcategories and articles for building blocks
    building_blocks_categories = categories.query.filter_by(
        type='building-blocks', weight=0).all()
    building_blocks_category_ids = [
        category.id for category in building_blocks_categories]
    bb_children_categories = categories.query.filter(
        categories.parent.in_(building_blocks_category_ids)).all()
    bb_children_category_ids = [
        sub_category.id for sub_category in bb_children_categories]
    articles_bb = articles.query.filter(
        articles.parent.in_(bb_children_category_ids)).all()

    # Fetch categories, articles for tutorials
    tutorials_categories = categories.query.filter_by(
        type='tutorials', weight=0).all()
    tutorials_category_ids = [
        tutorialcategory.id for tutorialcategory in tutorials_categories]
    tutorials_children_categories = categories.query.filter(
        categories.parent.in_(tutorials_category_ids)).all()
    tutorials_children_category_ids = [
        sub_category.id for sub_category in tutorials_children_categories]
    articles_tutorials = articles.query.filter(
        articles.parent.in_(tutorials_children_category_ids)).all()

    # Fetch articles for examples
    articles_examples = articles.query.filter_by(type='examples').all()

    # Create an empty dictionary to store the data
    data_dict = {}
    building_blocks = {}
    tutorials = {}

    # Iterate through building_blocks_categories
    for parent_category in building_blocks_categories:
        # Initialize a dictionary for the current parent category
        parent_category_dict = {
            'category_data': parent_category,
            'children_categories': {},
        }

        # Create a list to store child categories and their article counts
        child_categories_with_counts = []

        # Iterate through children_categories
        for child_category in bb_children_categories:
            if child_category.parent == parent_category.id:
                # Initialize a dictionary for the current child category
                child_category_dict = {
                    'category_data': child_category,
                    'articles': [],
                }

                # Iterate through articles_bb
                for article in articles_bb:
                    if article.parent == child_category.id:
                        # Append the article data to the current child category
                        child_category_dict['articles'].append(article)

                # Add the child category and its article count to the list
                child_categories_with_counts.append(
                    (child_category_dict, len(child_category_dict['articles'])))

        # Sort child categories by the number of articles in descending order
        sorted_child_categories = sorted(
            child_categories_with_counts, key=lambda x: x[1], reverse=True)

        # Reconstruct the children_categories dictionary with the sorted order
        parent_category_dict['children_categories'] = {
            child[0]['category_data'].id: child[0] for child in sorted_child_categories}

        # Add the parent category dictionary to the data_dict
        building_blocks[parent_category.id] = parent_category_dict

    # Iterate through tutorials
    for parent_category in tutorials_categories:
        # Initialize a dictionary for the current parent category
        parent_category_dict = {
            'category_data': parent_category,
            'children_categories': {},
        }

        # Create a list to store child categories and their article counts
        child_categories_with_counts = []

        # Iterate through children_categories
        for child_category in tutorials_children_categories:
            if child_category.parent == parent_category.id:
                # Initialize a dictionary for the current child category
                child_category_dict = {
                    'category_data': child_category,
                    'articles': [],
                }

                # Iterate through articles_bb
                for article in articles_tutorials:
                    if article.parent == child_category.id:
                        # Append the article data to the current child category
                        child_category_dict['articles'].append(article)

                # Add the child category and its article count to the list
                child_categories_with_counts.append(
                    (child_category_dict, len(child_category_dict['articles'])))

        # Sort child categories by the number of articles in descending order
        sorted_child_categories = sorted(
            child_categories_with_counts, key=lambda x: x[1], reverse=True)

        # Reconstruct the children_categories dictionary with the sorted order
        parent_category_dict['children_categories'] = {
            child[0]['category_data'].id: child[0] for child in sorted_child_categories}

        # Add the parent category dictionary to the data_dict
        tutorials[parent_category.id] = parent_category_dict

    # Voeg de reading_time toe aan elk artikel in building-blocks
    for parent_category_id, parent_category_data in building_blocks.items():
        for child_category_id, child_category_data in parent_category_data['children_categories'].items():
            for article in child_category_data['articles']:
                article.reading_time = calculate_reading_time(article.content)

    # Voeg de reading_time toe aan elk artikel in tutorials
    for parent_category_id, parent_category_data in tutorials.items():
        for child_category_id, child_category_data in parent_category_data['children_categories'].items():
            for article in child_category_data['articles']:
                article.reading_time = calculate_reading_time(article.content)

    # Voeg de reading_time toe aan elk artikel in examples
    for article in articles_examples:
        article.reading_time = calculate_reading_time(article.content)

    # Add to dict
    data_dict['building-blocks'] = building_blocks
    data_dict['tutorials'] = tutorials
    data_dict['examples'] = articles_examples

    return data_dict

# Generate table of contents


def generate_table_of_contents(content_html):
    # Parse de HTML-content met BeautifulSoup
    soup = BeautifulSoup(content_html, 'html.parser')

    # Zoek naar alle h2 en h3 elementen in de content
    headings = soup.find_all(['h2', 'h3'])

    # Bouw de inhoudsopgave op basis van de gevonden headings
    table_of_contents = []

    current_h2 = None
    for heading in headings:
        # Bepaal het niveau van de heading (h2 of h3)
        level = heading.name

        # Haal de tekst van de heading op
        text = heading.text.strip()

        # Genereer een anchor (id) op basis van de tekst van de heading
        anchor = text.lower().replace(' ', '-')

        if level == 'h2':
            current_h2 = {'text': text, 'anchor': anchor, 'subheadings': []}
            table_of_contents.append(current_h2)
        elif level == 'h3' and current_h2 is not None:
            current_h2['subheadings'].append({'text': text, 'anchor': anchor})

    return table_of_contents

# Functie om breadcrumbs op te halen


def get_breadcrumbs():
    base_url = "http://127.0.0.1:5000"
    current_url = request.url
    path = current_url.replace(base_url, "")
    url_parts = path.split("/")
    breadcrumbs = [{"name": "Home", "url": base_url}]

    # Bouw de breadcrumb-items op basis van de delen van de URL
    for i in range(1, len(url_parts)):
        breadcrumb = {
            "name": url_parts[i].replace("-", " ").title(),
            "url": base_url + "/".join(url_parts[:i + 1]) + "/"
        }
        breadcrumbs.append(breadcrumb)

    return breadcrumbs

# Generate related articles


def find_related_articles(keywords, articles, categories, id):
    keyword_list = keywords.split()

    # Find keywords in the 'keywords' or 'content' columns of the articles
    related_articles = articles.query.filter(
        or_(
            articles.keywords.ilike('%{}%'.format(keyword)) for keyword in keyword_list
        ),
        or_(
            articles.content.ilike('%{}%'.format(keyword)) for keyword in keyword_list
        ),
        not_(articles.id == id)
    ).all()

    # Order Based on Appearances
    related_articles.sort(key=lambda article: sum(keyword_list.count(
        keyword) for keyword in article.keywords.split() + article.content.split()), reverse=True)

    # Top 5
    top_related_articles = related_articles[:5]

    for top_article in top_related_articles:
        url = None
        if (top_article.type == 'building-blocks') or (top_article.type == 'tutorials'):
            child_category = categories.query.filter_by(id=top_article.parent).first()
            if child_category:
                category = categories.query.filter_by(id=child_category.parent).first()
                if category:
                    child_category_path = child_category.path
                    category_path = category.path
                    url = top_article.type + '/' + category_path + '/' + \
                        child_category_path + '/' + top_article.path

            # Add Url to Article
            top_article.url = url

    return top_related_articles

