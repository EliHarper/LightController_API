import subprocess

def apply(scene):
    process = subprocess.Popen("strandtest.py " + scene.functionCall + " " + scene.colors + " " + scene.defaultBrightness)
    output, error = process.communicate()
    if error:
        print(error)
    
    print(output)