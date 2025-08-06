1. Flow:
Terraform adds a webhook to the existing repo of your choosing. It's also possible to add resource to create new repo instead.    
Terraform also creates an EC2 instance and deploys on it a python app - webhook.py. The app runs on port 5000 with two routes: /webhook and /show
webhook.py file is not included here; it is placed in my public GitHub repo and Terraform gets it with curl to the Raw file, then copies it in the EC2 directory.  
The webhook's URL is a /webhook route to the python app. 
Note that there is initial webhook ping that fails because the EC2 is not fully initiated at that time. But re-delivery works and then git action will have successful delivery as well.  
When any push or pull is done to the created Repo, the webhook data is saved in the log file on the EC2 as Json file. 
Then filtered data from the Json, that includes only specific information, is sent to another route of the app: /show. The requested data is displayed on that page in a table for better visibility. 
2. Security considerations:
Security group that is created in Terraform has all traffic access in my configurations because it is a Test Project. But in correct configurations it would have limited access per need. 
Github repo is public for this Test, but in correct configurations it should be private. 
3. Load: 
In case there is a heavy traffic to the web app, it is possible to add ABL resource in main.tf and have a load balancer. 
4. Cost: 
The cost in my current configuration is a free tier EC2 instance. 
The IP is not Elastic, so the EC2 needs to be constantly active. Elastic IP will add to the cost.  
