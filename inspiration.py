
import pandas as pd
import requests
from datetime import date
from bs4 import BeautifulSoup
import random
import string
from urllib.parse import urljoin
import time
import logging
logger = logging.getLogger(__name__)


today = "{:%Y_%m_%d}".format(date.today())
MaxQuotes = 10
NumberofDigits = 1

def main():
    print("""Inspiration, an immersive motivational exercise.
By Robin McKinnie rbmckinnie@gmail.com
          
Who are some people who most inspire you? I have a sample of
    notable people to choose from here. 
    Let me know if any of them seem interesting, 
    and I'll share some of their wisdom.
          

    1 Booker T Washington
    2 Carol S Dweck
    3 Howard Thurman
    4 Kobe Bryant          
    5 Marshall B Rosenberg
    6 Robert Greene
    7 Tara Brach                  
    8 Timothy Gallwey
          
                    """)


    while True: # Main exercise loop set to true from start rather than with a "setter" variable

        numofQuotes = 1 ## set quote amount to 1, count against max quotes

        while numofQuotes <= MaxQuotes:
            ### set author to empty string in order to enter while loop
            # recieve based on author input
            # Store random quote person will 
            ## whle loop will continue calling until user puts in 3 digits in length where each is valid decimal
            author_choice = ""
            while len(author_choice) != NumberofDigits or not author_choice.isdigit():
                
                print("who from this list might you want to read from?")
                for key,author_name in name_dict.items():
                    print(f" {key}: {author_name}")
                
                author_choice = (input("> ")).lower()

                if author_choice not in author_dict:
                    print("Make sure you choice from this list. "
                            f"Please select a number 1-{len(author_dict)}")
                    try_again = input("Woud you like to try again? (Y/N) ")
                    if try_again.lower() != "y":
                        print("Leaving Author Selection...","Let's circle back to the top",sep="\n")
                        author_choice = "0"
                        """"exit author section with BREAK"""
                        break
                """exit outer loop"""
                if author_choice == "0":
                    break 
                
            print('Got it. this is Quote #{}'.format(numofQuotes))
            
            print()
            
            print("Give me just a moment to fetch a fresh one for you...")
            
            print()
            
            random_quote = return_random_quote(author=author_choice)

            print(random_quote)
            print()
            print("now.. lets take a moment to sit with this message:")
            print()
            initial_sleep = 2
            for pause in range(1,4):
                time.sleep(initial_sleep**pause)
                print("...."*initial_sleep**pause)
            
            numofQuotes += 1

            print()

            print('How was that? Would you like to hear another? (yes or no)')
            if not input('> ').lower().startswith('y'):
                live_session = False
                break
            else:
                live_session = True
        if live_session == False:
            break 
    print("Thanks for coming! \n I'll see you again next time.")

def flatten(xss):
    return [x for xs in xss for x in xs]

def create_link(extension):
    url_base = "https://www.azquotes.com/author/"
    url = url_base+extension
    return url

def return_soup_obj(url,max_retries=10,initial_delay=2,backoff_factor=2):

    """returns soup object from url passed as argument"""
    """retry mechanism for unsuccusful request"""
    """returns None when attempts exceed limit"""
    """keyword args for delay, backoff factor, max retries"""
    
    for attempt in range(max_retries):    

        try:
            r = requests.get(url)
            r.raise_for_status()
            soup = BeautifulSoup(r.content,'html.parser')
            return soup
        
        except requests.exceptions.RequestException as e:
            
            logger.info(f"error: {e}")
            print(f"Attempt {attempt+1} error: {e}")
            
            """ checks if retry threshold has been reached, 
            retries request if attempts still available"""

            if attempt < (max_retries - 1):
                delay = initial_delay * (backoff_factor ** attempt)  
                ## backoff factor raised to the nth power where n = attempt        
                print(f"Retrying request in {delay} seconds...")
                time.sleep(delay)
            else:
                """print/log when max retries exceeded"""
                print(f"Max retries reached for {url}")
                logger.info(f"Max retries reached for {url}")
                return None
            
def get_max_page_cnt(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    page_number = soup.select_one('div.pager > span')
    return page_number

def get_page_cnt(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    page_number = soup.select_one('div.pager > span')
    page_count = page_number.text.split('of ',1)[-1]
    return page_count


#TODO: STAGE KNOWN AUTHORS FOR SCRAPING
author_dict = {
"1" : '15322-Booker_T_Washington',
"2" : '19498-Carol_S_Dweck',
"3" : '14651-Howard_Thurman',
"4" : '2090-Kobe_Bryant',
"5" : '18421-Marshall_B_Rosenberg',
"6" : '19745-Robert-Greene',
"7" : '1769-Tara_Brach',
"8" : '22555-Timothy_Gallwey',
}
name_dict = { 
    "1": "Booker T Washington"      ,
    "2": "Carol S Dweck",
    "3": "Howard Thurman",
    "4": "Kobe Bryant",
    "5": "Marshall B Rosenberg",
    "6": "Robert Greene",
    "7": "Tara Brach",
    "8": "Timothy Gallwey"
}

default_author_list = ['1769-Tara_Brach','14651-Howard_Thurman','2090-Kobe_Bryant','18421-Marshall_B_Rosenberg','22555-Timothy_Gallwey','19498-Carol_S_Dweck','19745-Robert-Greene','15322-Booker_T_Washington']

def pull_pages(author_list):

    url_list = [create_link(ext) for ext in author_list]

    page_list = [get_page_cnt(url) for url in url_list]

    return page_list

def pull_all_quotes_by_author(item,format="list",max_retries=10,initial_delay=.5,backoff_factor=2):

    """retrieves soup objects by author, processes, returns
      1-dimensional list of quotes attributed to author"""

    root_url = create_link(item)

    page_parameter_str= "?p="
    
    """checks url for total page count, 
    paginates when count is greater than 1"""
    
    try:
        
        page_count = int(get_max_page_cnt(url=root_url).text.split()[-1])

    except AttributeError:
        
        page_count = 1

    """compile list of author urls 
    if more than one page exists"""
    author_page_list = []
    for i in range(page_count):
        url = root_url+page_parameter_str+str(i+1) 
        author_page_list.append(url)
    
    author_soup_list =[]

    """check pages, retry if return soup obj fails"""
    for num,url in enumerate(author_page_list):
        for attempt in range(max_retries):    
            try:
                author_soup = return_soup_obj(url)
                if author_soup is not None:
                    author_soup_list.append(author_soup)
                
            except requests.RequestException as e:
                print(f"Attempt number {attempt+1}")
                print(f"""error when loading url for page {num}""")
                logger.info(f"""error when loading url for page {num} for attempt {attempt+1}""")
                if attempt < (max_retries - 1):
                    delay = initial_delay * (backoff_factor ** attempt)  
                    ## backoff factor raised to the nth power where n = attempt        
                    print(f"Retrying request in {delay} seconds...")
                    time.sleep(delay)
                else:
                    """print/log when max retries exceeded"""
                    print(f"Max retries reached for {url}")
                    logger.info(f"Max retries reached for {url}")
                

    found_obj_list = [soup.find_all("a", class_="title") for soup in author_soup_list]

    flat_list = flatten(found_obj_list)


    if format == "list":
        
        quote_list = ['"'+row.text +'" -'+row['data-author'] for row in flat_list]
        
        return quote_list
    
    elif format == "dataframe":
        
        author = [i['data-author'] for i in flat_list][0]
        
        keys = [i['href'] for i in flat_list]
        
        values = [i.text for i in flat_list]
        
        url_list = [str('https://www.azquotes.com')+str(i) for i in keys]

        result_dict = {'Author': author, 'Quote-ID': keys, 'Text' : values, 'Author-Header' : item, 'url' : url_list }

        quote_df = pd.DataFrame(result_dict)
        
        return quote_df


def pull_all_quotes_for_random_author(main_list=default_author_list):

    random_author = random.choice(main_list)

    return pull_all_quotes_by_author(random_author)


def return_random_quote(author=None):

    if author:
        if author in author_dict:
            author_web_code = author_dict[author]

        # take 1 out of author choice to index at proper location
#        author_web_code = main_list[int(author) - 1]

            all_quotes = pull_all_quotes_by_author(author_web_code)

            quote = ""

            if len(all_quotes) > 0:

                quote = random.choice(all_quotes)

            return quote
        else:
            print("That author's name might not be in this list.")

            raise ValueError
    
    author_list = list(author_dict.values())

    quote = random.choice([q for q in pull_all_quotes_for_random_author(main_list=author_list)])

    return quote


# if the program is run (instead of imported), run the exercise: 
if __name__ == '__main__':
    main()




