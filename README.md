[![GitHub stars](https://img.shields.io/github/stars/nwjun/fopShowcase.svg?style=social&label=Stars&style=plastic)]() [![GitHub watchers](https://img.shields.io/github/watchers/nwjun/fopShowcase.svg?style=social&label=Watch&style=plastic)]() [![GitHub forks](https://img.shields.io/github/forks/nwjun/fopShowcase.svg?style=social&label=Fork&style=plastic)]()
[![GitHub license](https://badgen.net/github/license/nwjun/fopShowcase)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE) [![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://opensource.org/)
# :pushpin: Table of Contents
- [:pushpin: Table of Contents](#pushpin-table-of-contents)
- [:paperclip: Description](#paperclip-description)
- [:bulb: Inspiration](#bulb-inspiration)
- [:oncoming_automobile: RoadMap](#oncoming_automobile-roadmap)
- [:star2: Features](#star2-features)
- [:wrench: Tools & Technologies](#wrench-tools--technologies)
- [:exploding_head: Problems and Solutions](#exploding_head-problems-and-solutions)
  - [:bomb: CORS Issue](#bomb-cors-issue)
    - [What Is CORS](#what-is-cors)
    - [How It Happens](#how-it-happens)
    - [Solution](#solution)
  - [:bomb: Firebase Credential](#bomb-firebase-credential)
    - [Solution](#solution-1)
  - [:bomb: Layout](#bomb-layout)
    - [Solution](#solution-2)
- [:thought_balloon: Thoughts](#thought_balloon-thoughts)

# :paperclip: Description 
A website created using Flask, Bootstrap and firestore that allows Year 1 CS students from University of Malaya to showcase their FOP group project

# :bulb: Inspiration 
I am a CS student from University of Malaysia. In our first sem, we are required to take Fundamental of Programming (FOP). In this course, we need to form a team of 5 and each of the team is assigned to 1 of 5 projects. And because of the Covid-19, the presentation will be held online and we have no chance to see how the other teams do their projects :sob:. So I thought: why don't I make a website for students to upload their projects and the others to see it? I strongly believe that this will inspire and motivate each of us to improve our skills. And hopefully this will also give some inspiration for the future juniors. That's how I started this project. :sparkles:

# :oncoming_automobile: RoadMap
![Product RoadMap](https://i.imgur.com/ZR9ek4p.png)

# :star2: Features 
- Showing projects details in landing page
- Categorize all teams according to projects
- Showing team details
- Form for uploading team details
- Watching demo video in site

# :wrench: Tools & Technologies
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white) ![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white)  ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)  
![Firebase](https://img.shields.io/badge/firebase-%23039BE5.svg?style=for-the-badge&logo=firebase) ![Heroku](https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) 


# :exploding_head: Problems and Solutions 
## :bomb: CORS Issue
This happened when I was trying to validate github and youtube link by sending request on client side. 
### What Is CORS
From what I understood, CORS is HTTP-header based mechanism built in to browser that blocks all http requests from frontend to any url that is not in the same origin. [Read more about CORS](https://blog.container-solutions.com/a-guide-to-solving-those-mystifying-cors-issues)

### How It Happens
When we send request to server, the browser will first do security check via OPTIONS call. In the response header, the server will state who are allowed to access in 'Access-Control-Allow-Origin' in header. So in my case, when I request to github, it doesn't allow me to access. To solve this, we have 2 options:
1. Ask the server manager to add CORS support 
2. Build a middleware

### Solution
First option is not applicable to me, so I have to use option 2. I came out with a way to pass this by making a detour to server side. Only at the server side I send GET request to github and youtube. Then, I send the response back to client side.


## :bomb: Firebase Credential
Ok for this, before deployment, I used JSON file for Google credential. But because I didnt push the credential to GitHub, my server was unable to access the file. As the result, I was not able to start the server (cz I am using firebase).

### Solution
First, I manually key in all the credential in JSON file into the environment variable in Heroku website. I downloaded dotenv and make a `.env` file to store my credentials. Then, before running any code, in `app.py`:
```python
# load from .env file to environment
load_dotenv()

ggl_data = {
    "type": environ.get('FIREBASE_SERVICE_TYPE'),
    "project_id": environ.get('FIREBASE_PROJECT_ID'),
    "private_key_id": environ.get('FIREBASE_PRIVATE_KEY_ID'),
    "private_key": environ.get('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
    "client_email": environ.get('FIREBASE_CLIENT_EMAIL'),
    "client_id": environ.get('FIREBASE_CLIENT_ID'),
    "auth_uri": environ.get('FIREBASE_AUTH_URI'),
    "token_uri": environ.get('FIREBASE_TOKEN_URI'),
    "auth_provider_x509_cert_url": environ.get('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
    "client_x509_cert_url": environ.get('FIREBASE_CLIENT_X509_CER_URL')
}

# compile ggl credential and convert to certificate
credentials = firebase_admin.credentials.Certificate(ggl_data)
# Use a service account
firebase_admin.initialize_app(credential=credentials)
```

## :bomb: Layout
When the content is shorter than the screen size, the footer will not appear at the bottom.

### Solution
Wrap all the content into a div and set it to flexbox with justify-content-between.
```html
<section id="content" class='d-flex justify-content-between flex-column' style="min-height: 100vh;">
    <div>
        body content here
    </div>
    <footer>
        footer here
    </footer>
</section>
```

# :thought_balloon: Thoughts 
Although I had learnt about basics of web dev 2 years before, I had forgotten most of the content HAHAAHA. And to be honest, before this, I could barely implement JS in my project! Through this project, I re-learnt most of it and now I can say I am more familiar with Flask, JS and Bootstrap than before (I never implemented Bootstrap in any of my project! This is the first one hehe!) I know all of this is just a piece of cake for some pros, but I still wanna give a round of applause to myself <img src="https://c.tenor.com/RQXil8hk5yYAAAAj/wael-tsar-clapping.gif" style="width:25px"> (Ok stop)  

Overall, this is what I learnt through this journey:zap:: 
- session in flask
- Styling with Bootstrap
- More familiar with JS and Flask
- url validation

If there's any bug or space for improvement, do contact me! I hope that it can be expanded to other batches as well! Just leave me a message in my email if you wanna upload your FOP projects even though you're not from batch 21/22. 
Thank you and <img src="https://c.tenor.com/bkSYOM6M9xEAAAAM/%E3%83%90%E3%82%A4%E3%83%90%E3%82%A4-%E6%89%8B%E3%82%92%E6%8C%AF%E3%82%8B.gif" style="width:50px">