# Python wrapper for Atlas Scientific USB sensors

## Installing dependencies.

- Install libftdi package.

        sudo apt-get install libftdi-dev 
    
- Install pylibftdi python package.
    
        sudo pip install pylibftdi

- Install dependencies
    
        sudo apt-get install sqlite
        sudo pip install xlwt
        
- Create SYMLINK of the FTDI adaptors.
    
    The following will allow ordinary users (e.g. ‘pi’ on the RPi) to access to the FTDI device without needing root permissions:
    
    If you are using device with root permission, just skip this step. 
    
    Create udev rule file by typing `sudo nano /etc/udev/rules.d/99-libftdi.rules` and insert below:
    
        SUBSYSTEMS=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6015", GROUP="dialout", MODE="0660", SYMLINK+="FTDISerial_Converter_$attr{serial}"

    Press CTRL+X, Y and hit Enter to save & exit.
    
    Restart `udev` service to apply changes above.
        
        sudo service udev restart

- Modify FTDI python driver
    
    Since our FTDI devices use other USB PID(0x6015), we need to tweak the original FTDI Driver.
    
        sudo nano /usr/local/lib/python2.7/dist-packages/pylibftdi/driver.py
    
    Move down to the **line 70** and add `0x6015` at the end of line.

    Original line:
        
        USB_PID_LIST = [0x6001, 0x6010, 0x6011, 0x6014]
        
    Added line:
            
        USB_PID_LIST = [0x6001, 0x6010, 0x6011, 0x6014, 0x6015]        
        
        
- Testing Installation.

    Connect your device, and run the following (as a regular user):
        
        python -m pylibftdi.examples.list_devices
   
    If all goes well, the program should report information about each connected device. 

    If no information is printed, but it is when run with sudo,
    
    a possibility is permissions problems - see the section under Linux above regarding **udev** rules.
    
    You may get result like this:
        
        FTDI:FT230X Basic UART:DA00TN73
    
    FTDI adaptors has its own unique serial number.

    We need this to work with our sensors.

    In the result above, serial number is `DA00TN73`.
    
## Install library
    
    cd ~
    git clone https://github.com/Atlas-Scientific/R-pi-database-.git
    cd R-pi-database-
    sudo python setup.py install
    
    
## Test library
    
Here is the basic sample code.

    ```Python
    import pylibAtlas      # import pylibAtlas library
    
    db_test = 'test1.sqlite'
    table_test = 'tb_test'
    
    # Create database file and also table with given parameter.
    # Note that the table has columns named id, time stamp, val1, val2, val3, val4 to store sensor data. 
    pylibAtlas.create_table(db_test, table_test)    
    
    # Once creating the database file and table, now let us read data from the sensor and save to db.
    # Assume that sensor data has been saved to sensor_val variable.
    pylibAtlas.insert_data(db_test, table_test, sensor_val)

    # Now let us try to get last commited value
    print "Last value:", pylibAtlas.get_last_value(db_test, table_test)
    
    # Maximum value through the whole db
    print "Max value: ", pylibAtlas.get_max_value(db_test, table_test)
    
    # Minimum value through the whole db
    print "Min value: ", pylibAtlas.get_min_value(db_test, table_test)
    
    # When we forget table name, we can use this function to get table name from the db file.
    print "Table name: ", pylibAtlas.get_table_name(db_test)

    # export to excel file which has same file name with db file.
    # test1.xlsx file will be created in the same directory.
    print "Exporting: ", pylibAtlas.export_xls('test1.sqlite')
    
    ```
    
    