# CS50’s Web Programming with Python and JavaScript


## Project 2. Commerce.


Design an eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”

### Specification


* *Models*: The application has four models: one for the users, one for auction listings, one for bids, and one for comments made on auction listings. 
* *Create Listing*: Users are able to visit a page to create a new listing. They will to specify a title for the listing, a text-based description, and what the starting bid should be. Users although can provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).
* *Active Listings Page*: The default route ("/") let users view all of the currently active auction listings. For each active listing, this page displays the title, description, current price, and photo (if one exists for the listing).
* *Listing Page*: Clicking on a listing takes users to a page specific to that listing. On that page, users can view all details about the listing, including the current price for the listing. 
* *Watchlist*: Users who are signed in can to visit a Watchlist page, which displays all of the listings that a user has added to his watchlist. Clicking on any of those listings takes the user to that listing’s page.
* *Categories*: Users can to visit a page that displays a list of all listing categories. Clicking on the name of any category takes the user to a page that displays all of the active listings in that category.
* *Django Admin Interface*: Via the Django admin interface, a site administrator can view, add, edit, and delete any listings, comments, and bids made on the site.


### To Run the App

Open your code editor and in terminal go to the folder where you copies the code and run the following commands:

```
python manage.py makemigrations
python manage.py migrate
```

Now you can run your server:

`python manage.py runserver`