from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import streamlit as st


url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue'
page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')

#get only values from first table
table = soup.find_all('table')[0]
content = str(table) #convert to strings

#specify what is needed to be search for the titles (skip the unnecessary th part and capture the strings with (.*?))
re_titles = r'<th>\s*(.*?)\s*</th>'
#used for extracting all the table titles
titles = re.findall(re_titles, content)
#when extracted there are some that contains unneeded values which is <br/>, replace it with ''
titles = [title.strip().replace('<br>', '').replace('<br/>', '') for title in titles]
# print(titles)

# re_names = r'<a [^>]*>(.*?)</a>'
# re_names = r'<a href=".*?" title=".*?">(.*?)</a>'

# re_values = r'<td style=".*?">([0-9,]{1,15})'
# re_percentage = r'<td[^>]*>\s*.*?(\d+\.\d+%)\s*</td>'
# values = re.findall(re_values, content)
# percent = re.findall(re_percentage, content)

#Combination of re_values and re_percentage, this specify all the numeric values in the table
re_combined = r'<td[^>]*>\s*.*?(-?[0-9,]{1,15}|-?\d+\.\d+%)\s*</td>'
#extract values for td which contains all the numeric values in the wiki table (Revenue, Revenue growth%, and Employees)
combine = re.findall(re_combined, content)
filtered_values = [
    match.strip()  # Clean up any leading/trailing whitespace
    for match in combine
    if not (match.isdigit() and len(match) >= 1)  # Exclude Rank digits (already has in sublists)
]
numberlist = [] 
for j in range(0, len(filtered_values), 3): #seperate all the values into a sub list with 3 values for each list
    numberlist.append(filtered_values[j:j + 3])

for index2, numlist in enumerate(numberlist): #test
    # print(f"{index2 +1}: {numlist}")
    continue
    
# print(filtered_values)
# names = re.findall(re_names, content)
# print(values)
# print(titles)
# print(names2)

sublists = []
#call the td values in the table with strings
re_td = r'<td>\s*(.*?)\s*</td>'
names2 = re.findall(re_td, content)
cleaned_matches = [re.sub(r'<.*?>', '', match).strip() for match in names2] #remove unnecessary parts and leave out wanted strings
# print(cleaned_matches)

for i in range(0, len(cleaned_matches), 4): #seperate into a sub lists with 4 values in each list
    sublists.append(cleaned_matches[i:i + 4])

for index, sublist in enumerate(sublists):
    # print(f"{index +1}: {sublist}")
    continue

combined_lists= [] 
for sublist, numlist in zip(sublists, numberlist): 
    combined = sublist[:3] + numlist + [sublist[3]] #conbine the 2 by putting onlt the first 3 values from sublists[] first then all values from numlists followed by last value of sublists
    combined_lists.append(combined)

for index3, combined in enumerate(combined_lists): #test
    # print(f"{index3 + 1}: {combined}")
    continue
# print(sublists)

#put into a dataframe
df = pd.DataFrame(combined_lists, columns=titles)
print(df)

#show in a webapplication with streamlit
st.dataframe(df)

