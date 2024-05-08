import ast
import os
import tokenize


class CodeAnalyzer:
    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.graph = {"nodes": [], "edges": []}
        self.current_module = None
        self.current_class = None

    def analyze_directory(self):
        for subdir, dirs, files in os.walk(self.directory_path):
            for file in files:
                if file.endswith('.py'):
                    module_path = os.path.join(subdir, file)
                    self.current_module = self._format_module_name(subdir, file)
                    self.graph["nodes"].append(f"Module: {self.current_module}")
                    print(f"\nAnalyzing {module_path}")
                    self._analyze_file(module_path)

    def _analyze_file(self, file_path):
        with open(file_path, 'rb') as f:
            tokens = tokenize.tokenize(f.readline)
            self._extract_comments(tokens)
        tree = self._parse_file(file_path)
        self._extract_info(tree)

    def _parse_file(self, file_path):
        with open(file_path, "r") as file:
            return ast.parse(file.read(), filename=file_path)

    def _format_module_name(self, subdir, file):
        relative_path = os.path.relpath(subdir, self.directory_path)
        module_name = os.path.join(relative_path, file).replace(os.sep, ".")[:-3]
        return module_name if module_name != "__init__" else relative_path.replace(os.sep, ".")

    def _extract_info(self, node):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.ClassDef):
                self.current_class = f"Class: {child.name} in {self.current_module}"
                self.graph["nodes"].append(self.current_class)

                # Extracting inheritance information
                base_classes = [base.id for base in child.bases if isinstance(base, ast.Name)]
                for base_class in base_classes:
                    self.graph["edges"].append((self.current_class, f"Class: {base_class}"))

                self._extract_info(child)  # Process class body
                self.current_class = None  # Reset current class after processing

            elif isinstance(child, ast.FunctionDef):
                func_name = f"Function: {child.name} in {self.current_module}"
                if self.current_class:
                    func_name = f"Method: {child.name} of {self.current_class}"
                    self.graph["edges"].append((self.current_class, func_name))
                self.graph["nodes"].append(func_name)
                self._extract_info(child)  # Process function body

            if isinstance(child, ast.Raise):
                exception_name = self._get_exception_name(child)
                raise_detail = f"Raises: {exception_name}"
                self.graph["nodes"].append(raise_detail)
            elif isinstance(child, ast.Call):
                caller = self.current_class if self.current_class else f"Module: {self.current_module}"
                callee = self._get_callable_name(child)
                if callee:  # Ignore calls to built-in functions or methods
                    self.graph["edges"].append((caller, f"Call: {callee}"))

            elif isinstance(child, ast.Assign):
                for target in child.targets:
                    variable_name = f"Variable: {ast.unparse(target)} in {self.current_module}"
                    self.graph["nodes"].append(variable_name)
                    self.graph["edges"].append((self.current_module, variable_name))

            elif isinstance(child, ast.Import) or isinstance(child, ast.ImportFrom):
                for alias in child.names:
                    import_name = f"Import: {alias.name} in {self.current_module}"
                    self.graph["nodes"].append(import_name)
                    self.graph["edges"].append((f"Module: {self.current_module}", import_name))

            elif isinstance(child, ast.Try):
                try_block_name = f"Try block in {self.current_module}"
                self.graph["nodes"].append(try_block_name)
                self.graph["edges"].append((f"Module: {self.current_module}", try_block_name))
                for handler in child.handlers:
                    exception_type = handler.type.id if isinstance(handler.type, ast.Name) else "Exception"
                    handler_name = f"Handler for {exception_type} in {self.current_module}"
                    self.graph["nodes"].append(handler_name)
                    self.graph["edges"].append((try_block_name, handler_name))

            # Recursively process all child nodes
            self._extract_info(child)

    def _extract_comments(self, tokens):
        for token in tokens:
            if token.type == tokenize.COMMENT:
                comment_detail = f"Comment: {token.string}"
                self.graph["nodes"].append(comment_detail)

    def _get_exception_name(self, raise_node):
        if isinstance(raise_node.exc, ast.Name):
            return raise_node.exc.id
        elif isinstance(raise_node.exc, ast.Call) and isinstance(raise_node.exc.func, ast.Name):
            return raise_node.exc.func.id
        return "Exception"

    def _get_callable_name(self, call_node):
        """Extract the callable name from a Call node, if possible."""
        if isinstance(call_node.func, ast.Name):
            return call_node.func.id
        elif isinstance(call_node.func, ast.Attribute):
            return call_node.func.attr
        return None
