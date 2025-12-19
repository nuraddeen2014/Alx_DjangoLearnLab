- *Authentication guide*
- user access the register endpoint @ POST /api/register with username, password and email
- After succesful registration, a token would be generated in the response header
- The token would be used to access the profile @ GET api/profile
- Already registered users can get their token @ POST api/login
- Credentials for login are username and password

- Example register in postman:

Method = POST

Body(JSON)

{
    'username':'Type your username here',
    'password':'Type your password here',
    'email':'Type your email here',
}
# You can also consider accessing the /register endpoint on your browser.It returns your token

- Example login in postman:

Method = POST

{
    'username':'your_username',
    'password':'your_password',
}
# And that's all, you get a successful response with your token and a 403 error if user not exist

- Example profile view in postman:

Method = GET

Header

Type - Authentication     Key - Token bhdfjbvzcxvznnm
# That is absolutely not a token just a sample. Don't forget to type the 'Token ' before pasting your token. In words, type Token leave a space and paste your token. Super easy!