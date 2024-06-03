How to run compiler to convert source code to linear IR:
1) Need python3
2) Clone the repository and navigate to it
3) Make a valid cpp file that follows grammar below and utilizes valid operators
4) Run by entering in the command line
        python3 main.py ./(enter path to the cpp file you created)
5) Resulting intermediate representation will be outputted

Valid Operators:
1) Arithmetic operators: +, -, *, /
2) Comparison operators: ==, <
3) Assignment operator: =
4) Braces/parentheses: {, }, (, )
5) Semicolon: ;
6) ID: letter followed by series of letters/numbers
7) Number: integer or floating point value


Expected program grammar:

Function header
1) Starts with void, int or float 
2) Followed by sequence of references (sequence can be empty) to either int or float variables enclosed in parentheses. Ex: (int &x, float &y)
3) Followed by sequence of statements enclosed in braces
Look through the test cpp files for reference


Declaration statement
1) Only int and float data types are allowed
2) ID must start with a letter and can be followed by any sequence of letters and numbers
Ex: int x; 	or	float y;


Assignment statement
1) LHS must be a variable that has already been declared
2) RHS must be a valid expression followed by a semicolon
ex: x = 3+4-(4*9);


If-else statement
1) “if” followed by a set of parentheses that encloses a valid expression followed by “else” followed by a valid statement
ex: 
if(x>5)
    x = 2;
else
    x = 3
    
    
Block statement
1) { followed by a sequence of statements followed by }
ex: {x=5; y=2;}


For loop statement
1) “for” followed by left parenthesis followed by a valid assignment statement with a semicolon followed by a valid expression followed by a semicolon followed by a valid assignment statement without a semicolon followed by a right parenthesis followed by a valid statement 
ex:
for(x = 5; x<20; x = x+1){
    y = 27;
}
*note: a block statement is considered a valid statement

Error Reporting
1) If program is invalid at a specific point (ex: missing semicolon), the parser will raise an exception and let you know the exact line number, what it expected, and what it received instead
2) Use standard scoping rules for c++. Any errors in scoping will trigger a SymbolTable exception

Linear Intermediate Representation
1) Unlimited virtual registers
2) Virtual registers can be assigned to each other
3) virtual register operations: add, sub, mult, div, lt, eq
4) Each register operation takes in two virtual registers. Each operation is followed by either i or f.
    i - both registers must be ints
    f - both registers must be floats
    Ex: addi(vr0, vr7);
5) Branch: branch, beq, bne
6) Labels = label name followed by colon

