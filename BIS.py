# -*- coding: utf-8 -*-
!pip install pm4py==1.5.2
import pm4py

# Load XES file
from pm4py.objects.log.importer.xes import importer as xes_importer
log = xes_importer.apply("/content/drive/MyDrive/Fine_Management.xes")

# Number of cases
print(f"Number of cases: {len(log)}")

# Activities
from pm4py.statistics.attributes.log import get as attributes_get
activities = attributes_get.get_attribute_values(log, "concept:name")
print("Activities in log:")
for activity, count in activities.items():
    print(f"{activity}: {count}")
"""#
Number of cases: 150370
Activities in log:
Create Fine: 150370
Send Fine: 103987
Insert Fine Notification: 79860
Add penalty: 79860
Send for Credit Collection: 59013
Payment: 77601
Insert Date Appeal to Prefecture: 4188
Send Appeal to Prefecture: 4141
Receive Result Appeal from Prefecture: 999
Notify Result Appeal to Offender: 896
Appeal to Judge: 555
"""


"""# Filtering and Processing Log file"""

# Step 1: Filter traces with at least 3 events
filtered_log_by_length = [trace for trace in log if len(trace) >= 3]

# Step 2: Count activity occurrences
from collections import Counter
activity_counter = Counter(event["concept:name"] for trace in filtered_log_by_length for event in trace)

# Step 3: Keep only frequent activities (≥1000 occurrences)
frequent_activities = {activity for activity, count in activity_counter.items() if count >= 1000}

# Step 4: Filter events in each trace
filtered_log = []
for trace in filtered_log_by_length:
    new_trace = [event for event in trace if event["concept:name"] in frequent_activities]
    if new_trace:
        filtered_log.append(new_trace)

# Step 5: Print result
print(f"Filtered log - Number of cases: {len(filtered_log)}")
"""#
Filtered log - Number of cases: 83614
"""
# Step 6: Show remaining activities
remaining_activities = Counter(event["concept:name"] for trace in filtered_log for event in trace)
print("Remaining activities:")
for activity, count in remaining_activities.items():
    print(f"{activity}: {count}")
"""#
Remaining activities:
Create Fine: 83614
Send Fine: 83602
Insert Fine Notification: 79860
Add penalty: 79860
Send for Credit Collection: 59013
Payment: 31230
Insert Date Appeal to Prefecture: 4188
Send Appeal to Prefecture: 4141
"""

"""Discovery Techniques on Full Log"""
from pm4py.visualization.petrinet import visualizer as pn_visualizer

"""# Alpha Miner"""
# Apply Alpha Miner
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
net, initial_marking, final_marking = alpha_miner.apply(filtered_log)
# Visualize
gviz = pn_visualizer.apply(net, initial_marking, final_marking)
pn_visualizer.view(gviz)

"""# Inductive Miner"""
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
net, initial_marking, final_marking = inductive_miner.apply(filtered_log)
# Visualize the Petri net
gviz = pn_visualizer.apply(net, initial_marking, final_marking)
pn_visualizer.view(gviz)

"""# Heuristic Miner"""
from pm4py.algo.discovery.heuristics import algorithm as heuristic_miner
# Apply Heuristic Miner
net, initial_marking, final_marking = heuristic_miner.apply(filtered_log)
# Visualize the Petri net
gviz = pn_visualizer.apply(net, initial_marking, final_marking)
pn_visualizer.view(gviz)


"""Process Tree"""
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.visualization.process_tree import visualizer as pt_visualizer

process_tree = inductive_miner.apply_tree(log)
gviz = pt_visualizer.apply(process_tree)
pt_visualizer.view(gviz)


"""# Performance Comparison"""

import time

# Measure time for Alpha Miner
start_time = time.time()
alpha_net, alpha_initial_marking, alpha_final_marking = alpha_miner.apply(filtered_log)
alpha_time = time.time() - start_time
print(f"Alpha Miner time: {alpha_time:.2f} seconds")

# Measure time for Inductive Miner
start_time = time.time()
inductive_net, inductive_initial_marking, inductive_final_marking = inductive_miner.apply(filtered_log)
inductive_time = time.time() - start_time
print(f"Inductive Miner time: {inductive_time:.2f} seconds")

# Measure time for Heuristic Miner
start_time = time.time()
heuristic_net, heuristic_initial_marking, heuristic_final_marking = heuristic_miner.apply(filtered_log)
heuristic_time = time.time() - start_time
print(f"Heuristic Miner time: {heuristic_time:.2f} seconds")
"""# 
Alpha Miner time: 0.62 seconds
Inductive Miner time: 0.30 seconds
Heuristic Miner time: 5.61 seconds
"""


"""# Data Segmentation"""

# Example: Filter traces with 'Payment' activity
filtered_log_payment = [trace for trace in filtered_log if any(event["concept:name"] == "Payment" for event in trace)]

print(f"Filtered log for 'Payment' - Number of cases: {len(filtered_log_payment)}")
#Filtered log for 'Payment' - Number of cases: 23344

# Apply Alpha Miner to the Activity-Filtered Log
alpha_net_filtered, alpha_initial_marking_filtered, alpha_final_marking_filtered = alpha_miner.apply(filtered_log_payment)

# Apply Inductive Miner to the Activity-Filtered Log
inductive_net_filtered, inductive_initial_marking_filtered, inductive_final_marking_filtered = inductive_miner.apply(filtered_log_payment)

# Apply Heuristic Miner to the Activity-Filtered Log
heuristic_net_filtered, heuristic_initial_marking_filtered, heuristic_final_marking_filtered = heuristic_miner.apply(filtered_log_payment)



"""# Process Discovery on Filtered Data

1. Alpha Miner
"""
# Apply Alpha Miner on Activity-Filtered Log (Payment)
alpha_net_filtered, alpha_initial_marking_filtered, alpha_final_marking_filtered = alpha_miner.apply(filtered_log_payment)

# Visualize the Petri net
alpha_gviz = pn_visualizer.apply(alpha_net_filtered, alpha_initial_marking_filtered, alpha_final_marking_filtered)
pn_visualizer.view(alpha_gviz)

"""2. Inductive Miner"""

# Apply Inductive Miner on filtered data
inductive_net_filtered, inductive_initial_marking_filtered, inductive_final_marking_filtered = inductive_miner.apply(filtered_log_payment)

# Visualize the Petri net
inductive_gviz = pn_visualizer.apply(inductive_net_filtered, inductive_initial_marking_filtered, inductive_final_marking_filtered)
pn_visualizer.view(inductive_gviz)

"""3. Heuristic Miner"""

# Apply Heuristic Miner on filtered data
heuristic_net_filtered, heuristic_initial_marking_filtered, heuristic_final_marking_filtered = heuristic_miner.apply(filtered_log_payment)

# Visualize the Petri net
heuristic_gviz = pn_visualizer.apply(heuristic_net_filtered, heuristic_initial_marking_filtered, heuristic_final_marking_filtered)
pn_visualizer.view(heuristic_gviz)



"""# Predictive Analytics
1. Convert the XES Event Log to Tabular Format
"""
import pandas as pd

data = []

for trace in filtered_log:
    for event in trace:
        flat_event = {}
        for key, value in event.items():
            flat_event[key] = value
        data.append(flat_event)

# Create DataFrame
df = pd.DataFrame(data)
df.head()

"""2. Define the Prediction Goal"""

print(df.columns.tolist())
"""['amount', 'org:resource', 'dismissal', 'concept:name', 'vehicleClass', 'totalPaymentAmount', 'lifecycle:transition', 'time:timestamp', 'article', 'points', 'expense', 'notificationType', 'lastSent', 'paymentAmount']"""

# Add case ID based on row index to track the case for each event
df['case_id'] = df.groupby("concept:name").ngroup()

# Group events by case_id
grouped = df.groupby("case_id")["concept:name"].apply(list)

# Create label: 1 if 'Payment' is in the list of activities for the case, else 0
labels = grouped.apply(lambda activities: int("Payment" in activities)).reset_index()
labels.columns = ["case_id", "paid"]

labels.head()


"""# Feature Engineering (Handle time zone-aware datetime conversion correctly)"""

# Convert 'time:timestamp' to datetime objects if it's not already
df['time:timestamp'] = pd.to_datetime(df['time:timestamp'], utc=True) # Add utc=True to handle timezone-aware datetimes

if df['time:timestamp'].dt.tz is not None:
    # Convert to UTC if it is timezone-aware
    df['time:timestamp'] = df['time:timestamp'].dt.tz_convert('UTC').dt.tz_localize(None)
else:
    # If the timestamp is already in UTC, just ensure it's a datetime object without timezone info
    df['time:timestamp'] = pd.to_datetime(df['time:timestamp'])

# Now calculate the time differences
df['time_diff'] = df.groupby('case_id')['time:timestamp'].diff().fillna(pd.Timedelta(seconds=0))

# Calculate the total time from first event to last event for each case
case_times = df.groupby('case_id')['time:timestamp'].agg(['min', 'max'])
case_times['case_duration'] = (case_times['max'] - case_times['min']).dt.total_seconds()

# Count occurrences of each activity for each case
activity_counts = df.groupby(['case_id', 'concept:name']).size().unstack(fill_value=0)

# Merge the activity counts and case_times with the labels
features = pd.merge(labels, case_times[['case_duration']], left_on='case_id', right_index=True)

# Add activity counts to the features DataFrame
features = features.join(activity_counts)

features.head()



"""# Train a Model"""

# Rename the 'paid' column in labels to 'label'
labels.rename(columns={'paid': 'label'}, inplace=True)

# Now merge the features with the labels DataFrame on 'case_id'
features = pd.merge(features, labels[['case_id', 'label']], on='case_id', how='left')

# Clean up the column names (remove suffixes like '_x', '_y' from redundant columns)
features.columns = features.columns.str.replace(r'_x$', '', regex=True)
features.columns = features.columns.str.replace(r'_y$', '', regex=True)

# Verify the columns again to ensure 'label' is now included
print(features.columns)
"""(['case_id', 'paid', 'case_duration', 'Add penalty', 'Create Fine',
       'Insert Date Appeal to Prefecture', 'Insert Fine Notification',
       'Payment', 'Send Appeal to Prefecture', 'Send Fine',
       'Send for Credit Collection', 'label'],
      dtype='object')"""

# Drop the duplicate 'concept:name' columns, keeping the relevant ones
features = features.loc[:, ~features.columns.str.contains('concept:name')]

# Ensure that the 'label' column is properly placed
# If there is still any confusion, let's check if it's really added.
# print(features.columns)


"""Split the data and train a model:"""

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Split the data into features (X) and target (y)
X = features.drop(columns=['case_id', 'label'])  # Drop case_id and label columns from features
y = features['label']  # This is the target variable (whether 'Payment' occurred)

# Split into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize a RandomForestClassifier model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model performance
print(classification_report(y_test, y_pred))
"""              precision    recall  f1-score   support

           0       1.00      1.00      1.00         2

    accuracy                           1.00         2
   macro avg       1.00      1.00      1.00         2
weighted avg       1.00      1.00      1.00         2"""



"""**To ensure the model is generalized and not overfitting:**
Cross-validation: Perform cross-validation to evaluate the model on different splits of the data, which will give a better sense of the model’s robustness.
"""
from sklearn.model_selection import cross_val_score

# Perform cross-validation
cv_scores = cross_val_score(model, X, y, cv=5)  # 5-fold cross-validation

# Print the mean and standard deviation of cross-validation scores
print(f"Cross-validation scores: {cv_scores}")
print(f"Mean CV score: {cv_scores.mean()}")
print(f"Standard Deviation of CV scores: {cv_scores.std()}")
"""
Cross-validation scores: [1.  1.  0.5 1.  1. ]
Mean CV score: 0.9
Standard Deviation of CV scores: 0.2
"""
