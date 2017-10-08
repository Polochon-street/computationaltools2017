from lxml import etree
import regex
import time
import mmap

# All the validation queries
test_patterns = [
    [
        ('cat', [0, 10], 'are', [0, 10], 'to'),
        ('cat', [0, 100], 'anatomy'),
        ('china', [30, 150], 'washington'),
        ('english', [0, 200], 'cat'),
        ['kitten', [15, 85], 'cat', [0, 100], 'sire', [0, 200], 'oxford'],
    ],
    [
        ('arnold', [0, 10], 'schwarzenegger', [0, 10], 'is'),
        ('apache', [0, 100], 'software'),
        ('aarhus', [30, 150], 'denmark'),
        ('english', [0, 100], 'alphabet'),
        (
            'first', [0, 85], 'letter', [0, 100], 'alphabet', [0, 200],
            'consonant',
        ),
    ],
    [
        ('elephants', [0, 20], 'are', [0, 20], 'to'),
        ('technical', [0, 20], 'university', [0, 20], 'denmark'),
        (
            'testing', [0, 20], 'with', [0, 20], 'a', [0, 30], 'lot', [0, 4],
            'of', [0, 5], 'words',
        ),
        ('stress', [0, 250], 'test'),
        (
            'object', [10, 200], 'application', [0, 100], 'python', [10, 200],
            'system', [0, 100], 'computer', [0, 10], 'science', [0, 150], 'linux',
            [0, 200], 'ruby',
        ),
    ],
]

# The files where cleaned articles will be output
article_files = [
    'article_cat',
    'articles_a',
    'articles_all',
]


def get_text_and_clean(element):
    """
        Extract the full article text from element, and clean it.

        :param element: XML element
        :param output: The text string
    """
    # Find the revision associated to the article:
    # the full text is a child element of revision
    revision = element.find(
        '{http://www.mediawiki.org/xml/export-0.10/}revision',
    )
    # Find the actual article's text
    text = (
        revision
        .find('{http://www.mediawiki.org/xml/export-0.10/}text')
        .text
    )
    # Lowercase everything, replace newlines by spaces and
    # drop REDIRECT articles
    if text and '#REDIRECT' not in text:
        text = text.lower()
        text = regex.sub('[\n\r]+', ' ', text)
    else:
        text = ''
    return text

def output_clean_article(title, output):
    """
        Output a single article to a file.

        The output article will be in lower-case and single-lined.

        :param title: The title of the wanted article
        :param output: The name of the output file
        :type title: str
        :type output: str
        
    """
    with open(output, 'w') as f:
        # For all articles in the XML file
        for event,element in etree.iterparse(
            'articles.xml',
            tag='{http://www.mediawiki.org/xml/export-0.10/}page',
        ):
            # Check if the title matches
            if (
                element
                .find('{http://www.mediawiki.org/xml/export-0.10/}title')
                .text == title
            ):
                text = get_text_and_clean(element)
                # Append the cleaned content to the output file
                f.write(text)
                return
        # Cleaning everything else to avoid RAM overflow when itering
        # over articles
            element.clear()
        for ancestor in element.xpath('ancestor-or-self::*'):
            while ancestor.getprevious() is not None:
                del ancestor.getparent()[0]


def output_clean_articles_beginning_with_letter(title, output):
    """
        Output all articles beginning by a single letter to a file.

        The output articles will all be in lower-case and single-lined.

        :param title: The letter (or the beginning) of the wanted articles
        :param output: The name of the output file
        :type title: str
        :type output: str
        
    """
    with open(output, 'w') as f:
        # For all articles in the XML file
        for event,element in etree.iterparse(
            'articles.xml',
            tag='{http://www.mediawiki.org/xml/export-0.10/}page',
        ):
            # Check if the title matches, checking both uppercase and lowercase
            if (
                element
                .find('{http://www.mediawiki.org/xml/export-0.10/}title')
                .text.startswith(title.lower()) or
                element
                .find('{http://www.mediawiki.org/xml/export-0.10/}title')
                .text.startswith(title.upper())
            ):
                text = get_text_and_clean(element)
                # Append the cleaned content to the output file
                f.write(text)
        # Cleaning everything to avoid RAM overflow
            element.clear()
        for ancestor in element.xpath('ancestor-or-self::*'):
            while ancestor.getprevious() is not None:
                del ancestor.getparent()[0]


def output_clean_all_articles(output):
    """ 
        Output all articles to a file.

        The output articles will be all in lower-case and single-lined.
        :param output: The name of the output file
        :type output: str
    """
    with open(output, 'w') as f:
        # For all articles in the XML file
        for event,element in etree.iterparse(
            'articles.xml',
            tag='{http://www.mediawiki.org/xml/export-0.10/}page',
        ):
            text = get_text_and_clean(element)
            # Append the cleaned content to the output file
            f.write(text)
        # Cleaning everything to avoid RAM overflow
            element.clear()
        for ancestor in element.xpath('ancestor-or-self::*'):
            while ancestor.getprevious() is not None:
                del ancestor.getparent()[0]


def check_pattern(data, query):
    """
        Check if the query returns matching data.

        Run the query agains all the data, and return only matching data.
        :param data: The data to analyze
        :param query: The query, well-formatted (cf. assignment instructions)
        :type data: mmap.mmap
        :type query: a tuple like ('coucou', [0, 200], 'charlie')
    """
    # Will handle the query converted as a regex
    # The regex have this format: 'coucou.{0,200}charlie'
    # This looks for a string beginning with 'coucou', and with at most
    # 200 characters between the next 'charlie'
    regex_str = ''
    for element in query:
        # If the element is 'coucou' or 'charlie' for example
        if type(element) == str:
            regex_str += '{}'.format(element)
        # If the element is [0, 200] for example
        elif type(element) == list:
            regex_str += '.{{{},{}}}'.format(element[0],element[1])

    # Compile the regex into bytecode to make the search faster
    pattern = regex.compile(regex_str.encode())
    # The overlapped option matches only stuff that happens after
    # the start of the regex.
    # For example, matching 'A.{0,200}B' with string 'AxBxxAxxxB' with
    # 'overlapped' option will match ['AxBxxAxxxB', 'AxxxB'] but not
    # 'AxB'
    matches = pattern.findall(data, overlapped=True)
    final_matches = matches
    # Additional step to match the remaining 'AxB' values
    # We're removing the last matching bit and proceeding backwards
    # until there's no match. For example, it would try to match
    # 'A.{0,200}B' with 'AxBxxAxxx' which would match 'AxB' (because
    # we don't use the 'overlapped' option here), and then 'Ax' which
    # would lead to no further match.
    for match in matches:
        # Find the last string of the query and remove it from the match
        # e.g. replacing 'AxBxxAxxxB' by 'AxBxxAxxx'
        new_match = regex.sub((query[-1] + '$').encode(), ''.encode(), match)
        # Try to find a matching result against the new string
        found = regex.findall(regex_str.encode(), new_match)
        # If there's a match, continue doing the same until there's no more
        # match
        while found:
            # Add every new found match to the list of matches
            final_matches = final_matches + found
            # Find the last string of the query and remove it from the match
            # to find additional overlapping matches
            new_match = regex.sub(
                (query[-1] + '$').encode(),
                ''.encode(),
                found[0],
            )
            found = regex.findall(regex_str.encode(), new_match)
    return final_matches

# Output the cleaned files
output_clean_article('Cat', 'article_cat')
output_clean_articles_beginning_with_letter('A', 'articles_a')
output_clean_all_articles('all_articles')

# Test the solution against all the verification cases
for index, article_file in enumerate(article_files):
    with open(article_file, 'r+') as f:
        print('Articles {}'.format(article_file))
        # Use mmap to avoid reading the files in RAM but read them
        # directly on the disk
        data = mmap.mmap(f.fileno(), 0)
        # Actually test the matching patterns
        for pattern in test_patterns[index]:
            str_pattern = ''
            # Helper text to see where we are
            for elem in pattern:
                if type(elem) == list:
                    str_pattern += '[{},{}]'.format(elem[0], elem[1])
                else:
                    str_pattern += elem
            print('Pattern {}:'.format(str_pattern))
            # Measure the execution time of the matching
            exec_time = time.time()
            found = check_pattern(data, pattern)
            exec_time = time.time() - exec_time
            # Decode every match by running bytes.decode() against
            # all the elements of the found list
            found = list(map(bytes.decode, found))
            # Write down the results in a file
            with open('{}_{}'.format(str_pattern, article_file), 'w') as f:
                for item in found:
                    f.write('{}\n'.format(item))
            # Finally print the result
            print('{} matching patterns found, for an execution time of {:.4}s'.format(len(found), exec_time))
