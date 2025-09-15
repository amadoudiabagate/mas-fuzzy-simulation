from server import server
from model import CliniqueModel
import os
import subprocess
import sys

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--csv":
        print("Simulation mode CSV activated...")
        
        # Create and launch the model
        model = CliniqueModel(num_agents=12, width=10, height=10)
        print(f"✓ Model created with {len(model.schedule.agent)} agent")
        
        # Run the simulation
        print("Execution of the simulation (50 steps)...")
        for step_num in range(1, 51):
            model.step()
            if step_num % 10 == 0:
                events_count = len(model.custom_datacollector.records)
                print(f"Step {step_num}/50 - {events_count} collected events")
        
        # Save the outcome(s)
        print("\nSaving the outcome(s)...")
        saved_file = model.save_results()
        
        if saved_file:
            print(f"\n SUCCESS! File generated: {saved_file}")
            
            # Open the outputs folder
            try:
                subprocess.Popen(f'explorer "{os.path.abspath("outputs")}"')
                print(" Open file outputs")
            except:
                print(" Manually open the 'outputs' folder")
        else:
            print("\n FAILURE - No file generated")
    
    else:
        print("Starting the web server...")
        print("To generate a CSV: python run.py --csv")
        server.launch()

if __name__ == "__main__":
    main()