import os
import ast
from collections import defaultdict

def extract_classes_and_methods(filepath):
    """Extract classes and methods from a Python file."""
    with open(filepath, "r") as file:
        tree = ast.parse(file.read(), filename=filepath)
    
    classes = []
    methods = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)
            # Extract methods in the class
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    methods.append(item.name)
        elif isinstance(node, ast.FunctionDef):
            methods.append(node.name)
    
    return classes, methods

def traverse_directory(directory):
    """Traverse directory and analyze all Python files."""
    class_counts = defaultdict(int)
    method_counts = defaultdict(int)
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                classes, methods = extract_classes_and_methods(filepath)
                
                for cls in classes:
                    class_counts[cls] += 1
                
                for method in methods:
                    method_counts[method] += 1
    
    return class_counts, method_counts

def write_counts_to_file(class_counts, method_counts, output_file):
    """Write class and method counts to a text file."""
    with open(output_file, "w") as file:
        file.write("Classes:\n")
        for cls, count in class_counts.items():
            file.write(f"{cls}: {count}\n")
        
        file.write("\nMethods:\n")
        for method, count in method_counts.items():
            file.write(f"{method}: {count}\n")

def main():
    directory = r'C:\Users\mario\Github\Repositories\mariodbx\playing_with_python' #input("Enter the path to the directory: ").strip()
    output_file =r'C:\Users\mario\Github\Repositories\mariodbx\playing_with_python\py_tools\result.txt' # input("Enter the path for the output text file: ").strip()
    
    class_counts, method_counts = traverse_directory(directory)
    write_counts_to_file(class_counts, method_counts, output_file)
    
    print(f"Class and method counts have been written to {output_file}")

if __name__ == "__main__":
    main()
