import subprocess,traceback,platform,logging,time,psutil
if str(platform.system()) == "Linux" or str(platform.system()) == "Windows":
    try:
        _a_ = subprocess.check_output(['pip','install','pyglet==1.5.28','pygame','numpy','pyopengl==3.1.5'])
        if 'Requirement already satisfied: pyglet==1.5.28 in ' in str(_a_):
            print("You have already installed pyglet.")
        if 'Requirement already satisfied: pygame' in str(_a_):
            print("You have already installed pygame.")
        if 'Requirement already satisfied: numpy' in str(_a_):
            print("You have already installed numpyt.")
        if 'Requirement already satisfied: pyopengl' in str(_a_):
            print("You have already installed pyopengl==3.1.5.")
    except subprocess.CalledProcessError as e:
        print("Python.output.module.subprocess.CalledProcessError:")
        traceback.print_stack()
        print("######Debugging started########")
        print("extracted stack:")
        print(repr(traceback.extract_stack()))
        print("formatted stack:")
        print(repr(traceback.format_stack()))
        print("Error message:\n",e)
        print("the following may caused the problem:")
        print("1. OSError: [Errno 122] Disk quota exceeded,It means that the python doesn’t have enough storage space to install those packages.")
        print("2. FileNotFoundError: [Errno 2] No usable temporary directory found in ['/tmp', '/var/tmp', '/usr/tmp', '/home/.anon-09397858f5214a1..(bla bla bla)'] It means that python can not found usable temporary directory found in the dirs")
elif str(platform.system()) == "Darwin":
    try:
        _a_ = subprocess.check_output(['pip3','install','pyglet==1.5.28'])
        if 'Requirement already satisfied: pyglet==1.5.28 in ' in str(_a_):
            print("You have already installed pyglet.")
    except subprocess.CalledProcessError as e:
        print("Python.output.module.subprocess.CalledProcessError:")
        traceback.print_stack()
        print("######Debugging started########")
        print("extracted stack:")
        print(repr(traceback.extract_stack()))
        print("formatted stack:")
        print(repr(traceback.format_stack()))
        print("Error message:\n",e)
        print("the following may caused the problem:")
        print("1. OSError: [Errno 122] Disk quota exceeded,It means that the python doesn’t have enough storage space to install those packages.")
        print("2. FileNotFoundError: [Errno 2] No usable temporary directory found in ['/tmp', '/var/tmp', '/usr/tmp', '/home/.anon-09397858f5214a1..(bla bla bla)'] It means that python can not found usable temporary directory found in the dirs")
print("Checking System requirements...")
macos_list=["17.4.0","17.7.0","17.6.0","17.5.0","17.4.0","17.3.0","17.2.0","17.1.0","17.0.0"]
if str(platform.system()) == "Linux":
    print("Detected system: Linux")
    import os 
    print(os.uname())
if str(platform.system()) == "Windows":
    print("Detected system: windows")
    my_system = platform.uname()
    print(f"System: {my_system.system}")
    print(f"Node Name: {my_system.node}")
    print(f"Release: {my_system.release}")
    print(f"Version: {my_system.version}")
    print(f"Machine: {my_system.machine}")
    print(f"Processor: {my_system.processor}")
    subprocess.call(['pip','install','wmi'])
    import wmi
    c = wmi.WMI() 
    my_system = c.Win32_ComputerSystem()[0]

    print(f"Manufacturer: {my_system.Manufacturer}")
    print(f"Model: {my_system. Model}")
    print(f"Name: {my_system.Name}")
    print(f"NumberOfProcessors: {my_system.NumberOfProcessors}")
    print(f"SystemType: {my_system.SystemType}")
    print(f"SystemFamily: {my_system.SystemFamily}")
    if str(platform.release()) == "Vista" or str(platform.release()) == "7":
        logging.warn(msg="Warning:You are using an older version of windows,some components may not be ok!")
        logging.warn(msg=f"Detected version:{platform.release()}")
elif str(platform.system()) == "Darwin":
    print("Detected system: MacOS")
    if str(platform.release()) in macos_list :
        logging.warn(msg="Warning:You are using an older version of windows,some components may not be ok!")
        logging.warn(msg=f"Detected version:{platform.release()}")
print("checking memory usage")
for i in range(5):
    print(f"Memory :{psutil.virtual_memory()}")
    time.sleep(1)
print("Deep Checking System Configs... ")
# traverse the info
Id = subprocess.check_output(['systeminfo'])
new = []

print("All ready to go!")

time.sleep(1)
print(3)
time.sleep(1)
print(2)
time.sleep(1)
print(1)
print("running package...")
time.sleep(1)
import minecraft_main_program