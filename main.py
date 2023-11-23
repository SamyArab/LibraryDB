import requests
import json

#main loop 
count = 0
while (count < 100):
    
    url = "https://openlibrary.org/random"
    temp = requests.get(url)

    temp2 = temp.url.split("https://openlibrary.org/books/")

    temp3 = temp2[1].split('/')
    workID = temp3[0]


    website = requests.get("https://openlibrary.org/books/{}.json".format(workID))
    json = website.json()

    #ISBN
    run = True
    while(run):
        if (json.get("lccn") is not None):
            isbn = json['lccn']
            run = False
            break
        elif (json.get("isbn_13") is not None):
            isbn = json['isbn_13']
            run = False
            break
        elif (json.get("isbn_10") is not None):
            isbn = json['isbn_10']
            run = False
            break
        else:
            isbn = -1
            run = False
    
    
    #stops if the book doesn't have an ISBN
    if (isbn == -1):
        continue


    print("BOOK #{}".format(count+1))
    print("WORK ID: " + workID)

    print("ISBN: " + isbn[0])



    #title
    if (json.get("title") is not None):
        title = json['title']
    else:
        title = 'null'
    print("TITLE: " + title)

    #number of pages
    if (json.get("number_of_pages") is not None):
        pages = json['number_of_pages']
    else:
        pages = 'null'

    print('PAGES:', pages)

    #country of publication
    if (json.get("publish_country") is not None):
        country = json['publish_country']
    else:
        country = 'null'
    print('COUNTRY: ' + country)

    #language
    if (json.get("languages") is not None):
        temp =  str(json['languages'][0])
        temp2 = temp.split('/')
        temp3 = temp2[2].split("'")
        language = temp3[0]
    else:
        language = 'null'
    print('LANGUAGE:', language)

    #publishing date
    if (json.get("publish_date") is not None):
        date = json['publish_date']
    else:
        date = 'null'
    print('DATE:', date)

    #author id and name
    if (json.get("authors") is not None):
        temp = str(json['authors'][0])
        temp2 = temp.split('/')
        temp3 = temp2[2].split("'")
        authorID = temp3[0]

        author_website = requests.get("https://openlibrary.org/authors/{}.json".format(authorID))
        json_author = author_website.json()

        author = json_author['name']
    else:
        authorID = 'null'
        author = 'null'
    print('AUTHOR ID:', authorID)
    print('AUTHOR :', author)

    #subjects (comes in an array)
    if (json.get("subjects") is not None):
        subjects = json['subjects']
    else:
        subjects = 'null'
    print('SUBJECTS:', subjects)


    #insert prompt to be written into a text file
    book = "INSERT INTO Books (ISBN, title, publish_date, language, num_page)" + "\nVALUES({isbn}, {title}, {publish_date}, {author}, {country}, {language}, {num_page}, {subjects});".format(
                        isbn = isbn[0], 
                        title = title,
                        publish_date = date,
                        author = author,
                        country = country,
                        language = language,
                        num_page = pages,
                        subjects = subjects
            ).replace("'", "''")
    print(book)
    
    f = open("books2.sql", "a")
    f.write("--book#{}\n".format(count+1) + book + "\n")
    f.close()

    print("\n\n")
    count = count + 1


