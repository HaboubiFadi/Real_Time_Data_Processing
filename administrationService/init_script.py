import subprocess

if __name__=='__main__':
    database_script = ['bin/kafka-topics.sh','--create --topic quickstart-events --bootstrap-server broker:9092']

    database_results = subprocess.run(database_script, capture_output=True, text=True)
    if database_results.returncode == 0:
    
        output = database_results.stdout
        print("Output:", output)
    else:
    
        error = database_results.stderr
        print("Error:", error) 