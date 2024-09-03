# Sales-Team-Performance Analysis Using LLM


This project provides an API that helps to analyze and summarize sales performance data for individual sales representatives and the entire sales team. It uses state-of-the-art model: GPT-3.5 to generate analysis and practical feedback.

## Table of Contents
- [Features](#features)
- [How It Works](#how-it-works)
- [Technologies Used](#technologies-used)
- [Requirements](#requirements)
- [Installation](#installation)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Individual Sales Performance**: It gives insights and feedback for each sales representative based on their performance.
- **Team Performance **: It gives an overview and insights for the entire sales team.
- **Sales Trends and Forecasting**: Examines sales trends over time by Monthly or Quarterly and makes predictions.

## How It Works

1. **Data Loading**: I have load sales data from a CSV file using Pandas.
2. **Analysis**:
   - *Individual Performance*: Summarizes key performance details for each sales rep.
   - *Team Performance*: Summarizes overall team performance.
   - *Trends Analysis*: Looks at data over time to spot trends and predict future performance.
3. **OpenAI Integration**: Uses OpenAI’s GPT-3.5 to generate detailed analysis and feedback based on the data.
4. **API Endpoints**: Provides RESTful API endpoints to access the different features such as api/rep_performance','/api/team_performance' /api/performance_trends using GET methid.
5. **Error Handling**: Manages any mistakes or problems in a user-friendly way.

## Technologies Used
- Python 3.9
- Flask API
- Pandas Library
- NumPy Library 
- OpenAI GPT-3.5 API_KEY
- POSTMAN to test API

