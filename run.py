import os
import sys

#  Instructions:
#  python.exe .\run.py build  examples\light_switch\myclient
#  python.exe .\run.py clean  examples\light_switch\myclient
#  python.exe .\run.py flash  examples\light_switch\myclient
#  python.exe .\run.py rebuild  
#  python.exe .\run.py flash_softdevice  

SOFTDEVICE_PATH = 'nRF5_SDK_15.0.0_a53641a/components/softdevice/s140/hex/s140_nrf52_6.0.0_softdevice.hex'
MESH_ROOT = 'nrf5_SDK_for_Mesh_v2.1.1_src/build'
TOOLCHAIN = 'gccarmemb'
PLATFORM = 'nrf52840_xxAA'


if len(sys.argv) == 1:
    print('Error: No incoming parameters')
    print(r'Use: command {clean,flash,rebuild,build} build_path')
    exit()

path =os.path.abspath(sys.argv[0])
arg = path.rfind(os.sep)
path = os.path.join(path[:arg],MESH_ROOT)

def get_hex(path):
    lis = os.listdir(path)
    for i in lis:
        if os.path.splitext(i)[1] == '.hex':
            return os.path.join(path,i)
    return None

def burn_hex(path):
    path = os.path.join(path,sys.argv[2])
    if not os.path.isdir(path):
        print('error ,file is invalue')
        exit()
    path = get_hex(path)
    if path != None:
        os.system("nrfjprog -f nrf52 --eraseall")
        os.system("nrfjprog -f nrf52 --program %s --sectorerase" % (SOFTDEVICE_PATH))
        os.system("nrfjprog -f nrf52 --program %s --sectorerase" % (path))
        os.system("nrfjprog -f nrf52 --reset")

def build_pro(path):
    try:
        os.mkdir(path)
    except:
        pass
    finally:
        os.chdir(path)
        os.system('cmake -G Ninja -DTOOLCHAIN=%s -DPLATFORM=%s ..' % (TOOLCHAIN,PLATFORM))

comm = sys.argv[1]
if comm == 'flash':
    burn_hex(path)
elif comm == 'rebuild':
    build_pro(path)
elif comm == 'build':
    os.chdir(path)
    os.system('ninja %s/all' % (sys.argv[2]))
elif comm == 'clean':
    os.chdir(path)
    os.system('ninja clean %s/all' % (sys.argv[2]))
elif comm == 'erase':
    os.system("nrfjprog -f nrf52 --eraseall")
elif comm == 'flash_softdevice':
    os.system("nrfjprog -f nrf52 --program %s --sectorerase" % (SOFTDEVICE_PATH))
    os.system("nrfjprog -f nrf52 --reset")
