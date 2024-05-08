# Knowledge Graph Extraction Entities

## Objective

The objective of the Knowledge Graph Extraction project is to build a semantic network that represents and interlinks real-world entities within a codebase. These entities include classes, functions/methods, variables, modules/packages, interfaces, and more. The knowledge graph aims to capture relationships such as dependencies, inheritance, associations, aggregations/compositions, and function/method calls.

## Non-Technical Overview

### What is a Knowledge Graph?

A knowledge graph is a semantic network that organizes information in a graph structure. It consists of nodes representing entities and edges representing relationships between these entities. In the context of codebases, a knowledge graph can provide a visual representation of the structure and interactions within the code.

### Key Entities and Relationships

| No. | Entity                   | Description                                            |
|-----|--------------------------|--------------------------------------------------------|
| 1   | Nodes: Classes           | Represent classes in the code.                         |
| 2   | Nodes: Functions/Methods | Represent functions or methods.                        |
| 3   | Nodes: Variables         | Represent variables or constants.                     |
| 4   | Nodes: Modules/Packages   | Represent modules or packages.                        |
| 5   | Nodes: Interfaces        | Represent defined interfaces.                         |
| 6   | Relationships: Dependency | Indicates that a class, function, or module depends on another. |
| 7   | Relationships: Inheritance | Indicates inheritance among classes or interfaces.   |
| 8   | Relationships: Association | Shows how entities are associated with each other.    |
| 9   | Relationships: Aggregation/Composition | Represents 'part-of' type relationships between classes. |
| 10  | Relationships: Function/Method Call | Represents when one function or method calls another. |
| 11  | Node Attributes          | Additional details for each node, like type, parameters, and return value. |
| 12  | Nodes: Control Structures | Represent control structures like loops and conditions. |
| 13  | Nodes: Comments           | Represent comments in the code to provide context.    |
| 14  | Nodes: Exceptions         | Represent the exceptions handled or thrown.           |


### Parsing and Extracting Information

## 1. Classes, Functions/Methods, Variables, and Control Structures
Classes (ast.ClassDef) and Functions/Methods (ast.FunctionDef): These are straightforward to identify with their respective AST nodes.
Variables: Look for ast.Assign for variable assignments. Distinguishing constants might require a naming convention or value analysis.
Control Structures: ast.For, ast.While, ast.If, ast.Try, and more represent different control structures.

## 2. Modules/Packages and Imports (Dependencies)
Modules/Packages: The file structure of your Python project typically represents this. Each .py file is a module, and directories with an __init__.py file can be considered packages.
Imports: Use ast.Import and ast.ImportFrom nodes to identify dependencies.

## 3. Interfaces, Inheritance, and Exception Handling
Interfaces: Python doesn't have explicit interface definitions, but can identify them by conventions (e.g., abstract base classes or classes with only method declarations and no implementations).
Inheritance: Check the bases attribute of ast.ClassDef nodes.
Exceptions: Look for ast.Try and specifically its handlers attribute to find exception handling.

## 4. Associations, Aggregations/Compositions, and Function/Method Calls
Associations and Aggregations/Compositions: These relationships are more about design patterns and might be inferred from the way objects are used and referenced in the code, which can be quite complex to analyze statically.
Function/Method Calls: Identify ast.Call nodes. Determining the caller and callee can establish the call relationships.

## 5. Node Attributes, Comments, and Exceptions
Node Attributes: This might include type hints, parameters for functions (see ast.arguments), and more. Use the attributes of the respective AST nodes.
Comments: Python's AST does not directly include comments, but can use the tokenize module to extract them.
Exceptions: Look for ast.Raise and ast.ExceptHandler to identify thrown and handled exceptions.


