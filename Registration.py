import pandas as pd 
import re
from argparse import ArgumentParser
import sys
from matplotlib import pyplot as plt
import math

class School:
    
    def __init__(self,courses):
        """initializes a School object
        Args:
            students (list): list of student objects in the school
            studentsdict (dict): Dictionary of student names as keys and student object as value
            courses (DataFrame): a dataframe of availible courses and sections
            faculty (list): list of faculty members
        """
        self.students= []
        self.studentsdict = {}
        self.courses= pd.DataFrame(pd.read_csv(courses))
    
    def add_course(self, course):
        """Adds a course section to the courses dataframe
        Args:
            course (DataFrame): a course section
        """
        self.courses.append(course)
        
    def regex_match(self, line):    
        """matches values in a txt file line to create a Student object
        Args:
            line (string): a string containing student name, age, year, and credits earned
        """
        pattern = r"^(\S+\s\S+), (\d+), (\d+), (\d+)$"
        searched = re.search(pattern, line.strip())
        student = Student(searched.group(1), searched.group(2), searched.group(3), searched.group(4), self.courses)
        self.students.append(student)
        self.studentsdict[searched.group(1)] = student
        
    def addMultipleStudents(self, path):
        """allows users to use a txt file containing multiple students, and add them in mass to the School.students list
        Args:
            path (string): a path to a txt file
        """
        with open(path,'r',encoding='utf-8') as file:
           for line in file:
               self.regex_match(line)
            
        
    def addStudent(self, name, age, year, credits):
        """Adds a single student to the School.students list
        Args:
            name (str): student full name
            age (int): student age
            year (int): year of graduation
            schedule (dict, optional): student schedule. Defaults to {}.
        """
        self.students.append(Student(name, age, year,credits))
    
    def print_grades(self, student= None):
        """prints out student grades. If student does not have grades it prints out a generic schedule for the student
       Args:
            student (string): represents a student that is set to none
        Side effects:
            prints out a student grades if no grades gives student a generic schedule
            """
        generic_schedule = "Credits = 0, Grade = N/A"
        print(generic_schedule) if student==(None) else student.get_grades()
    
    def student_stats(self):
        """Graphs the GPA of all students enrolled at the school
        
            Side Effects: displays a plot of studnets gpa in a seperate window
        """
        
        zero, one, two, three, four = 0, 0, 0, 0, 0
        gpa_lst=[]
        for student in self.students:
            gpa_lst.append(student.gpa)
            
        for gpa in gpa_lst:
            simple_gpa = math.floor(gpa)
            if int(simple_gpa) == 0:
                zero += 1
            elif simple_gpa == 1:
                one += 1
            elif simple_gpa == 2:
                two += 1
            elif simple_gpa == 3:
                three += 1
            else:
                four += 1
                
        data = {'0.0':zero, '1.0':one, '2.0':two, '3.0':three, '4.0':four}
        x = list(data.keys())
        y = list(data.values())
        
        fig = plt.figure(figsize = (10, 5))
        
        plt.bar(x, y, color = 'b', width = 0.4)
        plt.xlabel('GPA')
        plt.ylabel('Number of Students')
        plt.title('Student Stats')
        plt.show()
        
    
    def calculate_gpa(student):
       """calls student gpa method
        
            Returns: results of method call"""
       return student.get_gpa()
    
    def give_grade(self,student,course,grade):
        """calls student method to recieve a grade based on user prompts
            Args: student(Student): student object of which grade will be given
                course(String): course student recieves grade in
                grade(String) : grade to be assigned
        """
        student.get_grade(course,grade)

       
    def add_course(self,df):
        """Adds a new course to the school courses dataframe based on dataframe build from user prompts
        
            Args: df(dataframe):dataframe containing the new course information to be concatenated
            
            Side effects: courses attribute is ubdated with a new course 
            """
        self.courses=pd.concat([self.courses,df])
        
                
    def class_rankings(self):
        """ Prints the students class rankings in order from greatest to least
       Args:
            self(intializer): Represents and instance used in the code
        Side effects:
            prints out class ranking
            """
        class_ranking =sorted(self.students, reverse = True, key = lambda Student : Student.gpa)
        top_5 =[]
        counter = 0
        
        while(counter<5):
            top_5.append(class_ranking[counter].name)
            counter+=1
            
        print(f"The top five students with the highest GPA starting from greatest to least are {top_5}.")
    
    def __str__(self):
        """Prints the informal representaion of the School object
        """
        return(f"This school has {len(self.students)} students and offers {len(self.courses)} courses.")
        
      
       
        
class Student():
    """Student class contains all student information for studnets held in the shchool, for use in 
        data aggregtion"""
        
    
    
    def __init__(self, name, age, year, credits, courses):
        self.name = name
        self.age = int(age)
        self.year = int(year)
        self.credits = int(credits)
        self.grades = {}
        self.gpa = 0.00
        self.schedule = pd.DataFrame()
        self.course_db = courses
     
    def add(self,prefix,course_num,section_num): 
       """Adds course to student schedule given they meet credit requirements
       Args:
            prefix (string): Four-letter string abbreviation of the course department
            course_num (int): The course number
            section_num (int): The section number
        Side effects:
            Adds row to schedule attribute
            """
       pfx_filt =  self.course_db["Prefix"] == prefix 
       course_num_filt = self.course_db["Course number"] == course_num 
       sec_num_filt = self.course_db["Section number"] == section_num
       combined_filter = pfx_filt & sec_num_filt & course_num_filt
       
       entry = self.course_db[combined_filter]
       
       if entry.loc[entry.index[0],"Credits needed"] > self.credits:
           print("you do not have enough credits for this class.")
       else:
            self.schedule = pd.concat([self.schedule,entry])
            self.grades[f"{prefix }{course_num}"] = None
            self.schedule = self.schedule.drop(columns=['Credits needed'])
       
    def drop(self,prefix,course_num):
        """Drops course from student schedule.
        
        Args:
            prefix (string): Four-letter string abbreviation of the course
            department.
            course_num (int): The course number.
            
        Side effects:
            Removes a row from the schedule attribute.
            """
        pfx_filt =  self.course_db["Prefix"] == prefix 
        course_num_filt = self.course_db["Course number"] == course_num 
        combined_filt = pfx_filt & course_num_filt
         
        entry = self.schedule[combined_filt]
        drop_val = entry.index[0]
        self.schedule = self.schedule.drop([drop_val], axis = 0)
    
    def get_grade(self,course,grade):
        """Student side: called by school to assign a grade to the students grade dictionary. When added, recalculates gpa accordingly
            Args: 
            Course (string): the course string which acts as a key for the dictionary
            
            Grade: (String): course grade, value in the grades dictionary 
            
            Side effects: student gpa is adjusted """
        self.grades[str(course)] = grade
        self.gpa = self.get_gpa()
        
    def get_grades(self):
        """Prints a formatted string of a students grades in classes which they have grades in
        
            Side effect: prints our student grades from grades dictionary to the terminal"""
        for grade in self.grades:
            print(f"{grade}: {self.grades[grade]}")
               
        
    def print_schedule(self):   
        """prints student schedule to console 
        
            Side effects: Prints schedule to console"""
        print(self.schedule.to_string())
        
    def get_gpa(self):
        """Calculates a students GPA based on their grades
        
            Returns:
                int: GPA value
            """
        GPAS = {'A': 4.0,'B':3.0,'C':2.0,'D':1.0}
        
        total = 0
        counter = 0
        for keys in self.grades:
            total += GPAS.get(self.grades[keys])
            counter += 1
            
        return total/counter
        
            
    
   
def parse_args(arglist):
    """Processes command line arguments for the files loaded"""
    parser = ArgumentParser("get filepaths to initiate the school program")
    parser.add_argument("students", help="filepath to a file containing students enrolled in the school") 
    parser.add_argument("courses",help = "filepath to a file containing the courses held at the school")
    args = parser.parse_args(arglist)
    
    return args  
     
if __name__ == "__main__":
    """Driver of the program, presents menus to the user and allows them to flow through the method use cases
    
        Side effects: Prints to teerminal the results of methods, dataframes, or prompts dynamically based on user input"""
    args = parse_args(sys.argv[1:])
    
    
    umd = School(args.courses)
    umd.addMultipleStudents(args.students)
    
    
    perspective = input("Hello, are you accessing from a student or school perspective? 1 for student, 2 for school: ") 

    if(perspective == '1'):

            name = input("Please enter your full name in format \"fname lname\": ")
            
            if(umd.studentsdict[name] == None):
                age = input("Please enter your age: ")
                year = input("Please enter your class (graduation year): ")
                credits = input("How many credits are you enrolling with?: ")
                umd.addStudent(name,age,year,credits)
            
            option = input("What would you like to do today? \n1.add class\n 2.drop class\n3.print schedule\n4.exit\n")

            while(option != '5'):
                
                if(option == '1'):
                    print(umd.courses.to_string())
                    print("\n")
                    
                    prefix = input("please enter the course prefix: ")
                    course_num = int(input("please enter the course number: "))
                    section_num = int(input("please enter the section number: "))
                    umd.studentsdict[name].add(prefix,course_num,section_num)
                    
                    option = input("Complete! would you like to do anything else? \n1.add class\n2.\
                    drop class\n3.print schedule\n4.exit")
                    
                elif(option =='2'):
                    prefix = input("please enter the course prefix: ")
                    course_num = int(input("please enter the course number: "))
                    
                    umd.studentsdict[name].drop(prefix,course_num)
                    option = input("Complete! would you like to do anything else? \n1.add class\n2.\
                    drop class\n3.print schedule\n4.exit")
                    
                elif(option =='3'):
                    umd.studentsdict[name].print_schedule()
                    option = input("Complete! would you like to do anything else? \n1.add class\n2.\
                    drop class\n3.print schedule\n4.exit")
                else:
                    option = input("Complete! would you like to do anything else? \n1.add class\n2.\
                    drop class\n3.print schedule\n4.exit")
            if(option == '4'):
                print("Goodbye!")
        
    else:
        option =input("What would you like to do today? \n1.Add multiple students\n2.Add single student\n3.\
Add course \n4.Print student transcript\n5.get student stats\n6.School stats\n7.Give grade\n8.Top five students\n9.Exit")
        
        while(option!='9'):
            
            
            
            if(option == '1'):
                choice = input("Please enter a file path to students you would like to add")
                
                umd.addMultipleStudents(input)
                
                option =input("Complete! What else would you like to do today? \n1.Add multiple students\n2.Add single student\n3.\
Add course \n4.Print student transcript\n5.get student stats\n6.School stats\n7.Give grade\n8.Top five students\n9.Exit")  
                
            elif(option == '2'):
                name = input("Please enter the student name:")
                age = input("Please enter the student age: ")
                year = input("please enter the student year: ")
                
                umd.addStudent(name,age,year)
                
                option =input("Complete! What else would you like to do today? \n1.Add multiple students\n2.Add single student\n3.\
Add course \n4.Print student transcript\n5.get student stats\n6.School stats\n7.Give grade\n8.Top five students\n9.Exit")        
            elif(option == '3'):
                df = pd.DataFrame(columns=["Prefix","Course number","Section number","Course name","Times","Instructor","Building","Credits needed"])
                prefix  = input("Enter course Prefix: ")
                course_num = input("Enter course number")
                section_num = input("Enter the section number: ")
                course_name = input("Enter the course name: ") 
                times = input("Enter the start time of the class: ")
                instructor = input("Enter the instructor name: ")
                building = input("Enter the class location: ")
                credits = input("Enter the credits needed: ")
                
                dict = {"Prefix": prefix, "Course number": course_num,"Section number": section_num,
                        "Course name": course_name, "Times": times,"Instructor":instructor,"Building":building,"Credits needed":credits}
                
                df = df.append(dict,ignore_index=True)
                umd.add_course(df)
                option =input("Complete! What else would you like to do today? \n1.Add multiple students\n2.Add single student\n3.\
Add course \n4.Print student transcript\n5.get student stats\n6.School stats\n7.Give grade\n8.Top five students\n9.Exit")  
                
            elif(option == '4'):
                name = input("please enter the student: ")
                
                umd.print_grades(umd.studentsdict[name])
                option =input("Complete! What else would you like to do today? \n1.Add multiple students\n2.Add single student\n3.\
Add course \n4.Print student transcript\n5.get student stats\n6.School stats\n7.Give grade\n8.Top five students\n9.Exit")  
                
            elif(option == '5'):
                
                print("Here is a graph of the GPA distribution of the school students currently enrolled. To continue, please close the graph window.")
                
                
                umd.student_stats()
                
                option =input("Complete! What else would you like to do today? \n1.Add multiple students\n2.Add single student\n3.\
Add course \n4.Print student transcript\n5.get student stats\n6.School stats\n7.Give grade\n8.Top five students\n9.Exit")  
            elif(option == '6'):
                print(umd)
                
                option =input("Complete! What else would you like to do today? \n1.Add multiple students\n2.Add single student\n3.\
Add course \n4.Print student transcript\n5.get student stats\n6.School stats\n7.Give grade\n8.Top five students\n9.Exit")  
            elif(option == '7'):  
                print(umd.courses.to_string())
                print("\n")
                
                student = input("Please enter the student name to give a grade: ") 
                prefix = input("Please enter the course prefix: ")
                course_num = input("Please enter the course number: ")
                grade = input("please enter the grade you wish to give the student: ")
                umd.give_grade(umd.studentsdict[student],f"{prefix}{course_num}",str(grade))  
                
                option =input("Complete! What else would you like to do today? \n1.Add multiple students\n2.Add single student\n3.\
Add course \n4.Print student transcript\n5.get student stats\n6.School stats\n7.Give grade\n8.Top five students\n9.Exit")
            elif(option == '8'):
                umd.class_rankings()
                option =input("Complete! What else would you like to do today? \n1.Add multiple students\n2.Add single student\n3.\
Add course \n4.Print student transcript\n5.get student stats\n6.School stats\n7.Give grade\n8.Top five students\n9.Exit")  
        if(option =='9' ):
            print("Goodbye!")
        
   
