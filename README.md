##Observe Image Pull
This repository provides a script to download images from the Janus AI platform based on data from an input CSV file. The script sets up a virtual environment, installs required dependencies, and allows the user to select the CSV file using a file explorer.

##Prerequisites
Ensure you have the following installed:

Python 3.6 or later
PowerShell (for Windows users)
Setup and Usage

###Step 1: Clone the Repository
sh
Copy code
git clone <repository-url>
cd observe_image_pull

###Step 2: Prepare the CSV File
Use the following Athena query template to generate the input CSV file. This query pulls Observe records with necessary fields:

Athena sql

SELECT ROW_NUMBER() OVER (PARTITION BY a.observe_username ORDER BY a.event_at asc) event_number, 
    a.*, predicted_task_id, task_id, inferred_identifier_type, inferred_identifier_value, metadata, logical_location, logical_bounding_rect, main_window_logical_rect, path, file_source_id
FROM "observe_processed"."user_day" a
left join "illuminate"."user_task_observe_record_id_relationship" b on
    a.observe_record_id = b.observe_record_id
left join "illuminate"."user_task" c on
    b.user_task_id = c.id
left join "observe_stream"."observe_record" d on 
    b.observe_record_id = d.id 
where
    a.org_id = '3cd46f18-2ae5-482f-9167-ccad07d5d5a1'
    and b.org_id = '3cd46f18-2ae5-482f-9167-ccad07d5d5a1'
    and c.org_id = '3cd46f18-2ae5-482f-9167-ccad07d5d5a1'
    and d.org_id = '3cd46f18-2ae5-482f-9167-ccad07d5d5a1'
    and a.event_date = '2024-04-01'
    and b.event_date = '2024-04-01'
    and c.event_date = '2024-04-01'
    and d.event_date = '2024-04-01'
    and a.observe_username = 'crose2'
order by a.event_at asc
Note: This query can pull any Observe records as long as org_id, filesource_id, and path are derived from observe_stream.observe_record.

###Step 3: Place the CSV File
Ensure the CSV file is placed in a known directory. For example, C:\Users\YourUsername\Downloads\Referral_Audit.csv.

###Step 4: Run the Setup Script
Windows Users
Open PowerShell and navigate to the project directory:

powershell

cd C:\path\to\observe_image_pull (update this to the folder where you stored the repository)
Run the setup script:

powershell
Copy code
.\setup_env.ps1

When prompted, enter the path to the CSV file:


Please enter the path to the CSV file: C:\Users\YourUsername\Downloads\Referral_Audit.csv

###Script Description

setup_env.ps1: Sets up a virtual environment, installs required dependencies, and runs the main script.

main.py: The main script that:
    Loads the CSV data.
    Generates API endpoints.
    Downloads images from the generated endpoints.
    Opens the folder containing the downloaded images.

Dependencies
The requirements.txt file includes the following dependencies:

pandas
requests
These will be installed automatically when running the setup script.

License
This project is licensed under the MIT License.