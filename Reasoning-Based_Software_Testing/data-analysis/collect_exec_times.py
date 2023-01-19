import glob
import sys
from datetime import datetime, timedelta

def get_time(stime):
   return stime.split(",")[0]

def handle_config(folder_names):
    
    file_writer = open('output/output-count.csv', 'w')
    file_writer_rep = open('output/output-count-rep.csv', 'w')
    file_writer.write("technique,avg_generation_time,avg_scenario_time,overhead\n")
    file_writer_rep.write("technique,avg_generation_time,avg_scenario_time,overhead\n")

    for folder_n in range(len(folder_names)):
        folder = folder_names[folder_n]
        file_writer.write(folder +", ")
        list_of_all_files = (glob.glob('data_for_scripts'  + "/" + folder + "/*.log"))

        compute_times_means = []
        execution_times_means = []
        overhead_means = []
        for file in list_of_all_files:
            file_writer_rep.write(folder +", ")
            compute_times = []
            execution_times = []

            starting_time = 0
            file_reader = open(file, "r")

            file_contents_ps = file_reader.read().split("\n")
            stime = file_contents_ps[0]
            if "Started" in stime:
                stime = get_time(stime)
                FMT = '%Y-%m-%d %H:%M:%S'
                starting_time = datetime.strptime(stime, FMT)
                
                count_test = 0
                previous_time = stime
                for content in file_contents_ps:
                    count_test +=1
                    if ']:' in content or 'Started' in content:
                        if ']:' not in content:
                            s_time = get_time(content)
                            test_stime = datetime.strptime(s_time, FMT)
                            compute_time = datetime.strptime(s_time, FMT) - datetime.strptime(previous_time, FMT)
                            compute_times.append(compute_time)
                            continue
                        n_time = get_time(content)
                        if n_time == stime:
                            continue

                        time = datetime.strptime(n_time, FMT)
                        execution_time = datetime.strptime(n_time, FMT) - datetime.strptime(previous_time, FMT)
                        previous_time = n_time
                        
                        execution_times.append(execution_time)       
                
            else:
                print("W not started in file")
        
            tot_compute = timedelta()
            for time in compute_times:
                tot_compute +=time
            tot_compute = tot_compute/len(compute_times)

            tot_execution = timedelta()
            for time in execution_times:
                tot_execution +=time
            tot_execution = tot_execution/len(execution_times)

            overhead = tot_compute/tot_execution

            compute_times_means.append(tot_compute)
            execution_times_means.append(tot_execution)
            overhead_means.append(overhead)
            file_writer_rep.write(str(tot_compute)+','+str(tot_execution)+','+str(overhead)+'\n')

        
        tot_compute_means = timedelta()
        for time in compute_times_means:
            tot_compute_means +=time

        tot_execution_means = timedelta()
        for time in execution_times_means:
            tot_execution_means +=time

        ov_tot = 0
        for ov in overhead_means:
            ov_tot += ov
        
        mean_compute = tot_compute_means/len(compute_times_means)
        mean_execution =tot_execution_means/len(compute_times_means)
        mean_overhead = round(ov_tot/len(overhead_means)*100,2)

        file_writer.write(str(mean_compute)+","+str(mean_execution) +","+str(mean_overhead)+ '\n')


if __name__ == "__main__":
    
    folder_names = ["RBST","SBST-ML","ART"]
    handle_config(folder_names)


