# Keylogger
An executable Keylogger for windows

This keylogger monitors key storkes but in addition to that it also has several features like
1. Video capturing 
2. Audio capturing
3. Takes screenshot
4. Clipboard information
5. Machine Information like IP address(both Public and Private etc)

After monitoring all these things program sends a mail to address specified in the code.

# Generating Executable 
#### Step1:- Fork repository and change the From mail address and To mail address to the mail which you want get mails. In the From and TO address is same for testing.<br/>
#### Step2:- Install pyinstaller using pip comaand pip install pyinstaller <br/>
#### Step3:- Run command pip install --onefile kelogger.py<br/>

after step 3, some dependency file will be installed like build, dist ect. In dist exe file will be there.
Now, run exe you see the console gets filled with some print statements then mail is send to address you specified
