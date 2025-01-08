import ctypes
import psutil
import time

class MemoryStream:
    def __init__(self):
        self.kernel32 = ctypes.windll.kernel32
        self.psapi = ctypes.windll.psapi

    def get_memory_status(self):
        class MEMORYSTATUS(ctypes.Structure):
            _fields_ = [("dwLength", ctypes.c_ulong),
                        ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong),
                        ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong),
                        ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong),
                        ("ullAvailVirtual", ctypes.c_ulonglong)]

        memory_status = MEMORYSTATUS()
        memory_status.dwLength = ctypes.sizeof(MEMORYSTATUS)
        self.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory_status))
        return memory_status

    def optimize_memory(self):
        # Freeing up standby memory
        self.psapi.EmptyWorkingSet(-1)
        
        # Reducing memory usage of all processes
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            try:
                p = psutil.Process(proc.info['pid'])
                p.suspend()
                p.resume()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    def display_memory_status(self, memory_status):
        print(f"Memory Load: {memory_status.dwMemoryLoad}%")
        print(f"Total Physical Memory: {memory_status.ullTotalPhys / (1024 ** 3):.2f} GB")
        print(f"Available Physical Memory: {memory_status.ullAvailPhys / (1024 ** 3):.2f} GB")
        print(f"Total Virtual Memory: {memory_status.ullTotalVirtual / (1024 ** 3):.2f} GB")
        print(f"Available Virtual Memory: {memory_status.ullAvailVirtual / (1024 ** 3):.2f} GB")

    def run(self):
        while True:
            memory_status = self.get_memory_status()
            self.display_memory_status(memory_status)
            if memory_status.dwMemoryLoad > 75:
                print("Optimizing memory...")
                self.optimize_memory()
            time.sleep(60)

if __name__ == "__main__":
    memory_stream = MemoryStream()
    memory_stream.run()