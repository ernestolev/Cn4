from interface import Conecta4App
import sys
import os

print("Python Path:", sys.path)
print("Working Directory:", os.getcwd())


if __name__ == "__main__":
    app = Conecta4App()
    app.mainloop()
