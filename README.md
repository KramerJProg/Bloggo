![image](https://github.com/KramerJProg/Bloggo/assets/72529822/b4c25c14-0dcf-4877-bc8b-c45d32a885a5)
<hr>

## This is a project I created to show case my skills in building a full stack web application using Python, Flask, SQLAlchemy, and much more!

<p>This is a project I mostly started from scratch (minus the css which is a template I got from https://startbootstrap.com/). 
  I mostly wanted to show case my logic and code for this project. I have other projects that show case CSS if desired. 
  Here I will add short clips demonstrating the application with full functionality.</p>

### Home Page

![HomePage](https://github.com/KramerJProg/Bloggo/assets/72529822/98f56cff-6842-4f2b-a746-833b943a9152)

<p>This is the Home Page when visiting the site. It will have Nav Bar with options for guests to interact with.
 Anonymous users can go read the blogs created but are unable to leave comments at the end of the posts.
 Register an account by navigating to the Register tab at the top-right of the page and fill ou the form.</p>
<hr>

### Register Account

![Register1](https://github.com/KramerJProg/Bloggo/assets/72529822/11e71d65-a470-427f-9126-f04c8013f249)

<p>This is the Register Page. You will notice the form to register your account has validation. I simply use Flask Forms / wtforms 
  with their built in validators. All fields must have input in order for the form to be submitted successfully. The Email field
 also must be a valid email input, in other words it is looking for the yourEmail@something.com format.</p>

![Register2Email](https://github.com/KramerJProg/Bloggo/assets/72529822/368a4bef-6fdc-4c6a-afb8-22260e15d92f)

<p>When the register form is successfully submitted you will be brought to the Home Page and will be logged in with a greeting at 
 the top of the page!</p>

 ![Register3](https://github.com/KramerJProg/Bloggo/assets/72529822/42935729-9e80-4fd3-af29-e5c6d5bc8f8d)
<hr>

### User Comments

![Comment1](https://github.com/KramerJProg/Bloggo/assets/72529822/8ec816db-e901-4d70-a982-64aab9767fcc)

<p>As a registered (and logged in) user, you will be able to leave comments on the blog posts for the author or other users.
 When leaving a comment it should bring you back down to the comment section upon submission of the comment for you to see.</p>

 ![Comment2](https://github.com/KramerJProg/Bloggo/assets/72529822/79e2f804-22a7-4dac-8424-35f3c8032438)

<p>Now you can see you will be able to ONLY delete the comment that you posted. Delete action with the 'x'.</p>

![Comment3Delete](https://github.com/KramerJProg/Bloggo/assets/72529822/42e5503b-5eb8-4332-aedd-9aab16ccc103)
<hr>

### Logout / Login

![Logout](https://github.com/KramerJProg/Bloggo/assets/72529822/559b2f57-6c0e-46d2-8549-558cc14cbf70)

<p>You can logout with one click to return to being an anonymous user. Lets look at the Login Page. You will notice it won't be submitted with empty fields.</p>

![LoginAuth](https://github.com/KramerJProg/Bloggo/assets/72529822/17281d81-31fb-47d7-86cf-8c37e7b65352)

<p>If you get the Email OR Password wrong, it will give the error message, "Email or Password is incorrect. Please try again." just to keep it harder to narrow down credentials. Now lets log in.</p>

![Login](https://github.com/KramerJProg/Bloggo/assets/72529822/b6a4e560-e4f9-49ce-97f8-729ab5f28d9f)
<hr>

## Thank you so much for checking out my project! Always learning. Always Coding. Always Improving.
