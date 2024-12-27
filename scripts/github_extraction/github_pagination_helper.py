def extract_max_pages(str_link):
    """
    Returns the total number of pages (pages of last) of the string passed as an argument.
    Returns 1 if str_link is malformed or null.
    If github the response is paginated, the link header will look something like this:
    link = '<https://api.github.com/repositories/1300192/issues?page=2>; rel="prev", 
    <https://api.github.com/repositories/1300192/issues?page=4>; rel="next", 
    <https://api.github.com/repositories/1300192/issues?page=515>; rel="last", 
    <https://api.github.com/repositories/1300192/issues?page=1>; rel="first"'
    And this function return: [515, 'https://api.github.com/repositories/1300192/issues']
    """
    if str_link is None:
        return 1

    # Split by the comma character ','
    array_result = str_link.split(',')
    
    # Find the element containing the text 'rel="last"' in the array
    for element in array_result:
        if 'rel="last"' in element:
            element_last = element
            break
    else:
        # If 'rel="last"' is not found, return empty values
        return 1
    
    # Extract full URL
    url_start_index = element_last.find('<') + 1
    url_end_index = element_last.find('>', url_start_index)
    url = element_last[url_start_index:url_end_index]
    
    # Find the start of '?page='
    page_start_index = url.find('?page=') + len('?page=')
    
    # Finding the end of the numeric part of 'page'
    page_end_index = url.find('&', page_start_index)
    
    # Assuming there could be more parameters after 'page'
    page_end_index = page_end_index if page_end_index != -1 else len(url)
    
    # Extract page number and base URL
    page_number = int(url[page_start_index:page_end_index])
    
    return page_number