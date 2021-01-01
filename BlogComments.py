from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv

# specify the url
MainBlog = 'https://www.firstinspires.org/robotics/frc/blog'

# query the website and return the html to the variable ‘page’
page = urlopen(MainBlog)

soup = BeautifulSoup(page, 'html.parser')
blogwebpages =[]
blogs = soup.select('div.blogArticle.row')
for blog in blogs:
    Title = blog.find('h2').text.strip()
    test = blog.select('footer.articleFooter')[0]
    # print(test.find('a').attrs['href'])
    webpage = "https://www.firstinspires.org/" + test.find('a').attrs['href']
    blogwebpages.append(webpage)
# blogwebpages = ['https://www.firstinspires.org//robotics/frc/blog/2021-the-2021-judging-process']

headers = ["Title", "link", "comment submitter", "comment title", "comment content"]
rows = [headers]
for blog in blogwebpages:
    blogpage = urlopen(blog)
    BlogSoup = BeautifulSoup(blogpage, 'html.parser')
    comments = BlogSoup.select('div.comment')
    Title = BlogSoup.select('header.articleHeader > h2')[0].text.strip()
    row = []
    for comment in comments:
        try:
            CommentTitle = comment.find('a').text
            Commentcontent = comment.find_all('p')

            Submitter = comment.select('span.username')[0].text
            commentstring = ""

            for content in Commentcontent:
                commentstring = commentstring + " " + content.text
        except:
            Submitter = ""
            CommentTitle = ""
            commentstring = ""
        row = [Title, blog, Submitter, CommentTitle, commentstring]
        rows.append(row)

with open("BlogComments.csv", mode='w', newline='', encoding='utf-8') as file:
    file_writer = csv.writer(file)
    file_writer.writerows(rows)
# productids = []
# mydivs = soup.select('div.product-item')
#
# for link in mydivs:
#     productid = link.find('a').attrs['href']
#     productids.append(productid)
#
# headers = ["Webpage", "FC Part ID", "Item", "Description", "Source", "Source Part Number", "onhand", "onhold", "available", "Credits Price", "Max Qty"]
# rows = [headers]
# for id in productids:
#     print(id)
#     idurl = "https://firstchoicebyandymark.com" + id
#     productpage = urlopen(idurl)
#     idsoup = BeautifulSoup(productpage, 'html.parser')
#     try:
#         description = idsoup.p.string
#     except:
#         description = "NA"
#     try:
#         onhand = idsoup.select('div.stock.onhand > span.value')[0].string
#     except:
#         onhand = "NA"