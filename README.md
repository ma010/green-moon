# Web App: green-moon
This is a web app used to be hosted on a [Linode](https://www.linode.com) server with the following architecture.


![alt text](./img/architecture.jpeg)

#### The app's structure is sketched below:
```
/green-moon
    db_init.py
    run.py
    /GreenMoon
        __init__.py  # App's initialization
        config.py  # Configure database settings
        views.py  # Implement views/pages and their routing
        models.py  # Declare functions that interact with the database
        /static
            /css
            /js
                license.js  # Implement interactive component and asyncrhonous calls to the database
            ...
        /templates
            base.html  # Jinjia2 template engine for Python
            index.html
            login.html
            license.html # 
            ...
        /tmp
            zipcode_boundary.geojson

```

#### Features implemented through this web app
* Analyze business license data from Chicago ([Open Data Portal](https://data.cityofchicago.org)) and visualize them on 
a map with zipcode boundaries. A user can search or hover the mouse over to discover frequently associated business 
entities in a neighborhood.
* Visualize sentiment analysis of twitter data
* Host results from a data science project on bike sharing in Chicago

#### A screen-shot of the front page.
![alt text](./img/GreenMoon.jpg)