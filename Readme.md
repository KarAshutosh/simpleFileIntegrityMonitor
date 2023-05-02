# Install 
```
git clone https://github.com/KarAshutosh/simpleFileIntegrityMonitor.git
```

#  Run
```
python v_1_1_FMI.py 
```

# About Program

The program generates a hash for each file in a directory and its subdirectories and compares the current hash values with the previous hash values saved in a file named lastHash.txt.
If there are any changes in the hash values, the program writes the new hash values to a new file named newHash.txt and updates the lastHash.txt file with the new hash values. 

In v_1_0_FMI.py it updates the log.txt file on detecting changes with timestamps.

In v_1_1_FMI.py it also sends an email notification to notify the recipient of the changes detected.

To change the directory, change the path in the variable ```dir_path```

To ignore certain files or folders, add them in the array ```ignore_list```




