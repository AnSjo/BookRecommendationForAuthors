import pandas as pd
dt1=pd.read_csv('ratings.csv')
dt2=pd.read_csv('books.csv')
dt3=pd.read_csv('book_tags.csv')
dt4=pd.read_csv('tags.csv')
dt5=pd.read_csv('to_read.csv')

#Removes duplicates
x1=dt1.drop_duplicates(subset=['book_id','user_id'],keep='first')

#contains all rows having author name as 'Suzanne Collins'
x2=dt2.loc[dt2['authors'] == 'Suzanne Collins']

#get all the book_ids and tags_ids based on max count
x11=dt3.loc[dt3.groupby(['goodreads_book_id'])['count'].idxmax()]   

#get the book id's who has average rating less than 4 within that bookids
x3=x2.loc[x2['average_rating'] <4.0,'book_id']

#get the tag_ids from to_read.csv which corresponds to the obtained id's(x3)
x4=x11.loc[x11['goodreads_book_id'].isin(x3)]


#stores the list of all book_ids that are rated maximum in their respetive genres
max_rated=[]

#iterate through each tag_ids  - set is used since multiple books may belong to same tagids
#which have rating less han 4 
for i in set(x4['tag_id']):
    #get all the rows from goodreads_book_id.csv which is equal to i
    x6=x11.loc[x11['tag_id'] ==i]
    
    #get the book details from books.csv that corresponds to those bookids that belong to same group 
    x7=dt2.loc[dt2['book_id'].isin(x6['goodreads_book_id'])]
    
    #find the rows whose average rating is equal to max of all the ratings
    x8=x7.loc[x7['average_rating']==x7['average_rating'].max()]
    
    max_rated.extend(x8['book_id'])
    
