from backend.analyzers.cpp_analyzer import analyze_cpp_code


cpp_code = """
#include <iostream>

using namespace std;

int main() {

    int sum = 0;

    for (int i = 0; i < 10; i++) {

        for (int j = 0; j < 10; j++) {

            sum = sum + i + j;

        }
    }

    cout << "Sum = " << sum << endl;

    return 0;
}
"""


# Run C++ static analysis
result = analyze_cpp_code(cpp_code)


# Display result
print("\n===================================")
print("       C++ STATIC ANALYSIS")
print("===================================\n")

print("Syntax            :", result["syntax"])
print("Lines             :", result["lines"])
print("Loops             :", result["loops"])
print("Nested Loops      :", result["nested_loops"])
print("Loop Depth        :", result["loop_depth"])
print("Time Complexity   :", result["time_complexity"])
print("Space Complexity  :", result["space_complexity"])
print("Functions         :", result["functions"])
print("Classes/Structs   :", result["classes"])
print("Quality Score     :", result["quality_score"])

print("\nCode Smells:")

if result["code_smells"]:

    for smell in result["code_smells"]:

        print("\nType       :", smell["type"])
        print("Severity   :", smell["severity"])
        print("Message    :", smell["message"])
        print("Suggestion :", smell["suggestion"])

else:

    print("No code smells detected.")

print("\n===================================")