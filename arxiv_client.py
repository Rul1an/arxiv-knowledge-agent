import requests
import xml.etree.ElementTree as ET

ARXIV_API_URL = "http://export.arxiv.org/api/query"

def fetch_arxiv_papers(query: str, max_results: int = 3) -> str:
    """
    Fetches paper summaries from the Arxiv API based on a query.

    Args:
        query: The search term for Arxiv.
        max_results: The maximum number of results to return.

    Returns:
        A formatted string containing the titles and summaries of the papers,
        or an error message if the request fails or no papers are found.
    """
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results
    }
    try:
        response = requests.get(ARXIV_API_URL, params=params, timeout=10) # Added timeout
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        root = ET.fromstring(response.content)
        namespace = {'atom': 'http://www.w3.org/2005/Atom'} # Atom feed namespace
        entries = root.findall('atom:entry', namespace)

        if not entries:
            return "No papers found on Arxiv for this query."

        output_lines = []
        for i, entry in enumerate(entries):
            title = entry.find('atom:title', namespace).text.strip()
            summary = entry.find('atom:summary', namespace).text.strip()
            # Clean up whitespace and newlines in title and summary
            cleaned_title = ' '.join(title.split())
            cleaned_summary = ' '.join(summary.split())
            output_lines.append(f"Paper {i+1}: {cleaned_title}\nAbstract: {cleaned_summary}")

        return "\n\n".join(output_lines)

    except requests.exceptions.RequestException as e:
        print(f"Error during Arxiv API request: {e}")
        return f"Error fetching data from Arxiv: {e}"
    except ET.ParseError as e:
        print(f"Error parsing Arxiv XML response: {e}")
        return "Error parsing the response from Arxiv."
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred in fetch_arxiv_papers: {e}")
        return "An unexpected error occurred while fetching from Arxiv."

# Example usage (for testing this module directly)
if __name__ == '__main__':
    test_query = "quantum machine learning"
    print(f"Testing Arxiv client with query: '{test_query}'")
    results = fetch_arxiv_papers(test_query)
    print("Results:\n")
    print(results)