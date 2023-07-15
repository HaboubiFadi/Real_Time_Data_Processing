# orchestrate Services 
import subprocess


produce_path='kafka_Api_finance/dataingestService/Script_yf.py'
consumer_path='kafka_Api_finance/dataProcessingService/Script_yf.py'
visualization_path='kafka_Api_finance/visualizationService/Script_yf.py'



produce_script = ['python3', produce_path]
consumer_script = ['python3', consumer_path]
visulatation_script = ['python3', visualization_path]

# Execute the command and capture the output
produce_result = subprocess.run(produce_script, capture_output=True, text=True)
consumer_result = subprocess.run(consumer_script, capture_output=True, text=True)
visulatation_result = subprocess.run(visulatation_script, capture_output=True, text=True)

# Check the return code
if produce_result.returncode == 0:
    # Success: access the output
    output = produce_result.stdout
    print("Output:", output)
else:
    # Error: access the error message
    error = produce_result.stderr
    print("Error:", error)    
