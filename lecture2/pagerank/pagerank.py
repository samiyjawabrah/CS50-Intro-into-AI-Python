import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    # ranks = iterate_pagerank(corpus, DAMPING)
    # print(f"PageRank Results from Iteration")
    # for page in sorted(ranks):
    #     print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    dictionary = {}

    links = corpus.get(page)

    n = len(links)

    if n == 0:

        m = len(corpus)

        for link in corpus:

            dictionary[link] = 1/m

            return dictionary
        
    surfer_page_prob = (1-damping_factor)/(n+1)

    other_page_prob = (damping_factor/n) + surfer_page_prob

    dictionary[page] = surfer_page_prob

    for link in links:

        dictionary[link] = other_page_prob

    return dictionary


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    sample = 0
    dictionary = {page:0 for page in corpus}
    cur_page = random.choice(list(corpus))

    while sample < n:

        dictionary[cur_page] += 1

        if not corpus[cur_page]:

            cur_page = random.choice(list(corpus))

        else: 
            transition_prob = transition_model(corpus, cur_page, damping_factor)
            
            weighted_list = []
            for key, value in transition_prob.items():


                multiply_by = round((value*100))

                new_list = [key]*multiply_by

                weighted_list.extend(new_list)
            

            cur_page = random.choice(weighted_list)

        sample += 1

    dictionary = {page: count/n for page,count in dictionary.items()}

    return dictionary

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
  