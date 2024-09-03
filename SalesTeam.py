from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import openai

app = Flask(__name__)

# Loading the data from CSV file
data = pd.read_csv('/Users/samannazir/Downloads/backenddevelopmentexercise /sales_performance_data.csv')
# GPT 3.5 API key
openai.api_key = 'MY_API_KEY'  



# Individual Sales Representative Performance Analysis
def rep_performance_summary(rep_data):
    if rep_data.empty:
        return {"error": "No data available for this representative."}
    row = rep_data.iloc[0]  
    # Summarizing main features from data to analyse Individual Representative Performance
    summary = {
        'Employee Name': str(row['employee_name']),
        'Leads Taken': int(row['lead_taken']),
        'Tours Booked': int(row['tours_booked']),
        'Applications': int(row['applications']),
        'Tours per Lead': float(row['tours_per_lead']),
        'Apps per Tour': float(row['apps_per_tour']),
        'Apps per Lead': float(row['apps_per_lead']),
        'Revenue Confirmed': float(row['revenue_confirmed']),
        'Avg Deal Value (30 Days)': float(row['avg_deal_value_30_days']),
        'Avg Close Rate (30 Days)': float(row['avg_close_rate_30_days']),
        }
    return summary


#  Overall Sales Team Performance 
def team_performance_summary(data):
    # Summarizing main features from data to analyse Overall Sales Team Performance 
    summary = {
        'Total Leads Taken': int(data['lead_taken'].sum()),
        'Total Tours Booked': int(data['tours_booked'].sum()),
        'Total Applications': int(data['applications'].sum()),
        'Avg Tours per Lead': float(data['tours_per_lead'].mean()),
        'Avg Apps per Tour': float(data['apps_per_tour'].mean()),
        'Avg Apps per Lead': float(data['apps_per_lead'].mean()),
        'Total Revenue Confirmed': float(data['revenue_confirmed'].sum()),
        'Avg Deal Value (30 Days)': float(data['avg_deal_value_30_days'].mean()),
        'Avg Close Rate (30 Days)': float(data['avg_close_rate_30_days'].mean())
    }
    return summary


# performance_trends and Forcasting 
def performance_trends_summary(data, time_period):

    data['dated'] = pd.to_datetime(data['dated'])
    data.set_index('dated', inplace=True)
    
    if time_period == 'monthly':
        summary = data[['revenue_runrate', 'tours_runrate', 'tours_scheduled', 'tours_pending', 'tours_cancelled']].resample('M').sum()
    elif time_period == 'quarterly':
        summary = data[['revenue_runrate', 'tours_runrate', 'tours_scheduled', 'tours_pending', 'tours_cancelled']].resample('Q').sum()
    else:
        return "Invalid time period Found"
    
    return summary.to_string()



# Function to generate analysis by giving commands to LLM model
def generate_analysis(summary, analysis_type):
    prompt = ""
    if analysis_type == "rep_performance":
        prompt = (
        "Provide a  analysis and actionable feedback based on the following individual sales representative performance data:\n\n"
        f"{summary}\n\n"
        "Focus on identifying strengths and areas for improvement, and suggest strategies for enhancing performance in paragraph."
    )
    elif analysis_type == "team_performance":
         prompt = (
        "provide a analysis and insightful feedback based on the following overall sales team performance data:\n\n"
        f"{summary}\n\n"
        "Highlight key achievements and areas where the team can improve. Include recommendations for boosting team performance and productivity in paragraph."
    )
    elif analysis_type == "performance_trends":
        prompt = (
        "Analyze the sales performance trends based on the following data:\n\n"
        f"{summary}\n\n"
        "Provide a detailed interpretation of these trends, including any noticeable patterns or anomalies. Offer predictions and actionable recommendations based on the analysis in paragraph"
    )
    else:
        return "No valid analysis type provided."

    # API call to OpenAI
    messages = [
        {"role": "system", "content": "You will provides insights on sales data."},
        {"role": "user", "content": prompt}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=150
    )
    
    return response['choices'][0]['message']['content'].strip()



# API Endpoints
# Individual rep_performance
@app.route('/api/rep_performance', methods=['GET'])
def rep_performance():
    rep_id = int(request.args.get('rep_id'))
    rep_data = data[data['employee_id'] == rep_id]
    
    if rep_data.empty:
        return jsonify({'error': 'Representative not found'}), 404
    
    summary = rep_performance_summary(rep_data)
    analysis = generate_analysis(summary, analysis_type="rep_performance")
    return jsonify({'rep_id': rep_id, 'analysis': analysis})

#team_performance
@app.route('/api/team_performance', methods=['GET'])
def team_performance():
    summary = team_performance_summary(data)
    analysis = generate_analysis(summary, analysis_type="team_performance")
    return jsonify({'team_analysis': analysis})

#performance_trends
@app.route('/api/performance_trends', methods=['GET'])
def performance_trends():
    time_period = request.args.get('time_period', 'monthly')
    trend_summary = performance_trends_summary(data, time_period)
    analysis = generate_analysis(trend_summary, analysis_type="performance_trends")
    return jsonify({'time_period': time_period, 'trend_summary': trend_summary, 'trend_analysis': analysis})


# Flask application
if __name__ == '__main__':
    app.run(debug=True)


