# from path import element_path

from bs4 import BeautifulSoup, Tag  
from typing import List, Tuple, TypeAlias
from bs4 import BeautifulSoup  # Assuming you're using BeautifulSoup

from ..encode.markdown import soup_to_markdown as md_soup  

Path: TypeAlias = List[Tuple[str, int]]

def element_path(element: Tag|None)-> Path:
    path: Path = []
    while element is not None and element.name is not None:
        parent = element.parent
        if parent is not None:
            siblings = parent.find_all(element.name, recursive=False)
            index = siblings.index(element) + 1  # 1-based index
        else:
            index = 0  # For top-level element or if it's been detached
        path.insert(0, (element.name, index))
        element = parent
    
    return path

def find_fragments(html_content:str)-> list[Tag]:
    soup: Tag = BeautifulSoup(html_content, 'html.parser')
    fragments = [soup]
    
    # Define the tags to look for
    tags_to_find = ['nav', 'aside', 'header', 'footer']
    
    for tag in tags_to_find:
        # Find all elements for the tag
        fragments.extend(soup.find_all(tag))
    
    return fragments


def sort_fragments(fragments: list[Tag])-> list[tuple[Tag, Path]]:
    # Get the path for each fragment
    sorted_fragments = [(frag, element_path(frag)) for frag in fragments]
    # Sort the fragments based on the length of their path (depth in the DOM) and the path itself
    sorted_fragments.sort(key=lambda x: (len(x[1]), x[1]), reverse=True)
    return sorted_fragments

# def extract_fragments(soup, sorted_fragments):
#     extracted_fragments = []

#     # Extract the fragments from the soup object.
#     for fragment, _ in sorted_fragments:
#         # Use extract() to remove the tag from the soup and store it
#         extracted_fragments.append(fragment.extract())
    
#     # Convert the modified soup back to a string
#     remaining_content = str(soup)

#     return remaining_content, extracted_fragments

def extract_fragments( sorted_fragments):
    # Initialize the list to store extracted fragments
    extracted_fragments = []

    # Extract the fragments from the soup object.
    for fragment, path in sorted_fragments:
        # Use extract() to remove the tag from the soup and store it
        extracted_fragment = fragment.extract()
        # Add the extracted fragment to the list
        extracted_fragments.append((extracted_fragment, path))

    # The original document is also considered a fragment
    # Convert the modified soup back to a string and add it as the last fragment
    # original_fragment = str(soup)
    # extracted_fragments.append(original_fragment)

    return extracted_fragments

def get_fragments(html_content: str) -> List[Tuple[Tag, Path ]]:
    fragments = find_fragments(html_content)
    sorted_fragments = sort_fragments(fragments)
    extracted_fragments = extract_fragments( sorted_fragments)
    # canonical_frags = [ (frag,path, md(frag)) for (frag, path) in extracted_fragments ]
    return extracted_fragments


# def get_fragments(html_content):
#     soup = BeautifulSoup(html_content, 'html.parser')
#     fragments = find_fragments(html_content)
#     sorted_fragments = sort_fragments(fragments)
#     remaining_content, extracted_fragments = extract_fragments(soup, sorted_fragments)
#     return remaining_content, extracted_fragments

# # Example usage:
# original_html_content = "..."  # Your original HTML content goes here
# remaining_content, fragments_to_process = extract_fragments(original_html_content)


# The previously defined functions go here...


# test_find_fragments()
# test_sort_fragments()

# test_extract_fragments()

# Call the function with the test HTML content
# remaining_content, extracted_fragments = get_fragments(test_html_content)

# # Print the results
# print("Remaining Content:")
# print(remaining_content)
# print("\nExtracted Fragments:")
# for fragment in extracted_fragments:`
#     print(str(fragment), "\n")

# if __name__ == "__main__":

#         # Test HTML content
#     from ..encode.html_snippets import test_html_content 
#     # Assuming find_fragments function is defined as above
#     def test_find_fragments():
#         fragments = find_fragments(test_html_content)
#         print(f"Found fragments: {fragments}")
#         # assert len(fragments) > 0, "Should find at least one fragment"


#     # Assuming sort_fragments function is defined as above
#     def test_sort_fragments():
#         fragments = find_fragments(test_html_content)
#         sorted_fragments = sort_fragments(fragments)
#         print(f"Sorted fragments: {sorted_fragments}")
#         # assert sorted_fragments, "Should return a non-empty list"


#     # Assuming extract_fragments function is defined as above
#     def test_extract_fragments():
#         soup = BeautifulSoup(test_html_content, 'html.parser')
#         fragments = find_fragments(test_html_content)
#         sorted_fragments = sort_fragments(fragments)
#         extracted_fragments = extract_fragments( sorted_fragments)
#         canonical_frags = [ (frag,path, md_soup(frag)) for (frag, path) in extracted_fragments ]

#         # print(f"Remaining content: {remaining_content}")
#         print(f"Extracted fragments: {canonical_frags}")
#         # assert extracted_fragments, "Should have extracted fragments"
#         # assert remaining_content, "Should have remaining content"

#     test_extract_fragments()