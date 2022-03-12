# Capstone One: Step Two - Write a Project Proposal
For my Capstone One project, I want to create a **Weather App** since the weather is something that greatly affects our lives and it's something that we have to deal with all over the world.

### Weather-or-Not
*Here I come...?*

***

**1. What goal will your website be designed to achieve?**

- The goal is to display weather forecasts around the world and to give the user the ability to create and customize tabs for different cities, and/or preferences on what the user sees when first visiting the website. For example, I want to customize a tab to see Seattle, Washington's weather based on a 7-day forecast, as opposed to a morning, afternoon, or even breakdown, and I want to toggle the temperature unit from Fahrenheit to Celsius.


**2. What kind of users will visit your site? In other words, what is the demographic of your users?**

- Anyone who is interested in finding out about what the weather forecast will be for that day or upcoming week. As a person who checks the weather everyday, I would assume the user is wanting to travel, or has a long commute to work or to a desired location, city, or Country. The demographic would be anyone between 18 years old and up. There is a possibility that most of the users are female users.

**3. What data do you plan on using? You may have not picked your actual API yet, which is fine, just outline what kind of data you would like to contain.**

- The Weather API I want to use on my website is [Open Weather Map API] (https://openweathermap.org/api). I want to the current weather data or a One Call API (get current, forecase, and historical weather data).

**4. In brief, outline your approach to creating your project (knowing that you may not**
know everything in advance and that these details might change later). Answer
questions like the ones below, but feel free to add more information:

- **What does your database schema look like?**
    - User Preferences (i.e. temperature unit from Fahrenheit to Celsius)
    - User Profiles (i.e. user's current location, other cities to save, country)
    - Weather Logs (i.e. date, temperature, city, etc.)
- **What kinds of issues might you run into with your API?**
    - Inaccurate information
    - This might be very unlikely, but if the API I'm using has a rate limit, and I've reached a limit on sending requests.
- **Is there any sensitive information you need to secure?**
    - The user's password and the API's access key.
- **What functionality will your app include?**
    - Search (Search by city, Country, etc.)
    - Add user preferences and profiles
- **What will the user flow look like?**
    - Users who do not have a profile set-up will have limited access to customizing their preferences and the website. For someone who wants to use the default settings of the website, they will still have access to the database search function, but they will have to input a city/location every time.
- **What features make your site more than CRUD? Do you have any stretch**
    goals?
    - The search interface, creating multi-user and user session, edit/add/delete locations or forecasts, customize profiles and user preferences. Goals is to make a simple, user-friendly weather app with lots of design features that stick out to other weather applications. A stretch goal I want to *try* and accomplish in my Capstone Project #1 is to find a way to send a reset password to the user's email that they registered with.
`