# Data Forecast Web App

This repository contains a web application for forecasting subscription data based on historical data. The app is built using Python, Gradio, and Facebook's Prophet library. It can be used as a learning resource to understand how to create forecasting models and visualize them using Gradio.

## Getting Started

To get started with the Subscription Forecast Web App, follow these steps:

### 1. Clone the repository

Clone the repository to your local machine by running the following command:

```bash
git clone https://github.com/ironlam/subscription-forecast.git
```

### 2. Install dependencies

```
make install
```

Activate the virtual environment:

* For Linux and macOS: `source venv/bin/activate`

Install the required dependencies using the Makefile: 

```make requirements```

### 3. Prepare the dataset
Place your dataset (in CSV format) in the dataset directory. The CSV file should contain the following columns:

* id
* source (e.g., "Android", "iOS", "web")
* subscription_level
* created_at

Make sure the dataset has a few months of data for accurate forecasting.

Example : 

```
"id","source","subscription_level","created_at"
"1","Android","premium","2021-02-04 11:57:07"
"2","Android","access","2021-02-05 08:06:14"
"3","Android","access","2021-02-05 17:12:35" 
```

### 4. Run the application

Run the web application using the Makefile:

```make run```

The application will be accessible at http://127.0.0.1:7860/.

## Using the Subscription Forecast Web App

To use the Subscription Forecast Web App:

1. Select a subscription source (Android, iOS, or web) from the dropdown menu.
2. Use the slider to choose the number of days for which you'd like to forecast the subscriptions.
3. Click on "Submit" to generate the forecast graph.

The graph will display the number of subscriptions (Y-axis) against the date (X-axis) for each subscription level, as well as the total subscriptions.

## Contributing
Contributions to the Subscription Forecast Web App are welcome. Feel free to open issues or submit pull requests to improve the app or its documentation.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.