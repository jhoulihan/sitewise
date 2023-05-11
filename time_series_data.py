import boto3
import pandas as pd

# Set up AWS Sitewise client
client = boto3.client('iotsitewise')

# Set up alias prefix filter
#alias_prefix = '/xxx/xxx/xxx/'
alias_prefix = '/MMM/Device1/MMMM/MTMLP1'

# Initialize list of time-series data
time_series_data = []

# Call ListTimeSeries API with alias prefix filter
response = client.list_time_series(
    aliasPrefix=alias_prefix
)

# Add initial set of time-series data to list
time_series_data += response['TimeSeriesSummaries']

# Check if there are more pages of results
while 'nextToken' in response:

    # Call ListTimeSeries API with nextToken to get next page of results
    response = client.list_time_series(
        aliasPrefix=alias_prefix,
        nextToken=response['nextToken']
    )

    # Add page of time-series data to list
    time_series_data += response['TimeSeriesSummaries']

# Create a Pandas DataFrame from the time-series data
#df = pd.DataFrame(time_series_data, columns=['alias', 'dataType'])
df = pd.DataFrame(time_series_data, columns=['alias'])

# Sort the DataFrame by the 'alias' column in ascending order
df_sorted = df.sort_values('alias', ascending=True)

# Export the DataFrame to a CSV file
#df.to_csv('tagnames.csv', index=False)
df_sorted.to_csv(alias_prefix.replace('/','_') + 'tagname.csv', index=False)

# Print a message indicating the export is complete
print('tagnames exported to CSV file.')
