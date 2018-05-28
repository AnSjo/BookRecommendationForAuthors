#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 23 19:57:49 2018

@author: anurita
"""

import pandas as pd
dt=pd.read_csv('ratings.csv')
book_details=pd.read_csv('books.csv')
book_tags=pd.read_csv('book_tags.csv')
tag_details=pd.read_csv('tags.csv')

book_details=book_details.dropna(how='any')
book_tags=book_tags.loc[book_tags['goodreads_book_id'].isin(book_details['book_id'])]
x1=dt.drop_duplicates(subset=['book_id','user_id'],keep='first')

author=input("Enter author name: \n")  

#get the book details corresponding to author whose name is as given
x2=book_details.loc[book_details['authors'] == author]

print("\nBooks written by author: %s \n" % (author))
#get the book id's who has average rating greater than 3.8 within that bookids
ans1=x2.loc[x2['average_rating'] <3.8,['book_id','title','average_rating']]
ans2=x2.loc[x2['average_rating'] >3.8,['book_id','title','average_rating']]

#get x values for graph
x_labels1=ans1['title']
x_labels2=ans2['title']

#get y values for graph
y_labels1=ans1['average_rating']
y_labels2=ans2['average_rating']

#print output
print("Best selling books: \n")
print(ans2,"\n")
print("Other books: \n")
print(ans1,"\n")

import matplotlib.pyplot as plt
plt.bar(x_labels2, y_labels2, color='green', align='center', label='Best selling books')
plt.bar(x_labels1, y_labels1, color='blue', align='center', label='Other books')
plt.title('Graph to show ratings of all books')
plt.legend()
plt.xticks(rotation=90)
plt.show()



