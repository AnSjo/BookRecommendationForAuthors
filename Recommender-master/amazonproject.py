import pandas as pd
book_details=pd.read_csv('books.csv')
book_tags=pd.read_csv('book_tags.csv')
tag_details=pd.read_csv('tag.csv')


def isAscii(string):
    return reduce(operator.and_,[ord(x)<256 for x in string],True)

tag_details=tag_details[tag_details.tag_name.apply(lambda x: isAscii(x))]

book_details=book_details.dropna(how='any')
book_tags=book_tags.loc[book_tags['goodreads_book_id'].isin(book_details['book_id'])]


#get all the book_ids and tags_ids based on max count
book_tags=book_tags.loc[book_tags.groupby(['goodreads_book_id'])['count'].idxmax()]   

Tags=tag_details.loc[tag_details['tag_id'].isin(book_tags['tag_id'])]

list_genres=Tags.drop_duplicates(subset=['tag_name'],keep='first')




#get the book details corresponding to author where name is provided by user F. Scott Fitzgerald,Suzanne Collins1, Stephenie Meyer0,John Green2

author=input("Enter author name: \n")  
author_books=book_details.loc[book_details['authors'] ==author]

#get the book id's who has average rating less than 4 within that bookids
low_rated_books=author_books.loc[author_books['average_rating'] <4.0]


author_book_det=pd.DataFrame(columns =  ["Genre", "Title","Rating"])


count=0
for index,row in low_rated_books.iterrows():
            title=row['original_title']
            rating=row['average_rating']
            genre_det=book_tags.loc[book_tags['goodreads_book_id']==row['book_id']]
            genre_name=Tags.loc[Tags['tag_id']==genre_det.iloc[0,1]]
            genre=genre_name.iloc[0,1]
            author_book_det.loc[count]=[genre,title,rating]
            count=count+1
            
print(author_book_det)

if low_rated_books.shape[0]>0:
   

    low_rated_genre=book_tags.loc[book_tags['goodreads_book_id'].isin(low_rated_books['book_id'])]
    
    
    
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
    
    print(max_rated)
else:
    print("CongratZ!!You have all your books rated above 4")
    
    
    
import matplotlib.pyplot as plt

print("Books written by author \n")
#get the book id's who has average rating greater than 3 within that bookids
print("\nBooks written by author: %s \n" % (author))
#get the book id's who has average rating greater than 3.8 within that bookids
ans1=author_books.loc[author_books['average_rating'] <3.8,['book_id','title','average_rating']]
ans2=author_books.loc[author_books['average_rating'] >3.8,['book_id','title','average_rating']]
print("Average selling books \n")
print(ans1)
print("Best selling books \n")
print(ans2)


ax=ans2[['average_rating','title']].plot(kind='bar', title="Average rating",figsize=(15,10),
       legend=True,fontsize=12)
ax.set_xlabel("Title",fontsize=12)
ax.set_ylabel("Rating",fontsize=12)
plt.show()
#get x values for graph
x_labels1=ans1['title']
x_labels2=ans2['title']

#get y values for graph
y_labels1=ans1['average_rating']
y_labels2=ans2['average_rating']

print("Best selling books: \n")
print(ans2,"\n")
print("Other books: \n")
print(ans1,"\n")


plt.bar(x_labels2, y_labels2, color='green', align='center', label='Best selling books')
plt.bar(x_labels1, y_labels1, color='blue', align='center', label='Other books')
plt.title('Graph to show ratings of all books')
plt.legend()
plt.xticks(rotation=90)
plt.show()

    

