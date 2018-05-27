import pandas as pd
book_details=pd.read_csv('books.csv')
book_tags=pd.read_csv('book_tags.csv')
tag_details=pd.read_csv('tag.csv')


book_details=book_details.dropna(how='any')
book_tags=book_tags.loc[book_tags['goodreads_book_id'].isin(book_details['book_id'])]

#get all the book_ids and tags_ids based on max count
book_tags=book_tags.loc[book_tags.groupby(['goodreads_book_id'])['count'].idxmax()]   

Tags=tag_details.loc[tag_details['tag_id'].isin(book_tags['tag_id'])]

list_genres=Tags.drop_duplicates(subset=['tag_name'],keep='first')




#get the book details corresponding to author whose name is as given Suzanne Collins1, Stephenie Meyer0,John Green2
author="F. Scott Fitzgerald"
author_books=book_details.loc[book_details['authors'] ==author]

#get the book id's who has average rating less than 4 within that bookids
low_rated_books=author_books.loc[author_books['average_rating'] <4.0,'book_id']

if low_rated_books.shape[0]>0:
   

    low_rated_genre=book_tags.loc[book_tags['goodreads_book_id'].isin(low_rated_books)]
    book_genre=Tags.loc[Tags['tag_id'].isin(low_rated_genre['tag_id'])]
    
    #stores the list of all book_ids that are rated maximum in their respetive genres
    max_rated={}
    max_rated = pd.DataFrame(columns =  ["Genre", "Title", "Rating"])

    count=0;
   
    for genre in set(book_genre['tag_name']):
        tag_det=Tags.loc[Tags['tag_name']==genre]
    
        #get all the rows from goodreads_book_id.csv which is equal to given tag_ids
        books=book_tags.loc[book_tags['tag_id'].isin(tag_det['tag_id'])]
    
        #get the book details from books.csv that corresponds to those bookids that belong to same group 
        booksofgenre=book_details.loc[book_details['book_id'].isin(books['goodreads_book_id'])]
    
        #find the rows whose average rating is equal to max of all the ratings
        sortedbooks= booksofgenre.sort_values(['average_rating'], ascending=[False])
        
        flag=0;
        for index,row in sortedbooks.iterrows():
            title=row['original_title']
            rating=row['average_rating']
            if rating>=4:
                max_rated.loc[count]=[genre,title,rating]
                count=count+1
            flag=flag+1
            if flag==5:
                break
else:
    print("Congrats!!You have all your books rated above 4")

