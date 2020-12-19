# import requests

# url":"https://onefilescrapedbucket.s3.amazonaws.com/sample.txt"

# url = "https://aylien-text.p.rapidapi.com/extract"

# # querystring = {"url":"https://towardsdatascience.com/how-to-deploy-a-streamlit-app-using-an-amazon-free-ec2-instance-416a41f69dc3"}
# querystring = {"url":"https://onefilescrapedbucket.s3.amazonaws.com/sample.txt"}
# # querystring = " a good data scientist needs to have a fair bit of knowledge of web frameworks to get along.And Web frameworks are hard to learn. I still get confused in all that HTML, CSS, and Javascript with all the hit and trials, for something seemingly simple to do. Not to mention the many ways to do the same thing, making it confusing for us data science folks for whom web development is a secondary skill. This is where StreamLit comes in and delivers on its promise to create web apps just using Python. In my last post on Streamlit, I talked about how to write Web apps using simple Python for Data Scientists. But still, a major complaint, if you would check out the comment section of that post, was regarding the inability to deploy Streamlit apps over the web. And it was a valid complaint."
# headers = {
#     'x-rapidapi-key': "71bc212db5mshc4194f3139b5410p14d0e4jsn1d89d35f8c32",
#     'x-rapidapi-host': "aylien-text.p.rapidapi.com"
#     }

# response = requests.request("GET", url, headers=headers, params=querystring)
# print(response.text)


import requests

url = "https://news-summarizer.p.rapidapi.com/summarize"

payload = "{\r\n    \"input_link\": \"\",\r\n    \"input_text\": \"  A Magna business damaged by a 5.7 magnitude earthquake last month has reopened.  Colosimos Market & Sausage Factory was forced to close for a month. Saturday, the business opened its doors to a line of waiting customers.  It feels great. It feels great, said Danny Colosimo, a member of the family that has owned the business for nearly a century. I had faith we would be back at some point.  Back in March, bricks fell from a wall of the building, leaving a gaping hole.  The inside weathered the earthquake well, Colosimo said. The damage is on the wall. We lost a few bricks, but its nothing that cant be fixed and nothing that we cant overcome.  Longtime customers are happy this family business has recovered, bringing some normalcy back to the town rattled by hundreds of quakes since the 5.7.  My kids love the spaghetti sauce that I make. I only use the sausage from here, said Tiffany Simons from Magna who was waiting in line before the store opened at noon. It shows you just how big a part of our community they are.  After being open for three hours Saturday, Colosimo expects the business to return to normal operating hours by Thursday.  God willing, we dont have any more of those big ones [earthquakes] and we will be here to stay, Colosimo said.   \"\r\n}"
headers = {
    'content-type': "application/json",
    'x-rapidapi-key': "71bc212db5mshc4194f3139b5410p14d0e4jsn1d89d35f8c32",
    'x-rapidapi-host': "news-summarizer.p.rapidapi.com"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)