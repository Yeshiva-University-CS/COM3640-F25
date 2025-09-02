# In-Class Lab: Getting Comfortable with a New Language

## Goal
The purpose of this lab is to **get hands-on experience with a new programming language** and practice identifying what feels familiar and what feels different. You’ll use Zig as the example, but the same process applies whenever you learn a new language.  

---

## Task

Install Zig, set up a development and debug environment for Zig in **Visual Studio Code**, and write a program in a file called `hello.zig` that does the following:

1. **Set up and run Zig**
   - Install Zig on your computer  
   - Verify your installation with:  
     ```bash
     zig version
     ```  

2. **Command-line input and conditional logic**
   - Accept a **name** as a command-line argument.  
   - If no argument is provided, print:  
     ```
     Usage: hello <name>
     ```  

3. **Functions and output**
   - Define a **function** that takes a name and returns the string `Hello <Name>`.  
   - Use that function to generate the output.  

4. **Control flow practice**
   - Print the greeting a total of **10 times**:  
     - **5 times using a `for` loop**  
     - **5 times using a `while` loop**  

5. **Debugging in Visual Studio Code**
   - Configure debugging in VS Code for Zig (using a `launch.json` or the built-in debugger).  
   - You should be able to **set a breakpoint** in your code and confirm that the debugger **stops execution at that point**.
   - Take a screenshot of the debugger while it is stopped and show that value of the variable containing the name that was input on the command line.

---

## Stretch Goal
- If the name is **longer than 10 characters**, truncate it to the first 10 characters before generating the greeting.  

---

## Guiding Questions
As you work, think about the following to help you get comfortable with learning a new language:

1. How does Zig’s syntax for declaring variables compare to Java, C, or Python?  
2. What differences do you notice in how Zig handles command-line arguments?  
3. How does Zig’s `for` loop differ from the loops you’ve used in other languages?  
4. How does the `while` loop compare?  
5. How do you define and call a function in Zig? Is the syntax more similar to C, Java, or Python?  
6. Did you run into any errors during compilation or execution? How did Zig’s error messages compare to those in other languages you’ve used?  
7. What did you notice about how Zig organizes programs (entry point, `main`, imports)?  
8. Do you see aspects of Zig that might make it easier or harder to learn compared to other languages you know?  
